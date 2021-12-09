from PIL import Image
import numpy as np
from os import walk
import os.path

def generateChar(color,bitImage,fileName):
    colorSelect = [[0, 0, 0],color]
    w, h = 8, 8
    data = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(8):
        for j in range(8):
            data[i:i+1, j:j+1] = colorSelect[int(bitImage[i][j])]
    img = Image.fromarray(data, 'RGB')
    img.save(f'./images/{fileName}.png')

def import_folders(path):
  surface_list = []
  for _, __, image_files in walk(path):
    for image in image_files:
      surface_list.append(image)

  return surface_list