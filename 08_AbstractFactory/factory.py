from abc import abstractmethod

from pydantic import BaseModel


class Item(BaseModel):
    caption: str

    @abstractmethod
    def make_html(self) -> str:
        pass


class Link(Item):
    url: str


class Tray(Item):
    tray: list[Item] = []

    def append(self, item: Item) -> None:
        self.tray.append(item)


class Page(BaseModel):
    title: str
    author: str
    content: list[Item] = []

    def append(self, item: Item) -> None:
        self.content.append(item)

    @abstractmethod
    def make_html(self) -> str:
        pass

    def output(self, file_name: str) -> None:
        with open(file=file_name, mode='w') as fs:
            fs.write(self.make_html())
        print(f'{file_name}を作成しました。')


class Factory(BaseModel):
    @abstractmethod
    def create_link(self, caption, url) -> Link:
        pass

    @abstractmethod
    def create_tray(self, caption: str) -> Tray:
        pass

    @abstractmethod
    def create_page(self, title: str, author: str) -> Page:
        pass
