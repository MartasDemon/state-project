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
            "Hospodarstvo": 5555,
            "Obranhy": 5555,
            "Financi":  5555,
            "Kultury": 5555,
            "Zdravotnictvo": 0,
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
    def __init__(self, x, y, width, height, text, color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, (255, 255, 255))  
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10)) 

    def check_click(self, pos):
        return self.rect.collidepoint(pos)


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
    "dalsi_mesiac": Button(950, 650, 200, 50, "Ďalší mesiac")  # New button
}

input_active = None
input_text = ""
running = True

while running:
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
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
                except ValueError:
                    Slovensko.output_text = "Zadajte platné číslo!"
                input_active = None
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    rect = img.get_rect()
    rect.center = 400, 150
    screen.blit(img, rect)
    
    for button in buttons.values():
        button.draw(screen, font)
    
    text_surface = font.render(Slovensko.output_text, True, (0, 0, 0))
    screen.blit(text_surface, (50, 500))
    
    if input_active:
        pygame.draw.rect(screen, (200, 200, 200), (300, 250, 200, 40))
        input_text_surface = font.render(input_text, True, (0, 0, 0))
        screen.blit(input_text_surface, (310, 260))
        prompt_surface = font.render("Zadajte hodnotu:", True, (0, 0, 0))
        screen.blit(prompt_surface, (300, 220))

    date_text = font.render(f'Dátum: {Slovensko.day}.{Slovensko.month}.{Slovensko.year}', True, (0, 0, 0))
    screen.blit(date_text, (950, 20))
    
    pygame.display.flip()

pygame.quit()
