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
      surface_list.append(f'images/{image}')

  return surface_list

def joinImage(imageList, name):
  if name == "": name = "Screen"
  images = []

  for i in range(1200):
    temp = Image.open(f'images/m{i}.png')
    keep = temp.copy()
    images.append(keep)
    temp.close()
  new_im = Image.new('RGB', (40 * 8, 30 * 8))

  x_offset = 0
  y_offset = 0
  for index, im in enumerate(images):
    if index % 40 == 0 and index != 0:
      x_offset = 0
      y_offset += 8
    new_im.paste(im, (x_offset, y_offset))
    x_offset += 8

  new_im.save(f'./screens/{name}.png')

def joinPersona(persona, name):
  if persona:
    xmin = persona[0][0] % 40
    xmax = persona[0][0] % 40
    ymin = persona[0][0] // 40
    ymax = persona[0][0] // 40

    for character in persona:
      if character[0] % 40 < xmin:
        xmin = character[0] % 40
      if character[0] % 40 > xmax:
        xmax = character[0] % 40
      if character[0] // 40 < ymin:
        ymin = character[0] // 40
      if character[0] // 40 > ymax:
        ymax = character[0] // 40

    if name == "": name = "Persona"
    images = []

    for character in persona:
      temp = Image.open(f'images/p{character[0]}.png')
      keep = temp.copy()
      images.append(keep)
      temp.close()
    new_im = Image.new('RGB', ((xmax - xmin +1) * 8, (ymax - ymin +1) * 8))

    for index, character in enumerate(persona):
      new_im.paste(images[index], ((character[0] % 40 - xmin) * 8, (character[0] // 40 - ymin) * 8))

    new_im.save(f'./persona/{name}.png')