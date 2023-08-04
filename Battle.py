from Hand import Hand
from Deck import Deck
from JQK import EnemyGroup


@staticmethod
def battle():
    if Hand().on_select == []:
        return 0
    vals = [card.get_val() for card in Hand().on_select]
    colors = [card.get_color() for card in Hand().on_select]
    atk_val = sum(vals)
    if "♠" in colors and not EnemyGroup().check_cls("♠"):
        EnemyGroup().down_atk(atk_val)
    if "♥" in colors and not EnemyGroup().check_cls("♥"):
        Deck().heart_event(atk_val)
    if "♣" in colors and not EnemyGroup().check_cls("♣"):
        atk_val *= 2
    if "♦" in colors and not EnemyGroup().check_cls("♦"):
        Hand().draw(atk_val)
    return atk_val


@staticmethod
def defence():
    Enemy_atk = EnemyGroup().get_atk()
    return Enemy_atk


if __name__ == "__main__":
    print(battle())
