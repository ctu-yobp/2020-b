import sys
import pygame
import random

class Hra:

    def __init__(self, SIRKA_OBRAZOVKY = 800, VYSKA_OBRAZOVKY = 600, VELIKOST_BUNKY = 5, ZIVA_BUNKA = (255,0,255), MRTVA_BUNKA = (0,0,0), MAX_FPS = 8):
        """
        Nastav pocatecni stav hry.

        :param SIRKA_OBRAZOVKY: sirka herniho okna
        :param VYSKA_OBRAZOVKY: vyska herniho okna
        :param VELIKOST_BUNKY: velikost bunky
        :param ZIVA_BUNKA: barva zive bunky - RGB N-tice napr. (255,0,255) pro purpurovou barvu
        :param MRTVA_BUNKA: barva mrtve bunky - RGB N-tice napr. (0,0,0) pro cernou barvu
        :param MAX_FPS: snimkova frekvence = rychlost hry
        """
        pygame.display.set_caption("HRA ŽIVOTA")
        icon = pygame.image.load('cell-division.png')
        pygame.display.set_icon(icon)

        pygame.init()
        self.SIRKA_OBRAZOVKY = SIRKA_OBRAZOVKY
        self.VYSKA_OBRAZOVKY = VYSKA_OBRAZOVKY
        self.VELIKOST_BUNKY = VELIKOST_BUNKY
        self.ZIVA_BUNKA = ZIVA_BUNKA
        self.MRTVA_BUNKA = MRTVA_BUNKA
        self.MAX_FPS = MAX_FPS

        self.screen = pygame.display.set_mode((self.SIRKA_OBRAZOVKY, self.VYSKA_OBRAZOVKY))
        self.vycisti_obrazovku()
        pygame.display.flip()

        self.posledni_update = 0
        self.pozad_ms_updatu = (1.0/self.MAX_FPS) * 1000.0

        self.aktivni_mrizka = 0
        self.pocet_sloupcu = int(self.SIRKA_OBRAZOVKY/self.VELIKOST_BUNKY)
        self.pocet_radku = int(self.VYSKA_OBRAZOVKY/self.VELIKOST_BUNKY)
        self.mrizky = []
        self.init_mrizka()
        self.nastav_mrizku()
        self.paused = False
        self.konec_hry = False

    def init_mrizka(self):
        """
        Vytvor aktivni a neaktivni mrizku

        :return: aktivni a neaktivni mrizka v seznamu
        """
        def vytvor_mrizku():
            """
            Vyvtor prazdne dvourozmerne pole, resp. naplnene nulami.

            :return: 2D mrizka
            """
            radky = []
            for cislo_radku in range(self.pocet_radku):
                temp = []
                for cislo_sloupce in range(self.pocet_sloupcu):
                    temp.append(0)
                radky.append(temp)
            return radky

        self.mrizky.append(vytvor_mrizku())
        self.mrizky.append(vytvor_mrizku())

    def nastav_mrizku(self, hodnota=None, mrizka=0):
        """
        Nastav globalni stav mrizky bud nahodnymi hodnotami 0/1 nebo zadanou hodnotou pro kazdou bunku.

        Priklad:
            nastav_mrizku(0) -> vsechny bunky mrizky mrtve
            nastav_mrizku(1) -> vsechny bunky mrizky zive
            nastav_mrizku() -> bunky zive/mrtve nahodne

        :param hodnota: 0/1/None = hodnota pro nastaveni stavu bunky
        :param mrizka:  0/1 = aktivni/neaktivni mrizka
        :return: celkovy stav mrizky
        """
        for r in range(self.pocet_radku):
            for s in range(self.pocet_sloupcu):
                if hodnota is None:
                    hodnota_bunky = random.choice([0, 1])
                else:
                    hodnota_bunky = hodnota
                self.mrizky[mrizka][r][s] = hodnota_bunky

    def kresli_mrizku(self):
        """
        Zobraz bunky do herniho okna na zaklade stavu bunky v aktualni generaci.

        :return: aktualizovane herni okno
        """
        self.vycisti_obrazovku()
        for s in range(self.pocet_sloupcu):
            for r in range(self.pocet_radku):
                if self.mrizky[self.aktivni_mrizka][r][s] == 1:
                    barva = self.ZIVA_BUNKA
                else:
                    barva = self.MRTVA_BUNKA
                pygame.draw.rect(self.screen, barva, (s*self.VELIKOST_BUNKY, r*self.VELIKOST_BUNKY, self.VELIKOST_BUNKY, self.VELIKOST_BUNKY), 0)

        pygame.display.flip()

    def vycisti_obrazovku(self):
        """
        Vypln celou obrazovku mrtvymi bunkami.

        :return: ciste herni okno
        """
        self.screen.fill(self.MRTVA_BUNKA)

    def vrat_stav_bunky(self, r, s):
        """
        Vrat stav bunky v aktivni mrizce. Pokud se soused nachazi mimo mrizku, povazuj ho za mrtveho.

        :param r: cislo radku souseda
        :param s: cislo sloupce souseda
        :return: 0/1 na zaklade stavu zkoumane bunky
        """

        if r < 0 or s < 0 or r > self.pocet_radku - 1 or s > self.pocet_sloupcu - 1:
            hodnota_bunky = 0
        else:
            hodnota_bunky = self.mrizky[self.aktivni_mrizka][r][s]

        return hodnota_bunky

    def analyzuj_sousedni_bunky(self, radek_index, sloupec_index):
        """
        Ziskej pocet zivych bunek v okoli zkoumanych bunek. Na zaklade previdel hry zivota urci stav zkoumane bunky v nasledujici generaci.

        Pravidla:
            1. Kazda ziva bunka s mene nez dvema zivymi sousedy zemre.
            2. Kazda ziva bunka se dvema nebo tremi zivymi sousedy zustava zit.
            3. kazda ziva bunka s vice nez tremi zivymi sousedy zemre.
            4. Kazda mrtva bunka s prave tremi zivymi sousedy ozivne.

        :param radek_index: cislo radku zkoumane bunky
        :param sloupec_index: cislo sloupce zkoumane bunky
        :return: stav bunky v budouci generaci (0/1)
        """

        pocet_zivych_sousedu = 0
        pocet_zivych_sousedu += self.vrat_stav_bunky(radek_index - 1, sloupec_index - 1)
        pocet_zivych_sousedu += self.vrat_stav_bunky(radek_index - 1, sloupec_index)
        pocet_zivych_sousedu += self.vrat_stav_bunky(radek_index - 1, sloupec_index + 1)
        pocet_zivych_sousedu += self.vrat_stav_bunky(radek_index, sloupec_index - 1)
        pocet_zivych_sousedu += self.vrat_stav_bunky(radek_index, sloupec_index + 1)
        pocet_zivych_sousedu += self.vrat_stav_bunky(radek_index + 1, sloupec_index - 1)
        pocet_zivych_sousedu += self.vrat_stav_bunky(radek_index + 1, sloupec_index)
        pocet_zivych_sousedu += self.vrat_stav_bunky(radek_index + 1, sloupec_index + 1)

        if self.mrizky[self.aktivni_mrizka][radek_index][sloupec_index] == 1:
            if pocet_zivych_sousedu < 2:
                return 0
            if pocet_zivych_sousedu == 2 or pocet_zivych_sousedu == 3:
                return 1
            if pocet_zivych_sousedu > 3:
                return 0
        elif self.mrizky[self.aktivni_mrizka][radek_index][sloupec_index] == 0:
            if pocet_zivych_sousedu == 3:
                return 1
        return self.mrizky[self.aktivni_mrizka][radek_index][sloupec_index]

    def oprav_generaci(self):
        """
        Vysetri soucasnou generaci a pripravi budouci generaci.

        :return: nova generace bunek
        """
        self.nastav_mrizku(0, self.neaktivni_mrizka())
        for s in range(self.pocet_sloupcu):
            for r in range(self.pocet_radku):
                stav_budouci_generace = self.analyzuj_sousedni_bunky(r, s)
                self.mrizky[self.neaktivni_mrizka()][r][s] = stav_budouci_generace
        self.aktivni_mrizka = self.neaktivni_mrizka()

    def neaktivni_mrizka(self):
        """
        Ziska index neaktivni mrizky. Pokud je aktivni mrizka 0, fce vrati hodnotu 1 a naopak

        :return: 0/1 hodnota reprezentujici neaktivni mrizku
        """
        return (self.aktivni_mrizka + 1) % 2

    def zpracuj_akce(self):
        """
        Zpracovani vstupu z klavesnice.

        Akce:
            s (stop) - pozastav hru
            r (random) - prestav mrizku
            q (quit) - ukonci hru

        :return:
        """
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

            if event.type == pygame.QUIT: sys.exit()

    def spust(self):
        """
        Spoustej hru v nekonecnem cyklu dokud nebude uzivatelem ukoncena.

        :return:
        """
        while True:
            if self.konec_hry:
                return
            self.zpracuj_akce()
            if self.paused:
               continue
            self.oprav_generaci()
            print(self.mrizky)
            self.kresli_mrizku()
            self.fps()

    def fps(self):
        """
        Pokud se obrazovka aktualizuje prilis rychle, pozastav hru do casu prednastavene frekvence.

        :return:
        """
        cas = pygame.time.get_ticks()
        cas_od_posl_update = cas - self.posledni_update
        pozastaveni = self.pozad_ms_updatu - cas_od_posl_update
        if pozastaveni > 0:
            pygame.time.delay(int(pozastaveni))
        self.posledni_update = cas

hra = Hra()
hra.spust()

