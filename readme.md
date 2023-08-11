# Regicide(Single ver.)

A simple python implementation using all default libs.

用python默认库实现的单人版弑君者桌游。

## How to play

This is the introduce of the game screen, not rule.

* Top left, Top right are enemy information and deck information.
* Bottom left is hand, each button represent one card. Click button to select the card and click again will unselect it.
* Buttom right is action pannel, selected card will displayed on top of the pannel and once the selected card match the requirement, the button below will become clickable.
  
这部分是操作指南，规则请参考官方。

* 左上，右上分别是敌人信息和卡堆信息。
* 左下是手牌，一个按钮对应一张牌。按下按钮即选择该牌，再次按下取消选择。
* 右下是操作区，所有被选择了的牌会显示在区域上方，当选择的牌满足要求时下方按钮会就会变得可以点击。

## Rule

The single player rule of the official Regicide. If any part of the game not follow the official rule, follow mine：）

即弑君者单人规则，如有不符，我说了算：）

## Start

``` shell
python3 main.py
```

## Special rule

The game is too easy, thus I removed the Joker. Just restart if you don't get Club.

太简单了，我就没放Joker。没有方片就重开哈哈。

## TODO

Add final boss with 60 hp and 40 atk, the color of finall boss will rotate at the end of the turn.

在所有Boss被击败后增加一个60hp, 40atk的final boss。
