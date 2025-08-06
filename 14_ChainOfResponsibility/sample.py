from abc import abstractmethod

from pydantic import BaseModel


class Trouble(BaseModel):
    number: int

    def get_number(self) -> int:
        return self.number

    def __repr__(self):
        return f'[Trouble {self.number}]'


class Support():
    def __init__(self, name):
        self.name = name
        self.next_support = None

    def set_next_support(self, next_support):
        self.next_support = next_support
        return next_support

    def support(self, trouble: Trouble) -> None:
        if self.resolve(trouble=trouble):
            self.done(trouble=trouble)
        elif self.next_support:
            self.next_support.support(trouble)
        else:
            self.fail(trouble=trouble)

    def __repr__(self):
        return f'[{self.name}]'

    @abstractmethod
    def resolve(self, trouble: Trouble) -> bool:
        pass

    def done(self, trouble: Trouble) -> None:
        print(f'{trouble} is resolved by {self}.')

    def fail(self, trouble: Trouble) -> None:
        print(f'{trouble} cannot be resolved.')


class NoSupport(Support):
    def resolve(self, trouble):
        return False


class LimitSupport(Support):
    def __init__(self, name, limit):
        super().__init__(name)
        self.limit = limit

    def resolve(self, trouble):
        if trouble.get_number() < self.limit:
            return True
        else:
            return False


class OddSupport(Support):
    def resolve(self, trouble):
        if trouble.get_number() % 2 == 1:
            return True
        else:
            return False


class SpecialSupport(Support):
    def __init__(self, name, number):
        super().__init__(name)
        self.number = number

    def resolve(self, trouble):
        if trouble.get_number() == self.number:
            return True
        else:
            return False


if __name__ == '__main__':
    alice = NoSupport(name='Alice')
    bob = LimitSupport("Bob", 100)
    charlie = SpecialSupport("Charlie", 429)
    diana = LimitSupport("Diana", 200)
    elmo = OddSupport("Elmo")
    fred = LimitSupport("Fred", 300)

    # 連鎖の形成
    alice.set_next_support(bob).set_next_support(charlie).set_next_support(diana).set_next_support(elmo).set_next_support(fred)

    for i in range(0, 500, 33):
        alice.support(trouble=Trouble(number=i))
