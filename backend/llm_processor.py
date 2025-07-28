import os
import logging
from typing import List, Literal
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Configuración de logging
logger = logging.getLogger(__name__)

# Validar OPENAI_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.warning("La variable de entorno OPENAI_API_KEY no está definida.")

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
    file_name: str = ""  # Campo opcional para el nombre del archivo

class LLMProcessor:
    """Clase para manejar el procesamiento de facturas con LLM."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            temperature=0,
            model="gpt-3.5-turbo"
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
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
    
    async def process_invoice(self, invoice_content: str) -> InvoiceData:
        """
        Procesa el contenido de una factura usando el LLM.
        
        Args:
            invoice_content (str): Contenido extraído de la factura
            
        Returns:
            InvoiceData: Datos estructurados de la factura
            
        Raises:
            Exception: Si hay un error en el procesamiento
        """
        try:
            # Limitar el contenido para evitar exceder el contexto
            # GPT-3.5-turbo tiene un límite de ~16k tokens, reservamos espacio para el prompt
            max_chars = 12000  # Aproximadamente 3000 tokens
            if len(invoice_content) > max_chars:
                logger.warning(f"Contenido demasiado largo ({len(invoice_content)} chars), truncando a {max_chars} chars")
                invoice_content = invoice_content[:max_chars] + "\n\n[CONTENIDO TRUNCADO...]"
            
            # Usar el método correcto para la versión de LangChain
            chain = self.prompt | self.llm
            result = await chain.ainvoke({"invoice_content": invoice_content})
            
            # Parsear manualmente el resultado
            try:
                # Intentar extraer JSON del resultado
                import json
                import re
                
                # Buscar JSON en la respuesta
                json_match = re.search(r'\{.*\}', result.content, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    parsed_data = json.loads(json_str)
                    
                    # Crear InvoiceData con los datos parseados
                    invoice_data = InvoiceData(
                        invoice_type=parsed_data.get('invoice_type', 'gasto'),
                        cost_center=parsed_data.get('cost_center', 'N/A'),
                        payment_method=parsed_data.get('payment_method', 'unknown'),
                        extracted_items=parsed_data.get('extracted_items', []),
                        total_amount=float(parsed_data.get('total_amount', 0)),
                        currency=parsed_data.get('currency', 'USD'),
                        invoice_date=parsed_data.get('invoice_date', '2024-01-01'),
                        supplier_name=parsed_data.get('supplier_name', 'N/A'),
                        file_name=""
                    )
                else:
                    # Si no se encuentra JSON, crear datos por defecto
                    invoice_data = InvoiceData(
                        invoice_type='gasto',
                        cost_center='N/A',
                        payment_method='unknown',
                        extracted_items=[],
                        total_amount=0.0,
                        currency='USD',
                        invoice_date='2024-01-01',
                        supplier_name='N/A',
                        file_name=""
                    )
                
                logger.info("Factura procesada exitosamente con LLM")
                return invoice_data
                
            except Exception as parse_error:
                logger.error(f"Error al parsear respuesta del LLM: {parse_error}")
                # Retornar datos por defecto en caso de error
                return InvoiceData(
                    invoice_type='gasto',
                    cost_center='N/A',
                    payment_method='unknown',
                    extracted_items=[],
                    total_amount=0.0,
                    currency='USD',
                    invoice_date='2024-01-01',
                    supplier_name='N/A',
                    file_name=""
                )
                
        except Exception as e:
            logger.error(f"Error al procesar la factura con LLM: {e}")
            raise
    
    def validate_invoice_data(self, data: InvoiceData) -> bool:
        """
        Valida que los datos de la factura sean correctos.
        
        Args:
            data (InvoiceData): Datos de la factura a validar
            
        Returns:
            bool: True si los datos son válidos
        """
        try:
            # Validar que el tipo de factura sea válido
            valid_types = ["purchase", "sale", "return", "compra", "gasto"]
            if data.invoice_type not in valid_types:
                logger.warning(f"Tipo de factura inválido: {data.invoice_type}")
                return False
            
            # Validar que el monto total sea positivo
            if data.total_amount <= 0:
                logger.warning(f"Monto total inválido: {data.total_amount}")
                return False
            
            # Validar que la fecha tenga el formato correcto
            if not data.invoice_date or len(data.invoice_date) != 10:
                logger.warning(f"Formato de fecha inválido: {data.invoice_date}")
                return False
            
            # Validar que el proveedor tenga un nombre
            if not data.supplier_name or data.supplier_name.strip() == "":
                logger.warning("Nombre del proveedor vacío")
                return False
            
            logger.info("Datos de factura validados correctamente")
            return True
            
        except Exception as e:
            logger.error(f"Error al validar datos de factura: {e}")
            return False

# Instancia global del procesador LLM (lazy initialization)
_llm_processor = None

def get_llm_processor():
    """Obtiene la instancia global del procesador LLM con inicialización lazy."""
    global _llm_processor
    if _llm_processor is None:
        _llm_processor = LLMProcessor()
    return _llm_processor

# Función de conveniencia para uso directo
async def process_invoice_with_llm(invoice_content: str) -> InvoiceData:
    """
    Función de conveniencia para procesar facturas con LLM.
    
    Args:
        invoice_content (str): Contenido extraído de la factura
        
    Returns:
        InvoiceData: Datos estructurados de la factura
    """
    processor = get_llm_processor()
    return await processor.process_invoice(invoice_content) 