from pydantic import BaseModel


class BigChar(BaseModel):
    char_name: str
    font_data: str = ''

    def model_post_init(self, context):
        file_name = f'20_Flyweight/big{self.char_name}.txt'
        try:
            with open(file=file_name, mode='r') as fs:
                self.font_data = '\n'.join(fs.readlines())
        except:
            self.font_data = f'{self.char_name}?'

    def print(self) -> None:
        print(self.font_data, end='')


class BigCharFactory():
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_singleton'):
            cls._singleton = super(BigCharFactory, cls).__new__(cls, *args, **kwargs)
        return cls._singleton

    def __init__(self):
        self.pool = {}

    @classmethod
    def get_instance(cls):
        return BigCharFactory()._singleton

    def get_big_char(self, char_name: str) -> BigChar:
        bc = self.pool.get(char_name)
        if not bc:
            bc = BigChar(char_name=char_name)
            self.pool[char_name] = bc
        return bc


class BigString(BaseModel):
    base_string: str

    _big_chars: list[BigChar]

    def model_post_init(self, context):
        factory = BigCharFactory.get_instance()
        self._big_chars = []
        for ch in self.base_string:
            self._big_chars.append(
                factory.get_big_char(char_name=ch)
            )

    def print(self) -> None:
        for bc in self._big_chars:
            bc.print()


if __name__ == '__main__':
    bs = BigString(base_string='12345')
    bs.print()
