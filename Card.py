class Card:
    def __init__(self, color, value) -> None:
        self.color = color
        self.value = value
        self.color_map = {"♠": 4, "♥": 3, "♣": 2, "♦": 1}
        self.value_map = {
            "A": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
        }

    def __str__(self) -> str:
        return f"{self.color}{self.value}"

    def __int__(self) -> int:
        return self.value_map[self.value]

    def __repr__(self) -> str:
        return self.__str__()

    def __lt__(self, other) -> bool:
        if other.__class__ != self.__class__:
            return False
        else:
            if self.value == other.value:
                return self.color_map[self.color] < self.color_map[other.color]
            else:
                return self.value_map[self.value] < self.value_map[other.value]

    def is_a(self):
        return self.value == "A"

    def get_color(self):
        return self.color

    def check_color(self, color):
        return self.color == color

    def get_val(self):
        return self.__int__()


if __name__ == "__main__":
    c1, c2, c3 = Card("♠", "8"), Card("♠", "5"), Card("♥", "4")
    ls = [c1, c2, c3]
    ls.sort()
    print(ls)
