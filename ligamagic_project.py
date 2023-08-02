from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from time import sleep

def replace_all_price(text):
    return text.replace("R$ ", "").replace(",", ".")

def get_soup(url):
    driver = webdriver.Firefox()
    driver.get(url)

    for i in range(30):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")

    return soup    

def get_rarity_and_type(name, set_code):
    sleep(0.1)
    
    response = requests.get(f"https://api.scryfall.com/cards/named?fuzzy={name}&set={set_code}")

    data = response.json()

    return(data["rarity"], data["type_line"])

def get_name(card):
    span = card.find("span")

    has_portuguese = str(span).find("<br/>") != -1

    if(has_portuguese):
        index = str(span).find("<br/>")
        name = str(span)[(index + 5):]
        index = name.find("</span>")
        name = name[:index]
    else:
        name = card.find('b').text

        if(name.find("(") != -1):
            index = name.find("(")
            name = name[:index]

    name = name.replace(" ", "+")

    return(name)

def get_card_infos(card, set_code, list_cards):
    name = get_name(card)
    min_price = card.find("div", class_="avgp-minprc")
    min_price = float(replace_all_price(min_price.text))
    rarity, type_line = get_rarity_and_type(name, set_code)

    if(not list_cards.count([name, min_price, rarity])):
        list_cards.append({"name": name, "min_price": min_price, "rarity": rarity, "set": set_code, "type_line": type_line})

def check_set(set_code):
    response = requests.get(f"https://api.scryfall.com/sets").json()

    list_sets = response["data"]
    sets_codes = []

    for set in list_sets:
        sets_codes.append(set["code"])

    return sets_codes.count(set_code) == 0

set_code = input("Digite o código do set que deseja buscar: ")

while(check_set(set_code.lower())):
    set_code = input("Este código de set não existe, favor informar outro ")

url = f"https://www.ligamagic.com.br/?view=cards/search&card=ed%3D{set_code}"
soup = get_soup(url)

list_cards_html = soup.find_all("div", class_="card-item")

if(len(list_cards_html) == 0):
    print("Nenhuma carta foi adcionada a esta coleção ainda")
else:
    list_cards = []
    for card in list_cards_html:
        get_card_infos(card, set_code, list_cards)

print(list_cards)