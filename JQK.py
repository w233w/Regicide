import random
from Utils import Singleton


class Enemy:
    def __init__(self, cls, level) -> None:
        self.cls = cls
        self.level = level
        level_map = {"J": 1, "Q": 2, "K": 3}
        self.jokerd = False
        self.atk = level_map[self.level] * 5 + 5
        self.hp = level_map[self.level] * 10 + 10
        self.temp_atk_down = 0

    def __repr__(self) -> str:
        return f"<Enemy {self.cls}{self.level} Hp:{self.hp} ATK:{self.atk-self.temp_atk_down}>"

    def check_cls(self, cls):
        return self.cls == cls

    def down_atk(self, val):
        self.temp_atk_down += val

    def turn_end(self):
        self.temp_atk_down = 0

    def get_info(self):
        return self.cls, self.level

    # first return is alive, second is royal kill or not
    # still alive will return royal kill False anyway.
    def royal_kill(self):
        if self.hp > 0:
            return True, False
        elif self.hp == 0:
            return False, True
        elif self.hp < 0:
            return False, False

    def on_hit(self, val):
        self.hp -= val
        return self.royal_kill()


@Singleton
class EnemyGroup:
    def __init__(self):
        self.group = []
        self.init_group()
        self.current = self.group.pop()

    def init_group(self):
        self.group = []
        color = ["♥", "♠", "♦", "♣"]
        value = ["K", "Q", "J"]
        for v in value:
            random.shuffle(color)
            for c in color:
                self.group.append(Enemy(c, v))

    def restart(self):
        self.__init__()

    def remains(self):
        return len(self.group)

    def on_hit(self, val):
        return self.current.on_hit(val)

    def check_cls(self, cls):
        if self.current.jokerd:
            return False
        return self.current.check_cls(cls)

    def down_atk(self, val):
        self.current.down_atk(val)

    def get_current_info(self):
        return self.current.get_info()

    def get_atk(self):
        return self.current.atk - self.current.temp_atk_down

    def next_enemy(self):
        if self.remains() > 0:
            self.current = self.group.pop()
        else:
            self.current = "You Win!!\nPlease press restart to start a new Game."

    def end_turn(self):
        self.current.turn_end()


EnemyGroup()

if __name__ == "__main__":
    eg = EnemyGroup()
    print(eg.group)
