import React from 'react';
import { useAuth } from '../AuthContext';

interface LandingPageProps {
  onGetStarted: () => void;
}

export function LandingPage({ onGetStarted }: LandingPageProps) {
  const { currentUser } = useAuth();

  return (
    <div className="landing-page">
      {/* Header */}
      <header className="landing-header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">📄</span>
            <span className="logo-text">InvoiceAI</span>
          </div>
          
          <nav className="nav-menu">
            <a href="#features">Características</a>
            <a href="#how-it-works">Cómo Funciona</a>
            <a href="#faq">FAQ</a>
            <a href="#contact">Contacto</a>
          </nav>
          
          <div className="header-actions">
            {currentUser ? (
              <button onClick={onGetStarted} className="btn-primary">
                Ir al Dashboard
              </button>
            ) : (
              <>
                <button onClick={onGetStarted} className="btn-secondary">
                  Iniciar Sesión
                </button>
                <button onClick={onGetStarted} className="btn-primary">
                  Empieza Ahora
                </button>
              </>
            )}
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            El Procesamiento de Facturas con{' '}
            <span className="highlight">IA</span>
            <span className="sparkle">✨</span>
          </h1>
          <p className="hero-subtitle">
            Extrae, procesa y analiza tus facturas en minutos, sin errores ni trabajo manual. 
            Automatiza tu contabilidad con inteligencia artificial.
          </p>
          <button onClick={onGetStarted} className="cta-button">
            Empieza Ahora
          </button>
        </div>
        
        <div className="hero-illustration">
          <div className="floating-card card-1">
            <span className="card-icon">📊</span>
            <span className="card-text">Análisis Automático</span>
          </div>
          <div className="floating-card card-2">
            <span className="card-icon">⚡</span>
            <span className="card-text">Procesamiento Rápido</span>
          </div>
          <div className="floating-card card-3">
            <span className="card-icon">🎯</span>
            <span className="card-text">Precisión 99%</span>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features-section">
        <div className="container">
          <h2 className="section-title">Características Principales</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>IA Avanzada</h3>
              <p>Procesamiento inteligente de facturas con machine learning</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📁</div>
              <h3>Múltiples Formatos</h3>
              <p>Soporte para PDF, XML y otros formatos de factura</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔒</div>
              <h3>Seguridad Total</h3>
              <p>Autenticación Firebase y encriptación de datos</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📈</div>
              <h3>Análisis en Tiempo Real</h3>
              <p>Reportes y métricas instantáneas</p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="container">
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-number">99%</div>
              <div className="stat-label">Precisión en Extracción</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">+10</div>
              <div className="stat-label">Formatos Soportados</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">24/7</div>
              <div className="stat-label">Disponibilidad</div>
            </div>
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section id="how-it-works" className="how-it-works">
        <div className="container">
          <h2 className="section-title">Cómo Funciona</h2>
          <div className="steps-grid">
            <div className="step">
              <div className="step-number">1</div>
              <h3>Sube tu Factura</h3>
              <p>Arrastra y suelta tu archivo PDF o XML</p>
            </div>
            <div className="step">
              <div className="step-number">2</div>
              <h3>Procesamiento IA</h3>
              <p>Nuestra IA extrae automáticamente los datos</p>
            </div>
            <div className="step">
              <div className="step-number">3</div>
              <h3>Resultados Inmediatos</h3>
              <p>Obtén datos estructurados en segundos</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <h2>¿Listo para Automatizar tu Contabilidad?</h2>
          <p>Únete a cientos de empresas que ya confían en nuestra IA</p>
          <button onClick={onGetStarted} className="cta-button-large">
            Comenzar Gratis
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-section">
              <h4>InvoiceAI</h4>
              <p>Procesamiento inteligente de facturas con IA</p>
            </div>
            <div className="footer-section">
              <h4>Producto</h4>
              <a href="#features">Características</a>
              <a href="#how-it-works">Cómo Funciona</a>
            </div>
            <div className="footer-section">
              <h4>Soporte</h4>
              <a href="#faq">FAQ</a>
              <a href="#contact">Contacto</a>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2024 InvoiceAI. Todos los derechos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  );
} 