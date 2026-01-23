from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from models import Transaction, TransactionCreate, Customer
from db import SessionDep

router = APIRouter()

@router.post("/transactions", tags =["transaction"])
async def create_transation(transaction_data: TransactionCreate, session: SessionDep) :

    transaction_data_dict = transaction_data.model_dump() 
    customer = session.get(Customer, transaction_data_dict.get('customer_id'))

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't Exists")
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)

    return transaction_db
 
@router.get("/transactions", tags =["transaction"])
async def list_transaction(session: SessionDep):
    query = select(Transaction)
    transactions = session.exec(query).all()
    return transactions