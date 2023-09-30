# ASTERR
 Abstract Syntax Trees Evaluated Restricted Run (ASTERR) is a Python Script executor for ComfyUI

# Installation

Clone the reposity to `ComfyUI/custom_nodes` and restart ComfyUI if running.

# Parameters

### Required Params
 - `script` (`STRING`): The script to process. Can be converted to input to provide custom text string input.
### Optional params
 - `trigger_run_01` (`INT`): `0` or `1` `INT` that defines whether the script should run or not.
 - `a` through `k` (`*`): Arbitrary input (`STRING`, `INT`, `FLOAT`, `IMAGE`, `MODEL`, etc) to pass as a variable to the execution namespace.
 - `preset_script` (`COMBO`): List of `.py` scripts located in `ASTERR/scripts` for preset execution. This will override the `script` input.
 - `always_run` (`COMBO`): `false` or `true` on whether to always run the script (similar to trigger on run, but a constant state). If false, it will only run when a change has been made.
### Hidden params
 - Accessible within scripts is `prmpt` and `extra_pnginfo` vars which can be used to investigate, fetch data. In the case of `extra_pnginfo` you can overwrite the variable with an updated version of the `extra_pnginfo` (`dict`) to return with the node to the executor. 

# Preset Scripts

Preset scripts allow you to pre-define functions to pick from and run any time. Scripts are saved a `.py` files (so editing is familiar).

### Return methods
- `asterr_result` var can be used to define the result to return to the node.
- `extra_pnginfo` can be used and overwritten to return edited extra_pnginfo

## Available Scripts

- **resize_maxsize.py**
  - Resize input `a` (`IMAGE`) propotionally with `b` (`INT`) as max size of the result.
