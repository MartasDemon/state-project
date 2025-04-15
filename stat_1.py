import pygame

class Stat:
    def __init__(self, rozpocet, vydaje, dlh, dan, inflacia):
        self.rozpocet = rozpocet
        self.vydaje = vydaje
        self.dlh = dlh
        self.dan = dan 
        self.inflacia = inflacia
        self.output_text = ""

        self.day = 1
        self.month = 10   
        self.year = 2023

        self.populacia = 5000000
        self.birthrate = 43000
        self.deathrate = 42000
    
        self.Ministerstva = {
            "MCRaS": 10000000,
            "Dopravy": 100000000,
            "Financii": 18000000,
            "Hospodarstva": 23000000,
            "MIRRI": 5200000,
            "Kultury": 27000000,
            "Obrany": 120000000,
            "MPRV": 12500000,
            "MPSVR": 630000000,
            "Spravodlivosti": 23000000,
            "MŠVVaM": 270000000,
            "Vnútra": 122000000,
            "Zachranicnych veci": 13200000,
            "Zdravotnictva": 412000000,
            "MZP": 17000000
        }

    def stav(self):
        self.output_text = (f'Narodny dlh: {self.dlh}€, Rozpočet: {self.rozpocet}€, '
                            f'Vydaje: {self.vydaje}, Daň: {self.dan * 100}%, '
                            f'Obyvatelia: {self.populacia}, Inflácia: {self.inflacia}%')

    def znizit_dane(self, percento):
        self.dan -= percento / 100
        self.output_text = f'Nová daň je {self.dan * 100}%'

    def zvysit_dane(self, percento):
        self.dan += percento / 100
        self.output_text = f'Nová daň je {self.dan * 100}%'

    def splatit_dlh(self, suma):
        if suma > self.rozpocet:
            self.output_text = 'Nemáme dosť peňazí'
        else:
            self.rozpocet -= suma
            self.dlh -= suma
            self.output_text = f'Splatili ste {suma}€, zostávajúci dlh: {self.dlh}€'
            if self.dlh == 0:
                self.output_text += '\nDlhy sú splatené!'
    def zmena_populacie(self):
        a = (self.birthrate - self.deathrate)
        self.populacia = self.populacia + a

    def dalsi_mesiac(self):
        self.zmena_populacie()
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1

class Button:
    def __init__(self, x, y, width, height, text, color=(10, 10, 80)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=10)
        text_surface = font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def check_click(self, pos):
        return self.rect.collidepoint(pos)

class Radio:
    def __init__(self):
        self.playlist = ['Písnička 1', 'Písnička 2',]
    
    def pridaj_pesnicku(self, pesnicka):
        self.pesnicka = pesnicka
        self.playlist.append()

pygame.init()
screen = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Economic Simulator")
font = pygame.font.Font(None, 30)

Slovensko = Stat(1000, 300, 200, 0.20, 2.8)
img = pygame.image.load('images/slovensko.png')
img = pygame.transform.scale(img, (400, 350))

buttons = {
    "stav": Button(50, 375, 200, 50, "Skontrolovať stav"),
    "znizit_dan": Button(50, 300, 200, 50, "Znížiť daň"),
    "zvysit_dan": Button(50, 225, 200, 50, "Zvýšiť daň"),
    "splatit_dlh": Button(50, 150, 200, 50, "Splatit dlh"),
    "dalsi_mesiac": Button(950, 650, 200, 50, "Ďalší mesiac"),
    "ministerstva": Button(50, 650, 200, 50, "Ministerstvá"),
    "radio": Button(300, 650, 200, 50, "Radio")
}

input_active = None
input_text = ""
current_ministerstvo = None
show_radio = False
show_ministerstva = False
running = True

while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if show_ministerstva:
                if 950 <= pos[0] <= 1150 and 650 <= pos[1] <= 700:
                    show_ministerstva = False
                else:
                    for i, (nazov, hodnota) in enumerate(Slovensko.Ministerstva.items()):
                        y = 50 + i * 40
                        rect = pygame.Rect(50, y, 500, 35)
                        if rect.collidepoint(pos):
                            current_ministerstvo = nazov
                            input_active = "ministerstvo"
                            input_text = ""
            elif show_radio:
                if 950 <= pos[0] <= 1150 and 650 <= pos[1] <= 700:
                    show_radio = False
                else:
                    pass
                    


            else:
                if buttons["stav"].check_click(pos):
                    Slovensko.stav()
                if buttons["znizit_dan"].check_click(pos):
                    input_active = "znizit_dan"
                    input_text = ""
                if buttons["zvysit_dan"].check_click(pos):
                    input_active = "zvysit_dan"
                    input_text = ""
                if buttons["splatit_dlh"].check_click(pos):
                    input_active = "splatit_dlh"
                    input_text = ""
                if buttons["dalsi_mesiac"].check_click(pos):  
                    Slovensko.dalsi_mesiac()
                if buttons["ministerstva"].check_click(pos):
                    show_ministerstva = True
                if buttons["radio"].check_click(pos):
                    show_radio = True

        if event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_RETURN:
                try:
                    value = int(input_text)
                    if input_active == "znizit_dan":
                        Slovensko.znizit_dane(value)
                    elif input_active == "zvysit_dan":
                        Slovensko.zvysit_dane(value)
                    elif input_active == "splatit_dlh":
                        Slovensko.splatit_dlh(value)
                    elif input_active == "ministerstvo" and current_ministerstvo:
                        Slovensko.Ministerstva[current_ministerstvo] = value
                        Slovensko.output_text = f"Nové výdavky pre {current_ministerstvo}: {value}€"
                except ValueError:
                    Slovensko.output_text = "Zadajte platné číslo!"
                input_active = None
                current_ministerstvo = None
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    if show_ministerstva:
        screen.fill((255, 255, 255))
        for i, (nazov, hodnota) in enumerate(Slovensko.Ministerstva.items()):
            y = 50 + i * 40
            rect = pygame.Rect(50, y, 500, 35)
            pygame.draw.rect(screen, (200, 200, 255), rect, border_radius=5)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=5)
            text = font.render(f"{nazov}: {hodnota} €", True, (0, 0, 0))
            screen.blit(text, (60, y + 7))
        Button(950, 650, 200, 50, "Späť").draw(screen, font)

    elif show_radio:
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=5)
        Button(950, 650, 200, 50, "Späť").draw(screen, font)

    else:
        rect = img.get_rect()
        rect.center = 400, 150
        screen.blit(img, rect)

        for key in ["stav", "znizit_dan", "zvysit_dan", "splatit_dlh", "dalsi_mesiac", "ministerstva","radio"]:
            buttons[key].draw(screen, font)

        text_surface = font.render(Slovensko.output_text, True, (0, 0, 0))
        screen.blit(text_surface, (50, 500))

        date_text = font.render(f'Dátum: {Slovensko.day}.{Slovensko.month}.{Slovensko.year}', True, (0, 0, 0))
        screen.blit(date_text, (950, 20))

    if input_active:
        pygame.draw.rect(screen, (200, 200, 200), (300, 250, 200, 40))
        input_text_surface = font.render(input_text, True, (0, 0, 0))
        screen.blit(input_text_surface, (310, 260))
        prompt_surface = font.render("Zadajte hodnotu:", True, (0, 0, 0))
        screen.blit(prompt_surface, (300, 220))

    pygame.display.flip()

pygame.quit()
