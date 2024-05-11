#!/usr/bin/env python3

"""
Generate a fairly unique user icon based on an arbitrary string.
The output is an SVG image and several PNG images of various sizes.

Usage:
  identicandy.py [options] render_icon <user_string>
      [-c <theme> -i <px>... -g <num> -n <color>...]

Commands:
  identicandy.py render_icon          Create an identicandy icon

Options:
  -h, --help                          Show this help.
  -c <theme>, --colors=<theme>        Force palette to any of: svg_colors_140, 
                                      svg_reds_32, svg_greens_33, svg_blues_27
                                      or web_colors_16
                                      [Default: svg_colors_140]
  -i <px>, --include_png_size=<px>    Ensure PNG creation of specific size.
                                      Just provide an integer for edge pixels.
                                      For example, 200
                                      Multiple of this option can be included.
  -g <num>, --grid=<num>              Change the complexity as an integer.
                                      Higher is more complex.
                                      Suggested range is 2 to 10, not higher.
                                      [Default: 4]
  -n <color>, --not_color <color>     Colors to NOT use. Specify using color
                                      names from svg_color_words.py
                                      Multiple of this option can be included.
  -q, --quiet                         Log very little
  --verbose                           Log a lot
  --debug                             Log even more to fix things
  --version                           Show the version
"""

from datetime import datetime
from docopt import docopt
import cairosvg
import logging
import os
import svgwrite
from hashlib import sha256
import svg_color_words

VERSION = "v0.0.2"
# Changes
# v0.0.2   Fix --not_color option to work.

def create_out_dir(user_string):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    subdirectory_name = f"output/{timestamp}_{user_string}"
    current_directory = os.getcwd()
    subdirectory_path = os.path.join(current_directory, subdirectory_name)
    if not os.path.exists(subdirectory_path):
        os.makedirs(subdirectory_path)
    logging.debug(f"Tried creating dir {subdirectory_name} if needed")
    return subdirectory_name


def find_points(scaled_integer, grid_edge_cell_count, cell_count):
    if scaled_integer < 1 or scaled_integer > 2**cell_count:
        return "Not in range.  Expected base-10 integer from 1 to 2^(number of cells)."

    filled_cells = []

    # Convert to binary representation and left-pad to ensure length of 100 bits
    binary_form = bin(scaled_integer)[2:].zfill(cell_count)
    logging.debug(f"binary_form = {binary_form}")

    # Iterate over each bit in the binary representation
    for i in range(len(binary_form)):
        # If the bit is '1', the corresponding cell is filled
        if binary_form[i] == '1':
            # Calculate the row and column indices
            row = i // grid_edge_cell_count
            col = i % grid_edge_cell_count
            filled_cells.append((row, col))

    return filled_cells

def convert_svg_to_png(input_svg, output_png, width, height):
    cairosvg.svg2png(url=input_svg, write_to=output_png, output_width=width, 
                     output_height=height)

def make_all_png_sizes(filename_svg, out_dir, png_sizes_to_add):
    logging.debug(f"filename_svg = {filename_svg}")
    logging.debug(f"out_dir = {out_dir}")
    png_sizes = {24, 32, 64, 128, 512}
    png_sizes.update(png_sizes_to_add)
    created_cnt = 0
    for png_size in png_sizes:
        convert_svg_to_png(filename_svg, os.path.join(out_dir, 
                           f"{png_size}px.png"), png_size, png_size)
        created_cnt += 1
    return created_cnt

def determine_bkg_color(string_hash, color_options):
    option_space_size = len(color_options)
    logging.debug(f"bkg string_hash = {string_hash}")
    integer_from_hexadecimal_hash = int(string_hash, 16)
    logging.debug(f"bkg integer_from_hexadecimal_hash = "
                  f"{integer_from_hexadecimal_hash}")
    upper_limit = option_space_size
    logging.debug(f"bkg upper_limit = {upper_limit}")
    scaled_integer = integer_from_hexadecimal_hash % upper_limit  
    # TODO: should above have a +1?
    logging.debug(f"bkg scaled_integer = {scaled_integer}")
    determined_bkg_color = color_options[scaled_integer] 
    return determined_bkg_color

