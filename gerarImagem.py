from PIL import Image
import numpy as np
import os.path
from charmap import charmap

def generateChar(color,bitImage,fileName):
    colorSelect = [[0, 0, 0],color]
    w, h = 8, 8
    data = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(8):
        for j in range(8):
            data[i:i+1, j:j+1] = colorSelect[int(bitImage[i][j])]
    img = Image.fromarray(data, 'RGB')
    img.save(f'./images/{fileName}.png')

bitImage0 =  [
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1]

            ]

bitImage1 =  [
                "00000000",
                "01100110",
                "01100110",
                "00000000",
                "00100100",
                "00100100",
                "00011000",
                "00000000"
            ]
#Colors
white = [255,255,255]
brown = [165,42,42]
green = [0,255,0]
oliveDrab = [107,142,35]
ultraMarine = [35,35,142]
darkPourple = [135,31,120]
teal = [0,128,128]
lavender = [220,232,250]
silver = [190,190,190]
red = [255,0,0]
limeGreen = [50,205,50]
yellow = [255,255,0]
blue = [0,0,255]
spicyPink = [255,28,174]
deYork = [122,219,147]
black = [0,0,0]

#Color sequence
colorSequence = [[255,255,255],[165,42,42],[0,255,0],[107,142,35],[35,35,142],[135,31,120],[0,128,128],[220,232,250],[190,190,190],[255,0,0],[50,205,50],[255,255,0],[0,0,255],[255,28,174],[122,219,147],[0,0,0]]

newpath = r'images'
if not os.path.exists(newpath):
    os.makedirs(newpath)

for i in range(128):
    generateChar(colorSequence[5],charmap[i],f"s{i}")

for i in range(16):
    generateChar(colorSequence[i],bitImage0,f"p{i}")

for i in range(1200):
    generateChar(black,bitImage0,f"m{i}")