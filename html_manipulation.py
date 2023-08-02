def get_name(card):
    has_portuguese = card.split("span")[1].find("<br/>")

    if(has_portuguese != -1):
        name = card.split("<br/>")[5].split("</")[0]
    else:
        name = card.split("<b>")[1].split("</b>")[0]

    return name

def get_price(card):
    price = card.split('minprc">')[1].split("</div>")[0].replace("R$", "")

    return price