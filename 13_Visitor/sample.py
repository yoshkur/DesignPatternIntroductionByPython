from abc import abstractmethod

from pydantic import BaseModel


class Element(BaseModel):
    @abstractmethod
    def accept(self, v):
        pass


class Entry(Element):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass

    def __repr__(self):
        return f'{self.get_name()} ({self.get_size()})'


class Directory(Entry):
    name: str
    directory: list[Entry] = []

    def get_name(self):
        return self.name

    def get_size(self):
        size = 0
        for entry in self.directory:
            size += entry.get_size()
        return size

    def append(self, entry: Entry) -> Entry:
        self.directory.append(entry)
        return self

    def iterator(self):
        return iter(self.directory)

    def __iter__(self):
        return self.iterator()

    def accept(self, v):
        v.visit(directory=self)


class File(Entry):
    name: str
    size: int

    def get_name(self):
        return self.name

    def get_size(self):
        return self.size

    def accept(self, v):
        return v.visit(file=self)


class Visitor(BaseModel):
    @abstractmethod
    def visit(self, file: File = None, directory: Directory = None):
        pass


class ListVisitor(Visitor):
    currentdir: str = ''

    def visit(self, file=None, directory=None):
        if file:
            print(f'{self.currentdir}/{file}')

        if directory:
            print(f'{self.currentdir}/{directory}')
            savedir = self.currentdir
            self.currentdir += f'/{directory.get_name()}'
            for entry in directory:
                entry.accept(self)

            self.currentdir = savedir


if __name__ == '__main__':
    print('Making root entries...')
    rootdir = Directory(name='root')
    bindir = Directory(name='bin')
    tmpdir = Directory(name='tmp')
    usrdir = Directory(name='usr')
    rootdir.append(bindir)
    rootdir.append(tmpdir)
    rootdir.append(usrdir)
    bindir.append(File(name='vi', size=10000))
    bindir.append(File(name='latex', size=20000))
    rootdir.accept(ListVisitor())
    print()

    print('Making user entries...')
    yuki = Directory(name='yuki')
    hanako = Directory(name='hanako')
    tomura = Directory(name='tomura')
    usrdir.append(yuki)
    usrdir.append(hanako)
    usrdir.append(tomura)
    yuki.append(File(name='diary.html', size=100))
    yuki.append(File(name='Composite.java', size=200))
    hanako.append(File(name='memo.tex', size=300))
    tomura.append(File(name='game.doc', size=400))
    tomura.append(File(name='junk.mail', size=500))
    rootdir.accept(ListVisitor())
