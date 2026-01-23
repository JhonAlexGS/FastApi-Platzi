from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship


class CustomerPlan(SQLModel, table=True):
    id: int = Field(primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer: int = Field(foreign_key="customer.id")

class Plan(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str = Field(default=None)
    price : int = Field(default=None)
    description: str = Field(default=None)
    customers: list["Customer"] = Relationship(
        back_populates = "plans", link_model=CustomerPlan
    )
class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: str = Field(default=None)
    age: int = Field(default=None)

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: int | None = Field(default= None, primary_key=True)
    transactions: list["Transaction"]= Relationship(back_populates="customer")
    plans:list[Plan] = Relationship(
        back_populates="customer", link_model= CustomerPlan
    )

class CustomerUpdate(CustomerBase):
    pass

class TransactionBase(SQLModel):
    ammount: int
    description: str

class Transaction(TransactionBase, table=True) :
    id: int | None = Field(default=None,primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")

class TransactionCreate(TransactionBase) :
    customer_id: int = Field(foreign_key="customer.id")

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
