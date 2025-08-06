from abc import abstractmethod
from time import sleep


class Observer():
    @abstractmethod
    def update(self, generator) -> None:
        pass


class DigitObserver(Observer):
    def update(self, generator):
        print(f'DigitObserver:{generator.get_number()}')
        sleep(0.1)


class GraphObserver(Observer):
    def update(self, generator):
        print('GraphObserver:', end='')
        for _ in range(generator.get_number()):
            print('*', end='')
        print()
        sleep(0.1)


class NumberGenerator():
    def __init__(self):
        self.observers = []

    def append_observer(self, observer: Observer) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        self.observers.remove(observer)

    def notify_observers(self) -> None:
        for observer in self.observers:
            observer.update(self)

    @abstractmethod
    def get_number(self) -> int:
        pass

    @abstractmethod
    def execute(self) -> None:
        pass


class RandomNumberGenerator(NumberGenerator):
    def __init__(self):
        import random

        super().__init__()
        self.random_generator = random
        self.number = self.random_generator.randint(0, 50)

    def get_number(self):
        return self.number

    def execute(self):
        for _ in range(20):
            self.number = self.random_generator.randint(0, 50)
            self.notify_observers()


if __name__ == '__main__':
    generator = RandomNumberGenerator()
    observer1 = DigitObserver()
    observer2 = GraphObserver()
    generator.append_observer(observer=observer1)
    generator.append_observer(observer=observer2)
    generator.execute()
