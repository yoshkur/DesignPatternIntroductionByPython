from abc import abstractmethod
from sys import argv

from pydantic import BaseModel


class Builder(BaseModel):
    @abstractmethod
    def make_title(self, title: str) -> None:
        pass

    @abstractmethod
    def make_string(self, string: str) -> None:
        pass

    @abstractmethod
    def make_items(self, items: list[str]) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class TextBuilder(Builder):
    sb: str = ''

    def make_title(self, title):
        self.sb += ''.join([
            '==============================\n',
            '『',
            title,
            '』\n\n',
        ])

    def make_string(self, string):
        self.sb += ''.join(['■', string, '\n\n'])

    def make_items(self, items):
        for item in items:
            self.sb += ''.join(['　・', item, '\n'])
        self.sb += '\n'

    def close(self):
        self.sb += '==============================\n'

    def get_text_result(self) -> str:
        return self.sb


class HTMLBuilder(Builder):
    file_name: str = 'untitled.html'
    sb: str = ''

    def make_title(self, title):
        self.file_name = f'{title}.html'
        self.sb += ''.join([
            '<!DOCTYPE html>\n',
            '<html>\n',
            '<head><title>',
            title,
            '</title></head>\n',
            '<body>\n',
            '<h1>',
            title,
            '</h1>\n\n',
        ])

    def make_string(self, string):
        self.sb += ''.join([
            '<p>',
            string,
            '</p>\n\n',
        ])

    def make_items(self, items):
        self.sb += '<ul>\n'
        for item in items:
            self.sb += ''.join([
                '<li>',
                item,
                '</li>\n',
            ])
        self.sb += '</ul>\n\n'

    def close(self):
        self.sb += ''.join(['</body>', '</html>\n'])

        with open(file=self.file_name, mode='w') as fs:
            fs.write(self.sb)

    def get_html_result(self) -> str:
        return self.file_name


class Director(BaseModel):
    builder: Builder

    def construct(self) -> None:
        self.builder.make_title('Greeting')
        self.builder.make_string('一般的な挨拶')
        self.builder.make_items([
            'How are you?',
            'Hello.',
            'Hi.',
        ])
        self.builder.make_string('時間帯に応じた挨拶')
        self.builder.make_items([
            'Good morning.',
            'Good afternoon.',
            'Good evening.',
        ])
        self.builder.close()


def usage() -> None:
    print('Usage: python sample.py text       テキストで文書作成')
    print('Usage: python sample.py html       HTMLファイルで文書作成')


if __name__ == '__main__':
    args = argv
    if len(args) != 2:
        usage()
        exit()

    if args[1] == 'text':
        builder = TextBuilder()
        director = Director(builder=builder)
        director.construct()
        result = builder.get_text_result()
        print(result)
    elif args[1] == 'html':
        builder = HTMLBuilder()
        director = Director(builder=builder)
        director.construct()
        file_name = builder.get_html_result()
        print(f'HTMLファイル{file_name}が作成されました')
    else:
        usage()
        exit()
