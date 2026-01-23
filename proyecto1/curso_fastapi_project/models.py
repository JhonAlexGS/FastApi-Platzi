from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: str = Field(default=None)
    age: int = Field(default=None)

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: int | None = Field(default= None, primary_key=True)

class CustomerUpdate(CustomerBase):
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
