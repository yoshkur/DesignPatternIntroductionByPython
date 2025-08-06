from pydantic import BaseModel


class Book(BaseModel):
    namae: str

    def get_namae(self) -> str:
        return self.namae


if __name__ == '__main__':
    book_shelf = []

    book_shelf.append(Book(namae='Around the World in 80 Days'))
    book_shelf.append(Book(namae='Bible'))
    book_shelf.append(Book(namae='Cinderella'))
    book_shelf.append(Book(namae='Daddy-Long-Legs'))

    for book in book_shelf:
        print(book.get_namae())

    print()
