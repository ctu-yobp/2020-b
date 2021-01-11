#instalace modulu pygame: https://www.pygame.org/wiki/GettingStarted
import sys
import pygame #https://www.pygame.org/docs/tut/PygameIntro.html
import random
import time

pygame.display.set_caption("Hra života")

OBRAZOVKA = SIRKA, VYSKA = 640, 480 #rozliseni
MRTVA_BUNKA = 0, 0, 0 #RGB 8bit cerna obrazovka
ZIVA_BUNKA = 255, 0, 255 #magenta
VELIKOST_BUNKY = 10

# print(temp)
class Hra: #tvorba tridy

    def __init__(self): #metodu zavola python vzdycky, kdyz vytvori novy objekt
        pygame.init() #inicializuje vsechny pygame moduly
        self.screen = pygame.display.set_mode(OBRAZOVKA) #tvorba grafickeho okna, cokoliv do nej nakreslime se zobrazi na obrazovce
        self.vycisti_obrazovku()
        pygame.display.flip()
        self.init_mrizka() #inicializuje mrizku

    def init_mrizka(self):
        self.pocet_sloupcu = int(SIRKA/VELIKOST_BUNKY)
        self.pocet_radku = int(VYSKA/VELIKOST_BUNKY)

        self.mrizky = []

        radky = []
        for cislo_radku in range(self.pocet_radku):
            temp = []
            for cislo_sloupce in range(self.pocet_sloupcu):
                temp.append(0)
            radky.append(temp)

        self.mrizky.append(radky)

        self.aktivni_mrizka = 0;

        self.nastav_mrizku()
        print(self.mrizky[0])

        self.mrizka_neaktivni = [] #vyvtvori prazdnou mrizku

    def nastav_mrizku(self, hodnota = None): #vytvoreni nahodne binarni mrizky #nastav_mrizku(0)  - jenom nuly (1) - jenom 1, (nahodne)
        # nastavi hodnotu bunek nebo
        # nahodne nastavi hodnotu 0 (vsechny bunky mrtve) nebo 1 (vsechny zive)
        for r in range(self.pocet_radku):
            for s in range(self.pocet_sloupcu):
                if hodnota is None:                 #pokud je hodnota fce None, vlozi se 0 nebo 1
                    hodnota_bunky = random.choice([0, 1])
                else:                               #jinak hodnota bunky
                    hodnota_bunky = hodnota
                self.mrizky[self.aktivni_mrizka][r][s] = hodnota_bunky #do mrizky hodnoty 0 nebo 1 nahodne

    def kresli_mrizku(self):
        self.vycisti_obrazovku()
        #circle_rect = pygame.draw.circle(self.screen, ZIVA_BUNKA, (100, 50), 5, 0)  # kresli kruznici (misto kam kreslit, barva, pozice(stred kruz),
        # polomer, sirka linie) kdyz se da width=0, kresli i vypln
        for s in range(self.pocet_sloupcu):
            for r in range(self.pocet_radku):
                if self.mrizky[self.aktivni_mrizka][r][s] == 1:         #definuje, jestli se bude bunka vykreslovat barvou mrtve nebo zive bunky
                    barva = ZIVA_BUNKA
                else:
                    barva = MRTVA_BUNKA
                # kresli kruh pro kazdou bunku, kterou mame
                pygame.draw.circle(self.screen, barva, (int(s*VELIKOST_BUNKY + (VELIKOST_BUNKY/2)), #souradnice stredu kruhu
                                                        int(r*VELIKOST_BUNKY + (VELIKOST_BUNKY/2))), int(VELIKOST_BUNKY/2), 0)
        pygame.display.flip()  # aktualizuje obsah obrazovky - vsechno co jsme nakreslili na obrazovku se vizualizuje


    def vycisti_obrazovku(self):
        self.screen.fill(MRTVA_BUNKA) #vycisti obrazovku (resp. vyplni obrazovku barvou prazdne bunky)

    def oprav_generaci(self):
            # zjisti, jaka je soucasna generace
            # aktivuje neaktivni herni mrizku, aby mohl ulozit novou generaci
            # vymeni aktivni mrizku
            self.nastav_mrizku(None)
            pass

    def zpracuj_akce(self):
        for event in pygame.event.get():
            # po zmacknuti klavesy "s" bude hra pozastavena
            # po zmacknuti klavesy "r" bude mrizka nahodne prestavena
            # po zmacknuti klavesy "q" bude hra ukoncena
            if event.type == pygame.QUIT: sys.exit()  # modul pygame ma ruzny promenny pro ruzny typy (atribut)
                    # kontrolujeme, jestli ma objekt event atribut quit, pokud ano, zavolam sys.exit()
                    # ktery program vypne
                    # pygame.quit() - opak pygame.init() -> jakoby deaktivuje pygame
                    #self.screen.fill(MRTVA_BUNKA)
                    #screen.blit(ball, ballrect) #=block transfer vykresli obraz do pameti, ktera ale jeste neni zobrazena

    def spust(self): #hlavni cast kodu - spousti

        while True: # donekonacne opakuje tyhle tri funkce
            self.zpracuj_akce() #zpracovava vstup z klavesnice
            self.oprav_generaci() #zpracovava generaci
            self.kresli_mrizku()
            time.sleep(1)

hra = Hra() #tvorba objektu
hra.spust()

