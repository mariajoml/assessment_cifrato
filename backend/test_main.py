import pytest
import json
import sys
import os
from unittest.mock import Mock, patch, AsyncMock

# Agregar el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.llm_processor import InvoiceData
from backend.text_extractor import TextExtractor

class TestInvoiceData:
    """Tests para el modelo InvoiceData."""
    
    def test_invoice_data_creation(self):
        """Test de creación de InvoiceData."""
        invoice = InvoiceData(
            invoice_type="gasto",
            cost_center="Marketing",
            payment_method="credit_card",
            extracted_items=["Servicio 1", "Servicio 2"],
            total_amount=1500.00,
            currency="USD",
            invoice_date="2024-01-15",
            supplier_name="Proveedor Test",
            file_name="test-invoice.pdf"
        )
        
        assert invoice.invoice_type == "gasto"
        assert invoice.cost_center == "Marketing"
        assert invoice.total_amount == 1500.00
        assert invoice.supplier_name == "Proveedor Test"
        assert len(invoice.extracted_items) == 2
    
    def test_invoice_data_validation(self):
        """Test de validación de InvoiceData."""
        # Test con datos válidos
        invoice = InvoiceData(
            invoice_type="purchase",
            cost_center="IT",
            payment_method="bank_transfer",
            extracted_items=[],
            total_amount=100.0,
            currency="EUR",
            invoice_date="2024-01-01",
            supplier_name="Test Supplier"
        )
        
        assert invoice.invoice_type in ["purchase", "sale", "return", "compra", "gasto"]
        assert invoice.total_amount > 0
        assert len(invoice.invoice_date) == 10  # YYYY-MM-DD format

class TestTextExtractor:
    """Tests para el extractor de texto."""
    
    def test_extract_text_from_xml(self):
        """Test de extracción de texto de XML."""
        extractor = TextExtractor()
        
        xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
        <Invoice>
            <InvoiceNumber>INV-001</InvoiceNumber>
            <Total>1000.00</Total>
            <Supplier>Test Supplier</Supplier>
        </Invoice>"""
        
        result = extractor.extract_text_from_xml(xml_content)
        assert "InvoiceNumber: INV-001" in result
        assert "Total: 1000.00" in result
        assert "Supplier: Test Supplier" in result
    
    def test_extract_text_by_type_xml(self):
        """Test de extracción por tipo XML."""
        extractor = TextExtractor()
        
        xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
        <Invoice>
            <InvoiceNumber>INV-002</InvoiceNumber>
            <Total>500.00</Total>
        </Invoice>"""
        
        result = extractor.extract_text_by_type(xml_content, "application/xml")
        assert "InvoiceNumber: INV-002" in result
        assert "Total: 500.00" in result
    
    def test_extract_text_by_type_invalid(self):
        """Test de extracción con tipo inválido."""
        extractor = TextExtractor()
        
        with pytest.raises(Exception):
            extractor.extract_text_by_type(b"content", "text/plain")

class TestLLMProcessor:
    """Tests para el procesador LLM."""
    
    @patch('backend.llm_processor.ChatOpenAI')
    @patch('backend.llm_processor.ChatPromptTemplate')
    def test_llm_processor_initialization(self, mock_prompt_template, mock_chat_openai):
        """Test de inicialización del LLMProcessor."""
        from backend.llm_processor import LLMProcessor
        processor = LLMProcessor()
        
        assert processor.llm is not None
        assert processor.prompt is not None
    
    @patch('backend.llm_processor.ChatOpenAI')
    @patch('backend.llm_processor.ChatPromptTemplate')
    def test_validate_invoice_data_valid(self, mock_prompt_template, mock_chat_openai):
        """Test de validación de datos válidos."""
        from backend.llm_processor import LLMProcessor
        processor = LLMProcessor()
        
        invoice = InvoiceData(
            invoice_type="gasto",
            cost_center="IT",
            payment_method="card",
            extracted_items=["item1"],
            total_amount=500.0,
            currency="USD",
            invoice_date="2024-01-01",
            supplier_name="Test Supplier"
        )
        
        assert processor.validate_invoice_data(invoice) == True
    
    @patch('backend.llm_processor.ChatOpenAI')
    @patch('backend.llm_processor.ChatPromptTemplate')
    def test_validate_invoice_data_invalid_type(self, mock_prompt_template, mock_chat_openai):
        """Test de validación con tipo inválido."""
        from backend.llm_processor import LLMProcessor
        processor = LLMProcessor()
        
        # Test que Pydantic valida correctamente tipos inválidos
        with pytest.raises(Exception):
            invoice = InvoiceData(
                invoice_type="invalid_type",  # Tipo inválido
                cost_center="IT",
                payment_method="card",
                extracted_items=["item1"],
                total_amount=500.0,
                currency="USD",
                invoice_date="2024-01-01",
                supplier_name="Test Supplier"
            )
    
    @patch('backend.llm_processor.ChatOpenAI')
    @patch('backend.llm_processor.ChatPromptTemplate')
    def test_validate_invoice_data_invalid_amount(self, mock_prompt_template, mock_chat_openai):
        """Test de validación con monto inválido."""
        from backend.llm_processor import LLMProcessor
        processor = LLMProcessor()
        
        invoice = InvoiceData(
            invoice_type="gasto",
            cost_center="IT",
            payment_method="card",
            extracted_items=["item1"],
            total_amount=-100.0,  # Monto negativo
            currency="USD",
            invoice_date="2024-01-01",
            supplier_name="Test Supplier"
        )
        
        assert processor.validate_invoice_data(invoice) == False

