from framework import Manager, Product


class UnderlinePen(Product):
    ulchar: str

    def use(self, string):
        ulen = len(string)
        print(string)
        for _ in range(ulen):
            print(self.ulchar, end='')
        print()

    def create_copy(self):
        product = None
        try:
            product = self.clone()
        except Exception as e:
            print(str(e))
        return product


class MessageBox(Product):
    decochar: str

    def use(self, string):
        decolen = 1 + len(string) + 1
        for _ in range(decolen):
            print(self.decochar, end='')
        print()
        print(f'{self.decochar}{string}{self.decochar}')
        for _ in range(decolen):
            print(self.decochar, end='')
        print()

    def create_copy(self):
        product = None
        try:
            product = self.clone()
        except Exception as e:
            print(str(e))
        return product


if __name__ == '__main__':
    manager = Manager()

    upen = UnderlinePen(ulchar='-')
    mbox = MessageBox(decochar='*')
    sbox = MessageBox(decochar='/')

    manager.register('strong message', upen)
    manager.register('warning box', mbox)
    manager.register('slash box', sbox)

    p1: Product = manager.create('strong message')
    p1.use('Hello, world.')

    p2: Product = manager.create('warning box')
    p2.use('Hello, world.')

    p3: Product = manager.create('slash box')
    p3.use('Hello, world.')
