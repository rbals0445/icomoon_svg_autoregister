## What is icomoon_svg_autoregister?

- This program easily changes svg_images to fonts from icomoon.
- You can easily add it to the existing font.

## Installation

### Download and Execute the source code

```bash
# download
$ git clone https://github.com/rbals0445/icomoon_svg_autoregister.git
$ cd icomoon_svg_autoregister

# before excution, plz check conditions!

# execute
$ python3 main.py
or
$ python main.py
```

## Condition

- Please include `selection.json` to save the existing image and add newly added images.
- The newly added svg file must be placed in the `newfiles`
- ligature name will be the same as the svg file name. However, characters other than '\_' are removed. (multiple color svg files will not be supported)
  - ```js
    //Example
    - abc_def-: => abc_def
    - _abc09=33 => _abc0933
    - ,a3bc=_32 => a3bc_32
    ```

## Result

- You can find the results in the `results folder`.
