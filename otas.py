import pygame
import sys
import math
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Economic Simulator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

# Party colors
PARTY_COLORS = {
    "KSS": (255, 0, 0),        # Red
    "Republika": (0, 0, 139),  # Dark blue
    "SMER": (220, 20, 60),     # Crimson
    "HLAS": (255, 69, 0),      # Orange-red
    "SNS": (0, 100, 0),        # Dark green
    "KDH": (0, 0, 255),        # Blue
    "PS": (255, 215, 0),       # Gold
    "Olano": (0, 128, 128),    # Teal
    "SAS": (30, 144, 255)      # Dodger blue
}

# Fonts
font_small = pygame.font.Font(None, 18)  # Smaller font for ministries
font_medium = pygame.font.Font(None, 24)
font_large = pygame.font.Font(None, 36)

class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hovered = False
        
    def draw(self, surface):
        color = self.color
        if self.hovered:
            color = (min(self.color[0] + 30, 255), 
                    min(self.color[1] + 30, 255), 
                    min(self.color[2] + 30, 255))
            
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_surf = font_medium.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
        
    def is_clicked(self, pos, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = font_small.render(text, True, self.color)  # Smaller font
        self.active = False

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            # Toggle active if clicked on the input box
            self.active = self.rect.collidepoint(event.pos)
        if event.type == KEYDOWN:
            if self.active:
                if event.key == K_RETURN:
                    return self.text
                elif event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text
                self.txt_surface = font_small.render(self.text, True, self.color)
        return None

    def draw(self, screen):
        # Draw the input box rectangle
        pygame.draw.rect(screen, WHITE, self.rect, 0)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # Draw the text
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

class Country:
    def __init__(self):
        # Initialize all country stats
        self.dlh = 200
        self.rozpocet = 1000
        self.vydaje = 300
        self.celkova_dan = 0.20
        self.pop = 500000
        
        # Date
        self.day = 1
        self.month = 10  # Changed to October
        self.year = 2023  # Changed to 2023
        
        # Economic stats
        self.inflacia = 0.0
        self.statna_kasa = 0.0
        self.statny_spending = 0.0
        self.dan_z_prijmu = 0.0
        self.predchadzajuca_dan = 0.0
        self.gdp_per_capita_mesacny = 0.0
        self.rast_or_pokles_populacie = 0.0
        self.dovera_na_pozicku = "abcdef"
        self.svk_pozickova_dovera = 'b'
        self.urokova_sadzba_mmf = 0.0
        self.pridane_peniaze = 0.0
        
        # Country statistics
        self.populacny_growth = 0.0
        self.splatene_peniaze_pozicky = 0.0
        self.musime_splatit_mmf = 0.0
        self.populacia = 5421272
        self.gdp = 132900000000
        self.gdp_per_capita = self.gdp / self.populacia
        self.zmena_splatenia_mmf = 0.0
        self.mesacna_splatka = 0.0
        self.ostatne_prijmy_spolu = 418059520
        self.statne_prijmy = self.ostatne_prijmy_spolu + (self.gdp_per_capita_mesacny * self.populacia) * self.celkova_dan
        
        # Ministry budgets with Slovak names (shorter names)
        self.ministerstva = {
            "Hospodárstvo": 239520379 / 12,
            "Financie": 400854206 / 12,
            "Doprava": 776581874 / 12,
            "Pôdohospodárstvo": 450000000 / 12,
            "Obrana": 2000000000 / 12,
            "Vnútra": 1927446797 / 12,
            "Spravodlivosť": 900000000 / 12,
            "Zahraničie": 950000000 / 12,
            "Práca a soc. veci": 4551851367 / 12,
            "Životné prostredie": 900000000 / 12,
            "Školstvo": 1500000000 / 12,
            "Kultúra": 250000000 / 12,
            "Zdravotníctvo": 4000000000 / 12,
            "Investície": 136207289 / 12,
            "Cestovný ruch": 350000000 / 12,
            "Úrad vlády": 52282149 / 12,
            "Protimonopolný": 15000000 / 12,
            "Štatistický": 60000000 / 12,
            "Geodézia": 40000000 / 12,
            "Jadrový dozor": 25000000 / 12,
            "Normalizácia": 40000000 / 12,
            "Verejné obstarávanie": 40000000 / 12,
            "Štátne rezervy": 200000000 / 12,
            "Územné plánovanie": 50000000 / 12,
            "Národná bezpečnosť": 17984619 / 12
        }
        
        # Initialize other country attributes
        self.typ_vladneho_zriadenia = ["prezidentská republika", "parlamentna republika", 
                                      "Absolutna Monarchia", "Konstitucna Monarchia", 
                                      "Autoritársky Rezim", "Anarchia"]
        self.typ_vladneho_zriadenia_svk = "parlamentna republika"
        
        self.svk_vsetky_strany = ["KSS", "Republika", "SMER", "HLAS", "SNS", "KDH", "PS", "Olano", "SAS"]
        self.svk_vsetky_strany_percenta = [0.00, 0.05, 0.24, 0.17, 0.07, 0.09, 0.21, 0.10, 0.07]
        
        self.posledne_volby_svk = "01/10/2023"
        self.dalsie_volby_svk = "01/10/2027"
        
        self.parlamentne_kresla = 150
        self.pocet_kresiel_s = [0] * 9
        
        self.zvysenie_or_znizenie_pop_koa_stran = 0.0
        self.zvysenie_or_znizenie_pop_opo_stran = 0.0
        
        # Initialize state
        self.current_screen = "main"
        self.selected_ministry = None
        self.input_box = None
        
        # Calculate initial values
        self.calculate_initial_values()
        self.konanie_volieb()  # Initialize seats
    
    def calculate_initial_values(self):
        self.gdp_per_capita = self.gdp / self.populacia
        self.gdp_per_capita_mesacny = self.gdp_per_capita / 12.0
        self.celkova_dan = 0.17
        self.predchadzajuca_dan = self.celkova_dan
        self.statna_kasa = self.ostatne_prijmy_spolu + (self.gdp_per_capita_mesacny * self.populacia) * self.celkova_dan
        self.statne_prijmy = self.ostatne_prijmy_spolu + (self.gdp_per_capita_mesacny * self.populacia) * self.celkova_dan
        
        # Calculate total spending
        self.statny_spending = sum(self.ministerstva.values())
    
    def zmena_ekonomiky(self):
        self.gdp = self.gdp * 1.00206
        self.gdp_per_capita = self.gdp / self.populacia
        self.statne_prijmy = self.ostatne_prijmy_spolu + (self.gdp_per_capita_mesacny * self.populacia) * self.celkova_dan
        self.statna_kasa = self.statna_kasa - self.statny_spending + (self.gdp_per_capita_mesacny * self.populacia) * self.celkova_dan
    
    def zvysenie_mesiaca(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
    
    def zmena_populacie(self):
        self.populacia = self.populacia - 14
    
    def splatenie_pozicky(self):
        self.musime_splatit_mmf = self.pridane_peniaze + self.pridane_peniaze * self.urokova_sadzba_mmf
        self.mesacna_splatka = (self.musime_splatit_mmf / 12)
        self.zmena_splatenia_mmf = self.musime_splatit_mmf
        
        if self.zmena_splatenia_mmf > 0 and self.statna_kasa > self.mesacna_splatka:
            self.zmena_splatenia_mmf -= self.mesacna_splatka
            self.statna_kasa -= self.mesacna_splatka
            self.pridane_peniaze -= (3000000000 + 3000000000 * self.urokova_sadzba_mmf) / 12
        
        if self.zmena_splatenia_mmf <= 0 and self.pridane_peniaze < 0:
            self.zmena_splatenia_mmf = 0
            self.pridane_peniaze = 0
            self.urokova_sadzba_mmf = 0
    
    def next_month(self):
        self.zvysenie_mesiaca()
        self.zmena_ekonomiky()
        self.zmena_populacie()
        self.splatenie_pozicky()
        
        # Update political popularity
        self.zvysenie_or_znizenie_pop_koa_stran -= 0.002
        self.zvysenie_or_znizenie_pop_opo_stran += 0.002
        
        # Check for elections
        if self.year == 2027 or self.year == 2031:  # Example election years
            self.konanie_volieb()
    
    def konanie_volieb(self):
        # Simple election simulation - in a real game you'd want more complex logic
        for i in range(len(self.svk_vsetky_strany_percenta)):
            if i in [2, 3, 4]:  # Coalition parties (example)
                self.svk_vsetky_strany_percenta[i] += self.zvysenie_or_znizenie_pop_koa_stran
            else:  # Opposition parties
                self.svk_vsetky_strany_percenta[i] += self.zvysenie_or_znizenie_pop_opo_stran
            
            # Ensure percentages don't go negative
            if self.svk_vsetky_strany_percenta[i] < 0:
                self.svk_vsetky_strany_percenta[i] = 0
        
        # Normalize percentages to sum to 1
        total = sum(self.svk_vsetky_strany_percenta)
        self.svk_vsetky_strany_percenta = [p/total for p in self.svk_vsetky_strany_percenta]
        
        # Calculate seats - simple proportional allocation
        total_seats = 0
        seats = []
        remainders = []
        
        # First allocate integer seats
        for i in range(len(self.svk_vsetky_strany_percenta)):
            exact_seats = self.svk_vsetky_strany_percenta[i] * self.parlamentne_kresla
            int_seats = int(exact_seats)
            seats.append(int_seats)
            remainders.append(exact_seats - int_seats)
            total_seats += int_seats
        
        # Distribute remaining seats to parties with highest remainders
        remaining_seats = self.parlamentne_kresla - total_seats
        while remaining_seats > 0:
            max_remainder = max(remainders)
            index = remainders.index(max_remainder)
            seats[index] += 1
            remainders[index] = -1  # So we don't select it again
            remaining_seats -= 1
        
        self.pocet_kresiel_s = seats
        
        # Update election dates
        self.posledne_volby_svk = f"{self.day:02d}/{self.month:02d}/{self.year}"
        self.dalsie_volby_svk = f"{self.day:02d}/{self.month:02d}/{self.year + 4}"
    
    def update_spending(self):
        self.statny_spending = sum(self.ministerstva.values())
    
    def change_ministry_budget(self, ministry, new_budget):
        if ministry in self.ministerstva:
            self.ministerstva[ministry] = new_budget
            self.update_spending()
            return True
        return False
    
    def get_date_string(self):
        return f"{self.day:02d}/{self.month:02d}/{self.year}"

def draw_main_screen(country, buttons):
    screen.fill(WHITE)
    
    # Draw date - centered at top
    date_text = font_large.render(country.get_date_string(), True, BLACK)
    screen.blit(date_text, (SCREEN_WIDTH // 2 - date_text.get_width() // 2, 20))
    
    # Draw country info
    info_y = 70
    info_lines = [
        f"Krajina: Slovensko",
        f"HDP per capita: {country.gdp_per_capita:,.2f} €",
        f"Štátna pokladnica: {country.statna_kasa:,.2f} €",
        f"Štátne výdavky: {country.statny_spending:,.2f} €",
        f"Štátne príjmy: {country.statne_prijmy:,.2f} €",
        f"Dôvera na pôžičku: {country.svk_pozickova_dovera}",
        f"Splácanie MMF: {country.zmena_splatenia_mmf:,.2f} € ({country.urokova_sadzba_mmf:.2f}%)"
    ]
    
    for line in info_lines:
        text = font_medium.render(line, True, BLACK)
        screen.blit(text, (50, info_y))
        info_y += 30
    
    # Draw buttons
    for button in buttons:
        button.draw(screen)
    
    # Warning if budget is negative
    if country.statna_kasa < 0:
        warning_text = font_large.render("Štátna pokladnica je v minuse!", True, RED)
        screen.blit(warning_text, (SCREEN_WIDTH // 2 - warning_text.get_width() // 2, SCREEN_HEIGHT - 100))

def draw_ministries_screen(country, back_button):
    screen.fill(WHITE)
    
    # Title
    title = font_large.render("Riadenie ministerstiev a úradov", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))
    
    # Draw ministry list with input boxes
    y_pos = 70
    scroll_offset = 0  # For scrolling if needed
    
    # Display total spending and balance - made smaller
    total_text = font_small.render(f"Celkové výdaje: {country.statny_spending:,.2f} €", True, BLACK)
    screen.blit(total_text, (SCREEN_WIDTH - 250, y_pos))
    
    balance_text = font_small.render(
        f"Bilancia: {'+' if country.statna_kasa >= 0 else ''}{country.statna_kasa:,.2f} €", 
        True, GREEN if country.statna_kasa >= 0 else RED
    )
    screen.blit(balance_text, (SCREEN_WIDTH - 250, y_pos + 20))
    
    income_text = font_small.render(f"Štátne príjmy: {country.statne_prijmy:,.2f} €", True, BLACK)
    screen.blit(income_text, (SCREEN_WIDTH - 250, y_pos + 40))
    
    # Draw each ministry with its budget - made smaller
    for i, (ministry, budget) in enumerate(country.ministerstva.items()):
        # Ministry name and current budget
        ministry_text = font_small.render(f"{ministry}:", True, BLACK)
        screen.blit(ministry_text, (50, y_pos + i * 30 + scroll_offset))  # Reduced spacing
        
        # Input box for budget - made smaller
        input_box = InputBox(300, y_pos + i * 30 + scroll_offset, 150, 25, f"{budget:,.2f}")  # Smaller dimensions
        
        # Handle input if this is the selected ministry
        if country.selected_ministry == ministry:
            country.input_box = input_box
        
        input_box.draw(screen)
        
        # Highlight if hovered
        input_rect = pygame.Rect(300, y_pos + i * 30 + scroll_offset, 150, 25)
        if input_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, LIGHT_BLUE, input_rect, 2)
    
    # Back button
    back_button.draw(screen)
    
    # If a ministry is selected, show input instructions
    if country.selected_ministry:
        instruction_text = font_small.render("Zmeňte hodnotu a stlačte Enter", True, BLACK)
        screen.blit(instruction_text, (300, y_pos + len(country.ministerstva) * 30 + scroll_offset + 10))

def draw_country_info_screen(country, back_button):
    screen.fill(WHITE)
    
    # Title
    title = font_large.render("Informácie o krajine", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))
    
    # Government info
    info_y = 70
    info_lines = [
        f"Vládne zriadenie: {country.typ_vladneho_zriadenia_svk}",
        f"Vládna strana: {country.svk_vsetky_strany[2]} ({country.svk_vsetky_strany_percenta[2]*100:.1f}%)",
        f"Koalícia: {country.svk_vsetky_strany[2]} ({country.svk_vsetky_strany_percenta[2]*100:.1f}%), "
        f"{country.svk_vsetky_strany[3]} ({country.svk_vsetky_strany_percenta[3]*100:.1f}%), "
        f"{country.svk_vsetky_strany[4]} ({country.svk_vsetky_strany_percenta[4]*100:.1f}%)",
        f"Opozícia: {', '.join(f'{s} ({country.svk_vsetky_strany_percenta[i]*100:.1f}%)' for i, s in enumerate(country.svk_vsetky_strany) if i not in [2, 3, 4])}",
        f"Posledné voľby: {country.posledne_volby_svk}",
        f"Ďalšie voľby: {country.dalsie_volby_svk}",
        "",
        "Rozdelenie kresiel v parlamente:"
    ]
    
    for line in info_lines:
        text = font_medium.render(line, True, BLACK)
        screen.blit(text, (50, info_y))
        info_y += 30
    
    # Parliament seats with colors
    seat_y = info_y
    for i, party in enumerate(country.svk_vsetky_strany):
        seats = country.pocet_kresiel_s[i]
        if seats > 0:
            # Draw colored circle
            pygame.draw.circle(screen, PARTY_COLORS[party], (40, seat_y + 15), 10)
            
            text = font_medium.render(f"{party}: {seats} kresiel ({country.svk_vsetky_strany_percenta[i]*100:.1f}%)", True, BLACK)
            screen.blit(text, (60, seat_y))
            seat_y += 20
    
    # Draw parliament seats visualization as a rainbow (improved version)
    seats_y = SCREEN_HEIGHT - 250
    seats_title = font_medium.render("Parlamentné kreslá:", True, BLACK)
    screen.blit(seats_title, (SCREEN_WIDTH - 560, seats_y-175))

    # Parametre pre vizualizáciu dúh
    center_x = SCREEN_WIDTH - 375
    center_y = seats_y + 150
    radius_step = 18  # Väčší odstup medzi radmi
    seat_radius = 5

    # Počet kresiel v jednotlivých radoch - zmenené na 5 radov s novými počtami
    seats_per_row = [36, 34, 30, 26, 24]  # Number of seats in each row

    row = 0  # Row counter
    seat_in_row = 0  # Seat counter within current row

    for party_index, seats in enumerate(country.pocet_kresiel_s):
        for _ in range(seats):
            # Check if we've exceeded available rows
            if row >= len(seats_per_row):
                break
                
            current_seat_count = seats_per_row[row]
            
            # Calculate angle based on seat position in current row (starting from 0)
            angle = math.pi * (seat_in_row / current_seat_count)
            radius = 150 + (row * radius_step)
            
            # Calculate coordinates
            x = center_x + radius * math.cos(angle) * 1.6
            y = center_y - radius * math.sin(angle) * 1.3
            
            pygame.draw.circle(screen, PARTY_COLORS[country.svk_vsetky_strany[party_index]], (int(x), int(y)), seat_radius)
            
            seat_in_row += 1
            
            # Move to next row when current row is filled
            if seat_in_row >= current_seat_count:
                row += 1
                seat_in_row = 0  # Reset seat counter for new row










        
    
    # Back button
    back_button.draw(screen)

def draw_budget_warning_screen(country, buttons):
    screen.fill(WHITE)
    
    # Title
    title = font_large.render("Štátna pokladnica je v minuse!", True, RED)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
    
    warning_text = font_medium.render("Musíte zvýšiť dane, znížiť štátne výdaje alebo požičať peniaze!", True, BLACK)
    screen.blit(warning_text, (SCREEN_WIDTH // 2 - warning_text.get_width() // 2, 100))
    
    info_text = font_medium.render(f"Aktuálny stav: {country.statna_kasa:,.2f} €", True, BLACK)
    screen.blit(info_text, (SCREEN_WIDTH // 2 - info_text.get_width() // 2, 150))
    
    # Draw buttons
    button_y = 200
    for button in buttons:
        button.rect.y = button_y
        button.draw(screen)
        button_y += 60
    
    # Loan info
    if country.svk_pozickova_dovera in country.dovera_na_pozicku:
        loan_text = font_medium.render(f"Dôvera na pôžičku: {country.svk_pozickova_dovera}", True, BLACK)
        screen.blit(loan_text, (SCREEN_WIDTH // 2 - loan_text.get_width() // 2, button_y))

def draw_tax_change_screen(country, input_box, confirm_button, back_button):
    screen.fill(WHITE)
    
    # Title
    title = font_large.render("Zmena daňovej sadzby", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
    
    current_tax_text = font_medium.render(f"Aktuálna daňová sadzba: {country.celkova_dan*100:.1f}%", True, BLACK)
    screen.blit(current_tax_text, (SCREEN_WIDTH // 2 - current_tax_text.get_width() // 2, 120))
    
    instruction_text = font_medium.render("Zadajte novú daňovú sadzbu (v %):", True, BLACK)
    screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 170))
    
    # Input box
    input_box.draw(screen)
    
    # Buttons
    confirm_button.draw(screen)
    back_button.draw(screen)

def draw_loan_screen(country, buttons, back_button):
    screen.fill(WHITE)
    
    # Title
    title = font_large.render("Pôžička od MMF", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
    
    # Loan info based on trust level
    trust_level = country.dovera_na_pozicku.index(country.svk_pozickova_dovera)
    loan_info = [
        "Dôvera na pôžičku: " + {
            0: "Vynikajúca (úrok 2%)",
            1: "Veľmi dobrá (úrok 4%)",
            2: "Dobrá (úrok 7%)",
            3: "Priemerná (úrok 10%)",
            4: "Zlá (úrok 13%)",
            5: "Veľmi zlá (žiadna pôžička)"
        }[trust_level],
        "",
        "Pôžička MMF pokryje váš deficit s 3 miliardami €"
    ]
    
    info_y = 120
    for line in loan_info:
        text = font_medium.render(line, True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, info_y))
        info_y += 30
    
    # Draw buttons (only if loan is available)
    if trust_level < 5:
        buttons[0].rect.y = info_y + 30
        buttons[0].draw(screen)
    
    back_button.draw(screen)

def main():
    clock = pygame.time.Clock()
    country = Country()
    
    # Main screen buttons
    next_month_button = Button(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 60, 150, 50, "Ďalší mesiac")
    ministries_button = Button(50, SCREEN_HEIGHT - 60, 200, 50, "Ministerstvá")
    country_info_button = Button(270, SCREEN_HEIGHT - 60, 200, 50, "Informácie o krajine")
    
    # Ministry screen buttons
    back_button = Button(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 60, 100, 50, "Späť")
    
    # Budget warning buttons
    increase_tax_button = Button(SCREEN_WIDTH // 2 - 150, 200, 300, 50, "Zvýšiť dane")
    decrease_spending_button = Button(SCREEN_WIDTH // 2 - 150, 260, 300, 50, "Znížiť výdaje")
    get_loan_button = Button(SCREEN_WIDTH // 2 - 150, 320, 300, 50, "Požičať od MMF")
    
    # Tax change screen elements
    tax_input_box = InputBox(SCREEN_WIDTH // 2 - 100, 200, 200, 40)
    confirm_tax_button = Button(SCREEN_WIDTH // 2 - 220, 300, 200, 50, "Potvrdiť")
    tax_back_button = Button(SCREEN_WIDTH // 2 + 20, 300, 200, 50, "Späť")
    
    # Loan screen buttons
    take_loan_button = Button(SCREEN_WIDTH // 2 - 150, 200, 300, 50, "Zobrať pôžičku")
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            # Handle button hover for all screens
            if country.current_screen == "main":
                next_month_button.check_hover(mouse_pos)
                ministries_button.check_hover(mouse_pos)
                country_info_button.check_hover(mouse_pos)
                
                if next_month_button.is_clicked(mouse_pos, event):
                    country.next_month()
                    if country.statna_kasa < 0:
                        country.current_screen = "budget_warning"
                
                if ministries_button.is_clicked(mouse_pos, event):
                    country.current_screen = "ministries"
                    country.selected_ministry = None
                    country.input_box = None
                
                if country_info_button.is_clicked(mouse_pos, event):
                    country.current_screen = "country_info"
            
            elif country.current_screen == "ministries":
                back_button.check_hover(mouse_pos)
                
                # Handle clicking on ministry input boxes
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    for i, (ministry, _) in enumerate(country.ministerstva.items()):
                        input_rect = pygame.Rect(300, 70 + i * 30, 150, 25)
                        if input_rect.collidepoint(mouse_pos):
                            country.selected_ministry = ministry
                            country.input_box = InputBox(300, 70 + i * 30, 150, 25, f"{country.ministerstva[ministry]:,.2f}")
                            break
                
                if back_button.is_clicked(mouse_pos, event):
                    country.current_screen = "main"
                    country.selected_ministry = None
                    country.input_box = None
            
            elif country.current_screen == "country_info":
                back_button.check_hover(mouse_pos)
                if back_button.is_clicked(mouse_pos, event):
                    country.current_screen = "main"
            
            elif country.current_screen == "budget_warning":
                increase_tax_button.check_hover(mouse_pos)
                decrease_spending_button.check_hover(mouse_pos)
                get_loan_button.check_hover(mouse_pos)
                
                if increase_tax_button.is_clicked(mouse_pos, event):
                    country.current_screen = "tax_change"
                
                if decrease_spending_button.is_clicked(mouse_pos, event):
                    country.current_screen = "ministries"
                
                if get_loan_button.is_clicked(mouse_pos, event):
                    country.current_screen = "loan"
            
            elif country.current_screen == "tax_change":
                confirm_tax_button.check_hover(mouse_pos)
                tax_back_button.check_hover(mouse_pos)
                
                # Handle input box
                new_tax = tax_input_box.handle_event(event)
                if new_tax is not None:
                    try:
                        new_tax_value = float(new_tax) / 100
                        if new_tax_value > country.celkova_dan:
                            country.celkova_dan = new_tax_value
                            country.statna_kasa += (country.gdp_per_capita_mesacny * country.populacia) * (country.celkova_dan - country.predchadzajuca_dan)
                            country.predchadzajuca_dan = country.celkova_dan
                            country.current_screen = "main"
                    except ValueError:
                        pass
                
                if confirm_tax_button.is_clicked(mouse_pos, event):
                    new_tax = tax_input_box.text
                    try:
                        new_tax_value = float(new_tax) / 100
                        if new_tax_value > country.celkova_dan:
                            country.celkova_dan = new_tax_value
                            country.statna_kasa += (country.gdp_per_capita_mesacny * country.populacia) * (country.celkova_dan - country.predchadzajuca_dan)
                            country.predchadzajuca_dan = country.celkova_dan
                            country.current_screen = "main"
                    except ValueError:
                        pass
                
                if tax_back_button.is_clicked(mouse_pos, event):
                    country.current_screen = "budget_warning"
            
            elif country.current_screen == "loan":
                take_loan_button.check_hover(mouse_pos)
                back_button.check_hover(mouse_pos)
                
                if take_loan_button.is_clicked(mouse_pos, event):
                    trust_level = country.dovera_na_pozicku.index(country.svk_pozickova_dovera)
                    if trust_level == 0:
                        country.urokova_sadzba_mmf = 0.02
                    elif trust_level == 1:
                        country.urokova_sadzba_mmf = 0.04
                    elif trust_level == 2:
                        country.urokova_sadzba_mmf = 0.07
                    elif trust_level == 3:
                        country.urokova_sadzba_mmf = 0.10
                    elif trust_level == 4:
                        country.urokova_sadzba_mmf = 0.13
                    
                    if trust_level < 5:
                        country.pridane_peniaze = 3000000000  # 3 billion
                        country.statna_kasa += country.pridane_peniaze
                        country.current_screen = "main"
                
                if back_button.is_clicked(mouse_pos, event):
                    country.current_screen = "budget_warning"
            
            # Handle ministry budget input
            if country.input_box and country.current_screen == "ministries":
                result = country.input_box.handle_event(event)
                if result is not None:
                    try:
                        new_budget = float(result.replace(",", ""))
                        if country.selected_ministry:
                            country.change_ministry_budget(country.selected_ministry, new_budget)
                            country.input_box = None
                            country.selected_ministry = None
                    except ValueError:
                        pass
        
        # Draw the appropriate screen
        if country.current_screen == "main":
            draw_main_screen(country, [next_month_button, ministries_button, country_info_button])
        elif country.current_screen == "ministries":
            draw_ministries_screen(country, back_button)
        elif country.current_screen == "country_info":
            draw_country_info_screen(country, back_button)
        elif country.current_screen == "budget_warning":
            draw_budget_warning_screen(country, [increase_tax_button, decrease_spending_button, get_loan_button])
        elif country.current_screen == "tax_change":
            draw_tax_change_screen(country, tax_input_box, confirm_tax_button, tax_back_button)
        elif country.current_screen == "loan":
            draw_loan_screen(country, [take_loan_button], back_button)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
