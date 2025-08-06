from abc import abstractmethod
from time import sleep

from pydantic import BaseModel


class Printable():
    @abstractmethod
    def set_printer_name(self, name: str) -> None:
        pass

    @abstractmethod
    def get_printer_name(self) -> str:
        pass

    @abstractmethod
    def print(self, string: str) -> None:
        pass


class Printer(Printable, BaseModel):
    name: str = ''

    def model_post_init(self, context):
        msg = 'Printerのインスタンスを生成中'
        if self.name:
            msg = f'Printerのインスタンス({self.name})を生成中'
        self.heavy_job(msg=msg)

    def set_printer_name(self, name):
        self.name = name

    def get_printer_name(self):
        return self.name

    def print(self, string):
        print(f'==={self.name}===')
        print(string)

    def heavy_job(self, msg: str) -> None:
        print(msg, end='')
        for _ in range(5):
            sleep(1)
            print('.', end='')
        print('完了。')


class PrinterProxy(Printable, BaseModel):
    name: str = 'No Name'
    real: Printer = None

    def set_printer_name(self, name):
        if self.real:
            self.real.set_printer_name(name=name)
        self.name = name

    def get_printer_name(self):
        return self.name

    def print(self, string):
        self.realize()
        self.real.print(string=string)

    def realize(self) -> None:
        if self.real is None:
            self.real = Printer(name=self.name)


if __name__ == '__main__':
    p = PrinterProxy(name='Alice')
    print(f'名前は現在{p.get_printer_name()}です。')
    p.set_printer_name(name='Bob')
    print(f'名前は現在{p.get_printer_name()}です。')
    p.print(string='Hello, world.')
