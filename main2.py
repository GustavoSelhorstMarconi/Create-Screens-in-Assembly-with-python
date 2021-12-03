import pygame, sys

def imprimirQuadradosTeste(xinicio, yinicio, linha, coluna, tamanho, gap, cor):
  for i in range(linha):
    for j in range(coluna):
      pygame.draw.rect(screen, cor, (xinicio+j*(tamanho+gap), yinicio+i*(tamanho+gap), tamanho, tamanho))

pygame.init()
screen_x = 450 * 2
screen_y = 350 * 2
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()

pixels = [["00000000"],
          ["01000010"],
          ["00000000"],
          ["01011010"],
          ["00011000"],
          ["00011000"],
          ["01111110"],
          ["00000000"]]

# Textos
fontetxt = pygame.font.SysFont('None', 40)
fonte_render = fontetxt.render('Gerador de Tela Assembly ICMC', True, (111, 196, 169))
fonte_rect = fonte_render.get_rect(center = (screen_x / 2, 30))

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
      
  screen.fill((114, 132, 157))

  imprimirQuadradosTeste(30,50,4,32,16,4,"black")
  pygame.draw.rect(screen, "white", (25, 135, 650, 490))

  imprimirQuadradosTeste(30,140,30,40,16,0,"black")
  imprimirQuadradosTeste(720,50,4,4,16,4,"red")

  screen.blit(fonte_render,fonte_rect)
  pygame.display.update()
  clock.tick(60)
