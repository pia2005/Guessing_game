import pygame as pg
from pygame.locals import (QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT)
import random as rd

pg.init()

VINDU_BREDDE = 800
VINDU_HOYDE = 500
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])
pg.display.set_caption('Trollspill')
display_surface = pg.display.set_mode((VINDU_BREDDE, VINDU_HOYDE))

font = pg.font.Font('freesansbold.ttf', 40)
text = font.render('Game over', True, (250, 0, 0), (0, 0, 255))
textRect = text.get_rect()
textRect.center = (VINDU_BREDDE // 2, VINDU_HOYDE // 2)



class Boks:
    def __init__(self, x, y, side, farge, vindusobjekt):
        self.x = x
        self.y = y
        self.side = side
        self.farge = farge
        self.vindusobjekt = vindusobjekt

    def tegn(self):
        rektangel = pg.Rect(self.x, self.y, self.side, self.side)
        pg.draw.rect(self.vindusobjekt, self.farge, rektangel)


class Spiller(Boks):
    def __init__(self, x, y, side, farge, vindusobjekt):
        super().__init__(x, y, side, farge, vindusobjekt)
        self.poeng = 0
        self.fart = 0.01
        self.spillOver = False
        self.retning = "høyre"

    # Fjern metoden kolliderer herfra
    # def kolliderer(self, annenBoks):
    #     kollidere = pg.Rect(self.x, self.y, self.bredde, self.hoyde).colliderect(
    #         pg.Rect(annenBoks.x, annenBoks.y, annenBoks.bredde, annenBoks.hoyde)
    #     )
    #     return kollidere

    def flytt(self, taster):
        if not self.spillOver:

            if self.retning == "venstre":
                self.x = self.x - self.fart
            elif self.retning == "opp":
                self.y = self.y - self.fart
            elif self.retning == "høyre":
                self.x = self.x + self.fart
            elif self.retning == "ned":
                self.y = self.y + self.fart

            '''
            if taster[K_UP]:
                self.y -= self.fart
            if taster[K_DOWN] :
                self.y += self.fart
            if taster[K_LEFT]:
                self.x -= self.fart
            if taster[K_RIGHT]:
                self.x += self.fart
            '''
            if self.x < 0 or self.x > VINDU_BREDDE or self.y < 0 or self.y > VINDU_HOYDE:
                self.spillOver = True

    def kolliderer(self, annenBoks):
        if abs(self.x - annenBoks.x) < self.side and abs(self.y - annenBoks.y) < self.side:
            return True
        else:
            return False

    def kollisjon(self, annenBoks):
        if annenBoks.farge == gul:
            self.poeng += 1

            annenBoks.farge = grå
            self.fart += 0.01
            # snu retning jett herfra
            '''if taster[K_UP]:
                taster[K_DOWN]
            if taster[K_LEFT]:
                taster[K_RIGHT]
            if taster[K_DOWN]:
                taster[K_UP]
            if taster[K_RIGHT]:
                taster[K_LEFT]'''
            if self.retning == "opp":
                self.retning = "ned"
            elif self.retning == "venstre":
                self.retning = "høyre"
            elif self.retning == "ned":
                self.retning = "opp"
            elif self.retning == "høyre":
                self.retning = "venstre"
            nysted = ledigsted(side, objekter)
            lagmat = Boks(nysted[0], nysted[1], side, (255, 192, 202), vindu)
            objekter.append(lagmat)

            lagmat.tegn()

        elif annenBoks.farge == (100, 100, 100):
            self.spillOver = True


def ledigsted(side, objekter):
    x = rd.randint(side, VINDU_BREDDE - side)
    y = rd.randint(side, VINDU_HOYDE - side)

    opptatt = True
    for i in objekter:
        opptatt = False
        if (abs(x - i.x) < side and abs(y - i.y) < side):
            opptatt = True
        if opptatt:
            x = rd.randint(side, VINDU_BREDDE - side)
            y = rd.randint(side, VINDU_HOYDE - side)
        else:
            return x, y


objekter = []
gul = (255, 192, 202)
grå = (100, 100, 100)
side = 50

spiller = Spiller(int(VINDU_BREDDE / 2 - side / 2), int(VINDU_HOYDE / 2 - side / 2), side, (0, 250, 0), vindu)
objekter.append(spiller)
spiller.tegn()

# Plasserer tre mat-objekter tilfeldige steder på skjermen
for i in range(3):
    pos = ledigsted(side, objekter)  # tuppel med tilfeldig ledig posisjon
    mat = Spiller(pos[0], pos[1], side, (255, 192, 202), vindu)
    mat.tegn()
    objekter.append(mat)

fortsett = True
while fortsett:
    for event in pg.event.get():
        if event.type == QUIT:
            fortsett = False

    taster = pg.key.get_pressed()
    if taster[K_UP]:
        spiller.retning = "opp"
    elif taster[K_DOWN]:
        spiller.retning = "ned"
    elif taster[K_LEFT]:
        spiller.retning = "venstre"
    elif taster[K_RIGHT]:
        spiller.retning = "høyre"

    text2 = font.render(f'Poeng: {spiller.poeng}', True, (30, 60, 90))

    vindu.fill((0, 0, 0))

    if not spiller.spillOver:
        spiller.flytt(taster)
        vindu.blit(text2, (20, 20))
    else:
        display_surface.blit(text, textRect)
        vindu.blit(text2, (20, 20))
    for i in objekter:
        i.tegn()
    for i in range(len(objekter)):
        if spiller.kolliderer(objekter[i]):
            spiller.kollisjon(objekter[i])
    if spiller.spillOver:
        vindu.blit(text, textRect)  # Draw text above everything when the game is over
        vindu.blit(mittBilde, (VINDU_BREDDE // 2, VINDU_HOYDE // 2))
    pg.display.flip()

pg.quit()
