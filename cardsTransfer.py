from card import Card
from cardscollection import CardsCollection

def transferCard(card:Card,source:CardsCollection,destination:CardsCollection):        
    source.remove(card)
    destination.add(card)
def transferCards(cards:list[Card],source:CardsCollection,destination:CardsCollection):        
    for card in  cards:
        transferCard(card, source, destination)