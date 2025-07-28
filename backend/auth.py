import os
import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import credentials, initialize_app, auth as firebase_auth
from firebase_admin.auth import InvalidIdTokenError
from dotenv import load_dotenv

# Configuración de logging
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Validar FIREBASE_SERVICE_ACCOUNT_PATH
FIREBASE_SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
if not FIREBASE_SERVICE_ACCOUNT_PATH:
    logging.critical("La variable de entorno FIREBASE_SERVICE_ACCOUNT_PATH no está definida.")
    raise ValueError("FIREBASE_SERVICE_ACCOUNT_PATH no está definida en el entorno.")

class FirebaseAuth:
    """Clase para manejar la autenticación con Firebase."""
    
    def __init__(self):
        self._initialized = False
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Inicializa Firebase Admin SDK."""
        try:
            cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_PATH)
            initialize_app(cred)
            self._initialized = True
            logger.info("Firebase Admin SDK inicializado correctamente.")
        except Exception as e:
            logger.critical(f"Error al inicializar Firebase Admin SDK: {e}")
            raise ValueError(f"No se pudo inicializar Firebase Admin SDK: {e}")
    
    def verify_token(self, token: str) -> dict:
        """
        Verifica un token de Firebase.
        
        Args:
            token (str): Token de Firebase a verificar
            
        Returns:
            dict: Información del usuario decodificada
            
        Raises:
            HTTPException: Si el token es inválido o expirado
        """
        if not self._initialized:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Firebase no está inicializado correctamente."
            )
        
        try:
            decoded_token = firebase_auth.verify_id_token(token)
            logger.info(f"Token verificado para UID: {decoded_token.get('uid')}")
            return decoded_token
        except InvalidIdTokenError as e:
            logger.error(f"Token inválido o expirado: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado."
            )
        except Exception as e:
            logger.error(f"Error al verificar el token: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se pudo verificar el token de autenticación."
            )

# Instancia global de autenticación
firebase_auth_instance = FirebaseAuth()

# Dependencia para verificar el token de Firebase
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Dependencia de FastAPI para verificar tokens de Firebase.
    
    Args:
        credentials (HTTPAuthorizationCredentials): Credenciales HTTP
        
    Returns:
        dict: Información del usuario autenticado
        
    Raises:
        HTTPException: Si la autenticación falla
    """
    token = credentials.credentials
    return firebase_auth_instance.verify_token(token) 