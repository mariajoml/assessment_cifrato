import os
import logging
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import credentials, initialize_app, auth as firebase_auth
from firebase_admin.auth import InvalidIdTokenError
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Firebase Admin SDK
firebase_initialized = False
try:
    service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
    if not service_account_path:
        raise ValueError("FIREBASE_SERVICE_ACCOUNT_PATH no está definida en el entorno.")
    cred = credentials.Certificate(service_account_path)
    initialize_app(cred)
    firebase_initialized = True
    logger.info("Firebase Admin SDK inicializado correctamente.")
except Exception as e:
    logger.error(f"Error al inicializar Firebase Admin SDK: {e}")
    raise SystemExit(f"No se pudo inicializar Firebase Admin SDK: {e}")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API de procesamiento de facturas en funcionamiento."}

# Dependencia para verificar el token de Firebase
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        logger.info(f"Token verificado para UID: {decoded_token.get('uid')}")
        return decoded_token
    except InvalidIdTokenError as e:
        logger.error(f"Token inválido o expirado: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado."
        )
    except Exception as e:
        logger.error(f"Error al verificar el token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo verificar el token de autenticación."
        )

# Endpoint protegido
@app.get("/protected-route")
async def protected_route(user=Depends(verify_token)):
    return {"message": "Acceso concedido a la ruta protegida.", "user": user} 