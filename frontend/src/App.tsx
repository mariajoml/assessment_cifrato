import { useState } from 'react';
import { useAuth } from './AuthContext';
import { Login } from './components/Auth/Login';
import { Register } from './components/Auth/Register';
import { Dashboard } from './components/Dashboard';
import { LandingPage } from './components/LandingPage';
import './App.css';

function App() {
  const { currentUser, loading } = useAuth();
  const [isRegistering, setIsRegistering] = useState(false);
  const [showAuth, setShowAuth] = useState(false);

  const handleGetStarted = () => {
    setShowAuth(true);
  };

  const handleBackToLanding = () => {
    setShowAuth(false);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner">Loading...</div>
      </div>
    );
  }

  // Si el usuario está autenticado, mostrar dashboard
  if (currentUser) {
    return (
      <div className="app-container">
        <Dashboard />
      </div>
    );
  }

  // Si no está autenticado y quiere ver auth, mostrar formularios
  if (showAuth) {
    return (
      <div className="app-container">
        <div className="auth-wrapper">
          <button 
            onClick={handleBackToLanding} 
            className="back-to-landing"
          >
            ← Volver
          </button>
          {isRegistering ? (
            <Register onSwitchToLogin={() => setIsRegistering(false)} />
          ) : (
            <Login onSwitchToRegister={() => setIsRegistering(true)} />
          )}
        </div>
      </div>
    );
  }

  // Por defecto, mostrar landing page
  return <LandingPage onGetStarted={handleGetStarted} />;
}

export default App; 