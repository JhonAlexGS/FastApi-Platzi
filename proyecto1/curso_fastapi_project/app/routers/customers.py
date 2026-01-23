from models import Customer, CustomerCreate, CustomerUpdate
from db import SessionDep
from sqlmodel import select
from fastapi import APIRouter, status, HTTPException

router = APIRouter()

current_id: int = 0
db_customers: list[Customer] = []

# @app.post("/customers", response_model=Customer)
# async def create_customer(customer_data: CustomerCreate, session: SessionDep):
#     customer = Customer.model_validate(customer_data.model_dump())
#     # Asumiendo que lo hace nen la base de datos 
#     customer.id = len(db_customers)
#     db_customers.append(customer)
    # return customer
@router.post("/customers", response_model=Customer, tags=["customers"])
async def create_customer(customer_data: CustomerCreate, session: SessionDep) :
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session. commit ( )
    session. refresh(customer)
    return customer

@router.get("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def read_customer(customer_id: int, session: SessionDep) :
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exists")
    return customer_db

@router.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=["customers"])
async def read_customer2(customer_id: int, customer_data: CustomerUpdate,session: SessionDep) :
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exists")
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session. commit ( )
    session. refresh(customer_db)
    customer_db.sqlmodel_update()
    return customer_db

@router.delete("/customers/{customer_id}", tags=["customers"])
async def read_customer(customer_id: int, session: SessionDep) :
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exists")
    session.delete(customer_db)
    session.commit()
    return {"detail":"ok"}

#endpoint para actualizar un cliente
@router.put("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def update_customer(customer_id: int, customer_data: CustomerCreate, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer does not exist")
    customer_db.name = customer_data.name
    customer_db.description = customer_data.description
    customer_db.email = customer_data.email
    customer_db.age = customer_data.age
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

@router.get("/customers", response_model=list [Customer], tags=["customers"] )
async def list_customer(session: SessionDep) :
    return session.exec(select (Customer) ).all()

@router.get("/customersOne/{idCustomer}", response_model=Customer, tags=["customers"])
async def get_one_customer(idCustomer: int):
    return next((c for c in db_customers if c.id == idCustomer), None)