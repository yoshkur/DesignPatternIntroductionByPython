from abc import ABC, abstractmethod
from enum import Enum
from random import randint


class HandValue(Enum):
    ROCK: int = 0
    SCISSORS: int = 1
    PAPER: int = 2


class Hand():
    hands: list = []

    def __init__(self, hand_value: int):
        self.hand_value = hand_value

    @classmethod
    def get_hand(cls, hand_value: int):
        return cls.hands[hand_value]

    def is_stronger_than(self, h):
        return self.fight(h=h) == 1

    def is_weaker_than(self, h):
        return self.fight(h=h) == -1

    def fight(self, h) -> int:
        if self.hand_value == h.hand_value:
            return 0
        elif (self.hand_value.value + 1) % 3 == h.hand_value.value:
            return 1
        else:
            return -1


Hand.hands.append(Hand(hand_value=HandValue.ROCK))
Hand.hands.append(Hand(hand_value=HandValue.SCISSORS))
Hand.hands.append(Hand(hand_value=HandValue.PAPER))


class Strategy(ABC):
    @abstractmethod
    def next_hand(self) -> Hand:
        pass

    @abstractmethod
    def study(self, win: bool) -> None:
        pass


class Player():
    name: str
    strategy: Strategy
    win_count: int = 0
    lose_count: int = 0
    game_count: int = 0

    def __init__(self, name: str, strategy: Strategy):
        self.name = name
        self.strategy = strategy

    def next_hand(self) -> Hand:
        return self.strategy.next_hand()

    def win(self) -> None:
        self.strategy.study(win=True)
        self.win_count += 1
        self.game_count += 1

    def lose(self) -> None:
        self.strategy.study(win=False)
        self.lose_count += 1
        self.game_count += 1

    def even(self) -> None:
        self.game_count += 1

    def __repr__(self):
        return f'[{self.name}: {self.game_count} games, {self.win_count} win, {self.lose_count} lose]'


class ProbStrategy(Strategy):
    prev_hand_value: Hand = Hand.get_hand(hand_value=0)
    current_hand_value: Hand = Hand.get_hand(hand_value=0)
    history: list = [[1] * 3] * 3

    def next_hand(self):
        bet = randint(0, self._get_sum(self.current_hand_value.hand_value.value))
        hand_value = 0
        if bet < self.history[self.current_hand_value.hand_value.value][0]:
            hand_value = 0
        elif bet < self.history[self.current_hand_value.hand_value.value][0] + self.history[self.current_hand_value.hand_value.value][1]:
            hand_value = 1
        else:
            hand_value = 2
        self.prev_hand_value = self.current_hand_value
        self.current_hand_value = Hand.get_hand(hand_value)
        return Hand.get_hand(hand_value=hand_value)

    def _get_sum(self, hand_value: int) -> int:
        sum_ = 0
        for i in range(3):
            sum_ += self.history[hand_value][i]
        return sum_

    def study(self, win):
        if win:
            self.history[self.prev_hand_value.hand_value.value][self.current_hand_value.hand_value.value] += 1
        else:
            self.history[self.prev_hand_value.hand_value.value][(self.current_hand_value.hand_value.value + 1) % 3] += 1
            self.history[self.prev_hand_value.hand_value.value][(self.current_hand_value.hand_value.value + 2) % 3] += 1


class WinningStrategy(Strategy):
    won: bool = False
    prev_hand: Hand = Hand.get_hand(hand_value=0)

    def next_hand(self):
        if not self.won:
            self.prev_hand = Hand.get_hand(hand_value=randint(0, 2))
        return self.prev_hand

    def study(self, win):
        self.won = win


if __name__ == '__main__':
    player1 = Player(name='Taro', strategy=WinningStrategy())
    player2 = Player(name='Hana', strategy=ProbStrategy())

    for _ in range(10000):
        next_hand1 = player1.next_hand()
        next_hand2 = player2.next_hand()

        if next_hand1.is_stronger_than(next_hand2):
            print(f'Winner:{player1}')
            player1.win()
            player2.lose()
        elif next_hand2.is_stronger_than(next_hand1):
            print(f'Winner:{player2}')
            player1.lose()
            player2.win()
        else:
            print('Even...')
            player1.even()
            player2.even()

    print('Total result:')
    print(player1)
    print(player2)
