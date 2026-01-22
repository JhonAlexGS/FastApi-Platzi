from pydantic import BaseModel

class CustomerBase(BaseModel):
    name: str
    description: str | None
    email: str
    age: int

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int | None = None

class CustomerCreate(CustomerBase):
    id: int | None = None 
    pass

class Transaction(BaseModel):
    id :int
    ammount: int
    description: str

class Invoice(BaseModel):
    
    id: int
    customer: CustomerBase
    transaction: list[Transaction]
    total: int

    @property 
    # El decorador @property en Python convierte un método de 
    # una clase en una propiedad de solo lectura que se accede 
    # como si fuera un atributo, sin necesidad de llamarlo con 
    # paréntesis.
    def ammount_total(self):
        return sum(transaction.ammount for transaction in  self.transaction);
