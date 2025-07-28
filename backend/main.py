import os
import sys
import logging
from typing import List, Literal
from fastapi import FastAPI, Depends, HTTPException, status, Request, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from firebase_admin import credentials, initialize_app, auth as firebase_auth
from firebase_admin.auth import InvalidIdTokenError
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import openai
import PyPDF2
import xml.etree.ElementTree as ET
from io import BytesIO

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

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# --- Funciones de extracción de contenido ---
def extract_text_from_pdf(file_content: bytes) -> str:
    """Extrae texto de un archivo PDF."""
    try:
        logger.info("Procesando archivo PDF...")
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
        text_content = ""
        
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            text_content += f"\n--- Página {page_num + 1} ---\n{page_text}"
        
        logger.info(f"Texto extraído de {len(pdf_reader.pages)} páginas del PDF")
        return text_content
    except Exception as e:
        logger.error(f"Error al procesar PDF: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al procesar el archivo PDF: {str(e)}"
        )

def extract_text_from_xml(file_content: bytes) -> str:
    """Extrae texto de un archivo XML."""
    try:
        logger.info("Procesando archivo XML...")
        xml_content = file_content.decode('utf-8')
        root = ET.fromstring(xml_content)
        
        # Intentar extraer elementos clave del XML
        extracted_text = ""
        
        # Buscar elementos comunes en facturas XML
        key_elements = [
            'Invoice', 'Factura', 'InvoiceNumber', 'InvoiceDate', 'Total',
            'Supplier', 'Customer', 'Items', 'Conceptos', 'SubTotal',
            'Tax', 'Amount', 'Description', 'Quantity', 'UnitPrice'
        ]
        
        for element in key_elements:
            for elem in root.findall(f'.//{element}'):
                if elem.text and elem.text.strip():
                    extracted_text += f"{element}: {elem.text.strip()}\n"
        
        # Si no se encontraron elementos específicos, extraer todo el texto
        if not extracted_text.strip():
            logger.info("No se encontraron elementos específicos, extrayendo todo el texto del XML")
            for elem in root.iter():
                if elem.text and elem.text.strip():
                    extracted_text += f"{elem.tag}: {elem.text.strip()}\n"
        
        logger.info("Texto extraído del XML exitosamente")
        return extracted_text if extracted_text.strip() else xml_content
    except ET.ParseError as e:
        logger.error(f"Error al parsear XML: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al parsear el archivo XML: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error al procesar XML: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al procesar el archivo XML: {str(e)}"
        )

# --- LLM Processing Function ---
async def process_invoice_with_llm(invoice_content: str) -> InvoiceData:
    try:
        # Limitar el contenido para evitar exceder el contexto
        # GPT-3.5-turbo tiene un límite de ~16k tokens, reservamos espacio para el prompt
        max_chars = 12000  # Aproximadamente 3000 tokens
        if len(invoice_content) > max_chars:
            logger.warning(f"Contenido demasiado largo ({len(invoice_content)} chars), truncando a {max_chars} chars")
            invoice_content = invoice_content[:max_chars] + "\n\n[CONTENIDO TRUNCADO...]"
        
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
    except Exception as e:
        logger.error(f"Error al procesar la factura: {e}")
        raise

# --- Endpoint actualizado para procesamiento de archivos ---
@app.post("/process-invoice", response_model=InvoiceData)
async def process_invoice(
    file: UploadFile = File(...),
    user: dict = Depends(verify_token)
):
    try:
        # Verificar tipo de archivo
        if file.content_type not in ["application/pdf", "application/xml", "text/xml"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se aceptan archivos PDF o XML. Tipos permitidos: application/pdf, application/xml, text/xml"
            )
        
        # Leer contenido del archivo
        file_content = await file.read()
        
        # Extraer texto según el tipo de archivo
        if file.content_type == "application/pdf":
            invoice_content = extract_text_from_pdf(file_content)
        else:  # XML
            invoice_content = extract_text_from_xml(file_content)
        
        logger.info(f"Contenido extraído del archivo {file.filename} ({file.content_type})")
        
        # Procesar con LLM
        invoice_data = await process_invoice_with_llm(invoice_content)
        return invoice_data
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la factura: {str(e)}"
        ) 