from abc import abstractmethod

from pydantic import BaseModel


class AbstractDisplay(BaseModel):
    @abstractmethod
    def open(self) -> None:
        pass

    @abstractmethod
    def print(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    def display(self) -> None:
        self.open()
        for _ in range(5):
            self.print()
        self.close()


class CharDisplay(AbstractDisplay):
    char: str

    def open(self):
        print('<<', end='')

    def print(self):
        print(self.char, end='')

    def close(self):
        print('>>')


class StringDisplay(AbstractDisplay):
    string: str
    width: int = 0

    def model_post_init(self, context):
        self.width = len(self.string)

    def print_line(self) -> None:
        print('+', end='')
        for _ in range(self.width):
            print('-', end='')
        print('+')

    def open(self):
        self.print_line()

    def print(self):
        print(f'|{self.string}|')

    def close(self):
        self.print_line()


if __name__ == '__main__':
    d1 = CharDisplay(char='H')

    d2 = StringDisplay(string='Hello, World.')

    d1.display()
    d2.display()
