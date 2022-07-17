#!/usr/bin/env python

##
##  I stole this here https://stackoverflow.com/a/31125282 !
## 

import math
from PIL import Image
width, height = 1000, 200
im = Image.new('RGB', (width, height))
ld = im.load()

# A map of rgb points in your distribution
# [distance, (r, g, b)]
# distance is percentage from left edge
heatmap = [
    [0.0, (0.5, 0, 0)],
    [0.34, (0, 0.5, 0)],
    [0.64, (0, 0, .5)],
    [0.74, (0, 0, 0)],
    [0.88, (.5, .5, .5)],
]
heatmap2 = [
    [0.0, (.5, 0, 0)],
    [0.45, (0, .5, 0)],
    [0.60, (0, .5, 0)],
    [0.75, (0, .5, 0)],
    [0.90, (0, .5, 0)],
]

def gaussian(x, a, b, c, d=0):
    return a * math.exp(-(x - b)**2 / (2 * c**2)) + d

def pixel(x, width=100, map=[], spread=1.5):
    width = float(width)
    r = sum([gaussian(x, p[1][0], p[0] * width, width/(spread*len(map))) for p in map])
    g = sum([gaussian(x, p[1][1], p[0] * width, width/(spread*len(map))) for p in map])
    b = sum([gaussian(x, p[1][2], p[0] * width, width/(spread*len(map))) for p in map])
    return min(1.0, r), min(1.0, g), min(1.0, b)


for x in range(im.size[0]):
    r, g, b = pixel(x, width=im.size[0], map=heatmap, spread=1.7)
    r, g, b = [int(256*v) for v in (r, g, b)]
    for y in range(math.floor(im.size[1] / 2)):
        ld[x, y] = r, g, b
    # r, g, b = pixel(x, width=im.size[0], map=heatmap2, spread=1)
    # r, g, b = [int(256*v) for v in (r, g, b)]
    # for y in range(math.floor(im.size[1] / 2), im.size[1]):
    #     ld[x, y] = r, g, b

im.save('grad.png')