def determine_cell_fill_color(string_hash, color_options, point_qty, idx):
    option_space_size = len(color_options)
    logging.debug(f"cell fill string_hash = {string_hash}")
    integer_from_hexadecimal_hash = int(string_hash, 16)
    logging.debug(f"cell fill integer_from_hexadecimal_hash = "
                  f"{integer_from_hexadecimal_hash}")
    upper_limit = option_space_size
    logging.debug(f"cell fill upper_limit = {upper_limit}")
    scaled_color_idx = integer_from_hexadecimal_hash % upper_limit  
    # TODO: should above have the +1?
    logging.debug(f"cell fill scaled_color_idx = {scaled_color_idx}")

    color_idx_before_adjustment = scaled_color_idx
    color_idx_mid_adjustment = scaled_color_idx + idx
    color_idx_after_adjustment = color_idx_mid_adjustment % option_space_size

    determined_cell_fill_color = color_options[color_idx_after_adjustment] 
    return determined_cell_fill_color

def create_svg(points, out_dir, clean_string, string_hash, color_palette,
               grid_edge_cell_count, exclude_colors):
    VIEWBOX_EDGE_LENGTH = 1000  # Internal user space coordinate system size 
    half_viewbox_edge_length = VIEWBOX_EDGE_LENGTH / 2
    _cell_edge_length = half_viewbox_edge_length / grid_edge_cell_count 
    # Ex: 1000 units / 10 cells = 100 unit/cell edge


    # Sort the input list of points by x and then by y
    sorted_points = sorted(points)
    logging.debug(f"sorted_points = {sorted_points}")

    filename_svg = f"{out_dir}/{clean_string}_{string_hash}.svg"

    dwg = svgwrite.Drawing(filename_svg, size=('8in', '8in'), profile='full', 
                           debug=True)

    dwg.viewbox(width=VIEWBOX_EDGE_LENGTH, height=VIEWBOX_EDGE_LENGTH)

    rand_bkg_color, available_bkg_colors = svg_color_words.get_svg_color(
        theme=color_palette,
        excluded_colors = exclude_colors
    ) # We don't use rand_bkg_color, but we use a deterministic one instead

    bkg_color = determine_bkg_color(
            string_hash,
            available_bkg_colors)
    logging.debug(f"bkg_color = {bkg_color}")
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=bkg_color))

    idx = 0
    for cell in points:
        idx = idx + 1
        x, y = cell
        logging.debug(f"Cell at (x, y) of ({x}, {y}) ")

        # top-left quadrant
        x1 = x * _cell_edge_length 
        y1 = y * _cell_edge_length 

        # top-right quadrant 
        x2 = VIEWBOX_EDGE_LENGTH - x1 - _cell_edge_length
        y2 = y1

        # bottom-left quadrant
        x3 = x1
        y3 = VIEWBOX_EDGE_LENGTH - y1 - _cell_edge_length 

        # bottom-right quadrant 
        x4 = VIEWBOX_EDGE_LENGTH - x1 - _cell_edge_length
        y4 = VIEWBOX_EDGE_LENGTH - y1 - _cell_edge_length

        width = _cell_edge_length
        height = _cell_edge_length
        
        all_excluded_colors = [bkg_color] + exclude_colors
        logging.debug(f"all_excluded_colors = {all_excluded_colors}")
        rand_fill_color, fill_color_options = svg_color_words.get_svg_color(
            theme=color_palette, 
            excluded_colors=all_excluded_colors)

        # fill_color = rand_fill_color 
        fill_color = determine_cell_fill_color(
            string_hash,
            fill_color_options,
            len(points),
            idx)
        logging.debug(f"fill_color = {fill_color}")

        dwg.add(dwg.rect((x1, y1), (width, height), fill=fill_color))
        dwg.add(dwg.rect((x2, y2), (width, height), fill=fill_color))
        dwg.add(dwg.rect((x3, y3), (width, height), fill=fill_color))
        dwg.add(dwg.rect((x4, y4), (width, height), fill=fill_color))
        logging.debug(f"Cell at (x, y) = ({x}, {y}) ")
        logging.debug(f"Rect at (x1, y1) = ({x1}, {y1}) ")
        logging.debug(f"Rect at (x2, y2) = ({x2}, {y2}) ")
        logging.debug(f"Rect at (x2, y3) = ({x3}, {y3}) ")
        logging.debug(f"Rect at (x2, y4) = ({x4}, {y4}) ")

    dwg.save()
    logging.debug("Done saving SVG")

    return filename_svg

