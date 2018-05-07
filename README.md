# ColorConvert

sublime text 3 plug-in, Support `RGB`,`RGBA`,`HEX`,`HSL`,`HSLA`,`HSV`,`CMYK` to transform each other.

![DEMO](http://g.recordit.co/Rgi5FuhGaw.gif)

## Installation

- You can easily install the plug-in through Package Control (https://packagecontrol.io/).

- If you want to install this plug-in manually for some reason, simply clone this repo into your packages directory (make sure not to put it in the user sub dir).

## Instruction

1. Select a color declaration (e.g. '#008080', 'rgb(0,128,128)', or 'hsl(39.84,100.0%,25.1%)')
2. Mac user can use `cmd+alt+c`, Windows and Linux user can use `ctrl+alt+c`

OR:

1. Select a color declaration
2. Right click and choose `ColorConvert`, click the mode you need to convert.

## Settings

- `convert_mode`: convert to rgba mode, default `rgb`
- `capitalization`: whether the converted letters need to be capitalized, default `false`.
- `is_android`: Hex containing transparency is not the same format in android and css,if you are a Android Developer, please change it to `true`.

## Support

- Support `RGB`,`RGBA`,`HEX`,`HSL`,`HSLA`,`HSV`,`CMYK` to convert each other.
- Support [css3 color name](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value) convert to `HEX`
- Support convert the color values in the entire page.
- Support css color name and hex conversion

## Notes

1. Do not support css3 color:`transparent` and `currentColor`.
2. When `RGBA` is converted to other color value(like `RGB`,`HSL` etc...) it will lose the alpha value.
3. Some values are lost when some precision values are converted to CMYK and HSV, this is the result of the algorithm, so be careful in the process of using it.
