from framework import Factory, Product


class IDCard(Product):
    owner: str

    def model_post_init(self, context):
        print(f'{self.owner}のカードを作ります。')

    def to_string(self) -> str:
        return f'[IDCard:{self.owner}]'

    def use(self):
        print(f'{self.to_string()}を使います。')


class IDCardFactory(Factory):
    def create_product(self, owner):
        return IDCard(owner=owner)

    def register_product(self, product):
        print(f'{product}を登録しました。')
