from Deck import Deck
from Utils import Singleton
from JQK import EnemyGroup


@Singleton
class Hand:
    def __init__(self) -> None:
        self.hand = self.init_hand()
        self.on_select = []

    def size(self):
        return len(self.hand)

    def init_hand(self):
        temp = Deck().draw(8)
        temp.sort()
        return temp

    def restart(self):
        self.__init__()

    def draw(self, val):
        temp = Deck().draw(val)
        self.hand += temp
        self.hand.sort()

    def play(self):
        Deck().deprecate_event(self.on_select)
        for card in self.on_select:
            self.hand.remove(card)
        self.on_select = []

    def select(self, card):
        self.on_select.append(card)

    def unselect(self, card):
        self.on_select.remove(card)

    def select_handler(self, card):
        if card in self.on_select:
            self.unselect(card)
        else:
            if len(self.on_select) < 4:
                self.select(card)

    def validate_play_hand(self):
        if len(self.on_select) <= 0:
            return False, "None"
        elif 0 < len(self.on_select) <= 1:
            return True, "normal"
        elif 1 < len(self.on_select) <= 2:
            if sum([card.is_a() for card in self.on_select]) == 1:
                return True, "pet"
            elif (
                self.on_select[0].get_val() == self.on_select[1].get_val()
                and self.on_select[0].get_val() + self.on_select[1].get_val() <= 10
                and self.on_select[0].get_val() != 1
            ):
                return True, "combo"
            else:
                return False, "None"
        elif 2 < len(self.on_select):
            vals = [card.get_val() for card in self.on_select]
            if all([vals[i] == vals[0] for i in range(len(vals))]) and sum(vals) <= 10:
                return True, "combo"
            else:
                return False, "None"

    def validate_defence_hand(self):
        Enemy_atk = EnemyGroup().get_atk()
        if Enemy_atk <= 0:
            return True, 0
        vals = [card.get_val() for card in self.on_select]
        defence = sum(vals)
        return defence >= Enemy_atk, defence


Hand()

if __name__ == "__main__":
    from Card import Card

    h = Hand()
    h.on_select = [Card("♠", "2"), Card("♠", "2")]
    res = h.validate_play_hand()
    print(res)
