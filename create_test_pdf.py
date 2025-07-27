from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def create_test_pdf():
    # Crear el PDF
    c = canvas.Canvas("test_invoice.pdf", pagesize=letter)
    width, height = letter
    
    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, 10*inch, "FACTURA")
    
    # Información de la empresa
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, 9.5*inch, "Empresa: Tech Solutions Inc.")
    c.drawString(1*inch, 9.2*inch, "Dirección: 123 Business St, Tech City")
    c.drawString(1*inch, 8.9*inch, "Teléfono: (555) 123-4567")
    
    # Información del cliente
    c.drawString(1*inch, 8.3*inch, "Cliente: Acme Corporation")
    c.drawString(1*inch, 8.0*inch, "Dirección: 456 Corporate Ave, Business District")
    
    # Detalles de la factura
    c.drawString(1*inch, 7.3*inch, "Número de Factura: INV-2024-002")
    c.drawString(1*inch, 7.0*inch, "Fecha: 2024-01-20")
    
    # Tabla de productos
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, 6.3*inch, "Descripción")
    c.drawString(4*inch, 6.3*inch, "Cantidad")
    c.drawString(5*inch, 6.3*inch, "Precio Unit.")
    c.drawString(6.5*inch, 6.3*inch, "Total")
    
    c.setFont("Helvetica", 10)
    # Producto 1
    c.drawString(1*inch, 6.0*inch, "Monitor LED 24\"")
    c.drawString(4*inch, 6.0*inch, "3")
    c.drawString(5*inch, 6.0*inch, "$299.99")
    c.drawString(6.5*inch, 6.0*inch, "$899.97")
    
    # Producto 2
    c.drawString(1*inch, 5.7*inch, "Teclado Mecánico")
    c.drawString(4*inch, 5.7*inch, "5")
    c.drawString(5*inch, 5.7*inch, "$89.99")
    c.drawString(6.5*inch, 5.7*inch, "$449.95")
    
    # Producto 3
    c.drawString(1*inch, 5.4*inch, "Mouse Inalámbrico")
    c.drawString(4*inch, 5.4*inch, "10")
    c.drawString(5*inch, 5.4*inch, "$25.00")
    c.drawString(6.5*inch, 5.4*inch, "$250.00")
    
    # Totales
    c.setFont("Helvetica-Bold", 12)
    c.drawString(5*inch, 4.8*inch, "Subtotal:")
    c.drawString(6.5*inch, 4.8*inch, "$1,599.92")
    
    c.drawString(5*inch, 4.5*inch, "IVA (16%):")
    c.drawString(6.5*inch, 4.5*inch, "$255.99")
    
    c.drawString(5*inch, 4.2*inch, "TOTAL:")
    c.drawString(6.5*inch, 4.2*inch, "$1,855.91")
    
    # Información adicional
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, 3.5*inch, "Método de Pago: Tarjeta de Crédito")
    c.drawString(1*inch, 3.2*inch, "Centro de Costos: Departamento de IT")
    c.drawString(1*inch, 2.9*inch, "Moneda: USD")
    
    # Guardar el PDF
    c.save()
    print("PDF de prueba creado: test_invoice.pdf")

if __name__ == "__main__":
    create_test_pdf() 