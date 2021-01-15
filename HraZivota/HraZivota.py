#instalace modulu pygame: https://www.pygame.org/wiki/GettingStarted
import sys
import pygame #https://www.pygame.org/docs/tut/PygameIntro.html
import random

pygame.display.set_caption("Hra života")
OBRAZOVKA = SIRKA, VYSKA = 640, 480  # rozliseni
MRTVA_BUNKA = 0, 0, 0  # RGB 8bit cerna obrazovka
ZIVA_BUNKA = 255, 0, 255  # magenta
VELIKOST_BUNKY = 5
MAX_FPS = 8  # snimek za sekundu
cislo_gen = 1


# print(temp)
class Hra: #tvorba tridy

    def __init__(self): #metodu zavola python vzdycky, kdyz vytvori novy objekt

        pygame.init() #inicializuje vsechny pygame moduly
        self.screen = pygame.display.set_mode(OBRAZOVKA) #tvorba grafickeho okna, cokoliv do nej nakreslime se zobrazi na obrazovce
        self.vycisti_obrazovku()
        pygame.display.flip()

        self.posledni_update = 0
        self.pozad_ms_updatu = (1.0/MAX_FPS) * 1000.0 #pozadovany FPS = snimkova frekvence [ms]

        self.aktivni_mrizka = 0
        self.pocet_sloupcu = int(SIRKA/VELIKOST_BUNKY)
        self.pocet_radku = int(VYSKA/VELIKOST_BUNKY)
        self.mrizky = []
        self.init_mrizka() #inicializuje mrizku
        self.nastav_mrizku()
        self.paused = False
        self.konec_hry = False

    def init_mrizka(self):

        def vytvor_mrizku(): #dvourozmerne pole
            radky = []
            for cislo_radku in range(self.pocet_radku):
                temp = []
                for cislo_sloupce in range(self.pocet_sloupcu):
                    temp.append(0)
                radky.append(temp)
            return radky

        self.mrizky.append(vytvor_mrizku()) #aktivni #trojrozmernep pole
        self.mrizky.append(vytvor_mrizku()) #neaktivni

    def nastav_mrizku(self, hodnota = None, mrizka = 0): #vytvoreni nahodne binarni mrizky #nastav_mrizku(0)  - jenom nuly (1) - jenom 1, (nahodne)
        # nastavi hodnotu bunek nebo
        # nahodne nastavi hodnotu 0 (vsechny bunky mrtve) nebo 1 (vsechny zive)
        for r in range(self.pocet_radku):
            for s in range(self.pocet_sloupcu):
                if hodnota is None:                 #pokud je hodnota fce None, vlozi se 0 nebo 1
                    hodnota_bunky = random.choice([0, 1])
                else:                               #jinak hodnota bunky
                    hodnota_bunky = hodnota
                self.mrizky[mrizka][r][s] = hodnota_bunky #do mrizky hodnoty 0 nebo 1 nahodne
        # print("poc.hodnota")
        # print(self.mrizky)

    def kresli_mrizku(self):
        self.vycisti_obrazovku()
        #pygame.draw.circle(self.screen, ZIVA_BUNKA, (100, 50), 5, 0)  # kresli kruznici (misto kam kreslit, barva, pozice(stred kruz),
        # polomer, sirka linie) kdyz se da width=0, kresli i vypln
        for s in range(self.pocet_sloupcu):
            for r in range(self.pocet_radku):
                if self.mrizky[self.aktivni_mrizka][r][s] == 1:         #definuje, jestli se bude bunka vykreslovat barvou mrtve nebo zive bunky
                    barva = ZIVA_BUNKA
                else:
                    barva = MRTVA_BUNKA
                # kresli kruh pro kazdou bunku, kterou mame
                #pygame.draw.circle(self.screen, barva, (int(s*VELIKOST_BUNKY + (VELIKOST_BUNKY/2)), #souradnice stredu kruhu
                                                       # int(r*VELIKOST_BUNKY + (VELIKOST_BUNKY/2))), int(VELIKOST_BUNKY/2), 0)
                pygame.draw.rect(self.screen, barva, (s*VELIKOST_BUNKY, r*VELIKOST_BUNKY, VELIKOST_BUNKY, VELIKOST_BUNKY), 0)

        pygame.display.flip()  # aktualizuje obsah obrazovky - vsechno co jsme nakreslili na obrazovku se vizualizuje

    def vycisti_obrazovku(self):
        self.screen.fill(MRTVA_BUNKA) #vycisti obrazovku (resp. vyplni obrazovku barvou prazdne bunky)

    def vrat_bunku(self, r, s):
        try:
             hodnota_bunky = self.mrizky[self.aktivni_mrizka][r][s]
        except:
            # print("Chyba v ziskani hodnoty bunky r{}, s{}".format(r,s))
            hodnota_bunky = 0 #pokud nelze ziskat hodnotu bunky(je mimo mrizku), reknu, ze je mrtva
        return hodnota_bunky

    def checkni_sousedni_bunky(self, radek_index, sloupec_index):
        #pravidla Hry Zivota
        # pocet zivych budek v okoli
        #zcekni vsechny sousedy a pridej hodnotu
        pocet_zivych_sousedu = 0

        # for r in range(radek_index-1,radek_index+1):
        #     for s in range(sloupec_index-1,sloupec_index+1):
        #         #print(r,s)
        #         if r == 0 and s == 0:
        #             pocet_zivych_sousedu += 0
        #         else:
        #             pocet_zivych_sousedu += self.vrat_bunku(r, s)
        pocet_zivych_sousedu += self.vrat_bunku(radek_index - 1, sloupec_index - 1)
        pocet_zivych_sousedu += self.vrat_bunku(radek_index -1, sloupec_index) #levy horni roh
        pocet_zivych_sousedu += self.vrat_bunku(radek_index - 1,sloupec_index + 1)

        pocet_zivych_sousedu += self.vrat_bunku(radek_index, sloupec_index - 1)
        pocet_zivych_sousedu += self.vrat_bunku(radek_index, sloupec_index + 1)
        
        pocet_zivych_sousedu += self.vrat_bunku(radek_index + 1,sloupec_index - 1)
        pocet_zivych_sousedu += self.vrat_bunku(radek_index + 1,sloupec_index)
        pocet_zivych_sousedu += self.vrat_bunku(radek_index + 1,sloupec_index + 1)
        print(pocet_zivych_sousedu)


        if self.mrizky[self.aktivni_mrizka][radek_index][sloupec_index] == 1:  # ziva bunka
            if pocet_zivych_sousedu > 3:  # Každá živá buňka s více než třemi živými sousedy zemře.
                return 0
            if pocet_zivych_sousedu < 2:  # Každá živá buňka s méně než dvěma živými sousedy zemře
                return 0
            if pocet_zivych_sousedu == 2 or pocet_zivych_sousedu == 3:
                return 1  # Každá živá buňka se dvěma nebo třemi živými sousedy zůstává žít.
        elif self.mrizky[self.aktivni_mrizka][radek_index][sloupec_index] == 0:  # mrtva bunka
            if pocet_zivych_sousedu == 3:
                return 1  # Každá mrtvá buňka s právě třemi živými sousedy oživne
        return self.mrizky[self.aktivni_mrizka][radek_index][sloupec_index]  # vratim tu puvodni hodnotu

    def oprav_generaci(self):
            # zjisti, jaka je soucasna generace, pripravuje dalsi generaci
            # aktivuje neaktivni herni mrizku, aby mohl ulozit novou generaci
            # vymeni aktivni mrizku
            self.nastav_mrizku(0, self.neaktivni_mrizka()) #nastavani na pocatku celou neaktivni mrizku na 0
            for s in range(self.pocet_sloupcu):
                for r in range(self.pocet_radku):
                    stav_budouci_generace = self.checkni_sousedni_bunky(r,s) #kazde bunce vypocteme jeji budouci stav na zaklade okoli
                    self.mrizky[self.neaktivni_mrizka()][r][s] = stav_budouci_generace #stav budouci generace ulozim do aktualni pozice neaktivni mrizky
            self.aktivni_mrizka = self.neaktivni_mrizka() #nastavi neaktivni mrizce jeji budouci stav

            # global cislo_gen
            # cislo_gen += 1
            # print("generace: {}".format(cislo_gen))
            # print(self.mrizky)

    def neaktivni_mrizka(self):
        return (self.aktivni_mrizka + 1) % 2 #prohodi aktivni bunky na neaktivni a naopak #zjisti stav nekativni mrizky

    def zpracuj_akce(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode == 's':
                    print("Pozastaveni hry")
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
                if event.unicode == 'r':
                    print("Nahodne prestaveni mrizky")
                    self.aktivni_mrizka = 0
                    self.nastav_mrizku(None, self.aktivni_mrizka)
                    self.nastav_mrizku(0, self.neaktivni_mrizka())
                    self.kresli_mrizku()
                if event.unicode == 'q':
                    print("Ukonceni hry")
                    self.konec_hry = True
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
            if self.konec_hry:
                return
            self.zpracuj_akce() #zpracovava vstup z klavesnice
            if self.paused:
               continue
            self.oprav_generaci() #zpracovava generaci
            self.kresli_mrizku()
            self.fps()

    def fps(self): #pokud je cas od posledniho vykresleni obrazu mensi nez 1/fps, spi po zbytek casu
        cas = pygame.time.get_ticks() #ziskame cas v ms od pygame.init()
        # print("cas")
        # print(cas)
        # print(self.posledni_update)
        cas_od_posl_update = cas - self.posledni_update #u prvniho = casu od pygame.init()
        # print(cas_od_posl_update)
        # print(self.pozad_ms_updatu)
        pozastaveni = self.pozad_ms_updatu - cas_od_posl_update #spi po zbytek casu
        # print(pozastaveni)
        if pozastaveni > 0:
            pygame.time.delay(int(pozastaveni)) #pauzne program
        self.posledni_update = cas
        # print(self.posledni_update)

hra = Hra() #tvorba objektu
hra.spust()