def create_icon(clean_string, out_dir, color_palette, png_sizes_to_add, 
        grid_edge_cell_count, exclude_colors):

    cell_count = grid_edge_cell_count**2 

    hash_from_clean_string = sha256(clean_string.encode('utf-8')).hexdigest()

    integer_from_hexadecimal_hash = int(hash_from_clean_string, 16)
    logging.debug(f"create_icon integer_from_hexadecimal_hash = {integer_from_hexadecimal_hash}")
    logging.debug(f"create_icon integer_from_hexadecimal_hash = "
                  f"{integer_from_hexadecimal_hash}")
    upper_limit = 2**cell_count  # possible combinations of active/inactive grid cells 
    logging.debug(f"create_icon upper_limit = {upper_limit}")
    # Ok to reduce unqiueness slightly here since we add in more uniqueness 
    # later through colors.  Also, start numbering cells at 1.
    scaled_integer = integer_from_hexadecimal_hash % upper_limit + 1
    # TODO: should above this have the +1?
    filled_cells = find_points(scaled_integer, grid_edge_cell_count, cell_count)

    svg_created = create_svg(filled_cells, out_dir, clean_string, 
                             hash_from_clean_string, color_palette, 
                             grid_edge_cell_count, exclude_colors)
    logging.debug(f"Made SVG, returned was: {svg_created}")
    pngs_created_cnt = make_all_png_sizes(svg_created, out_dir, png_sizes_to_add)

    logging.debug(f"filled_cells = {filled_cells}")
    
    logging.debug(f"pngs_created_cnt = {pngs_created_cnt}")

    return pngs_created_cnt

def main(args):
    logging.basicConfig()
    if args['--verbose'] == True:
        logging.getLogger().setLevel(logging.INFO)
    elif args['--quiet'] == True:
        logging.getLogger().setLevel(logging.ERROR)
    elif args['--debug'] == True:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.WARNING)
    logging.debug("Got args:\n{args}".format(**locals()))

    color_palette = 'svg_colors_140'
    if args['--colors']:
        logging.debug("Arg for --colors was:")
        logging.debug(args['--colors'])
        color_palette = args['--colors'].strip()

    png_sizes_to_add = {}
    if args['--include_png_size']:
        logging.debug("Arg for --include_png_size was:")
        logging.debug(args['--include_png_size'])
        include_png_sizes = args['--include_png_size']
        if include_png_sizes == ['""']:
            include_png_sizes = ()
        else: 
            png_sizes_to_add = {int(size) for size in include_png_sizes}

    exclude_colors = []
    if args['--not_color']:
        logging.debug("Arg for --not_color was:")
        logging.debug(args['--not_color'])
        exclude_colors = args['--not_color']
        if exclude_colors == ['""']:
            exclude_colors = []

    if args['--grid']:
        logging.debug("Arg for --grid was:")
        logging.debug(args['--grid'])
        grid_edge_cell_count = int(args['--grid'].strip())

    if args['render_icon'] == True:
        user_string = args['<user_string>'].strip()
        subdirectory_name = create_out_dir(user_string)
        logging.debug(f"subdirectory_name = {subdirectory_name}")

        pngs_created_cnt = create_icon(
            user_string, 
            subdirectory_name, 
            color_palette,
            png_sizes_to_add,
            grid_edge_cell_count,
            exclude_colors
        )

        if pngs_created_cnt > 0:
            logging.info(f"Done rendering SVG and {pngs_created_cnt} PNG icons.  "
                          "Check ./output directory.")
        else:
            logging.warning("Failed to render icon.  Check logs or enable debugging.")

if __name__ == "__main__": 
    arguments = docopt(__doc__, version=VERSION)
    main(arguments)
