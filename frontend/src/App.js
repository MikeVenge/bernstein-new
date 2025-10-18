import React, { useState, useCallback } from 'react';
import FileUpload from './components/FileUpload';
import MappingConfiguration from './components/MappingConfiguration';
import ExecutionStatus from './components/ExecutionStatus';
import ResultsDisplay from './components/ResultsDisplay';
import './index.css';

function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [jobId, setJobId] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState({});
  const [mappingConfig, setMappingConfig] = useState({
    targetColumn: 71,
    dataColumn: 'CO'
  });
  const [executionResult, setExecutionResult] = useState(null);

  const handleFilesUploaded = useCallback((jobId, files) => {
    setJobId(jobId);
    setUploadedFiles(files);
    setCurrentStep(2);
  }, []);

  const handleConfigurationSet = useCallback((config) => {
    setMappingConfig(config);
    setCurrentStep(3);
  }, []);

  const handleExecutionComplete = useCallback((result) => {
    setExecutionResult(result);
    setCurrentStep(4);
  }, []);

  const handleReset = useCallback(() => {
    setCurrentStep(1);
    setJobId(null);
    setUploadedFiles({});
    setMappingConfig({ targetColumn: 71, dataColumn: 'CO' });
    setExecutionResult(null);
  }, []);

  const steps = [
    { number: 1, title: 'Upload Files', description: 'Upload source, destination, and mapping files' },
    { number: 2, title: 'Configure Mapping', description: 'Set target column and data source' },
    { number: 3, title: 'Execute Mapping', description: 'Run the field mapping process' },
    { number: 4, title: 'Download Results', description: 'Download populated files and audit trail' }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Field Mapper</h1>
              <p className="text-gray-600 mt-1">Parameterized Excel field mapping and population tool</p>
            </div>
            <button
              onClick={handleReset}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              Start New Mapping
            </button>
          </div>
        </div>
      </header>

      {/* Progress Steps */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          {steps.map((step, index) => (
            <div key={step.number} className="flex items-center">
              <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 ${
                currentStep >= step.number 
                  ? 'bg-primary-500 border-primary-500 text-white' 
                  : 'bg-white border-gray-300 text-gray-500'
              }`}>
                {currentStep > step.number ? (
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                ) : (
                  step.number
                )}
              </div>
              <div className="ml-3">
                <p className={`text-sm font-medium ${currentStep >= step.number ? 'text-gray-900' : 'text-gray-500'}`}>
                  {step.title}
                </p>
                <p className="text-xs text-gray-500">{step.description}</p>
              </div>
              {index < steps.length - 1 && (
                <div className={`flex-1 mx-4 h-0.5 ${
                  currentStep > step.number ? 'bg-primary-500' : 'bg-gray-300'
                }`} />
              )}
            </div>
          ))}
        </div>

        {/* Step Content */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          {currentStep === 1 && (
            <FileUpload onFilesUploaded={handleFilesUploaded} />
          )}
          
          {currentStep === 2 && (
            <MappingConfiguration
              uploadedFiles={uploadedFiles}
              onConfigurationSet={handleConfigurationSet}
              jobId={jobId}
            />
          )}
          
          {currentStep === 3 && (
            <ExecutionStatus
              jobId={jobId}
              mappingConfig={mappingConfig}
              onExecutionComplete={handleExecutionComplete}
            />
          )}
          
          {currentStep === 4 && (
            <ResultsDisplay
              jobId={jobId}
              executionResult={executionResult}
              onReset={handleReset}
            />
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="text-center text-sm text-gray-500">
            <p>Field Mapper v1.0.0 - Parameterized Excel Field Mapping Tool</p>
            <p className="mt-1">Supports multiple mapping strategies and data transformations</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
