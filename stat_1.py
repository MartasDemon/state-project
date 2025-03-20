import pygame

class Stat:
    def __init__(self, rozpocet,vydaje, dlh, dan, pop ):
        self.rozpocet = rozpocet
        self.vydaje = vydaje
        self.dlh = dlh
        self.dan = dan 
        self.pop = pop

    def stav(self):
        print(f'Narodny dlh:{self.dlh}€, Narodny rozpočet je:{self.rozpocet},Narodne vydaje(mesacne):{self.vydaje} Nasa dan je {self.dan * 100}%, Pocet obyvatelov je {self.pop}')

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
    
    def znizit_dane(self):
        percento = int(input("O kolko percent chcete znizit dane"))
        self.dan = self.dan - (percento / 100)
        print(f'Nasa dan je {self.dan * 100}%')
    
#classes for pygame 
class Utvar:
    def __init__(self, x, y, farba=None):
        self.x = x
        self.y = y
        self.farba = farba

class Button(Utvar):
    def __init__(self, x, y, sirka, vyska, text, farba=None):
        super().__init__(x, y, farba)
        self.sirka = sirka
        self.vyska = vyska
        self.text = text
        self.rect = pygame.Rect(x, y, sirka, vyska)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.farba, self.rect)
        text_surface = font.render(self.text, True, (255, 255, 255))  
        screen.blit(text_surface, (self.x + 10, self.y + 10)) 

    def check_click(self, pos):
        if self.rect.collidepoint(pos):  
            return True
        return False

    



image = pygame.image.load('images/slovensko.png') 
image = pygame.transform.scale(image, (300, 200))

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Economic Simulator")

# Nastavenie fontu
font = pygame.font.Font(None, 30)

# Vytvorenie objektu štátu
Slovensko = Stat(1000, 300, 200, 0.20, 500000)

# Vytvorenie tlačítok
button1 = Button(50, 375, 200, 50, "Skontrolovat stav", ("black"))
button2 = Button(50, 300, 200, 50, "Znižat dan", ("black"))

running = True

# Hlavná slučka
while running:
    screen.fill((255, 255, 255))  

    # Spracovanie udalostí (napr. kliknutie na tlačítko)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if button1.check_click(pos):
                Slovensko.stav()
            if button2.check_click(pos):
                Slovensko.znizit_dane()


    # Vykreslenie tlačítok
    button1.draw(screen)
    button2.draw(screen)


    # Zobrazenie obrázka
    image = pygame.image.load('images/slovensko.png')  # Uisti sa, že cesta k obrázku je správna
    image = pygame.transform.scale(image, (300, 200))
    screen.blit(image, (250, 50))

    # Aktualizácia okna
    pygame.display.flip()

pygame.quit()



