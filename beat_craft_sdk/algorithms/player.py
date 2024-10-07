import pygame

pygame.mixer.init()
pygame.mixer.music.load('../../.output/output.mid')
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pass
