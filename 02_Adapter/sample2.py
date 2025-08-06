from abc import abstractmethod

from pydantic import BaseModel


class Banner(BaseModel):
    string: str

    def show_with_paren(self) -> None:
        print(f'({self.string})')

    def show_with_aster(self) -> None:
        print(f'*{self.string}*')


class Print(BaseModel):
    @abstractmethod
    def print_weak(self) -> None:
        pass

    @abstractmethod
    def print_strong(self) -> None:
        pass


class PrintBanner(Print):
    banner: Banner

    def print_weak(self) -> None:
        self.banner.show_with_paren()

    def print_strong(self):
        self.banner.show_with_aster()


if __name__ == '__main__':
    banner = Banner(string='Hello')
    printer = PrintBanner(banner=banner)
    printer.print_weak()
    printer.print_strong()
