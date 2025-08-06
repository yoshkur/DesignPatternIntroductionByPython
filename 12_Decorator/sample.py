from abc import abstractmethod

from pydantic import BaseModel


class Display(BaseModel):
    @abstractmethod
    def get_columns(self) -> int:
        pass

    @abstractmethod
    def get_rows(self) -> int:
        pass

    @abstractmethod
    def get_row_text(self, row: int) -> str:
        pass

    def show(self) -> None:
        for i in range(self.get_rows()):
            print(self.get_row_text(row=i))


class StringDisplay(Display):
    string: str

    def get_columns(self):
        return len(self.string)

    def get_rows(self):
        return 1

    def get_row_text(self, row):
        if row != 0:
            raise IndexError
        return self.string


class Border(Display):
    display: Display


class FullBorder(Border):
    def get_columns(self):
        return 1 + self.display.get_columns() + 1

    def get_rows(self):
        return 1 + self.display.get_rows() + 1

    def get_row_text(self, row):
        if row == 0:
            return f'+{self.make_line(ch='-', count=self.display.get_columns())}+'
        elif row == self.display.get_rows() + 1:
            return f'+{self.make_line(ch='-', count=self.display.get_columns())}+'
        else:
            return f'|{self.display.get_row_text(row=row - 1)}|'

    def make_line(self, ch: str, count: int) -> str:
        line = [ch] * count
        return ''.join(line)


class SideBorder(Border):
    border_char: str

    def get_columns(self):
        return 1 + self.display.get_columns() + 1

    def get_rows(self):
        return self.display.get_rows()

    def get_row_text(self, row):
        return f'{self.border_char}{self.display.get_row_text(row)}{self.border_char}'


if __name__ == '__main__':
    b1 = StringDisplay(string='Hello, world.')
    b2 = SideBorder(display=b1, border_char='#')
    b3 = FullBorder(display=b2)

    b1.show()
    b2.show()
    b3.show()

    b4 = SideBorder(
        display=FullBorder(
            display=FullBorder(
                display=SideBorder(
                    display=FullBorder(
                        display=StringDisplay(string='Good morning, space.')
                    ),
                    border_char='*',
                )
            )
        ),
        border_char='/'
    )
    b4.show()
