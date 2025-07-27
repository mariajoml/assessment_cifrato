import os
import sys
import logging
from typing import List, Literal
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from firebase_admin import credentials, initialize_app, auth as firebase_auth
from firebase_admin.auth import InvalidIdTokenError
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import openai

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Validar OPENAI_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.warning("La variable de entorno OPENAI_API_KEY no está definida.")

# Validar FIREBASE_SERVICE_ACCOUNT_PATH
FIREBASE_SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
if not FIREBASE_SERVICE_ACCOUNT_PATH:
    logging.critical("La variable de entorno FIREBASE_SERVICE_ACCOUNT_PATH no está definida.")
    raise ValueError("FIREBASE_SERVICE_ACCOUNT_PATH no está definida en el entorno.")

# Inicializar Firebase Admin SDK
try:
    cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_PATH)
    initialize_app(cred)
    logger.info("Firebase Admin SDK inicializado correctamente.")
except Exception as e:
    logger.critical(f"Error al inicializar Firebase Admin SDK: {e}")
    raise ValueError(f"No se pudo inicializar Firebase Admin SDK: {e}")

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

@app.get("/protected-route")
async def protected_route(user=Depends(verify_token)):
    return {"message": "Acceso concedido a la ruta protegida.", "user": user}

# --- Pydantic Schema para la salida del LLM ---
class InvoiceData(BaseModel):
    invoice_type: Literal["purchase", "sale", "return", "compra", "gasto"]
    cost_center: str
    payment_method: str
    extracted_items: List[str]
    total_amount: float
    currency: str
    invoice_date: str  # YYYY-MM-DD
    supplier_name: str

# --- LLM Processing Function ---
async def process_invoice_with_llm(invoice_content: str) -> InvoiceData:
    try:
        # Inicializar el modelo LLM
        llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            temperature=0,
            model="gpt-3.5-turbo"
        )

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "Eres un experto en procesamiento de facturas. Extrae la información estructurada de la siguiente factura. "
                "Asegúrate de que 'invoice_type' sea uno de: purchase, sale, return, compra, gasto. "
                "Si no puedes determinar el tipo, usa 'gasto'. "
                "Si no puedes inferir 'cost_center' o 'payment_method', usa 'N/A' o 'unknown'. "
                "Asegúrate de que 'invoice_date' esté en formato YYYY-MM-DD. "
                "Extrae todos los campos definidos en el esquema."
            ),
            ("user", "{invoice_content}")
        ])

        # Usar with_structured_output directamente
        chain = prompt | llm.with_structured_output(InvoiceData)
        result = await chain.ainvoke({"invoice_content": invoice_content})
        return result
    except openai.error.OpenAIError as e:
        logger.error(f"Error de OpenAI al procesar la factura: {e}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado al procesar la factura: {e}")
        raise

# --- Nuevo endpoint para procesamiento de facturas ---
from fastapi import Body

@app.post("/process-invoice", response_model=InvoiceData)
async def process_invoice(
    invoice_content: str = Body(..., embed=True),
    user: dict = Depends(verify_token)
):
    try:
        invoice_data = await process_invoice_with_llm(invoice_content)
        return invoice_data
    except openai.error.OpenAIError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la factura con LLM: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {e}"
        ) 