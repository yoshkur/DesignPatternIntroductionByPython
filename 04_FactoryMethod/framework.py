from abc import abstractmethod

from pydantic import BaseModel


class Product(BaseModel):
    @abstractmethod
    def use(self) -> None:
        pass


class Factory(BaseModel):
    def create(self, owner: str) -> Product:
        product = self.create_product(owner=owner)
        self.register_product(product=product)
        return product

    @abstractmethod
    def create_product(self, owner: str) -> Product:
        pass

    @abstractmethod
    def register_product(self, product: Product) -> None:
        pass
