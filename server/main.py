from typing import List
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from . import crud, database, models, schemas
from .database import db_state_default
import os

ROUTE_USER_PREFIX = os.getenv('CA_SERVER_ROUTE_USER_PREFIX', "/appusers")
ROUTE_CERTIFICATE_PREFIX = os.getenv('CA_SERVER_ROUTE_CERTIFICATE_PREFIX', "/certificates")

database.db.connect()
database.db.create_tables(models.MODELS)
database.db.close()

app = FastAPI()

sleep_time = 10


async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()

app_user_router = APIRouter(prefix=ROUTE_USER_PREFIX)

@app_user_router.post("/", response_model=schemas.AppUser, dependencies=[Depends(get_db)])
def create_app_user(req: schemas.AppUserCreate):
    db_user = crud.get_app_user(user=req.user)
    if db_user:
        raise HTTPException(status_code=400, detail="App User already registered")
    return crud.create_app_user(req=req)


@app_user_router.get("/", response_model=List[schemas.AppUser], dependencies=[Depends(get_db)])
def read_app_users():
    users = crud.get_app_users()
    return users


@app_user_router.get("/{user}", response_model=schemas.AppUser, dependencies=[Depends(get_db)])
def read_app_user(user: str):
    db_user = crud.get_app_user(user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="App User not found")
    return db_user


@app_user_router.delete("/{user}", response_model=int, dependencies=[Depends(get_db)])
def delete_app_user(user: str):
    n = crud.delete_app_user(user=user)
    if n is None:
        raise HTTPException(status_code=404, detail="Couldn't delete User")
    return n


# Certificates
cert_router = APIRouter(prefix=ROUTE_CERTIFICATE_PREFIX)
@cert_router.post("/", response_model=schemas.Certificate, dependencies=[Depends(get_db)])
def create_certificate(req: schemas.CertificateCreate):
    if req.user == None:
        raise HTTPException(status_code=400, detail="user not supplied")
    elif crud.get_app_user(user=req.user) is None:
        raise HTTPException(status_code=404, detail="App User not found")
    elif req.installationId == '1':
        raise HTTPException(status_code=500, detail= "Cannot post a certificate with this installationId")
    elif req.installationId == None:
        raise HTTPException(status_code=500, detail="installationId not supplied")
    elif req.csr == None:
        raise HTTPException(status_code=500, detail="csr not supplied")

    cert = crud.get_certificate(req.installationId)
    if cert:
        raise HTTPException(status_code=400, detail="InstallationId already registered")
    return crud.create_certificate(req)

@cert_router.get("/", response_model=List[schemas.Certificate], dependencies=[Depends(get_db)])
def get_certificates():
    certs = crud.get_certificates()
    return certs

@cert_router.get("/{installationId}", response_model=schemas.Certificate, dependencies=[Depends(get_db)])
def get_certificate(installationId: str):
    cert = crud.get_certificate(installation_id=installationId)
    if cert is None:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return cert


@cert_router.put("/", response_model=schemas.Certificate, dependencies=[Depends(get_db)])
def update_certificate(req: schemas.CertificateUpdate):
    if req.installationId == '1':
        raise HTTPException(status_code=500, detail= "Cannot post a certificate with this installationId")
    elif req.installationId == None:
        raise HTTPException(status_code=500, detail="installationId not supplied")
    elif req.csr == None:
        raise HTTPException(status_code=500, detail="csr not supplied")

    cert = crud.update_certificate(req)
    if cert is None:
        raise HTTPException(status_code=400, detail="InstallationId already registered")

    return cert

@cert_router.delete("/{installationId}", response_model=int, dependencies=[Depends(get_db)])
def delete_certificate(installationId: str):
    if installationId == '1':
        raise HTTPException(status_code=500, detail="Cannot post a certificate with this installationId")
    elif installationId == None:
        raise HTTPException(status_code=500, detail="installationId not supplied")

    n = crud.delete_certificate(installation_id = installationId)
    if n is None:
        raise HTTPException(status_code=404, detail="Couldn't delete Certificiate")
    return n

@app.get("/ca_certificate", response_model=str)
def get_ca_certificate():
    return crud.get_ca_certificate()

@app.get("/", response_model=str)
def get_home_page():
    return 'Server is Running...'

@app.get("/health")
def get_server_health():
    return "Healthy: OK"

app.include_router(app_user_router)
app.include_router(cert_router)