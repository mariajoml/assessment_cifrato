# Backend - Invoice Processing API

API de procesamiento de facturas con inteligencia artificial construida con FastAPI y desplegada en Google Cloud Run.

## 🚀 Características

- **Procesamiento de Facturas**: Extracción y análisis de datos de archivos PDF y XML
- **Autenticación Firebase**: Integración completa con Firebase Authentication
- **Persistencia Firestore**: Almacenamiento de datos procesados en Google Firestore
- **Inteligencia Artificial**: Procesamiento con OpenAI/LangChain para clasificación automática
- **Exportación**: Funcionalidad de exportación en formatos JSON y CSV
- **Arquitectura Modular**: Código organizado en módulos separados para mejor mantenibilidad

## 📋 Requisitos

- Python 3.10+
- Google Cloud Platform (GCP) con APIs habilitadas:
  - Cloud Firestore
  - Cloud Run
  - Cloud Build
  - IAM
- Firebase Project configurado
- OpenAI API Key

## 🛠️ Configuración Local

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto:
```env
OPENAI_API_KEY=tu_openai_api_key
FIREBASE_SERVICE_ACCOUNT_PATH=ruta/a/tu/service-account.json
```

### 3. Ejecutar localmente
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🐳 Despliegue con Docker

### 1. Construir imagen
```bash
docker build -t invoice-processing-api .
```

### 2. Ejecutar contenedor
```bash
docker run -p 8000:8000 invoice-processing-api
```

## ☁️ Despliegue en Google Cloud Run

### 1. Configurar Google Cloud CLI
```bash
gcloud auth login
gcloud config set project cifrato-617a3
```

### 2. Habilitar APIs necesarias
```bash
gcloud services enable run.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 3. Desplegar en Cloud Run
```bash
gcloud run deploy invoice-processing-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="OPENAI_API_KEY=tu_openai_api_key" \
  --set-env-vars="FIREBASE_SERVICE_ACCOUNT_PATH=/app/service-account.json"
```

### 4. Configurar variables de entorno en Cloud Run
```bash
gcloud run services update invoice-processing-api \
  --set-env-vars="OPENAI_API_KEY=tu_openai_api_key" \
  --set-env-vars="FIREBASE_SERVICE_ACCOUNT_PATH=/app/service-account.json"
```

## 📊 Estructura de Datos en Firestore

### Colección: `invoices`
Cada documento contiene:
- `invoice_type`: Tipo de factura (purchase, sale, return, compra, gasto)
- `cost_center`: Centro de costos
- `payment_method`: Método de pago
- `extracted_items`: Lista de items extraídos
- `total_amount`: Monto total
- `currency`: Moneda
- `invoice_date`: Fecha de la factura (YYYY-MM-DD)
- `supplier_name`: Nombre del proveedor
- `file_name`: Nombre del archivo original
- `uid`: ID del usuario que subió la factura
- `timestamp`: Timestamp de procesamiento (ISO format)
- `uploaded_at`: Timestamp de subida (ISO format)

## 🔧 Endpoints

### GET `/`
- **Descripción**: Endpoint raíz para verificar el estado de la API
- **Respuesta**: Información básica de la API

### POST `/process-invoice`
- **Descripción**: Procesa una factura PDF o XML
- **Autenticación**: Requerida (Firebase token)
- **Parámetros**: 
  - `file`: Archivo PDF o XML
- **Respuesta**: Datos estructurados de la factura

### POST `/export-invoices`
- **Descripción**: Exporta facturas procesadas
- **Autenticación**: Requerida (Firebase token)
- **Parámetros**:
  - `invoices`: Lista de facturas a exportar
  - `format`: Formato de exportación (json, csv)
- **Respuesta**: Archivo exportado

## 🧪 Testing

Ejecutar tests:
```bash
pytest test_main.py -v
```

## 📝 Logs

La aplicación registra logs informativos sobre:
- Inicialización de servicios
- Procesamiento de archivos
- Guardado en Firestore
- Errores y excepciones

## 🔒 Seguridad

- Autenticación Firebase obligatoria para endpoints sensibles
- Validación de tipos de archivo
- Manejo seguro de errores
- Variables de entorno para credenciales sensibles

## 📈 Monitoreo

La aplicación está preparada para:
- Logs estructurados para Cloud Logging
- Métricas de rendimiento
- Trazabilidad de requests
- Alertas de errores 