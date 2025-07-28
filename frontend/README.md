# Invoice Processing Frontend

Este es el frontend de la aplicación de procesamiento de facturas, construido con React, TypeScript y Firebase Authentication.

## Configuración

### 1. Instalar dependencias

```bash
npm install
```

### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto frontend basándote en `env.example`:

```bash
cp env.example .env
```

Edita el archivo `.env` con tus credenciales de Firebase:

```env
VITE_APP_API_BASE_URL="http://127.0.0.1:8000"
VITE_FIREBASE_API_KEY="tu-api-key"
VITE_FIREBASE_AUTH_DOMAIN="tu-proyecto.firebaseapp.com"
VITE_FIREBASE_PROJECT_ID="tu-project-id"
VITE_FIREBASE_STORAGE_BUCKET="tu-proyecto.appspot.com"
VITE_FIREBASE_MESSAGING_SENDER_ID="123456789"
VITE_FIREBASE_APP_ID="tu-app-id"
```

### 3. Ejecutar en modo desarrollo

```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:3000`

## Características

- 🔐 Autenticación con Firebase
- 📝 Formularios de login y registro
- 🎨 Interfaz moderna y responsive
- 📱 Diseño adaptativo para móviles
- 🚀 Construido con Vite para desarrollo rápido

## Estructura del proyecto

```
frontend/
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── Login.tsx
│   │   │   └── Register.tsx
│   │   └── Dashboard.tsx
│   ├── AuthContext.tsx
│   ├── firebaseConfig.ts
│   ├── App.tsx
│   ├── main.tsx
│   ├── App.css
│   └── index.css
├── package.json
├── vite.config.ts
├── tsconfig.json
└── index.html
```

## Scripts disponibles

- `npm run dev` - Ejecutar en modo desarrollo
- `npm run build` - Construir para producción
- `npm run preview` - Previsualizar build de producción
- `npm run lint` - Ejecutar linter 