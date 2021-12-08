import pygame, sys
import pygame_textinput
from os import walk
from PIL import Image
import numpy as np
import os.path
from gerarImagem import generateChar, bitImage0, bitImage1
from charmap import charmap, charmapDescription

def import_folders(path):
  surface_list = []

  for _, __, image_files in walk(path):
    for image in image_files:
      #full_path = path + '/' + image
      #image_surf = pygame.image.load(full_path).convert_alpha()
      surface_list.append(image)

  return surface_list

def updateColors(color):
  create_selects(color)
  for sprite in characterSelected_group.sprites():
    sprite.updateColor(color)

def create_selects(color):
  xstart = 30
  ystart = 60
  for i in range(128):
    generateChar(colorSequence[color],charmap[i],f"s{i}")
  for sprite in charactere_group.sprites():
    sprite.updateImage()
    sprite.color = color

def changeCharacterSelected(index_charmap, color):
  bitSequence = ""
  cont = 0
  for row in charmap[index_charmap]:
    bitSequence += row

  for sprite in characterSelected_group.sprites():
    sprite.updateCharacterSelected(int(bitSequence[cont]), index_charmap, color)
    cont += 1

def updateCharacter(color, index_charmap):
  generateChar(colorSequence[color], charmap[index_charmap], f's{index_charmap}')
  create_selects(color)

class Charactere(pygame.sprite.Sprite):
  def __init__(self, xstart, ystart, image, description, color, index_charmap):
    super().__init__()
    self.image = pygame.image.load(f'images/{image}')
    self.image = pygame.transform.scale2x(self.image)
    self.rect = self.image.get_rect(topleft = (xstart, ystart))

    self.name = image
    self.description = description
    self.pos = pygame.math.Vector2(xstart, ystart)
    self.color = color
    self.index_charmap = index_charmap

    self.control_mouse_press = False
  
  def detection_click(self):
    if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
      self.control_mouse_press = True
      changeCharacterSelected(self.index_charmap, self.color)
    if pygame.mouse.get_pressed()[0] and not self.rect.collidepoint(pygame.mouse.get_pos()):
      self.control_mouse_press = False
  
  def updateImage(self):
    self.image = pygame.image.load(f'images/{self.name}')
    self.image = pygame.transform.scale2x(self.image)
  
  def update(self):
    self.detection_click()

class CharacterSelected(pygame.sprite.Sprite):
  def __init__(self, xstart, ystart):
    super().__init__()
    self.image = pygame.Surface((16, 16))
    self.rect = self.image.get_rect(topleft = (xstart, ystart))
    self.selected = False
    self.color = 0
    self.handled = False

    self.index_charmap = 0

  def updateColor(self, color):
    self.color = color
    if self.selected:
      self.image.fill(colorSequence[self.color])
    else:
      self.image.fill('black')
  
  def updateCharacterSelected(self, selected, index_charmap, color):
    self.selected = bool(selected)
    self.index_charmap = index_charmap
    self.color = color
    if self.selected:
      self.image.fill(colorSequence[self.color])
    else:
      self.image.fill('black')
  
  def detection_click(self):
    global mouse_pressed
    if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()) and mouse_pressed == False:
      mouse_pressed = True
      self.selected = not self.selected
      if self.selected:
        self.image.fill(colorSequence[self.color])
      else:
        self.image.fill('black')
    
    elif not pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
      mouse_pressed = False
  
  def display_text(self):
    fontetxt = pygame.font.SysFont('None', 40)
    fonte_render = fontetxt.render(str(self.index_charmap), True, (30, 30, 30))
    fonte_rect = fonte_render.get_rect(center = (875, 360))
    screen.blit(fonte_render, fonte_rect)
  
  def update(self):
    self.detection_click()
    self.display_text()

class ColorPalette(pygame.sprite.Sprite):
  def __init__(self, xstart, ystart, color, index):
    super().__init__()
    self.image = pygame.Surface((32, 32))
    self.image.fill(color)
    self.rect = self.image.get_rect(topleft = (xstart, ystart))

    self.selection = False
    self.index = index

    if color == [255,255,255]:
      self.selection = True
    else: self.selection = False
  
  def display(self):
    screen.blit(self.image, self.rect)

  def detection_click(self):
    if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
      self.pos = pygame.mouse.get_pos()
      self.remove_detection()
      self.selection = True
      updateColors(self.index)
    if self.selection:
      marcacao = pygame.image.load('marcacao.png').convert_alpha()
      marcacao = pygame.transform.scale(marcacao, (36, 36))
      screen.blit(marcacao, (self.rect.topleft - pygame.math.Vector2(2, 2)))
  
  def remove_detection(self):
    for sprite in palette_group.sprites():
      sprite.selection = False
  
  def update(self):
    self.detection_click()
    self.display()

