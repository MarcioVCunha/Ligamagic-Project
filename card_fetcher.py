from soup import get_soup
import html_manipulation
import scryfall
from time import sleep

set_exists = False

while(not set_exists):
    set_code = input(f"Qual coleção gostaria de acessar?\n")
    url = f"https://www.ligamagic.com.br/?view=cards/search&card=ed%3D{set_code}"
    soup = get_soup(url)
    list_cards_html = soup.find_all("div", class_="card-item")

    if(len(list_cards_html) == 0):
        print("Nenhuma carta foi adcionada a esta coleção ainda ou ela não existe")

    else:
        print("Carregando...")
        set_exists = True

common_list = []
uncommon_list = []
rare_list = []
mythic_list = []

for card in list_cards_html:
    card = str(card)

    name = html_manipulation.get_name(card)
    price = html_manipulation.get_price(card)
    sleep(0.1)
    rarity = scryfall.get_rarity(name, set_code)
    if(rarity == "common"):
        common_list.append([name, price, rarity])
    elif(rarity == "uncommon"):
        uncommon_list.append([name, price, rarity])
    elif(rarity == "rare"):
        rare_list.append([name, price, rarity])
    elif(rarity != "not include" and name.find("Emblem - ") != -1):
        mythic_list.append([name, price, rarity])
