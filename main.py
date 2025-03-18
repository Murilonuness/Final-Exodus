import random
import pygame

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('audio/Demoiselle Döner - Une très mauvaise idée.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
x, y = 1280, 720
font = pygame.font.SysFont("Arial", 36)
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption('Final Exodus')
icon = pygame.image.load('images/icon.webp').convert_alpha()
pygame.display.set_icon(icon)
bg = pygame.image.load('images/bg.jpg').convert_alpha()
bg = pygame.transform.scale(bg, (x, y))
alien = pygame.image.load('images/spaceship.png').convert_alpha()
alien = pygame.transform.scale(alien, (70, 70))
playerImg = pygame.image.load('images/nave.png').convert_alpha()
playerImg = pygame.transform.scale(playerImg, (70, 70))
missil = pygame.image.load('images/missil.png').convert_alpha()
missil = pygame.transform.scale(missil, (45, 45))

pos_alien_x, pos_alien_y = 500, 360
pos_player_x, pos_player_y = 200, 300
vel_missil_x, pos_missil_x, pos_missil_y = 0, 200, 300
triggered, rodando, pontos = False, True, 0

player_rect, alien_rect, missil_rect = playerImg.get_rect(), alien.get_rect(), missil.get_rect()

def respawn():
    return [random.randint(1300, 1350), random.randint(1, 640)]

def respawn_missil():
    global pos_missil_x, pos_missil_y, triggered, vel_missil_x  
    triggered, pos_missil_x, pos_missil_y, vel_missil_x = False, pos_player_x, pos_player_y, 0

def colisions(pontos):
    global pos_missil_x, pos_alien_x, pos_alien_y
    if missil_rect.colliderect(alien_rect):
        pontos += 5
        respawn_missil()
        pos_alien_x, pos_alien_y = respawn()
        return pontos, True
    elif player_rect.colliderect(alien_rect):
        pontos -= 5
        pos_alien_x, pos_alien_y = respawn()
        return pontos, True
    return pontos, False

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    screen.blit(bg, (0, 0))
    rel_x = x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    if rel_x < 1280:
        screen.blit(bg, (rel_x, 0))

    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and pos_player_y > 1:
        pos_player_y -= 1
        if not triggered:
            pos_missil_y -= 1
    if tecla[pygame.K_DOWN] and pos_player_y < 665:
        pos_player_y += 1
        if not triggered:
            pos_missil_y += 1
    if tecla[pygame.K_SPACE]:
        triggered = True
        vel_missil_x = 0.8

    if pos_alien_x <= -20:
        pontos -= 5
        pos_alien_x, pos_alien_y = respawn()
    if pos_missil_x >= 1300:
        respawn_missil()
    
    if pos_alien_x == 50:
        pos_alien_x, pos_alien_y = respawn()

    x -= 0.5
    pos_alien_x -= 0.8
    pos_missil_x += vel_missil_x

    player_rect.x, player_rect.y = pos_player_x, pos_player_y
    alien_rect.x, alien_rect.y = pos_alien_x, pos_alien_y
    missil_rect.x, missil_rect.y = pos_missil_x, pos_missil_y

    pontos, _ = colisions(pontos)
    if pontos < 0:
        rodando = False

    score = font.render(f'Pontos: {int(pontos)}', True, (255, 255, 255))
    screen.blit(score, (50, 50))

    screen.blit(alien, (pos_alien_x, pos_alien_y))
    screen.blit(missil, (pos_missil_x, pos_missil_y))
    screen.blit(playerImg, (pos_player_x, pos_player_y))

    pygame.display.update()