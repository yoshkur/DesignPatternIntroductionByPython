from abc import abstractmethod

from pydantic import BaseModel


class DisplayImpl(BaseModel):
    @abstractmethod
    def raw_open(self) -> None:
        pass

    @abstractmethod
    def raw_print(self) -> None:
        pass

    @abstractmethod
    def raw_close(self) -> None:
        pass


class StringDisplayImpl(DisplayImpl):
    string: str
    width: int = 0

    def model_post_init(self, context):
        self.width = len(self.string)

    def raw_open(self):
        self.print_line()

    def raw_print(self):
        print(f'|{self.string}|')

    def raw_close(self):
        self.print_line()

    def print_line(self) -> None:
        print('+', end='')
        for _ in range(self.width):
            print('-', end='')
        print('+')


class Display(BaseModel):
    impl: DisplayImpl

    def open(self) -> None:
        self.impl.raw_open()

    def print(self) -> None:
        self.impl.raw_print()

    def close(self) -> None:
        self.impl.raw_close()

    def display(self) -> None:
        self.open()
        self.print()
        self.close()


class CountDisplay(Display):

    def multi_display(self, times: int) -> None:
        self.open()
        for _ in range(times):
            self.print()
        self.close()


if __name__ == '__main__':
    d1 = Display(impl=StringDisplayImpl(string='Hello, Japan.'))
    d2 = CountDisplay(impl=StringDisplayImpl(string='Hello, World.'))
    d3 = CountDisplay(impl=StringDisplayImpl(string='Hello, Universe.'))
    d1.display()
    d2.display()
    d3.display()
    d3.multi_display(5)
