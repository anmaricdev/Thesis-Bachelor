GRID_COLOR = "BLACK"
FIGURE_MARGIN = 0.1
# With this you can configure which kind of colors each item gets.
# For this, a color gradient (colormap) is used.
# Please see here to find all the available colormaps:
# https://matplotlib.org/stable/gallery/color/colormap_reference.html
# I recommend not picking one, which has white in its gradient.
BIN_PACKING_COLORMAP_NAME = "gist_rainbow"
# If enabled, one cell will not always correspond to one unit, but scale according to size.
# For example, by having each cell represent two units.
ALLOW_SCALE_UNITS = True
BASE_GRID_WIDTH = 15
# When an approach fails to pack all the items in the bin, 
# a slightly transparent cross is displayed by default.
# Here one can configure how transparent the cross should be (0=fully transparent, 1=fully opaque)
FAILURE_MARKING_TRANSPARENCY = 0.3
# How large gap should be between bins.
GAP_BETWEEN_BINS = 0.05