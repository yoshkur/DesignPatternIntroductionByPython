from abc import abstractmethod
from copy import deepcopy

from pydantic import BaseModel


class Product(BaseModel):
    @abstractmethod
    def use(self, string: str) -> None:
        pass

    @abstractmethod
    def create_copy(self):
        pass

    def clone(self):
        return deepcopy(self)


class Manager(BaseModel):
    showcase: dict = {}

    def register(self, namae: str, prototype: Product) -> None:
        self.showcase[namae] = prototype

    def create(self, prototype_namae: str):
        product: Product = self.showcase.get(prototype_namae)
        return product.create_copy()