class Button(pygame.sprite.Sprite):
  def __init__(self, posx, posy, text, color, width, height, text_size):
    super().__init__()
    self.image = pygame.Surface((width, height))
    self.image.fill(color)
    self.rect = self.image.get_rect(topleft = (posx, posy))
    self.text = text
    
    self.fontetxt = pygame.font.SysFont('None', text_size)
    self.text_render = self.fontetxt.render(self.text, True, (30, 30, 30))
    self.text_rect = self.text_render.get_rect(center = (self.rect.center))

  def detectButton(self):
    if self.text == 'Salvar Alteração':
      self.saveChange()
  
  def saveChange(self):
    if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
      newCharmap = []
      newCharAux = ""
      indexAux = 0
      colorAux = 0
      for index, sprite in enumerate(characterSelected_group.sprites()):
        if index == 0:
          indexAux = sprite.index_charmap
          colorAux = sprite.color
        if index != 0 and index %8 == 0:
          newCharmap.append(newCharAux)
          newCharAux = ""
        if not sprite.selected:
          newCharAux += "0"
        if sprite.selected:
          newCharAux += "1"
      newCharmap.append(newCharAux)
      charmap[indexAux] = newCharmap
      updateCharacter(colorAux, indexAux)

  def display(self):
    screen.blit(self.text_render, self.text_rect)
  
  def update(self):
    self.display()
    self.detectButton()

class Matrix(pygame.sprite.Sprite):
  def __init__(self, xstart, ystart, image, index_charmap, index_color):
    super().__init__()
    self.image = pygame.image.load(f'images/{image}.png').convert_alpha()
    self.image = pygame.transform.scale2x(self.image)
    self.rect = self.image.get_rect(topleft = (xstart, ystart))

    self.index_charmap = index_charmap
    self.index_color = index_color

pygame.init()
screen_x = 450 * 2
screen_y = 350 * 2
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()

# Text input
textinput = pygame_textinput.TextInputVisualizer()

# Colors
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

# Generate Images
newpath = r'images'
if not os.path.exists(newpath):
  os.makedirs(newpath)

for i in range(128):
  generateChar(colorSequence[0],charmap[i],f"s{i}")

for i in range(16):
  generateChar(colorSequence[i],bitImage0,f"p{i}")

for i in range(1200):
  generateChar(black,bitImage0,f"m{i}")

# Texts
fontetxt = pygame.font.SysFont('None', 40)
fonte_render_title = fontetxt.render('Gerador de Tela Assembly ICMC', True, (30, 30, 30))
fonte_rect_title = fonte_render_title.get_rect(center = (screen_x / 2 - 110, 30))

fontetxt = pygame.font.SysFont('None', 30)
fonte_render_edit = fontetxt.render('Editar caractere', True, (30, 30, 30))
fonte_rect_edit = fonte_render_edit.get_rect(topleft = (710, 200))

# Groups
charactere_group = pygame.sprite.Group()
palette_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()
matrix_group = pygame.sprite.Group()
characterSelected_group = pygame.sprite.Group()

# Add button
button_group.add(Button(710, 500, 'Gerar charmap', 'Green', 160, 60, 30))
button_group.add(Button(710, 580, 'Gerar tela', 'Green', 160, 60, 30))
button_group.add(Button(710, 380, 'Salvar Alteração', 'Green', 135, 25, 20))

# Add character
xstart = 30
ystart = 60
for i in range(4):
  for j in range(32):
    charactere_group.add(Charactere(xstart+j*20, ystart+i*20, f's{32*i+j}.png', charmapDescription[32*i+j], 0, 32*i+j))

# Add color palette
xstart = 710
ystart = 20
for i in range(4):
  for j in range(4):
    palette_group.add(ColorPalette(xstart+j*40, ystart+i*40, colorSequence[4*i+j], 4*i+j))

# Add matrix
xstart = 30
ystart = 160
for i in range(30):
  for j in range(40):
    matrix_group.add(Matrix(xstart+j*16, ystart+i*16, f'm{32*i+j}', 32*i+j, 0))

# Add character selected
xstart = 710
ystart = 240
for i in range(8):
  for j in range(8):
    characterSelected_group.add(CharacterSelected(xstart+j*17, ystart+i*17))

while True:
  events = pygame.event.get()

  for event in events:
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
      
  screen.fill((114, 132, 157))

  # Matrix display
  matrix_group.update()
  matrix_group.draw(screen)

  # Palette display
  palette_group.update()
  palette_group.draw(screen)

  # Button display
  button_group.draw(screen)
  button_group.update()

  # Characteres display
  charactere_group.update()
  charactere_group.draw(screen)

  # Charactere Selected display
  characterSelected_group.update()
  characterSelected_group.draw(screen)

  textinput.update(events)
  screen.blit(textinput.surface, (710, 450))

  # Display texts
  screen.blit(fonte_render_title, fonte_rect_title)
  screen.blit(fonte_render_edit, fonte_rect_edit)

  pygame.display.update()
  clock.tick(60)