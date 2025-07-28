import logging
import PyPDF2
import xml.etree.ElementTree as ET
from io import BytesIO
from fastapi import HTTPException, status

# Configuración de logging
logger = logging.getLogger(__name__)

class TextExtractor:
    """Clase para extraer texto de diferentes tipos de archivos."""
    
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """
        Extrae texto de un archivo PDF.
        
        Args:
            file_content (bytes): Contenido del archivo PDF
            
        Returns:
            str: Texto extraído del PDF
            
        Raises:
            HTTPException: Si hay un error al procesar el PDF
        """
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
    
    @staticmethod
    def extract_text_from_xml(file_content: bytes) -> str:
        """
        Extrae texto de un archivo XML.
        
        Args:
            file_content (bytes): Contenido del archivo XML
            
        Returns:
            str: Texto extraído del XML
            
        Raises:
            HTTPException: Si hay un error al procesar el XML
        """
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
                'Tax', 'Amount', 'Description', 'Quantity', 'UnitPrice',
                'Vendor', 'Client', 'Product', 'Service', 'Price'
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
    
    @staticmethod
    def extract_text_by_type(file_content: bytes, content_type: str) -> str:
        """
        Extrae texto según el tipo de contenido del archivo.
        
        Args:
            file_content (bytes): Contenido del archivo
            content_type (str): Tipo MIME del archivo
            
        Returns:
            str: Texto extraído del archivo
            
        Raises:
            HTTPException: Si el tipo de archivo no es soportado
        """
        if content_type == "application/pdf":
            return TextExtractor.extract_text_from_pdf(file_content)
        elif content_type in ["application/xml", "text/xml"]:
            return TextExtractor.extract_text_from_xml(file_content)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de archivo no soportado: {content_type}. Tipos soportados: PDF, XML"
            )

# Instancia global del extractor de texto
text_extractor = TextExtractor()

# Funciones de conveniencia para uso directo
def extract_text_from_pdf(file_content: bytes) -> str:
    """Función de conveniencia para extraer texto de PDF."""
    return TextExtractor.extract_text_from_pdf(file_content)

def extract_text_from_xml(file_content: bytes) -> str:
    """Función de conveniencia para extraer texto de XML."""
    return TextExtractor.extract_text_from_xml(file_content) 