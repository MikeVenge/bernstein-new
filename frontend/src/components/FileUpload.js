import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

const FileUpload = ({ onFilesUploaded }) => {
  const [files, setFiles] = useState({
    source: null,
    destination: null,
    mapping: null
  });
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  // Define callbacks for each file type
  const onDropSource = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setFiles(prev => ({ ...prev, source: acceptedFiles[0] }));
      setError(null);
    }
  }, []);

  const onDropDestination = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setFiles(prev => ({ ...prev, destination: acceptedFiles[0] }));
      setError(null);
    }
  }, []);

  const onDropMapping = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setFiles(prev => ({ ...prev, mapping: acceptedFiles[0] }));
      setError(null);
    }
  }, []);

  // Create dropzones at the top level
  const sourceDropzone = useDropzone({
    onDrop: onDropSource,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls']
    },
    multiple: false,
    maxSize: 50 * 1024 * 1024 // 50MB
  });

  const destinationDropzone = useDropzone({
    onDrop: onDropDestination,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls']
    },
    multiple: false,
    maxSize: 50 * 1024 * 1024 // 50MB
  });

  const mappingDropzone = useDropzone({
    onDrop: onDropMapping,
    accept: {
      'text/csv': ['.csv']
    },
    multiple: false,
    maxSize: 50 * 1024 * 1024 // 50MB
  });

  const handleUpload = async () => {
    if (!files.source || !files.destination || !files.mapping) {
      setError('Please select all three files');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('source_file', files.source);
      formData.append('destination_file', files.destination);
      formData.append('mapping_file', files.mapping);

      const response = await axios.post('/api/upload-files', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.status === 'success') {
        onFilesUploaded(response.data.job_id, response.data.files);
      } else {
        setError('Upload failed: ' + response.data.message);
      }
    } catch (err) {
      setError('Upload failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setUploading(false);
    }
  };

  const FileDropArea = ({ dropzone, fileType, file, title, description }) => (
    <div
      {...dropzone.getRootProps()}
      className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
        dropzone.isDragActive
          ? 'border-primary-500 bg-primary-50'
          : file
          ? 'border-green-500 bg-green-50'
          : 'border-gray-300 hover:border-gray-400'
      }`}
    >
      <input {...dropzone.getInputProps()} />
      <div className="space-y-2">
        {file ? (
          <>
            <svg className="w-8 h-8 text-green-500 mx-auto" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
            <p className="text-sm font-medium text-green-600">{file.name}</p>
            <p className="text-xs text-gray-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
          </>
        ) : (
          <>
            <svg className="w-8 h-8 text-gray-400 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <p className="text-sm font-medium text-gray-700">{title}</p>
            <p className="text-xs text-gray-500">{description}</p>
          </>
        )}
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Upload Files</h2>
        <p className="text-gray-600">
          Upload your source Excel file, destination Excel file, and CSV mapping file to begin the field mapping process.
        </p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex">
            <svg className="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <p className="ml-3 text-sm text-red-600">{error}</p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Source File (.xlsx)
          </label>
          <FileDropArea
            dropzone={sourceDropzone}
            fileType="source"
            file={files.source}
            title="Drop source Excel file"
            description="Excel file containing source data"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Destination File (.xlsx)
          </label>
          <FileDropArea
            dropzone={destinationDropzone}
            fileType="destination"
            file={files.destination}
            title="Drop destination Excel file"
            description="Excel file to populate with data"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Mapping File (.csv)
          </label>
          <FileDropArea
            dropzone={mappingDropzone}
            fileType="mapping"
            file={files.mapping}
            title="Drop mapping CSV file"
            description="CSV file defining field relationships"
          />
        </div>
      </div>

      {/* File Requirements */}
      <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
        <h3 className="text-sm font-medium text-blue-800 mb-2">File Requirements</h3>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>• <strong>Source File</strong>: Excel file (.xlsx) containing the data to map from</li>
          <li>• <strong>Destination File</strong>: Excel file (.xlsx) to populate with mapped data</li>
          <li>• <strong>Mapping File</strong>: CSV file defining the field relationships and transformations</li>
        </ul>
      </div>

      {/* Upload Button */}
      <div className="flex justify-center">
        <button
          onClick={handleUpload}
          disabled={!files.source || !files.destination || !files.mapping || uploading}
          className={`px-8 py-3 rounded-md font-medium focus:outline-none focus:ring-2 focus:ring-primary-500 ${
            !files.source || !files.destination || !files.mapping || uploading
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-primary-600 text-white hover:bg-primary-700'
          }`}
        >
          {uploading ? (
            <div className="flex items-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Uploading Files...
            </div>
          ) : (
            'Upload Files & Continue'
          )}
        </button>
      </div>
    </div>
  );
};

export default FileUpload;
