import random
from Utils import Singleton
from Card import Card


@Singleton
class Deck:
    def __init__(self) -> None:
        self.deck = self.init_deck()
        self.deprecated = []
        self.jocker = 2

    def init_deck(self):
        self.deck = []
        self.deprecated = []
        color = ["♠", "♥", "♣", "♦"]
        value = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        temp_deck = []
        for c in color:
            for v in value:
                temp_deck.append(Card(c, v))
        random.shuffle(temp_deck)
        return temp_deck

    def restart(self):
        self.__init__()

    def __repr__(self) -> str:
        return f"Deck: {len(self.deck)}\nDeprecated: {len(self.deprecated)}"

    def draw(self, num):
        temp = []
        if num <= len(self.deck):
            temp = self.deck[:num]
            self.deck = self.deck[num:]
        else:
            temp = self.deck
            self.deck = []
        return temp

    def new_member_event(self, color, value):
        self.deck = [Card(color, value)] + self.deck

    def heart_event(self, num):
        temp = []
        if num <= len(self.deprecated):
            random.shuffle(self.deprecated)
            temp = self.deprecated[:num]
            self.deprecated = self.deprecated[num:]
            for card in temp:
                self.deck.append(card)
        else:
            random.shuffle(self.deprecated)
            for card in self.deprecated:
                self.deck.append(card)
            self.deprecated = []

    def deprecate_event(self, cards):
        for card in cards:
            self.deprecated.append(card)


Deck()

if __name__ == "__main__":
    d1 = Deck()
    d2 = Deck()
    print(d1 is d2)
