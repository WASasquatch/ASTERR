# ASTERR
 Abstract Syntax Trees Evaluated Restricted Run (ASTERR) is a Python Script executor for ComfyUI

### <font color="red">WARNING:</font> ASTERR runs Python Code from a Web Interface! It is highly recommended to run this in a closed-off environment, as it could have potential security risks.

# Installation

Clone the reposity to `ComfyUI/custom_nodes` and restart ComfyUI if running.

# Configuration

The default configuration specifies a maximum recursion limit of 100 for loops and nested operations. The allowed modules list is empty, and uses the internal default allowed imports.

**DEFAULT CONFIG:**
```json
{
	"recursion_limit": 100,
	"allowed_modules": []
}
```

You can added allowed modules by their name, and optionally plus their submodule. For exmaple to allow PIL import and it's submodules you could either do
```json
	"allowed_modules": ["PIL", "PIL.Image", "PIL.ImageFilter"]
```
And so on, or you could do
```json
	"allowed_modules": ["PIL.*"]
```

***To live dangerously and allow any imports like a og boss, you can use:***
```json
	"allowed_modules": ["*"]
```

---

# Nodes

## `ASTERR Script` Node

### Required Params
 - `script` (`STRING`): The script to process. Can be converted to input to provide custom text string input.
### Optional params
 - `trigger_run_01` (`INT`): `0` or `1` `INT` that defines whether the script should run or not.
 - `a` through `k` (`*`): Arbitrary input (`STRING`, `INT`, `FLOAT`, `IMAGE`, `MODEL`, etc) to pass as a variable to the execution namespace.
 - `preset_script` (`COMBO`): List of `.py` scripts located in `ASTERR/scripts` for preset execution. This will override the `script` input.
 - `always_run` (`COMBO`): `false` or `true` on whether to always run the script (similar to trigger on run, but a constant state). If false, it will only run when a change has been made.
### Hidden params
 - Accessible within scripts is `prmpt` and `extra_pnginfo` vars which can be used to investigate, fetch data. In the case of `extra_pnginfo` you can overwrite the variable with an updated version of the `extra_pnginfo` (`dict`) to return with the node to the executor. 

## `Save ASTERR Script` Node

Save a ASTERR script which would then be available under `ASTERR/scripts` and the `preset_scripts` menu in the [ASTERR Script](https://github.com/WASasquatch/ASTERR#ASTERR-Script) node.

### Requited Params
 - `script_string` (`STRING`): Script content string input. This string is saved to a python script file under `ASTERR/scripts`
 - `script_name` (`STRING`): Script name to use, does not include the extension.
 - `overwrite_script` (`COMBO`): `false` or `true` on whether to overwrite the script that already exists on disk.

---

# PRESET SCRIPTS

Preset scripts allow you to pre-define functions to pick from and run any time. Scripts are saved a `.py` files (so editing is familiar).

### Return methods
- `asterr_result` var can be used to define the result to return to the node.
- `extra_pnginfo` can be used and overwritten to return edited extra_pnginfo

## Available Scripts

- **resize_maxsize.py**
  - Resize input `a` (`IMAGE`) propotionally with `b` (`INT`) as max size of the result.

### Script Code
```python
# Inside functions, we must import our modules as they are scoped from the main script
# tensor2pil() and pil2tensor() are built-in methods to help with `IMAGE` input

# a = image (tensor batched image)
# b = max size (INT)

def resizeImage(image, max_size):
    import PIL
    width, height = image.size
    new_width, new_height = width, height

    if width > max_size or height > max_size:
        ratio = min(max_size / width, max_size / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)

    elif max_size > max(width, height):
        ratio = max_size / max(width, height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)

    resized_image = image.resize((new_width, new_height))
    return resized_image


# We define the result to return to the node with the `asterr_result` var
asterr_result = pil2tensor(resizeImage(tensor2pil(a), b))
```