class TestInvoiceDataValidation:
    """Tests adicionales para validación de InvoiceData."""
    
    def test_invoice_data_required_fields(self):
        """Test de campos requeridos en InvoiceData."""
        # Test que todos los campos requeridos estén presentes
        invoice = InvoiceData(
            invoice_type="gasto",
            cost_center="IT",
            payment_method="card",
            extracted_items=[],
            total_amount=100.0,
            currency="USD",
            invoice_date="2024-01-01",
            supplier_name="Test Supplier"
        )
        
        # Verificar que todos los campos están presentes
        assert hasattr(invoice, 'invoice_type')
        assert hasattr(invoice, 'cost_center')
        assert hasattr(invoice, 'payment_method')
        assert hasattr(invoice, 'extracted_items')
        assert hasattr(invoice, 'total_amount')
        assert hasattr(invoice, 'currency')
        assert hasattr(invoice, 'invoice_date')
        assert hasattr(invoice, 'supplier_name')
        assert hasattr(invoice, 'file_name')
    
    def test_invoice_data_default_values(self):
        """Test de valores por defecto en InvoiceData."""
        invoice = InvoiceData(
            invoice_type="gasto",
            cost_center="IT",
            payment_method="card",
            extracted_items=[],
            total_amount=100.0,
            currency="USD",
            invoice_date="2024-01-01",
            supplier_name="Test Supplier"
        )
        
        # Verificar valor por defecto de file_name
        assert invoice.file_name == ""

class TestFileProcessing:
    """Tests para el procesamiento de archivos reales."""
    
    def test_extract_text_from_real_xml_file(self):
        """Test de extracción de texto de archivo XML real."""
        extractor = TextExtractor()
        
        # Leer el archivo XML de prueba
        with open('test_invoice.xml', 'rb') as f:
            xml_content = f.read()
        
        result = extractor.extract_text_from_xml(xml_content)
        
        # Verificar que se extrajo información clave
        assert "INV-TEST-001" in result
        assert "2750.00" in result
        assert "Web Development Services" in result
        assert "Consulting Services" in result
    
    def test_extract_text_by_type_real_xml(self):
        """Test de extracción por tipo con archivo XML real."""
        extractor = TextExtractor()
        
        # Leer el archivo XML de prueba
        with open('test_invoice.xml', 'rb') as f:
            xml_content = f.read()
        
        result = extractor.extract_text_by_type(xml_content, "application/xml")
        
        # Verificar que se extrajo información clave
        assert "INV-TEST-001" in result
        assert "2750.00" in result
        assert "Web Development Services" in result
    
    def test_extract_text_from_real_pdf_file(self):
        """Test de extracción de texto de archivo PDF real."""
        extractor = TextExtractor()
        
        # Leer el archivo PDF de prueba
        with open('test_invoice.pdf', 'rb') as f:
            pdf_content = f.read()
        
        result = extractor.extract_text_from_pdf(pdf_content)
        
        # Verificar que se extrajo información clave
        # El PDF de prueba es muy simple, solo verificamos que se procesó
        assert len(result) > 0
        assert "Página" in result

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 