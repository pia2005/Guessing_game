# Kaller opp bibliotek
import pygame as pg
from pygame.locals import (QUIT, K_UP, K_DOWN)
from pygame.locals import (QUIT, K_w, K_s)
import random as rd

pg.init()

# Bredde og Høyde av vinduet
VINDU_BREDDE = 800
VINDU_HOYDE = 600
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])
pg.display.set_caption('Pong Game')
display_surface = pg.display.set_mode((VINDU_BREDDE, VINDU_HOYDE))

gameover = False

class Kvadrat:
    """Klasse for å representere en Kvadrat"""

    def __init__(self, x, y, bredde, hoyde, farge, vindusobjekt):
        """Konstruktør"""
        self.x = x
        self.y = y
        self.bredde = bredde
        self.hoyde = hoyde
        self.farge = farge
        self.vindusobjekt = vindusobjekt

    def tegn(self):
        # Tegner en rektangel
        pg.draw.rect(self.vindusobjekt, self.farge, (self.x, self.y, self.bredde, self.hoyde))


class Spiller(Kvadrat):
    """Klasse for å representere spillerne"""
    def __init__(self, x, y, bredde, hoyde, farge, vindusobjekt, fart):
        super().__init__(x, y, bredde, hoyde, farge, vindusobjekt)
        self.fart = fart

    def flytt(self, K_w, K_s):
        if not gameover:
            """Metode for å flytte spillerne"""
            taster = pg.key.get_pressed()
            if taster[K_w] and (self.y - self.bredde) >= 0:
                self.y -= self.fart
            if taster[K_s] and (self.y + self.hoyde) < self.vindusobjekt.get_height():
                self.y += self.fart


class Ball:
    """Klasse for å representere en ball"""
    def __init__(self, x, y, radius, farge, vindusobjekt):
        """Konstruktør"""
        self.x = x
        self.y = y
        self.radius = radius
        self.farge = farge
        self.vindusobjekt = vindusobjekt
        self.xFart = rd.choice([-1, 1]) * rd.uniform(5, 7)
        self.yFart = rd.choice([-1, 1]) * rd.uniform(5, 7)
        self.nullstill()

    def tegn(self):
        """Metode for å tegne ballen"""
        pg.draw.circle(self.vindusobjekt, self.farge, (self.x + self.radius, self.y + self.radius), self.radius)

    def flytt(self):
        if not gameover:
            if self.y <= 0 or self.y >= VINDU_HOYDE-self.radius:
                self.yFart = -self.yFart
            if self.x <= 0:
                self.nullstill()
                return 2
            if self.x >= VINDU_BREDDE:
                self.nullstill()
                return 1

                # Flytter hinderet
            self.x += self.xFart
            self.y += self.yFart

    def nullstill(self):
        """ Nullstriller ballen så den ender opp på samme sted"""
        self.x = VINDU_BREDDE // 2 - self.radius // 2
        self.y = VINDU_HOYDE // 2 - self.radius // 2
        self.xFart = rd.choice([-1, 1]) * rd.uniform(5, 7)
        self.yFart = rd.choice([-1, 1]) * rd.uniform(5, 7)

    def kollisjon(self, spiller):
        """Metode for å finne avstanden mellom ball og spiller"""
        if (self.x < spiller.x + spiller.bredde and self.x + self.radius > spiller.x and
                self.y < spiller.y + spiller.hoyde and self.y + self.radius > spiller.y):
            self.xFart *= -1

            # Øker farten når ballen koliderer med spiller pedalen
            if abs(self.xFart) < 10:
                self.xFart += 0.2 if self.xFart > 0 else - 0.2
            if abs(self.yFart) < 10:
                self.yFart += 0.2 if self.yFart > 0 else - 0.2


# Lager begge spillerne og ballen
spiller1 = Spiller(50, VINDU_HOYDE // 2 - 100 // 1, 10, 100, (255, 255, 255), vindu, 10)
spiller2 = Spiller(VINDU_BREDDE - 50 - 10, VINDU_HOYDE//2 - 100//2, 10, 100, (255, 255, 255), vindu, 10)
ball = Ball(VINDU_BREDDE // 2 - 10 // 2, VINDU_HOYDE // 2 - 10//2, 10, (255, 255, 255), vindu)


# Game loop
clock = pg.time.Clock()
font = pg.font.Font(None, 36)
# Spillernes poeng
Sp1_poeng = 0
Sp2_poeng = 0

# Gjenta helt til brukeren lukker vinduet
fortsett = True
while fortsett:

    # Sjekker om brukeren har lukket vinduet
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False

    # Henter en ordbok med status for alle tastatur-taster
    trykkede_taster = pg.key.get_pressed()

    # Flytter spiller
    spiller1.flytt(K_w, K_s)
    spiller2.flytt(K_UP, K_DOWN)

    # Teller poeng når ballen treffer veggen
    poeng = ball.flytt()
    if poeng == 1:
        Sp1_poeng += 1
    elif poeng == 2:
        Sp2_poeng += 1
    ball.kollisjon(spiller1)
    ball.kollisjon(spiller2)

    # Farger bakgrunnen svart
    vindu.fill((0, 0, 0))

    # Tegner Spillere og ball
    spiller1.tegn()
    spiller2.tegn()
    ball.tegn()

    # Tegner linja i mindten
    pg.draw.aaline(vindu, (255, 255, 255), (VINDU_BREDDE // 2, 0), (VINDU_BREDDE // 2, VINDU_HOYDE))

    # Viser spillerens poeng
    poengstilling = font.render(f' Spiller1: {Sp1_poeng}  Spiller2: {Sp2_poeng}', True, (255, 255, 255))
    vindu.blit(poengstilling, (VINDU_BREDDE / 3, 0))

    # if-Løkke for å avslutte spillet når en spiller har nådd en poengsum
    if Sp1_poeng == 8 or Sp2_poeng == 8:
        gameover = True

        # Wiser endelige poengsum til spillerne
        vindu.fill((0, 0, 0))
        poengstilling = font.render(f' Spiller1: {Sp1_poeng}   Spiller2: {Sp2_poeng}', True, (255, 255, 255))
        vindu.blit(poengstilling, (VINDU_BREDDE / 3, 0))

        # Lager en tekst som viser at spillet er over
        Gameover = font.render("Spillet er over!", True, (255, 255, 255))
        vindu.blit(Gameover, (VINDU_BREDDE / 3 + 30, VINDU_HOYDE // 2))

    # Oppdaterer the display
    pg.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pg.quit()
