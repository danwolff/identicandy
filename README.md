# Objectives

Goals:
- Visual appeal: Outputs need to be visually appealing for the app to not be degarded by this. If they are joyful/inspiring, that is better.  But they should not be overly distracting or likely to clash with a business UI, either.
- Uniqueneness: We want similar-looking inputs to have noticably different outupts.
- Speed: We want generation/availability fast enough to load into the app.
- Repeatabilty: Any app in our ecosystem could (re)generate a "match" programmatically if the input same is exactly the same, assuming that app knows the algorithm.
- Gestalt: The icons should all fit well together as a family, if many are seen together in a collection/list.
- Suitabilty for use: in practice, image sizes should be possible for squares with edges ranging from roughly 32px to 512px.  Output the requested size, make all these look ok (32, 64, 128, 512 pixel sizes ok for simplicity).
- Storage space - store reasonably compactly.
- Accessibility - be accommodating of color blindness by avoiding Blue-Green and Yellow-Red issues if needed may be developed.


# Files
- `identicandy.zip` - all files
  - `identicandy.py` - the main module
  - `svg_color_words.py` - help module where we configure color themes
  - `README.md` - this file


# Environment setup

Install modules if needed, e.g.:

```
conda create -n "idneticandy1"
conda activate idneticandy1
conda install -c conda-forge docopt cairosvg python-xxhash svgwrite
```


# Usage

The built-in help output is pasted below:

```
$ ./identicandy.py -h
Generate a fairly unique user icon based on an arbitrary string.
The output is an SVG image and several PNG images of various sizes.

Usage:
  identicandy.py [options] render_icon <user_string>
      [-c <theme> -i <px>... -g <num> -n <color>...]

Commands:
  identicandy.py render_icon          Create an identicandy icon

Options:
  -h, --help                          Show this help
  -c <theme>, --colors=<theme>        Force palette to any of: svg_colors_140,
                                      svg_reds_32, svg_greens_33, svg_blues_27
                                      or web_colors_16
                                      [Default: svg_colors_140]
  -i <px>, --include_png_size=<px>    Ensure PNG creation of specific size
                                      Just provide an integer for edge pixels
                                      For example, 200
                                      Multiple of this option can be included
  -g <num>, --grid=<num>              Change the complexity as an integer
                                      Higher is more complex
                                      Approximate suggested range is 2 to 10.
                                      [Default: 4]
  -n <color>, --not_color <color>     Do not paint with these colors
                                      Use color names from svg_color_words.py
                                      Multiple of this option can be included
  -q, --quiet                         Log very little
  --verbose                           Log a lot
  --debug                             Log even more to fix things
  --version                           Show the version
```

# Example usage
./identicandy.py render_icon John
./identicandy.py render_icon Jane
./identicandy.py render_icon 931D387731bBbC988B31220

mkdir output
