import React, { useState } from 'react';
import { useAuth } from '../../AuthContext';

interface LoginProps {
  onSwitchToRegister: () => void;
}

export function Login({ onSwitchToRegister }: LoginProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await login(email, password);
    } catch (error: any) {
      console.error('Login failed:', error);
      setError(error.message || 'Failed to login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modern-auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <div className="auth-logo">
            <span className="logo-icon">📄</span>
            <span className="logo-text">InvoiceAI</span>
          </div>
          <h2 className="auth-title">
            Bienvenido
            <span className="sparkle-icon">✨</span>
          </h2>
          <p className="auth-subtitle">
            Inicia sesión para acceder a tu cuenta
          </p>
        </div>

        <form onSubmit={handleSubmit} className="modern-auth-form">
          <div className="form-group">
            <label htmlFor="email">Correo electrónico</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="tu@email.com"
              required
              disabled={loading}
              className="modern-input"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <div className="password-input-container">
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                disabled={loading}
                className="modern-input"
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
                disabled={loading}
                title={showPassword ? "Ocultar contraseña" : "Mostrar contraseña"}
              >
                {showPassword ? "👁️" : "👁️‍🗨️"}
              </button>
            </div>
          </div>

          {error && <div className="modern-error-message">{error}</div>}

          <button type="submit" disabled={loading} className="modern-auth-button">
            {loading ? 'Iniciando sesión...' : 'Iniciar sesión'}
          </button>
        </form>

        <div className="modern-auth-switch">
          <p>
            ¿No tienes cuenta?{' '}
            <button 
              type="button" 
              onClick={onSwitchToRegister}
              className="modern-switch-button"
            >
              Regístrate aquí
            </button>
          </p>
        </div>

        <div className="auth-footer">
          <p>Hecho con ❤️ desde 🇪🇨</p>
        </div>
      </div>
    </div>
  );
} 