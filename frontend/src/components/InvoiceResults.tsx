import React from 'react';

interface InvoiceData {
  invoice_type?: string;
  cost_center?: string;
  payment_method?: string;
  extracted_items?: string[];
  total_amount?: number;
  currency?: string;
  invoice_date?: string;
  supplier_name?: string;
  // Campos adicionales que podrían venir del backend
  invoice_number?: string;
  vendor_address?: string;
  customer_name?: string;
  customer_address?: string;
  items?: Array<{
    description?: string;
    quantity?: string;
    unit_price?: string;
    total?: string;
  }>;
  tax_amount?: string;
  subtotal?: string;
  payment_terms?: string;
  due_date?: string;
}

interface InvoiceResultsProps {
  data: InvoiceData;
  fileName: string;
  onClose: () => void;
}

export function InvoiceResults({ data, fileName, onClose }: InvoiceResultsProps) {
  const formatCurrency = (amount: string, currency: string = 'USD') => {
    if (!amount) return 'N/A';
    const num = parseFloat(amount);
    if (isNaN(num)) return amount;
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: currency || 'USD'
    }).format(num);
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return 'N/A';
    try {
      return new Date(dateString).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    } catch {
      return dateString;
    }
  };

  return (
    <div className="invoice-results">
      <div className="results-header">
        <div className="results-title">
          <h3>📄 Datos Extraídos</h3>
          <p className="file-name">{fileName}</p>
        </div>
        <button onClick={onClose} className="close-button">
          ✕
        </button>
      </div>

      <div className="results-content">
        {/* Basic Information */}
        <div className="results-section">
          <h4>📋 Información Básica</h4>
          <div className="info-grid">
            <div className="info-item">
              <span className="info-label">Tipo de Factura:</span>
              <span className="info-value">{data.invoice_type || 'N/A'}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Fecha:</span>
              <span className="info-value">{formatDate(data.invoice_date || '')}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Total:</span>
              <span className="info-value total-amount">
                {formatCurrency(String(data.total_amount || ''), data.currency)}
              </span>
            </div>
            <div className="info-item">
              <span className="info-label">Moneda:</span>
              <span className="info-value">{data.currency || 'N/A'}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Centro de Costos:</span>
              <span className="info-value">{data.cost_center || 'N/A'}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Método de Pago:</span>
              <span className="info-value">{data.payment_method || 'N/A'}</span>
            </div>
          </div>
        </div>

        {/* Supplier Information */}
        <div className="results-section">
          <h4>🏢 Información del Proveedor</h4>
          <div className="info-grid">
            <div className="info-item">
              <span className="info-label">Nombre:</span>
              <span className="info-value">{data.supplier_name || 'N/A'}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Dirección:</span>
              <span className="info-value">{data.vendor_address || 'N/A'}</span>
            </div>
          </div>
        </div>

        {/* Customer Information */}
        <div className="results-section">
          <h4>👤 Información del Cliente</h4>
          <div className="info-grid">
            <div className="info-item">
              <span className="info-label">Nombre:</span>
              <span className="info-value">{data.customer_name || 'N/A'}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Dirección:</span>
              <span className="info-value">{data.customer_address || 'N/A'}</span>
            </div>
          </div>
        </div>

        {/* Extracted Items */}
        {data.extracted_items && data.extracted_items.length > 0 && (
          <div className="results-section">
            <h4>📦 Artículos Extraídos</h4>
            <div className="extracted-items">
              {data.extracted_items.map((item, index) => (
                <div key={index} className="extracted-item">
                  <span className="item-icon">📄</span>
                  <span className="item-text">{item}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Items */}
        {data.items && data.items.length > 0 && (
          <div className="results-section">
            <h4>📦 Artículos Detallados</h4>
            <div className="items-table">
              <div className="table-header">
                <span>Descripción</span>
                <span>Cantidad</span>
                <span>Precio Unit.</span>
                <span>Total</span>
              </div>
              {data.items.map((item, index) => (
                <div key={index} className="table-row">
                  <span>{item.description || 'N/A'}</span>
                  <span>{item.quantity || 'N/A'}</span>
                  <span>{formatCurrency(item.unit_price || '', data.currency)}</span>
                  <span>{formatCurrency(item.total || '', data.currency)}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Totals */}
        <div className="results-section">
          <h4>💰 Totales</h4>
          <div className="totals-grid">
            <div className="total-item">
              <span className="total-label">Subtotal:</span>
              <span className="total-value">{formatCurrency(data.subtotal || '', data.currency)}</span>
            </div>
            <div className="total-item">
              <span className="total-label">Impuestos:</span>
              <span className="total-value">{formatCurrency(data.tax_amount || '', data.currency)}</span>
            </div>
            <div className="total-item total-final">
              <span className="total-label">Total:</span>
              <span className="total-value">{formatCurrency(String(data.total_amount || ''), data.currency)}</span>
            </div>
          </div>
        </div>

        {/* Payment Information */}
        <div className="results-section">
          <h4>💳 Información de Pago</h4>
          <div className="info-grid">
            <div className="info-item">
              <span className="info-label">Términos de Pago:</span>
              <span className="info-value">{data.payment_terms || 'N/A'}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Fecha de Vencimiento:</span>
              <span className="info-value">{formatDate(data.due_date || '')}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="results-actions">
        <button className="action-button secondary" onClick={onClose}>
          Cerrar
        </button>
        <button className="action-button primary">
          📥 Descargar JSON
        </button>
      </div>
    </div>
  );
} 