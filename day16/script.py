import numpy as np
from functools import lru_cache
import sys
import resource
sys.setrecursionlimit(1000000)
Nmax=20
#resource.setrlimit(resource.RLIMIT_STACK, [0x1000000, resource.RLIM_INFINITY])
dataraw = """\
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....""".split("\n")
data = np.array([list(dat) for dat in dataraw])
with open("input.txt") as f:
    dataraw = [line.strip() for line in f]
data = np.array([list(dat) for dat in dataraw])
# \
backslash = {(1,0):(0,1),
             (0,-1):(-1,0),
             (0,1):(1,0),
             (-1,0):(0,-1)}
# /
slash = {(1,0):(0,-1),
         (0,1):(-1,0),
         (0,-1):(1,0),
         (-1,0):(0,1)}

@lru_cache(maxsize=None)
def do_step(irow, jcol, vrow, vcol):
    #print(irow, jcol, vrow, vcol)

    # update position
    irow, jcol = irow + vrow, jcol + vcol
    #print("updated:", irow, jcol, vrow, vcol)

    try:
        char = data[irow, jcol]
    except IndexError:
        return
    if irow<0 or jcol<0:
        return

    if vrow and char not in "-|":
        heatmap_horizontal[irow, jcol] += 1
        if heatmap_horizontal[irow, jcol] >=Nmax:
            return

    if vcol and char not in "-|":
        heatmap_vertical[irow, jcol] += 1
        if heatmap_vertical[irow, jcol] >=Nmax:
            return

    #print(char)

    if data[irow, jcol]=="\\":
        vrow, vcol = backslash[(vrow, vcol)]
        do_step(irow, jcol, vrow, vcol)
    elif data[irow, jcol]=="/":
        vrow, vcol = slash[(vrow, vcol)]
        do_step(irow, jcol, vrow, vcol)
    elif data[irow, jcol]=="|" and vcol:
        do_step(irow, jcol, 1, 0)
        do_step(irow, jcol,-1, 0)
    elif data[irow, jcol]=="-" and vrow:
        do_step(irow, jcol, 0, 1)
        do_step(irow, jcol, 0,-1)
    else: # if char . or v opposite to | or -
        do_step(irow, jcol, vrow, vcol)


irow, jcol = 0, 0
vrow, vcol = 0, 1

heatmap_horizontal = np.zeros(data.shape)
heatmap_vertical = np.zeros(data.shape)

do_step(irow, jcol, vrow, vcol)
canvas = np.full(data.shape, '.', dtype=str)
canvas[0,0]="#"
canvas[np.logical_or(heatmap_horizontal, heatmap_vertical)] = "#"
# too low: 8176 / # too low 8376 #9: 8378  #10: 8380 # 11: 8397 # 12: 8380
print(np.sum(np.logical_or(heatmap_horizontal, heatmap_vertical)) + 1)
