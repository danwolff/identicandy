#!/usr/bin/env python

'''
Call get_svg_color() to get a color 

Inputs are both optional:
 - specify a theme to constrain the selection
 - specify an exclusion list to further constrain the selection

Outputs:
 - a random eligible color
 - a list of all eligible colors

The 147 SVG color words are from https://www.w3.org/TR/SVG11/types.html#ColorKeywords
The 16 HTML 4.01 colors are from https://www.w3.org/TR/html401/types.html#h-6.5

'''

import logging
import random

def get_svg_color(theme='svg_colors_140', excluded_colors=[]):
    svg_colors_140 = [
        'aliceblue',
        'antiquewhite',
        'aqua',
        'aquamarine',
        'azure',
        'beige',
        'bisque',
        'black',
        'blanchedalmond',
        'blue',
        'blueviolet',
        'brown',
        'burlywood',
        'cadetblue',
        'chartreuse',
        'chocolate',
        'coral',
        'cornflowerblue',
        'cornsilk',
        'crimson',
        'cyan',
        'darkblue',
        'darkcyan',
        'darkgoldenrod',
        'darkgray',
        'darkgreen',
        'darkkhaki',
        'darkmagenta',
        'darkolivegreen',
        'darkorange',
        'darkorchid',
        'darkred',
        'darksalmon',
        'darkseagreen',
        'darkslateblue',
        'darkslategray',
        'darkturquoise',
        'darkviolet',
        'deeppink',
        'deepskyblue',
        'dimgray',
        'dodgerblue',
        'firebrick',
        'floralwhite',
        'forestgreen',
        'fuchsia',
        'gainsboro',
        'ghostwhite',
        'gold',
        'goldenrod',
        'gray',
        'green',
        'greenyellow',
        'honeydew',
        'hotpink',
        'indianred',
        'indigo',
        'ivory',
        'khaki',
        'lavender',
        'lavenderblush',
        'lawngreen',
        'lemonchiffon',
        'lightblue',
        'lightcoral',
        'lightcyan',
        'lightgoldenrodyellow',
        'lightgray',
        'lightgreen',
        'lightpink',
        'lightsalmon',
        'lightseagreen',
        'lightskyblue',
        'lightslategray',
        'lightsteelblue',
        'lightyellow',
        'lime',
        'limegreen',
        'linen',
        'magenta',
        'maroon',
        'mediumaquamarine',
        'mediumblue',
        'mediumorchid',
        'mediumpurple',
        'mediumseagreen',
        'mediumslateblue',
        'mediumspringgreen',
        'mediumturquoise',
        'mediumvioletred',
        'midnightblue',
        'mintcream',
        'mistyrose',
        'moccasin',
        'navajowhite',
        'navy',
        'oldlace',
        'olive',
        'olivedrab',
        'orange',
        'orangered',
        'orchid',
        'palegoldenrod',
        'palegreen',
        'paleturquoise',
        'palevioletred',
        'papayawhip',
        'peachpuff',
        'peru',
        'pink',
        'plum',
        'powderblue',
        'purple',
        'red',
        'rosybrown',
        'royalblue',
        'saddlebrown',
        'salmon',
        'sandybrown',
        'seagreen',
        'seashell',
        'sienna',
        'silver',
        'skyblue',
        'slateblue',
        'slategray',
        'snow',
        'springgreen',
        'steelblue',
        'tan',
        'teal',
        'thistle',
        'tomato',
        'turquoise',
        'violet',
        'wheat',
        'white',
        'whitesmoke',
        'yellow',
        'yellowgreen'
    ]
    logging.debug("length of svg_colors_140 is: " + str(len(svg_colors_140)))

    web_colors_16 = [
        'aqua',
        'black',
        'blue',
        'fuchsia',
        'gray',
        'green',
        'lime',
        'maroon',
        'navy',
        'olive',
        'purple',
        'red',
        'silver',
        'teal',
        'white',
        'yellow'
    ]
    logging.debug("length of web_colors_16 is: " + str(len(web_colors_16)))

    svg_blues_obvious = [color for color in svg_colors_140 if 'blue' in color]
    svg_blues_nonobvious = [
        'aqua', 
        'aquamarine', 
        'indigo', 
        'navy', 
        'mintcream',
        'paleturquoise', 
        'teal',
        'turquoise']
    svg_blues_27 = sorted(svg_blues_obvious + svg_blues_nonobvious)
    logging.debug("length of svg_blues_27 is: " + str(len(svg_blues_27)))

    svg_reds_obvious = [color for color in svg_colors_140 if 'red' in color]
    svg_reds_nonobvious = [
        'brown', 
        'coral', 
        'crimson', 
        'darkmagenta', 
        'darksalmon', 
        'deeppink', 
        'firebrick', 
        'fuchsia', 
        'hotpink', 
        'lightcoral', 
        'lightpink', 
        'lightsalmon', 
        'maroon', 
        'orange', 
        'orchid', 
        'pink', 
        'plum', 
        'purple', 
        'rosybrown', 
        'saddlebrown', 
        'salmon', 
        'sandybrown', 
        'sienna', 
        'tan', 
        'tomato', 
        'violet'
    ]
    svg_reds_32 = sorted(svg_reds_obvious + svg_reds_nonobvious)
    logging.debug("length of svg_reds_32 is: " + str(len(svg_reds_32)))

    svg_greens_obvious = [color for color in svg_colors_140 if 'green' in color]
    svg_greens_nonobvious = [
        'aquamarine', 
        'cadetblue', 
        'darkcyan', 
        'darkslategray', 
        'gray', 
        'khaki', 
        'lightgoldenrodyellow', 
        'lightgray', 
        'lightslategray', 
        'lime', 
        'mediumaquamarine', 
        'mediumturquoise', 
        'olive', 
        'olivedrab', 
        'teal', 
        'turquoise', 
        'yellowgreen'
    ]
    svg_greens_33 = sorted(svg_greens_obvious + svg_greens_nonobvious)
    logging.debug("length of svg_greens_33 is: " + str(len(svg_greens_33)))


    if theme == 'web_colors_16':
        start_colors = web_colors_16
    elif theme == 'svg_colors_140':
        start_colors = svg_colors_140
    elif theme == 'svg_reds_32':
        start_colors = svg_reds_32
    elif theme == 'svg_greens_33':
        start_colors = svg_greens_33
    elif theme == 'svg_blues_27':
        start_colors = svg_blues_27

    filtered_colors = [color for color in start_colors if color not in excluded_colors]

    return [random.choice(filtered_colors), sorted(filtered_colors)]

def main():
    logging.basicConfig()
    # logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().setLevel(logging.INFO)

    rand_color, all_colors = get_svg_color(theme='web_colors_16')
    logging.info(f"rand_color = {rand_color}")
    logging.info(f"all_colors = {all_colors}")

if __name__ == "__main__": 
    main()
