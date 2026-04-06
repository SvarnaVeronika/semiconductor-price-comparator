
class InvalidPriceError(Exception):                                              #vlastna vynimka tzkajuca sa ceny
    pass

class SemiconductorPart:                                                         #trieda polovodicovej suciastky s atributmi: mpn, opis, puzdro, rozmery a slovnik cien
    def __init__(self, mpn: str, description: str, package: str, dimensions: str, prices: dict):
        self.mpn = mpn
        self.description = description
        self.package  = package
        self.dimensions =  dimensions
        self.prices = prices

    def add_price(self, distributor: str, price: float):                          #prida cenu do slovnika s novym klucom resp cenu prepise pri uz existujucom kluci
        try:                                                                      #pokusi sa konvertovat cenu
            price = float(price)
        except (ValueError, TypeError):                                           #zachyti chybu ak cena nie je cislo aleb je nespravneho typu a vyhodi vynimku
            raise InvalidPriceError("Cena nie je cislo")
        if price < 0:                                                             #aj ak je cena zaporna vyhodi vynimku
            raise InvalidPriceError("Cena nemoze byt zaporna")
        if distributor not in self.prices or price < self.prices[distributor]:
            self.prices[distributor] = price

        self.prices[distributor] = price

    def has_price(self):                                                          #metoda zisti, ci je slovniku pritomna cena a vrati bool hodnotu
        return len(self.prices) > 0

    def get_lowest_price(self):                                                    #metoda najde vo vsetkych ulozenyc cenach tu najnizsiu
        try:                                                                       #pokusi sa vratit minimalnu hodnotu
            return min(self.prices.values())
        except ValueError:                                                         #v pripade, ze slovnik neobsahuje ziadne ceny, vyhodi value error a vrati None
            return None

from api_client import OEMSecretsClient                                            #import triedy OEMSecretsClient zo suboru api_client


def create_part_from_api_response(mpn: str, data: dict) -> SemiconductorPart:      #funkcia na vytvorenie suciastky z odpovede api
    stock_items = data.get("stock", [])                                # v slovniku data ziska ponuku v casti stock, v pri
    description = ""                                                               #nastavenie defaultnej hodnoty pre popis suciastky
    package = ""                                                                   #nastavenie defaultnej hodnoty pre package
    dimensions = ""                                                                #nastavenie defaultnej hodnoty pre rozmery

    if stock_items:                                                                #ak stock items nieco obsahuje
        first_item = stock_items[0]                                                #vezme prvu polozku
        description = first_item.get("description", "")                            #dostane popis z prvej polozky
        package = first_item.get("packaging", "")                                  #dostane typ packageu

    part = SemiconductorPart(                                                      #vytvorenie objektu triedy SemiconductorPart
        mpn=mpn,
        description=description,
        package=package,
        dimensions=dimensions,
        prices={}
    )

    for item in stock_items:                                                       #prezera zaznamy distributorov v stock_items
        distributor_info = item.get("distributor", {})                             #dostane informacie o distributorovi ako slovnik
        distributor_name = distributor_info.get("distributor_name", "Unknown distributor")  #dostane nayov distributra; ak ho nenajde, nastavi defaultnu hodnotu

        prices_dict = item.get("prices", {})                                       #dostane slovnik cien
        eur_prices = prices_dict.get("EUR", [])                                    #zo slovnika cien vytiahne do zoznamu len tie, ktore su v eurach

        if not eur_prices:                                                         #ak cena nie je v eurach program preskoci celz slovnik
            continue


        first_break = eur_prices[0]                                                #veyme zaznam o najmensom mnoztve, ktore je mozne objednat
        unit_price = first_break.get("unit_price")                                 #dostane cenu jedneho kusu z najmensieho mnozstva

        if unit_price in (None, "0.0000"):                                         #ak polozkanema cenu alebo je cena 0 tak preskoci zaznam
            continue

        try:                                                                       #skusi pridat cenu disty do objektu suciastky
            part.add_price(distributor_name, unit_price)
        except InvalidPriceError:                                                  #ak cena nie je pplatna tak preskoci zaznam
            continue

    return part                                                                    #vrati vytvoreny objekt suciastky aj s cenami


def main():                                                                         #hlavna funkcia je volana na konci
    print("Volam API...")                                                           #test print na overenie, ze hlavna funkcia sa spustila

    client = OEMSecretsClient()                                                     #vztvorenie objektu lkienta z triedy OEMSecretsClient
    mpn = "NCV1117ST50T3G"                                                          #priradenie konkretneho mpn do premennej mpn (docasne rieseine)

    data = client.search_part(mpn)                                                  #vola api a do premennej data ulozi response

    part = create_part_from_api_response(mpn, data)                                 #z api odpovede vytvori objekt SemicnoductorPart

    print("\nMPN:", part.mpn)                                                       #vypis jednotlivych poloyiek objektu part
    print("Description:", part.description)
    print("Package:", part.package)
    print("Ceny:", part.prices)
    print("Ma cenu?", part.has_price())
    print("Najnizsia cena:", part.get_lowest_price())


if __name__ == "__main__":                                                          #funkcia main sa spusti len pri priamom spusteni suboru
    main()