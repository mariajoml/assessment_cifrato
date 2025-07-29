# assessment_cifrato
AI-powered Invoice Processing Microservice for accounting automation. Built with FastAPI, LangChain (OpenAI), React, and deployed on Google Cloud Platform.
## 🚀 Live Demo

## 📋 Project Overview

This application provides an intelligent invoice processing system that:

- **Extracts structured data** from PDF and XML invoices using AI
- **Authenticates users** via Firebase Authentication
- **Stores processed data** in Google Cloud Firestore
- **Provides a modern web interface** for invoice management
- **Runs entirely on Google Cloud Platform** with automatic scaling

## 🏗️ Architecture

### Frontend (React + TypeScript + Vite)
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Authentication**: Firebase Auth Web SDK
- **UI Components**: Custom components with CSS Modules
- **File Upload**: React-Dropzone for drag-and-drop functionality
- **Deployment**: Firebase Hosting

### Backend (FastAPI + Python)
- **Framework**: FastAPI with async support
- **AI Processing**: LangChain + OpenAI GPT-3.5-turbo
- **Authentication**: Firebase Admin SDK
- **Database**: Google Cloud Firestore
- **File Processing**: PyPDF2 for PDF extraction
- **Deployment**: Google Cloud Run with Buildpacks

### Infrastructure (Google Cloud Platform)
- **Container Registry**: Google Container Registry
- **Compute**: Cloud Run (serverless containers)
- **Database**: Firestore (NoSQL)
- **Authentication**: Firebase Auth
- **Hosting**: Firebase Hosting
- **CI/CD**: GitHub integration with Cloud Build

## 🛠️ Tech Stack

### Frontend
```json
{
  "react": "^18.2.0",
  "typescript": "^5.0.0",
  "vite": "^4.4.0",
  "firebase": "^10.0.0",
  "react-dropzone": "^14.2.0",
  "axios": "^1.4.0"
}
```

### Backend
```json
{
  "fastapi": "^0.104.1",
  "uvicorn": "^0.24.0",
  "langchain": "^0.2.0",
  "langchain-openai": "^0.1.0",
  "openai": "^1.97.1",
  "firebase-admin": "^6.2.0",
  "pypdf2": "^3.0.1",
  "pydantic": "^2.5.0"
}
```

## 📁 Project Structure

```
assessment_cifrato/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── contexts/         # React contexts
│   │   ├── firebaseConfig.ts # Firebase configuration
│   │   └── App.tsx          # Main application component
│   ├── package.json
│   ├── vite.config.ts
│   ├── firebase.json        # Firebase hosting config
│   └── .env                 # Environment variables
├── backend/                  # FastAPI backend application
│   ├── app/
│   │   ├── main.py          # FastAPI application entry point
│   │   ├── models/          # Pydantic models
│   │   ├── services/        # Business logic services
│   │   ├── utils/           # Utility functions
│   │   └── llm_processor.py # AI processing logic
│   ├── requirements.txt     # Python dependencies
│   ├── runtime.txt          # Python version specification
│   └── .env                 # Environment variables
├── tests/                   # Test files
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Google Cloud Platform account
- Firebase project
- OpenAI API key

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/assessment_cifrato.git
   cd assessment_cifrato
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Set environment variables
   cp .env.example .env
   # Edit .env with your API keys
   
   # Run the backend
   uvicorn app.main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   
   # Set environment variables
   cp .env.example .env
   # Edit .env with your Firebase config and backend URL
   
   # Run the frontend
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🌐 Deployment

### Frontend Deployment (Firebase Hosting)

1. **Install Firebase CLI**
   ```bash
   npm install -g firebase-tools
   ```

2. **Login to Firebase**
   ```bash
   firebase login
   ```

3. **Initialize Firebase Hosting**
   ```bash
   cd frontend
   firebase init hosting
   # Select your project and set public directory to 'dist'
   ```

4. **Build and Deploy**
   ```bash
   npm run build
   firebase deploy --only hosting
   ```

### Backend Deployment (Cloud Run)

1. **Enable required APIs**
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

2. **Deploy to Cloud Run**
   ```bash
   cd backend
   gcloud run deploy your-service-name \
     --source . \
     --region=us-central1 \
     --allow-unauthenticated \
     --platform=managed
   ```

3. **Set environment variables**
   ```bash
   gcloud run services update your-service-name \
     --region=us-central1 \
     --set-env-vars="OPENAI_API_KEY=your-key-here"
   ```

## 🔧 Configuration

### Environment Variables

For detailed environment setup instructions, see:
- **Backend**: [`backend/ENVIRONMENT_SETUP.md`](backend/ENVIRONMENT_SETUP.md)
- **Frontend**: [`frontend/ENVIRONMENT_SETUP.md`](frontend/ENVIRONMENT_SETUP.md)

### 📖 API Documentation

The API includes automatic documentation generated with FastAPI:

#### 🌐 Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs` (when server is running)
- **ReDoc**: `http://localhost:8000/redoc` (alternative documentation)
- **OpenAPI JSON**: `http://localhost:8000/openapi.json` (specification)

#### 📄 Static Documentation
- **HTML**: [`backend/docs/api-documentation.html`](backend/docs/api-documentation.html)
- **Markdown**: [`backend/docs/api-documentation.md`](backend/docs/api-documentation.md)
- **OpenAPI**: [`backend/docs/openapi.json`](backend/docs/openapi.json)

#### 🔧 Generate Documentation
```bash
cd backend
make docs  # Generate static documentation
make docs-serve  # Serve HTML documentation at http://localhost:8080
```

#### Quick Setup

**Backend (.env)**
```bash
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Firebase Admin SDK
FIREBASE_SERVICE_ACCOUNT_PATH=./service-account.json
```

**Frontend (.env)**
```bash
# Backend API URL
VITE_APP_API_BASE_URL=http://localhost:8000

# Firebase Web SDK Configuration
VITE_FIREBASE_API_KEY=your-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
```

## 📊 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user

### Invoice Processing
- `POST /process-invoice` - Process uploaded invoice
- `GET /invoices` - Get user's processed invoices
- `GET /invoices/{invoice_id}` - Get specific invoice details

### Health Check
- `GET /` - Health check endpoint
- `GET /docs` - Interactive API documentation

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔒 Security Features

- **Firebase Authentication** for user management
- **CORS configuration** for secure cross-origin requests
- **Input validation** with Pydantic models
- **Rate limiting** on API endpoints
- **Secure environment variable** management

## 📈 Performance

- **Serverless architecture** with automatic scaling
- **Async processing** for better concurrency
- **Optimized builds** with Vite
- **CDN delivery** via Firebase Hosting
- **Database indexing** for fast queries


## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the API documentation at `/docs` endpoint
- Review the Firebase console for authentication issues

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

1. **Push to main branch** triggers automatic build
2. **Cloud Build** compiles and tests the application
3. **Cloud Run** deploys the backend automatically
4. **Firebase Hosting** deploys the frontend

## 📊 Monitoring

- **Cloud Run logs** for backend monitoring
- **Firebase Analytics** for frontend usage
- **Firestore logs** for database operations
- **Cloud Build logs** for deployment status

---

**Last Updated**: July 28, 2025
**Version**: 1.0.0
**Status**: �� Production Ready
