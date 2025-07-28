import React, { useState } from 'react';
import { useAuth } from '../AuthContext';
import { FileUpload } from './FileUpload';
import { InvoiceResults } from './InvoiceResults';

export function Dashboard() {
  const { currentUser, logout } = useAuth();
  const [uploadedData, setUploadedData] = useState<any>(null);
  const [uploadedFileName, setUploadedFileName] = useState<string>('');
  const [showResults, setShowResults] = useState(false);
  const [uploadError, setUploadError] = useState<string>('');
  const [processedInvoices, setProcessedInvoices] = useState<Array<{
    id: string;
    fileName: string;
    data: any;
    timestamp: Date;
  }>>([]);

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const handleUploadSuccess = (data: any) => {
    const newInvoice = {
      id: Date.now().toString(),
      fileName: data.file_name || 'Archivo procesado',
      data: data,
      timestamp: new Date()
    };
    
    setProcessedInvoices(prev => [newInvoice, ...prev]);
    setUploadedData(data);
    setUploadedFileName(data.file_name || 'Archivo procesado');
    setShowResults(true);
    setUploadError('');
  };

  const handleUploadError = (error: string) => {
    setUploadError(error);
    setShowResults(false);
  };

  const handleCloseResults = () => {
    setShowResults(false);
  };

  const handleViewInvoice = (invoice: any) => {
    setUploadedData(invoice.data);
    setUploadedFileName(invoice.fileName);
    setShowResults(true);
  };

  const handleDeleteInvoice = (invoiceId: string, e: React.MouseEvent) => {
    e.stopPropagation(); // Evitar que se abra el modal
    setProcessedInvoices(prev => prev.filter(invoice => invoice.id !== invoiceId));
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="modern-dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="header-left">
            <div className="dashboard-logo">
              <span className="logo-icon">📄</span>
              <span className="logo-text">InvoiceAI</span>
            </div>
            <h1 className="dashboard-title">Dashboard</h1>
          </div>
          
          <div className="header-right">
            <div className="user-info">
              <div className="user-avatar">
                <span>{currentUser?.email?.charAt(0).toUpperCase()}</span>
              </div>
              <div className="user-details">
                <span className="user-name">{currentUser?.email}</span>
                <span className="user-status">Conectado</span>
              </div>
            </div>
            <button onClick={handleLogout} className="logout-button">
              <span className="logout-icon">🚪</span>
              Cerrar Sesión
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="dashboard-main">
        {/* Welcome Section */}
        <section className="welcome-section">
          <div className="welcome-content">
            <h2>¡Bienvenido de vuelta! 👋</h2>
            <p>Estás listo para procesar tus facturas con inteligencia artificial</p>
          </div>
          <div className="welcome-stats">
            <div className="stat-card">
              <div className="stat-icon">📊</div>
              <div className="stat-info">
                <span className="stat-number">{processedInvoices.length}</span>
                <span className="stat-label">Facturas Procesadas</span>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">⚡</div>
              <div className="stat-info">
                <span className="stat-number">99%</span>
                <span className="stat-label">Precisión IA</span>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">🎯</div>
              <div className="stat-info">
                <span className="stat-number">0s</span>
                <span className="stat-label">Tiempo Promedio</span>
              </div>
            </div>
          </div>
        </section>

        {/* Upload Section */}
        <section className="upload-section">
          <div className="section-header">
            <h3>Procesar Nueva Factura</h3>
            <p>Sube tu archivo para extraer datos automáticamente</p>
          </div>
          
          <FileUpload 
            onUploadSuccess={handleUploadSuccess}
            onUploadError={handleUploadError}
          />

          {uploadError && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {uploadError}
            </div>
          )}

          {showResults && uploadedData && (
            <div className="success-message">
              <span className="success-icon">✅</span>
              ¡Archivo procesado exitosamente! Revisa los resultados abajo.
            </div>
          )}
        </section>

        {/* Results Modal */}
        {showResults && uploadedData && (
          <div className="results-modal-overlay">
            <div className="results-modal">
              <InvoiceResults
                data={uploadedData}
                fileName={uploadedFileName}
                onClose={handleCloseResults}
              />
            </div>
          </div>
        )}

        {/* Recent Activity */}
        <section className="activity-section">
          <div className="section-header">
            <h3>Actividad Reciente</h3>
            <p>Historial de facturas procesadas</p>
          </div>
          
          <div className="activity-list">
            {processedInvoices.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">📋</div>
                <h4>No hay actividad aún</h4>
                <p>Sube tu primera factura para comenzar</p>
              </div>
            ) : (
              <div className="invoices-list">
                {processedInvoices.map((invoice) => (
                  <div key={invoice.id} className="invoice-item" onClick={() => handleViewInvoice(invoice)}>
                    <div className="invoice-icon">📄</div>
                    <div className="invoice-info">
                      <h4>{invoice.fileName}</h4>
                      <p>Procesado el {formatDate(invoice.timestamp)}</p>
                      <div className="invoice-details">
                        <span className="invoice-type">{invoice.data.invoice_type || 'Factura'}</span>
                        <span className="invoice-amount">
                          {new Intl.NumberFormat('es-ES', {
                            style: 'currency',
                            currency: invoice.data.currency || 'USD'
                          }).format(invoice.data.total_amount || 0)}
                        </span>
                      </div>
                    </div>
                    <div className="invoice-actions">
                      <button className="view-button">👁️ Ver</button>
                      <button 
                        className="delete-button"
                        onClick={(e) => handleDeleteInvoice(invoice.id, e)}
                        title="Eliminar del historial"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>

        {/* Quick Actions */}
        <section className="quick-actions">
          <div className="section-header">
            <h3>Acciones Rápidas</h3>
          </div>
          
          <div className="actions-grid">
            <button className="action-card">
              <div className="action-icon">📤</div>
              <h4>Subir Factura</h4>
              <p>Procesar nueva factura</p>
            </button>
            
            <button className="action-card">
              <div className="action-icon">📊</div>
              <h4>Ver Reportes</h4>
              <p>Analizar datos extraídos</p>
            </button>
            
            <button className="action-card">
              <div className="action-icon">⚙️</div>
              <h4>Configuración</h4>
              <p>Personalizar preferencias</p>
            </button>
            
            <button className="action-card">
              <div className="action-icon">❓</div>
              <h4>Ayuda</h4>
              <p>Documentación y soporte</p>
            </button>
          </div>
        </section>
      </main>
    </div>
  );
} 