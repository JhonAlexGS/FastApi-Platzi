from pydantic import BaseModel

class Customer(BaseModel):
    id: int
    name: str
    description: str | None
    email: str
    age: int

class Transaction(BaseModel):
    id :int
    ammount: int

class Invoice(BaseModel):
    
    id: int
    customar: Customer
    transaction: list[Transaction]
    total: int

    @property 
    # El decorador @property en Python convierte un método de 
    # una clase en una propiedad de solo lectura que se accede 
    # como si fuera un atributo, sin necesidad de llamarlo con 
    # paréntesis.
    def ammount_total(self):
        return sum(transaction.ammount for transaction in  self.transaction);
