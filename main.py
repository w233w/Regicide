import tkinter as tk
from Deck import Deck
from Hand import Hand
from JQK import EnemyGroup
from math import ceil
from itertools import product
import Battle

HEIGHT, WIDTH = 360, 480
MAX_CARD_COL, MAX_CARD_ROW = 8, 7


class UI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("test")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(width=False, height=False)
        self.root.configure(background="#d3d3d3")

        # 菜单
        self.menubar = tk.Menu(self.root)
        self.menu_start = tk.Menu(self.menubar, tearoff=0)
        self.menu_start.add_command(label="Restart", command=self.restart_event)
        self.menu_start.add_separator()
        self.menu_start.add_command(label="Exit", command=self.root.destroy)
        self.menubar.add_cascade(label="Game", menu=self.menu_start)

        self.root.config(menu=self.menubar)

        # Config
        self.state = "Play"  # ['Play', 'Defence']
        self.button_valid = {True: tk.ACTIVE, False: tk.DISABLED}

        self.draw()

    def draw(self):
        # 左上JQK相关
        self.top_left = tk.Frame(self.root, bd=2, relief=tk.GROOVE)
        self.top_left.place(relx=0, rely=0, relheight=0.6, relwidth=0.7)

        self.enemy_label_text = tk.StringVar()
        self.enemy_label_text.set(EnemyGroup().current)
        self.enemy_label = tk.Label(self.top_left, textvariable=self.enemy_label_text)
        self.enemy_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # 右上Deck相关
        self.top_right = tk.Frame(self.root, bd=2, relief=tk.GROOVE)
        self.top_right.place(relx=0.7, rely=0, relheight=0.6, relwidth=0.3)

        self.deck_info = tk.Label(self.top_right, text=Deck())
        self.deck_info.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # 左下Hand相关
        self.buttom_left = tk.Frame(self.root, bd=2, relief=tk.GROOVE)
        self.buttom_left.place(relx=0, rely=0.6, relheight=0.4, relwidth=0.7)

        self.button_texts = [
            [tk.StringVar() for i in range(MAX_CARD_COL)] for j in range(MAX_CARD_ROW)
        ]
        self.button_group = [
            [
                tk.Button(self.buttom_left, textvariable=self.button_texts[j][i])
                for i in range(MAX_CARD_COL)
            ]
            for j in range(MAX_CARD_ROW)
        ]

        self._replace_buttons()

        # 右下Play相关
        self.buttom_right = tk.Frame(self.root, bd=2, relief=tk.GROOVE)
        self.buttom_right.place(relx=0.7, rely=0.6, relheight=0.4, relwidth=0.3)

        self.action_label_text = tk.StringVar()
        self.action_label_text.set("[]\nNone")
        self.play_label = tk.Label(
            self.buttom_right, textvariable=self.action_label_text
        )
        self.play_label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

        self.play_button = tk.Button(
            self.buttom_right,
            text="Play",
            state=tk.DISABLED,
            command=self.play_event,
        )
        self.play_button.place(
            relx=0.5, rely=0.5, relheight=0.4, relwidth=0.8, anchor=tk.N
        )

        self.defence_button = tk.Button(
            self.buttom_right,
            text="Defence",
            state=tk.DISABLED,
            command=self.defence_event,
        )

    def restart_event(self):
        Deck().restart()
        Hand().restart()
        EnemyGroup().restart()

        self.enemy_label_text.set(EnemyGroup().current)
        self.deck_info.config(text=Deck())
        self._replace_buttons()
        self.select_event()

    def play_event(self):
        dmg = Battle.battle()
        alive, royal = EnemyGroup().on_hit(dmg)
        if not alive:
            if royal:
                color, value = EnemyGroup().get_current_info()
                Deck().new_member_event(color, value)
            EnemyGroup().next_enemy()
        Hand().play()

        self._replace_buttons()
        
        if EnemyGroup().remains() == 0:
            self.play_button.config(state=tk.DISABLED)
            self.action_label_text.set("You Win!")

        elif alive:
            self.action_label_text.set("[]\n0")
            self.play_button.place_forget()
            self.play_button.config(state=tk.DISABLED)
            self.defence_button.place(
                relx=0.5, rely=0.5, relheight=0.4, relwidth=0.8, anchor=tk.N
            )
            self.state = "Defence"

            atk = EnemyGroup().get_atk()
            if atk <= 0:
                self.defence_button.config(state=tk.ACTIVE)

        self.deck_info.config(text=Deck())
        self.enemy_label_text.set(EnemyGroup().current)

    def defence_event(self):
        EnemyGroup().end_turn()
        Hand().play()

        self._replace_buttons()
        self.action_label_text.set("[]\n0")
        self.defence_button.place_forget()
        self.defence_button.config(state=tk.DISABLED)
        self.play_button.place(
            relx=0.5, rely=0.5, relheight=0.4, relwidth=0.8, anchor=tk.N
        )
        self.deck_info.config(text=Deck())
        self.enemy_label_text.set(EnemyGroup().current)
        self.state = "Play"

    def surrender_event(self):
        self.restart_event()

    def _replace_buttons(self):
        for i, j in product(range(MAX_CARD_ROW), range(MAX_CARD_COL)):
            self.button_group[i][j].place_forget()
        for i in range(Hand().size()):
            self.button_texts[i // 8][i % 8].set(Hand().hand[i])
            self.button_group[i // 8][i % 8].config(
                command=lambda card=Hand().hand[i]: [
                    Hand().select_handler(card),
                    self.select_event(),
                ]
            )
            self.button_group[i // 8][i % 8].place(
                relx=(i % 8) / 8,
                rely=(i // 8) / ceil(Hand().size() / 8),
                relheight=1 / ceil(Hand().size() / 8),
                relwidth=1 / 8,
            )

    def select_event(self):
        if self.state == "Play":
            hand_validation, play_type = Hand().validate_play_hand()
            self.play_button.config(state=self.button_valid[hand_validation])
            self.action_label_text.set(f"{Hand().on_select}\n{play_type}")
        if self.state == "Defence":
            hand_validation, sum_up = Hand().validate_defence_hand()
            self.defence_button.config(state=self.button_valid[hand_validation])
            self.action_label_text.set(f"{Hand().on_select}\n{sum_up}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    UI().run()
