import ast
import json
import os

asterr_root = os.path.dirname(__file__)
scripts_path =  os.path.join(asterr_root, "scripts")
config_path = os.path.join(asterr_root, "config.json")

configuration = {}
try:
    with open(config_path, 'r', encoding='utf-8') as file:
        configuration = json.load(file)
        print("ASTERR config loaded successfully")
except Exception as e:
    print(f"ASTERR config could not be loaded: {e}")
    pass

class ASTERR:
    """
    Abstract Syntax Trees Evaluated Restricted Run (ASTERR)

    Provides a restricted execution environment for Python code using Abstract Syntax Trees (AST).

    Parameters:
        code (str): arbitrary code to run
        params (dict): dictionary of parameter names and values used as vars within the namespace
        allowed_modules (list): list of additional allowed module names: ["*"] would allow all modules to be imported

    """

    # Modules that are hunky-dory to import run.
    # Using "*" would allow any import. 
    # Using "Module.*" would allow any submodule from a module to be imported
    default_allowed_modules = [
        # Comfy modules
        "nodes",
        "folder_paths",
        # Other modules
        "math",
        "PIL",
        "PIL.*",
        "cv2",
        "random",
        "time",
        "numpy",
    ]

    params = {}
    recursion_limit = 100
    insecure_execution = False

    def __init__(self, code, params=None, allowed_modules=None, recursion_limit=None):
        self.code = code
        if params:
            self.params = params
        if allowed_modules:
            if isinstance(allowed_modules, list):
                self.allowed_modules = allowed_modules + self.default_allowed_modules
        else:
            self.allowed_modules = self.default_allowed_modules
        if recursion_limit:
            self.recursion_limit = int(recursion_limit)

    def _check_imports(self, node):
        if "*" in self.allowed_modules:
            self.insecure_execution = True
            return

        for allowed_module in self.allowed_modules:
            if allowed_module.endswith('.*'):
                module_name = allowed_module[:-2]
                if isinstance(node, ast.ImportFrom) and node.module.startswith(module_name):
                    return
            else:
                for alias in node.names:
                    module_name = alias.name
                    if module_name == allowed_module:
                        return

        raise ImportError(f"Module '{module_name}' is not allowed")

    def execute(self):
        return_result = None
        extra_pnginfo = None
        error = None
        try:
            tree = ast.parse(self.code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    self._check_imports(node)

            if self.insecure_execution:
                print("\033[93mWarning:\033[0m ASTERR is allowing any module or package imports. This is a potential security risk.")

            exec_header = [
                # imports / setup
                "from importlib import reload as ReloadModule",
                "import sys",
                f"sys.setrecursionlimit({self.recursion_limit})",
                "del sys",
                
                # helpers
                "def tensor2pil(image):",
                "   from PIL import Image",
                "   import numpy as np",
                "   return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))",
                "def pil2tensor(image):",
                "    from PIL import Image",
                "    import numpy as np",
                "    import torch",
                "    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)",
            ]
            exec_header = "\n".join(exec_header) + "\n"

            self.code = exec_header + self.code

            exec(self.code, {}, self.params)
            return_result = self.params.get('asterr_result', None)
            extra_pnginfo = self.params.get('extra_pnginfo', None)
            
        except NameError as e:
            error = e
        except ImportError as e:
            error = e
        except Exception as e:
            error = e
            
        out = (return_result, extra_pnginfo), error
        
        return out

class SuspiciousName(Exception):
    def __init__(self, original_error):
        self.original_error = original_error

    def __str__(self):
        return str(self.original_error)

class SuspiciousImport(Exception):
    def __init__(self, original_error):
        self.original_error = original_error

    def __str__(self):
        return str(self.original_error)
        
def get_asterr_scripts():
    scripts = {"None": None}
    if not os.path.exists(scripts_path):
        os.makedirs(scripts_path, exist_ok=True)
    for script_name in os.listdir(scripts_path):
        script_path = os.path.join(scripts_path, script_name)
        if os.path.isfile(script_path):
            scripts[script_name] = script_path
    return scripts

# Hack: string type that is always equal in not equal comparisons
# Borrowed from: https://github.com/M1kep/Comfy_KepListStuff/blob/main/utils.py
class AnyType(str): 
    def __ne__(self, __value): 
        return False

wildcard = AnyType("*")

class ASTERRNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        scripts = get_asterr_scripts()
        return {
            "required": {
                "script": ("STRING", {"multiline": True, "dynamicPrompts": False}),
            },
            "optional": {
                "trigger_run_01":  ("INT", {"forceInput": True}),
                "a": (wildcard, {}),
                "b": (wildcard, {}),
                "c": (wildcard, {}),
                "d": (wildcard, {}),
                "e": (wildcard, {}),
                "f": (wildcard, {}),
                "g": (wildcard, {}),
                "h": (wildcard, {}),
                "i": (wildcard, {}),
                "j": (wildcard, {}),
                "k": (wildcard, {}),
                "preset_script": (list(scripts.keys()),),
                "always_run": (["false", "true"],),
            },
            "hidden": {
                "prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"
            }
        }
        
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        try:
            if kwargs.__contains__('trigger_run_01'):
                if kwargs['trigger_run_01'] == 1:
                    return float("NaN")
            if kwargs.__contains__('always_run'):
                if kwargs['always_run'] == "true":
                    return float("NaN")
        except Exception as e:
            raise e

    RETURN_TYPES = (wildcard,  )
    RETURN_NAMES = ("result", )

    FUNCTION = "evaluate"

    CATEGORY = "_for_testing"

    def evaluate(self, script, trigger_run_01=None, preset_script=None, always_run=None, **kwargs):
    
        scripts = get_asterr_scripts()
        if preset_script:
            script_path = scripts[preset_script]
            if script_path:
                if os.path.exists(script_path):
                    print(f"Loading preset script: {os.path.basename(script_path)}")
                    with open(script_path, 'r', encoding="utf-8") as file:
                        new_script = file.read()
                    if new_script:
                        script = new_script
    
        recursion_limit = configuration.get("recursion_limit", None)
        allowed_modules = configuration.get("allowed_modules", None)
    
        asterr = ASTERR(code=script, params=kwargs, allowed_modules=allowed_modules, recursion_limit=recursion_limit)
        out, error = asterr.execute()
        
        if error:
            raise error
		
        if out[1]:
            return out[0], { "extra_pnginfo": out[1] }
        else:
            return out[0],
            
class SaveASTERRScript:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "script_string": ("STRING", {"forceInput": True}),
                "script_name": ("STRING", {"default": ""}),
                "overwrite_script": (["false", "true"],),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("script_string",)

    FUNCTION = "save_script"

    CATEGORY = "_for_testing"

    def save_script(self, script_string, script_name, overwrite_script):
    
        do_continue = True
        save_script_path = os.path.join(scripts_path, script_name + '.py')
    
        if script_string.strip():
        
            if not script_name.strip():
                print("\033[93mWarning:\033[0m `script_name` is empty. You must provide a valid script name.")
                
            try:
            
                if not os.path.exists(scripts_path):
                    os.makedirs(scripts_path, exist_ok=True)
                    
                if os.path.exists(save_script_path):
                    do_continue = True if overwrite_script == "true" else False
                    
                if do_continue:
                    with open(save_script_path, "w", encoding="utf-8") as file:
                        file.write(script_string)
                    print(f"ASTERR saved script to: {save_script_path}")
                        
            except Exception as e:
                raise e
                
        else:
            print("\033[93mWarning:\033[0m `script_string` is empty. You must provide a script to save.")
            
        return (script_string, )

NODE_CLASS_MAPPINGS = {
    "ASTERR": ASTERRNode,
    "SaveASTERR": SaveASTERRScript
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ASTERR": "ASTERR Script",
    "SaveASTERR": "Save ASTERR Script"
}