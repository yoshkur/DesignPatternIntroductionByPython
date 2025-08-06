from copy import deepcopy
import random
from time import sleep

from pydantic import BaseModel


class Mement(BaseModel):
    money: int
    fruits: list = []

    def append_fruit(self, fruit: str) -> None:
        self.fruits.append(fruit)

    def get_money(self) -> int:
        return self.money

    def get_fruits(self) -> list:
        return deepcopy(self.fruits)


class Gamer():
    FRUITS_NAME: list = ['リンゴ', 'ぶどう', 'バナナ', 'みかん',]

    def __init__(self, money: int):
        self.money = money
        self.fruits: list = []
        self.random_generator = random

    def get_money(self) -> int:
        return self.money

    def get_fruit(self) -> str:
        fruit = self.FRUITS_NAME[self.random_generator.randint(1, len(self.FRUITS_NAME) - 1)]
        if self.random_generator.choice([True, False]):
            return f'おいしい{fruit}'
        else:
            return fruit

    def bet(self) -> None:
        dice = self.random_generator.randint(1, 6)
        if dice == 1:
            self.money += 100
            print('所持金が増えました。')
        elif dice == 2:
            self.money //= 2
            print('所持金が半分になりました。')
        elif dice == 6:
            fruit = self.get_fruit()
            print(f'フルーツ({fruit})をもらいました。')
            self.fruits.append(fruit)
        else:
            print('何も起こりませんでした。')

    def create_mement(self) -> Mement:
        mement = Mement(money=self.money)
        for fruit in self.fruits:
            if fruit.startswith('おいしい'):
                mement.append_fruit(fruit)
        return mement

    def restore_mement(self, mement: Mement) -> None:
        self.money = mement.get_money()
        self.fruits = mement.get_fruits()

    def __repr__(self):
        return f'[money = {self.money}, fruits = {self.fruits}]'


if __name__ == '__main__':
    gamer = Gamer(money=100)
    mement = gamer.create_mement()

    for i in range(100):
        print(f'===={i}')
        print(f'現状:{gamer}')

        gamer.bet()
        print(f'所持金は{gamer.get_money()}円になりました。')

        if gamer.get_money() > mement.get_money():
            print('※だいぶ増えたので、現在の状態を保存しておこう！')
            mement = gamer.create_mement()
        elif gamer.get_money() < mement.get_money() / 2:
            print('※だいぶ減ったので、以前の状態を復元しよう！')
            gamer.restore_mement(mement=mement)

        sleep(1)
        print()
