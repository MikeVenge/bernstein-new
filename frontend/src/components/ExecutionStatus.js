import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ExecutionStatus = ({ jobId, mappingConfig, onExecutionComplete }) => {
  const [status, setStatus] = useState('ready');
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [executing, setExecuting] = useState(false);

  const startExecution = async () => {
    try {
      setExecuting(true);
      setError(null);
      setStatus('starting');

      const formData = new FormData();
      formData.append('target_column', mappingConfig.targetColumn.toString());
      formData.append('data_column', mappingConfig.dataColumn);

      const response = await axios.post(`/api/execute-mapping/${jobId}`, formData);

      if (response.data.status === 'success') {
        setResult(response.data.result);
        setStatus('completed');
        setProgress(100);
        onExecutionComplete(response.data.result);
      } else {
        setError(response.data.message || 'Execution failed');
        setStatus('error');
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      setStatus('error');
    } finally {
      setExecuting(false);
    }
  };

  const pollJobStatus = async () => {
    try {
      const response = await axios.get(`/api/job-status/${jobId}`);
      const jobStatus = response.data;
      
      setStatus(jobStatus.status);
      setProgress(jobStatus.progress);
      
      if (jobStatus.status === 'completed') {
        setResult(jobStatus.result);
        onExecutionComplete(jobStatus.result);
      } else if (jobStatus.status === 'error') {
        setError(jobStatus.error);
      }
    } catch (err) {
      console.error('Failed to poll job status:', err);
    }
  };

  useEffect(() => {
    if (executing && status === 'processing') {
      const interval = setInterval(pollJobStatus, 1000);
      return () => clearInterval(interval);
    }
  }, [executing, status, jobId]);

  const getStatusColor = (status) => {
    switch (status) {
      case 'ready': return 'text-gray-500';
      case 'starting': case 'processing': return 'text-blue-500';
      case 'completed': return 'text-green-500';
      case 'error': return 'text-red-500';
      default: return 'text-gray-500';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'ready':
        return (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      case 'starting':
      case 'processing':
        return (
          <svg className="animate-spin w-6 h-6" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        );
      case 'completed':
        return (
          <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
        );
      case 'error':
        return (
          <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
        );
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Execute Field Mapping</h2>
        <p className="text-gray-600">
          Run the field mapping process with your configured parameters.
        </p>
      </div>

      {/* Configuration Summary */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-sm font-medium text-blue-800 mb-2">Configuration Summary</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-blue-700">
              <span className="font-medium">Target Column:</span> {mappingConfig.targetColumn} 
              <span className="text-blue-500"> (Destination)</span>
            </p>
          </div>
          <div>
            <p className="text-sm text-blue-700">
              <span className="font-medium">Data Column:</span> {mappingConfig.dataColumn}
              <span className="text-blue-500"> (Source)</span>
            </p>
          </div>
        </div>
        <div className="mt-2 text-xs text-blue-600">
          Data will flow from Source Column {mappingConfig.dataColumn} → Destination Column {mappingConfig.targetColumn}
        </div>
      </div>

      {/* Execution Status */}
      <div className="bg-white border rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <div className={`${getStatusColor(status)} mr-3`}>
              {getStatusIcon(status)}
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-900">
                {status === 'ready' && 'Ready to Execute'}
                {status === 'starting' && 'Starting Execution...'}
                {status === 'processing' && 'Processing Mappings...'}
                {status === 'completed' && 'Execution Completed!'}
                {status === 'error' && 'Execution Failed'}
              </h3>
              <p className="text-sm text-gray-500">
                {status === 'ready' && 'Click the button below to start the mapping process'}
                {status === 'starting' && 'Initializing field mapping engine...'}
                {status === 'processing' && 'Processing field mappings and populating data...'}
                {status === 'completed' && 'All mappings have been successfully processed'}
                {status === 'error' && 'An error occurred during execution'}
              </p>
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        {(status === 'processing' || status === 'starting') && (
          <div className="mb-4">
            <div className="flex justify-between text-sm text-gray-600 mb-1">
              <span>Progress</span>
              <span>{progress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-primary-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-4">
            <div className="flex">
              <svg className="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <div className="ml-3">
                <h4 className="text-sm font-medium text-red-800">Execution Error</h4>
                <p className="text-sm text-red-700 mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Results Summary */}
        {result && (
          <div className="bg-green-50 border border-green-200 rounded-md p-4 mb-4">
            <h4 className="text-sm font-medium text-green-800 mb-2">Execution Results</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-green-700">Mappings Processed</p>
                <p className="text-lg font-semibold text-green-800">{result.mappings_processed}</p>
              </div>
              <div>
                <p className="text-sm text-green-700">Values Populated</p>
                <p className="text-lg font-semibold text-green-800">{result.values_populated}</p>
              </div>
              <div>
                <p className="text-sm text-green-700">Success Rate</p>
                <p className="text-lg font-semibold text-green-800">{result.success_rate?.toFixed(1)}%</p>
              </div>
              <div>
                <p className="text-sm text-green-700">Errors</p>
                <p className="text-lg font-semibold text-green-800">{result.errors?.length || 0}</p>
              </div>
            </div>
          </div>
        )}

        {/* Action Button */}
        <div className="flex justify-center">
          {status === 'ready' && (
            <button
              onClick={startExecution}
              disabled={executing}
              className="px-8 py-3 bg-primary-600 text-white rounded-md font-medium hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              Execute Field Mapping
            </button>
          )}
          
          {status === 'error' && (
            <button
              onClick={startExecution}
              className="px-8 py-3 bg-red-600 text-white rounded-md font-medium hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              Retry Execution
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ExecutionStatus;
