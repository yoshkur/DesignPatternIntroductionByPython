import os

from pydantic import BaseModel


class Database(BaseModel):
    @classmethod
    def get_properties(cls, db_name: str) -> dict:
        data_dir = os.path.dirname(__file__)
        file_name = os.path.join(data_dir, f'{db_name}.txt')
        prop = {}
        with open(file=file_name, mode='r') as fs:
            for line in fs.readlines():
                key, value = line.split('=')
                prop[key] = value.removesuffix('\n')
        return prop


class HtmlWriter():
    def __init__(self, writer):
        self.writer = writer

    def title(self, title: str) -> None:
        self.writer.write('<!DOCTYPE html>')
        self.writer.write('<html>')
        self.writer.write('<head>')
        self.writer.write(f'<title>{title}</title>')
        self.writer.write('</head>')
        self.writer.write('<body>')
        self.writer.write('\n')
        self.writer.write(f'<h1>{title}</h1>')
        self.writer.write('\n')

    def paragraph(self, msg: str) -> None:
        self.writer.write(f'<p>{msg}</p>')
        self.writer.write('\n')

    def link(self, href: str, caption: str) -> None:
        self.paragraph(msg=f'<a href="{href}">{caption}</a>')

    def mailto(self, mail_address: str, user_name: str) -> None:
        self.link(href=f'mailto:{mail_address}', caption=user_name)

    def close(self) -> None:
        self.writer.write('</body>')
        self.writer.write('</html>')
        self.writer.write('\n')
        self.writer.close()


class PageMaker(BaseModel):
    @classmethod
    def make_welcome_page(cls, mail_address: str, file_name: str) -> None:
        try:
            mail_prop = Database.get_properties(db_name='maildata')
            user_name = mail_prop.get(mail_address)
            fs = open(file=file_name, mode='w', encoding='utf-8')
            writer = HtmlWriter(writer=fs)
            writer.title(title=f'{user_name}\'s web page!')
            writer.paragraph(msg=f'Welcom to {user_name}\'s web page!')
            writer.paragraph(msg='Nice to meet you!')
            writer.mailto(mail_address=mail_address, user_name=user_name)
            writer.close()
            print(f'{file_name} is created for {mail_address}({user_name})')
        except FileNotFoundError as e:
            print(str(e))
