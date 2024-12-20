import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))  # Postavljanje prozora
    pygame.display.set_caption("Kontrola drona")

def getKey(keyName):
    ans = False
    for event in pygame.event.get(): pass  # Osiguraj da događaji budu obrađeni
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, f'K_{keyName}')
    if keyInput[myKey]:
        ans = True
    return ans
