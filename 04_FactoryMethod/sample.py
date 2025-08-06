from idcard import IDCardFactory


if __name__ == '__main__':
    factory = IDCardFactory()
    card1 = factory.create('Hiroshi Yuki')
    card2 = factory.create('Tomura')
    card3 = factory.create('Hanako Sato')

    card1.use()
    card2.use()
    card3.use()
