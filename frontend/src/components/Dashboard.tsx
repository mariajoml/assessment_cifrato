import React from 'react';
import { useAuth } from '../AuthContext';

export function Dashboard() {
  const { currentUser, logout } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout failed:', error);
    }
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
                <span className="stat-number">0</span>
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
          
          <div className="upload-area">
            <div className="upload-icon">📁</div>
            <h4>Arrastra y suelta tu factura aquí</h4>
            <p>o haz clic para seleccionar archivo</p>
            <div className="supported-formats">
              <span className="format-badge">PDF</span>
              <span className="format-badge">XML</span>
              <span className="format-badge">+ más</span>
            </div>
            <button className="upload-button">
              <span className="upload-icon-btn">📤</span>
              Seleccionar Archivo
            </button>
          </div>
        </section>

        {/* Recent Activity */}
        <section className="activity-section">
          <div className="section-header">
            <h3>Actividad Reciente</h3>
            <p>Historial de facturas procesadas</p>
          </div>
          
          <div className="activity-list">
            <div className="empty-state">
              <div className="empty-icon">📋</div>
              <h4>No hay actividad aún</h4>
              <p>Sube tu primera factura para comenzar</p>
            </div>
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