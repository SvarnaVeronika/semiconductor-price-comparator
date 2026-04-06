import requests
from config import API_KEY


class OEMSecretsClient:                                                     # trieda sluziaca na komunikaciu s OEMSecrets API
    def __init__(self):                                                     # konstruktor triedy, nastavuje zakladnu URL endpointu
        self.base_url = "https://oemsecretsapi.com/partsearch"              # base_url obsahuje URL endpointu pre vyhladvanie suciastok

    def search_part(self, mpn: str):                                        # metoda na vyhladanie partu podľa MPN; nastavuje menu na EUR a krajinu na Slovensko
        params = {                                                          # parametre HTTP requestu pre API
            "searchTerm": mpn,
            "apiKey": API_KEY,
            "currency": "EUR",
            "countryCode": "SK"
        }

        response = requests.get(self.base_url, params=params, timeout=10)   # odoslanie HTTP GET requestu na API
        response.raise_for_status()                                         #ak o odpoved nie je uspesna, vyhodi vynimku
        return response.json()                                              #metoda vracia odpoved z Api vo forme json