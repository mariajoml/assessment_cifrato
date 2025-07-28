import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useAuth } from '../AuthContext';

interface FileUploadProps {
  onUploadSuccess?: (data: any) => void;
  onUploadError?: (error: string) => void;
}

export function FileUpload({ onUploadSuccess, onUploadError }: FileUploadProps) {
  const { currentUser } = useAuth();
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setUploadedFile(file);
    setIsUploading(true);
    setUploadProgress(0);

    try {
      const formData = new FormData();
      formData.append('file', file);

      // Simulate progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      // Obtener el token de Firebase
      const token = await currentUser?.getIdToken();
      if (!token) {
        throw new Error('No se pudo obtener el token de autenticación');
      }

      const response = await fetch(`${import.meta.env.VITE_APP_API_BASE_URL}/process-invoice`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData,
      });

      clearInterval(progressInterval);
      setUploadProgress(100);

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      
      setTimeout(() => {
        setIsUploading(false);
        setUploadProgress(0);
        setUploadedFile(null);
        onUploadSuccess?.(data);
      }, 1000);

    } catch (error) {
      console.error('Upload error:', error);
      setIsUploading(false);
      setUploadProgress(0);
      setUploadedFile(null);
      onUploadError?.(error instanceof Error ? error.message : 'Error al subir el archivo');
    }
  }, [onUploadSuccess, onUploadError]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/xml': ['.xml'],
      'text/xml': ['.xml']
    },
    maxFiles: 1,
    disabled: isUploading
  });

  const getFileIcon = (fileName: string) => {
    if (fileName.toLowerCase().endsWith('.pdf')) return '📄';
    if (fileName.toLowerCase().endsWith('.xml')) return '📋';
    return '📁';
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="file-upload-container">
      <div
        {...getRootProps()}
        className={`upload-area ${isDragActive ? 'drag-active' : ''} ${isDragReject ? 'drag-reject' : ''} ${isUploading ? 'uploading' : ''}`}
      >
        <input {...getInputProps()} />
        
        {isUploading ? (
          <div className="upload-progress">
            <div className="progress-icon">⏳</div>
            <h4>Procesando archivo...</h4>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
            <p>{uploadProgress}% completado</p>
            {uploadedFile && (
              <div className="uploaded-file-info">
                <span>{getFileIcon(uploadedFile.name)} {uploadedFile.name}</span>
                <span className="file-size">({formatFileSize(uploadedFile.size)})</span>
              </div>
            )}
          </div>
        ) : (
          <>
            <div className="upload-icon">📁</div>
            <h4>
              {isDragActive 
                ? (isDragReject ? 'Tipo de archivo no soportado' : 'Suelta el archivo aquí')
                : 'Arrastra y suelta tu factura aquí'
              }
            </h4>
            <p>o haz clic para seleccionar archivo</p>
            <div className="supported-formats">
              <span className="format-badge">PDF</span>
              <span className="format-badge">XML</span>
              <span className="format-badge">+ más</span>
            </div>
            <button className="upload-button" disabled={isUploading}>
              <span className="upload-icon-btn">📤</span>
              Seleccionar Archivo
            </button>
          </>
        )}
      </div>
    </div>
  );
} 