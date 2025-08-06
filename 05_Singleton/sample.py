class Singleton():
    _singleton: object = None

    def __new__(cls):
        if cls._singleton:
            cls._singleton = super(Singleton, cls).__new__(cls=cls)
        return cls._singleton


if __name__ == '__main__':
    print('Start.')

    obj1 = Singleton()
    obj2 = Singleton()

    if obj1 is obj2:
        print('obj1とobj2は同じインスタンスです。')
    else:
        print('obj1とobj2は同じインスタンスではありません。')

    print('End.')
