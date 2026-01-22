from fastapi import FastAPI, HTTPException
from datetime import datetime
from models import Customer, CustomerCreate, Transaction, Invoice
import zoneinfo

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City", 
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}

app = FastAPI()

@app.get("/")
def root():
    return {"mensaje": "Hola, Mundo"}

@app.get("/horaDia")
def rootHoraDia():
    dataTime = datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    return {"mensaje": dataTime}

@app.get("/time")
async def get_time():
    dataTime = datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    return {"mensaje": dataTime}

@app.get("/time2/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)

    if not timezone_str:
        raise HTTPException(
            status_code=404,
            detail=f"Código ISO {iso_code} no soportado"
        )

    tz = zoneinfo.ZoneInfo(timezone_str)
    formatted_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "iso": iso,
        "timezone": timezone_str,
        "time": formatted_time
    }


@app.get("/timeIso/{iso_code}")
async def get_time_by_iso(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    if not timezone_str:
        raise HTTPException(status_code=404, detail=f"Código ISO {iso_code} no soportado")
    try:
        tz = zoneinfo.ZoneInfo(timezone_str)
        dataTime = datetime.now(tz).strftime("%A, %d. %B %Y %I:%M%p")
        return {"mensaje": dataTime, "status": 201}
    except zoneinfo.ZoneInfoNotFoundError:
        raise HTTPException(status_code=400, detail=f"Zona horaria {timezone_str} no encontrada")

current_id: int = 0
db_customers: list[Customer] = []

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate):
    customer = Customer.model_validate(customer_data.model_dump())
    # Asumiendo que lo hace nen la base de datos 
    customer.id = len(db_customers)
    db_customers.append(customer)
    return customer

@app.get("/customers", response_model=list[Customer])
async def list_customer():
    return db_customers

@app.get("/customersOne/{idCustomer}", response_model=Customer)
async def get_one_customer(idCustomer: int):
    return next((c for c in db_customers if c.id == idCustomer), None)

@app.post("/transactions")
async def create_transactions(transactions_data: Transaction):
    return transactions_data

@app.post("/invoices")
async def create_invoices(invoices_data: Invoice):
    return invoices_data