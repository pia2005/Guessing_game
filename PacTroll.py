import pygame as pg
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT)
import math as m
import random as rd

# Initialiserer/starter pygame
pg.init()

# Oppretter et vindu der vi skal "tegne" innholdet vårt
VINDU_BREDDE = 500
VINDU_HOYDE = 500
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])

font = pg.font.SysFont("Arial", 24)

gameover = False
class Kvadrat:
    """Klasse for å representere en ball"""

    def __init__(self, x, y, side, farge, vindusobjekt):
        """Konstruktør"""
        self.x = x
        self.y = y
        self.side = side
        self.farge = farge
        self.vindusobjekt = vindusobjekt

    def tegn(self):
        """Metode for å tegne hinderet"""
        # Tegner et rektangel
        pg.draw.rect(self.vindusobjekt, self.farge, (self.x, self.y, self.side, self.side))

    def finnAvstand(self, annenBall):
        """Metode for å finne avstanden til en annen ball"""
        if abs(self.x-annenBall.x)< self.side and abs(self.y-annenBall.y)<self.side:
            return True
        else:
            return False

class Mat(Kvadrat):
    """Klasse for å representere et hinder"""

    def __init__(self, x, y, side, farge, vindusobjekt):
        super().__init__(x, y, side, farge, vindusobjekt)


class Troll(Kvadrat):
    """Klasse for å representere en spiller"""

    def __init__(self, x, y, side, farge, vindusobjekt, fart):
        super().__init__(x, y, side, farge, vindusobjekt)
        self.fart = fart

    def flytt(self, taster):
        if not gameover:
            """Metode for å flytte spilleren"""
            if taster[K_UP] and (self.y - self.hoyde) > 0:
                self.y -= self.fart
            if taster[K_DOWN] and (self.y + self.hoyde) < self.vindusobjekt.get_height():
                self.y += self.fart
            if taster[K_LEFT] and (self.x - self.bredde) > 0:
                self.x -= self.fart
            if taster[K_RIGHT] and (self.x + self.bredde) < self.vindusobjekt.get_width():
                self.x += self.fart


# Lager et Spiller-objekt
spiller = Troll(250, 250,10,(10,255,255), vindu, 0.1)


# Lager et Hinder-objekt
MatHindre = []

for i in range(6):
    bredde = 10
    hoyde = 10
    x = rd.randint(bredde, VINDU_BREDDE-bredde)
    y = rd.randint(hoyde, VINDU_HOYDE-hoyde)
    xFart = rd.uniform(0.05,0.07)
    yFart = rd.uniform(0.05,0.07)
    farge = (253,255,0)

    MatHindre.append(Mat(x, y, bredde, hoyde, farge, vindu))


# Gjenta helt til brukeren lukker vinduet
fortsett = True
while fortsett:

    # Sjekker om brukeren har lukket vinduet
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False

    # Henter en ordbok med status for alle tastatur-taster
    trykkede_taster = pg.key.get_pressed()

    # Farger bakgrunnen lyseblå
    vindu.fill((0, 0, 0))

    # Tegner og flytter spiller og hinder
    spiller.tegn()
    spiller.flytt(trykkede_taster)

    for hinder in MatHindre:
        hinder.tegn()




    tekst = font.render(f'Poengsum: {poengsum}', True, (255, 255, 255))
    vindu.blit(tekst, (0, 0))

    for hinder in MatHindre:
        if spiller.finnAvstand(hinder):
            gaveover = True
            poengsum += 1
            hinder.farge = (123,50,150)
            hinder.tegn()







    # Oppdaterer alt innholdet i vinduet
    pg.display.flip()

# Avslutter pygame
pg.quit()