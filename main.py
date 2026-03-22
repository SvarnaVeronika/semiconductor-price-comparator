
class SemiconductorPart:    #trieda polovodicovej suciastky s atributmi: mpn, opis, puzdro, rozmery a slovnik cien
    def __init__(self, mpn: str, description: str, package: str, dimensions: str, prices: dict):
        self.mpn = mpn
        self.description = description
        self.package  = package
        self.dimensions =  dimensions
        self.prices = prices

    def add_price(self, distributor: str, price: float):    #prida cenu do slovnika s novym klucom resp cenu prepise pri uz existujucom kluci
        self.prices[distributor] = price

    def has_price(self):    #metoda zisti, ci je slovniku pritomna cena a vrati bool hodnotu
        return len(self.prices) > 0

    def get_lowest_price(self): #metoda najde vo vsetkych ulozenyc cenach tu najnizsiu
        return min(self.prices.values())
