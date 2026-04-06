from secrets import API_KEY

if not API_KEY:
    raise ValueError("API key nie je validny.") #vynimku vyhodi ak nie je nastaveny apI kluc resp je prazdny

TIMEOUT = 10                                    #max cas na http request

#print(API_KEY)                                 #testovaci vypis; overenie, ci vypise rovnaky api key, ktory bol zadany v secrets.py