from fastapi import Depends, FastAPI, HTTPException, Request, status
from datetime import datetime
from models import Transaction, Invoice
from .routers import customers, transactions, plans
import zoneinfo
from db import create_all_tables
import time
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City", 
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}



app = FastAPI(lifespan=create_all_tables)

app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)

@app.middleware("http")
async def log_request_time(request: Request, call_next) :
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.url} completed in: {process_time:.4f} seconds")
    return response

security = HTTPBasic()

@app.get("/")
async def root(credentials: Annotated [HTTPBasicCredentials ,Depends
(security)]):
    if credentials.username == "lcmartinez" and credentials.password == "qwerty":
        return {"message": f"Hola, {credentials.username}!"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.get("/horaDia")
def rootHoraDia():
    dataTime = datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    return {"mensaje": dataTime}

@app.get("/time")
async def get_time():
    dataTime = datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    return {"mensaje": dataTime}

@app.get("/time2/{iso_code}")
async def time_ISO(iso_code: str):
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


@app.post("/invoices")
async def create_invoices(invoices_data: Invoice):
    return invoices_data