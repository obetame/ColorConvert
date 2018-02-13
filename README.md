# ColorCovert

sublime text 3 plug-in, Support `RGB`,`RGBA`,`HEX`,`HSL`,`HSLA`,`HSV`,`CMYK` to transform each other.

## Installation

- You can easily install the plug-in through Package Control (https://packagecontrol.io/).

- If you want to install this plug-in manually for some reason, simply clone this repo into your packages directory (make sure not to put it in the user sub dir).

## Instruction

1. Select a color declaration (e.g. '#008080', 'rgb(0,128,128)', or 'hsl(39.84,100.0%,25.1%)')
2. Mac user can use `cmd+alt+c`, Windows and Linux user can use `ctrl+alt+c`

OR:

1. Select a color declaration
2. Right click and choose `ColorCovert`, click the mode you need to convert.

## Settings

- `covert_mode`: covert to rgba mode
- `capitalization`: whether the converted letters need to be capitalized

## Support

- Support `RGB`,`RGBA`,`HEX`,`HSL`,`HSLA`,`HSV`,`CMYK` to covert each other.
- Support [css3 color name](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value) covert to `HEX`
- Support convert the color values in the entire page.

## Notes

1. Do not support css3 color:`transparent` and `currentColor`.
2. When `RGBA` is converted to other color value(like `RGB`,`HEX`,`HSL` etc...) it will lose the alpha value.