# Objectives

Goals:
- Visual appeal: Outputs need to be visually appealing for the consuming app(s) to not be degraded by this feature. If the icons generated are joyful/inspiring, that is better.  But the icons should not be overly distracting or likely to clash with a business UI, either.
- Uniqueneness: We want similar-looking inputs to have noticably different outputs.
- Speed: We want generation/availability fast enough to load into the app.
- Repeatabilty: Any app in our ecosystem could (re)generate a "match" programmatically if the input same is exactly the same, assuming that app knows the algorithm.
- Gestalt: The icons should all fit well together as a family, if many are seen together in a collection/list.
- Suitabilty for use: in practice, image sizes should be possible for squares with edges ranging from roughly 32px to 512px.  Output the requested size, make all these look ok (32, 64, 128, 512 pixel sizes ok for simplicity).
- Storage space - store reasonably compactly.
- Accessibility - be accommodating of possible visual impairment; for example, for color blindness, make it possible to avoid blue-green and yellow-red ambiguity, if wanted.


# Files
## Code
- `identicandy.py` - the main module
- `svg_color_words.py` - the module to configure color themes
## Documentation
- `example_output_gallery.pdf` - contains sample generated images using various settings
- `README.md` - this file


# Environment setup

Install modules if needed, e.g.:

```
pip install docopt cairosvg svgwrite
```

or, if using conda, something like:

```
conda create -n identicandy1
conda activate identicandy1 
conda install -c conda-forge docopt cairosvg svgwrite
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
You are encouraged to try your own settings.  Below are simply references showing the syntax:
```
# Show help
./identicandy.py -h

# Default usage
./identicandy.py render_icon Jon
./identicandy.py render_icon John  # See output is different for similar input
./identicandy.py render_icon John  # See output is the same for the exact same input
./identicandy.py render_icon Jane
./identicandy.py render_icon 931D387731bBbC988B31220
./identicandy.py render_icon "name@example.com"
./identicandy.py render_icon "Firstname Lastname"

# Add 200px and 300px PNG images to output
./identicandy.py render_icon John -i 200 -i 300

# Specify fewer colors, but with increasing complex grids
./identicandy.py render_icon Bob -c web_colors_16 -g 6
./identicandy.py render_icon Bob -c web_colors_16 -g 12

# Specify specific a specific blue theme and high complexity
./identicandy.py render_icon Bob -c svg_blues_27 -g 12 

# Specify specific color theme and high complexity, avoiding specific colors, and providing debug level output logs
./identicandy.py render_icon Bob -c svg_blues_27 -g 12 -n indigo -n lightblue -n mediumblue --debug
```
