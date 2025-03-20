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

    


Slovensko = Stat(1000,300,200,0.20,500000)
Slovensko.stav()
# Slovensko.zvysit_dane()
# Slovensko.splatit_dlh(100) 
# Slovensko.znizit_dane()


