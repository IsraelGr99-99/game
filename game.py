import pygame
import random
import math
import sys
import os

#Inicializar pygame
pygame.init()

#Establecer el tamaño de la pantalla
screen_width = 800
screen_heigth = 600
screen = pygame.display.set_mode((screen_width,screen_width))

#Funcion para obtener la ruta de los recursos
def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
  
#Cargar background
asset_background = resource_path("assets/img/background.png")
background = pygame.image.load(asset_background)

#Cargar icon de ventana
asset_icon = resource_path("assets/img/ufo.png")
icon = pygame.image.load(asset_icon)

#Cargar sonido de fondo
asset_sound = resource_path("assets/audio/background_music.mp3")
background_sound = pygame.mixer.music.load(asset_sound)

#Cargar imagen de jugador
asset_player_img = resource_path("assets/img/space-invaders1.png")
player_img = pygame.image.load(asset_player_img)


#Cargar imagen de bala
asset_bullet_img = resource_path("assets/img/bullet.png")
bullet_img = pygame.image.load(asset_bullet_img)

#Cargar fuente de texto en game over
asset_over_font = resource_path("assets/fonts/RAVIE.TTF")
over_font = pygame.font.Font(asset_over_font, 60)

#Cargar fuente de texto de la puntuacion
asset_font = resource_path("assets/fonts/comicbd.ttf")
font = pygame.font.Font(asset_font, 32)

#Establecer el titulo de ventana
pygame.display.set_caption("Space Invader")

#Establecer el icon de la venta
pygame.display.set_icon(icon)

#Reproducir sonido de fondo en loop
pygame.mixer.music.play(-1)

#Crear reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

#Posicion inicial del jugador
playerX = 370
playerY = 470
playerX_change = 0
playerY_change = 0

#Lista para almacenar posiciones de los enemigs
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 10

#Se inicializan las variables para guardar las posiciones de los enemigos
for i in range(no_of_enemies):
  #Se cargan las imagenes del enemigo 1
  enemy1 = resource_path("assets/img/enemy1.png")
  enemy_img.append(pygame.image.load(enemy1))
  #Se cargan las imagenes del enemigo 2
  enemy2 = resource_path("assets/img/enemy2.png")
  enemy_img.append(pygame.image.load(enemy2))

  #Se asigna una posicion aleatoria en x para el enemigo
  enemyX.append(random.randint(0, 736))  
  enemyY.append(random.randint(0, 150))
  
  #Se establece la velocidad de movimiento del enemigo en X e Y
  enemyX_change.append(15)
  enemyY_change.append(30)

  #Se inicializan las variables para guardar la posicion de la bala
  bulletX = 0
  bulletY = 480
  bulletX_change = 0
  bulletY_change = 10
  bullet_state = "ready"

  #Se inicializa la puntuacion en 0
  score = 0

  #Funcion para mostrar la puntuacion en la pantalla
  def show_score():
    score_value = font.render("SCORE " + str(score), True, (255, 255, 255))
    screen.blit(score_value,(10,10))

  #Funcion para dibujar al jugor en la pantalla
  def player(x,y):
    screen.blit(player_img, (x,y))

  #Funcion para dibujar al enemigo en la pantalla
  def enemy(x, y, i):
    screen.blit(enemy_img[i],(x, y))

  #Funcion para disparar la bala
  def fire_bullet(x,y):
    global bullet_state

    bullet_state = "fire"
    screen.blit(bullet_img,(x + 16, y + 10))

  #Funcion para comprobar si existe colision entre bala y el enemigo
  def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) +
                         (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
      return True
    else:
      return False

  #Funcion para mostrar texto de game over
  def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    #Centrar texto
    text_rect = over_text.get_rect(
      center = (int(screen_width / 2), int(screen_heigth / 2)))
    screen.blit(over_text, text_rect)

  #Funcion principal del juego
  def gameloop():

    #Declarar variables glables
    global score
    global playerX
    global playerX_change
    global bulletX
    global bulletY
    global Collision
    global bullet_state

    in_game = True
    while in_game:
      #Maneja eventos, actualiza y renderiza el juego
      #Limpia la pantalla
      screen.fill((0, 0, 0))
      screen.blit(background, (0,0))

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          in_game = False
          pygame.quit()
          sys.exit()

        if event.type == pygame.KEYDOWN:
          #Maneja los movimientos del juegador y del disparo
          if event.key == pygame.K_LEFT:
            playerX_change = -5

          if event.key == pygame.K_RIGHT:
            playerX_change = 5
          
          if event.key == pygame.K_SPACE:
            if bullet_state == "ready":
              bulletX = playerX
              bulletY = playerY
              fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
          playerX_change = 0
          
          #Aqui actualiza la posicion del jugador
      playerX += playerX_change

      if playerX <= 0:
        playerX = 0 
      elif playerX >= 736:
        playerX = 736

      #Bucle que se ejecuta para cada enemigo
      for i in range(no_of_enemies):
        if enemyY[i] > 440:
          for j in range(no_of_enemies):
            enemyY[j] = 2000
          game_over_text()
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
          enemyX_change[i] = 5
          enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
          enemyX_change[i] = -5
          enemyY[i] += enemyY_change[i]

        #Aqui se comprueba si ha habido collision entre el enemigo y la bala

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
          bulletY = 454
          bullet_state = "ready"
          score += 1
          enemyX[i] = random.randint(0,736)
          enemyY[i] = random.randint(0, 150)
        enemy(enemyX[i], enemyY[i], i)
      
      if bulletY < 0:
        bulletY = 454
        bullet_state = "ready"
      if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

      player(playerX, playerY)
      show_score()

      pygame.display.update()

      clock.tick(120)       


gameloop()



