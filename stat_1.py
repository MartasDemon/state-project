import pygame

class Stat:
    def __init__(self, rozpocet, vydaje, dlh, dan, pop, inflacia):
        self.rozpocet = rozpocet
        self.vydaje = vydaje
        self.dlh = dlh
        self.dan = dan 
        self.pop = pop
        self.inflacia = inflacia
        self.output_text = ""

    def stav(self):
        self.output_text = (f'Narodny dlh: {self.dlh}€, Rozpočet: {self.rozpocet}, '
                            f'Vydaje: {self.vydaje}, Dan: {self.dan * 100}%, '
                            f'Obyvatelia: {self.pop}, Inflacia: {self.inflacia}%')

    def znizit_dane(self, percento):
        self.dan -= percento / 100
        self.output_text = f'Nova dan je {self.dan * 100}%'
    
    
    def zvysit_dane(self):
        percento = int(input("O kolko percent chcete zvyit dane"))
        self.dan = self.dan + (percento / 100)
        print(f'Nasa dan je {self.dan * 100}%')


    def splatit_dlh(self,kolko):
        if kolko > self.rozpocet:
            print('Nemame dost penazi')
        else:
            self.rozpocet = self.rozpocet - kolko
            self.dlh = self.dlh - kolko
            print(f'splatil si {kolko}€, ostava nam Dlh {self.dlh }')
            if self.dlh == 0:
                print('Dlhy sa uz splatili')

    def zvysit_dane(self):
        percento = int(input("O kolko percent chcete zvyit dane"))
        self.dan = self.dan + (percento / 100)
        print(f'Nasa dan je {self.dan * 100}%')

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

Slovensko = Stat(1000, 300, 200, 0.20, 500000, 2.8)
button_stav = Button(50, 375, 200, 50, "Skontrolovat stav")
button_dan = Button(50, 300, 200, 50, "Znižat dan")

input_active = False
input_text = ""
running = True

while running:
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if button_stav.check_click(pos):
                Slovensko.stav()
            if button_dan.check_click(pos):
                input_active = True
                input_text = ""
        if event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_RETURN:
                try:
                    percent = int(input_text)
                    Slovensko.znizit_dane(percent)
                except ValueError:
                    Slovensko.output_text = "Zadajte platne cislo!"
                input_active = False
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
    
    button_stav.draw(screen, font)
    button_dan.draw(screen, font)
    
    text_surface = font.render(Slovensko.output_text, True, (0, 0, 0))
    screen.blit(text_surface, (50, 500))
    
    if input_active:
        pygame.draw.rect(screen, (200, 200, 200), (300, 250, 200, 40))
        input_text_surface = font.render(input_text, True, (0, 0, 0))
        screen.blit(input_text_surface, (310, 260))
        prompt_surface = font.render("O kolko percent chcete znizit dane:", True, (0, 0, 0))
        screen.blit(prompt_surface, (300, 220))
    
    pygame.display.flip()

pygame.quit()

