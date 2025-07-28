import logging
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
# Importar módulos personalizados
from backend.auth import verify_token
from backend.text_extractor import text_extractor
from backend.llm_processor import process_invoice_with_llm, InvoiceData

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Invoice Processing API",
    description="API para procesamiento de facturas con inteligencia artificial",
    version="1.0.0"
)

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
    """Endpoint raíz para verificar que la API está funcionando."""
    return {
        "message": "API de procesamiento de facturas en funcionamiento.",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/protected-route")
async def protected_route(user=Depends(verify_token)):
    """Ruta protegida para verificar autenticación."""
    return {"message": "Acceso concedido a la ruta protegida.", "user": user}

@app.post("/process-invoice", response_model=InvoiceData)
async def process_invoice(
    file: UploadFile = File(...),
    user: dict = Depends(verify_token)
):
    """
    Procesa una factura subida por el usuario.
    
    Args:
        file: Archivo PDF o XML a procesar
        user: Usuario autenticado
        
    Returns:
        InvoiceData: Datos estructurados de la factura
    """
    try:
        # Verificar tipo de archivo
        if file.content_type not in ["application/pdf", "application/xml", "text/xml"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se aceptan archivos PDF o XML. Tipos permitidos: application/pdf, application/xml, text/xml"
            )
        
        # Leer contenido del archivo
        file_content = await file.read()
        
        # Extraer texto usando el módulo text_extractor
        invoice_content = text_extractor.extract_text_by_type(file_content, file.content_type)
        
        logger.info(f"Contenido extraído del archivo {file.filename} ({file.content_type})")
        
        # Procesar con LLM usando el módulo llm_processor
        invoice_data = await process_invoice_with_llm(invoice_content)
        
        # Agregar información del archivo procesado
        invoice_data.file_name = file.filename
        
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

@app.post("/export-invoices")
async def export_invoices(
    invoices: list[InvoiceData],
    format: str = "json",
    user: dict = Depends(verify_token)
):
    """
    Exporta facturas procesadas en diferentes formatos.
    
    Args:
        invoices: Lista de facturas a exportar
        format: Formato de exportación (json, csv)
        user: Usuario autenticado
        
    Returns:
        Archivo exportado en el formato solicitado
    """
    try:
        if format.lower() == "json":
            # Exportar como JSON
            from fastapi.responses import JSONResponse
            return JSONResponse(
                content={
                    "invoices": [invoice.dict() for invoice in invoices],
                    "exported_by": user.get("uid"),
                    "export_date": "2024-01-01",
                    "total_invoices": len(invoices)
                },
                media_type="application/json"
            )
        
        elif format.lower() == "csv":
            # Exportar como CSV
            import csv
            from io import StringIO
            from fastapi.responses import Response
            
            output = StringIO()
            writer = csv.writer(output)
            
            # Headers
            writer.writerow([
                "Invoice Type", "Cost Center", "Payment Method", 
                "Total Amount", "Currency", "Invoice Date", 
                "Supplier Name", "File Name"
            ])
            
            # Data
            for invoice in invoices:
                writer.writerow([
                    invoice.invoice_type,
                    invoice.cost_center,
                    invoice.payment_method,
                    invoice.total_amount,
                    invoice.currency,
                    invoice.invoice_date,
                    invoice.supplier_name,
                    invoice.file_name
                ])
            
            csv_content = output.getvalue()
            return Response(
                content=csv_content,
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=invoices.csv"}
            )
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato no soportado. Formatos disponibles: json, csv"
            )
            
    except Exception as e:
        logger.error(f"Error al exportar facturas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al exportar facturas: {str(e)}"
        ) 