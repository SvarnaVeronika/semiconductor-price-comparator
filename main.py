
class InvalidPriceError(Exception):                                 #vlastna vynimka tzkajuca sa ceny
    pass

class SemiconductorPart:                                            #trieda polovodicovej suciastky s atributmi: mpn, opis, puzdro, rozmery a slovnik cien
    def __init__(self, mpn: str, description: str, package: str, dimensions: str, prices: dict):
        self.mpn = mpn
        self.description = description
        self.package  = package
        self.dimensions =  dimensions
        self.prices = prices

    def add_price(self, distributor: str, price: float):            #prida cenu do slovnika s novym klucom resp cenu prepise pri uz existujucom kluci
        try:                                                        #pokusi sa konvertovat cenu
            price = float(price)
        except (ValueError, TypeError):                             #zachyti chybu ak cena nie je cislo aleb je nespravneho typu a vyhodi vynimku
            raise InvalidPriceError("Cena nie je cislo")
        if price < 0:                                               #aj ak je cena zaporna vyhodi vynimku
            raise InvalidPriceError("Cena nemoze byt zaporna")

        self.prices[distributor] = price

    def has_price(self):                                            #metoda zisti, ci je slovniku pritomna cena a vrati bool hodnotu
        return len(self.prices) > 0

    def get_lowest_price(self):                                     #metoda najde vo vsetkych ulozenyc cenach tu najnizsiu
        try:                                                        #pokusi sa vratit minimalnu hodnotu
            return min(self.prices.values())
        except ValueError:                                          #v pripade, ze slovnik neobsahuje ziadne ceny, vyhodi value error a vrati None
            return None