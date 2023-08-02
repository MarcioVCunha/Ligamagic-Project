import requests

def get_rarity(name, set_code):
    response = requests.get(f"https://api.scryfall.com/cards/named?fuzzy={name.strip()}&set={set_code}")
    data = response.json()

    try:
        if(data["type_line"].find("Basic") != -1 or data["type_line"].find("Token") != -1 or data["type_line"].find("Emblem") != -1):
            return "not include"

        return data["rarity"]
    except:
        return "not include"