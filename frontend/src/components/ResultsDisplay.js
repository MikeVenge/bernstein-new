import React, { useState } from 'react';
import axios from 'axios';

const ResultsDisplay = ({ jobId, executionResult, onReset }) => {
  const [downloading, setDownloading] = useState({});

  const downloadFile = async (fileType, filename) => {
    try {
      setDownloading(prev => ({ ...prev, [fileType]: true }));

      const response = await axios.get(`/api/download-result/${jobId}/${fileType}`, {
        responseType: 'blob'
      });

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

    } catch (err) {
      console.error('Download failed:', err);
      alert('Download failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setDownloading(prev => ({ ...prev, [fileType]: false }));
    }
  };

  const cleanupJob = async () => {
    try {
      await axios.delete(`/api/cleanup-job/${jobId}`);
      onReset();
    } catch (err) {
      console.error('Cleanup failed:', err);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Mapping Results</h2>
        <p className="text-gray-600">
          Your field mapping has been completed successfully. Download the results below.
        </p>
      </div>

      {/* Success Banner */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-6">
        <div className="flex items-center">
          <svg className="w-8 h-8 text-green-500 mr-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
          <div>
            <h3 className="text-lg font-medium text-green-800">Field Mapping Completed Successfully!</h3>
            <p className="text-sm text-green-700 mt-1">
              {executionResult?.values_populated} fields populated with {executionResult?.success_rate?.toFixed(1)}% success rate
            </p>
          </div>
        </div>
      </div>

      {/* Results Summary */}
      <div className="bg-white border rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Execution Summary</h3>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-primary-600">{executionResult?.mappings_processed}</div>
            <div className="text-sm text-gray-500">Mappings Processed</div>
          </div>
          
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">{executionResult?.values_populated}</div>
            <div className="text-sm text-gray-500">Values Populated</div>
          </div>
          
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">{executionResult?.success_rate?.toFixed(1)}%</div>
            <div className="text-sm text-gray-500">Success Rate</div>
          </div>
          
          <div className="text-center">
            <div className="text-3xl font-bold text-red-600">{executionResult?.errors?.length || 0}</div>
            <div className="text-sm text-gray-500">Errors</div>
          </div>
        </div>

        {/* Sheet Breakdown */}
        {executionResult?.sheet_stats && Object.keys(executionResult.sheet_stats).length > 0 && (
          <div className="mt-6">
            <h4 className="text-sm font-medium text-gray-900 mb-2">Population by Source Sheet</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(executionResult.sheet_stats).map(([sheet, count]) => (
                <div key={sheet} className="bg-gray-50 rounded-md p-3">
                  <div className="text-sm font-medium text-gray-900">{sheet}</div>
                  <div className="text-lg font-bold text-gray-700">{count} fields</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Download Options */}
      <div className="bg-white border rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Download Results</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Populated Excel File */}
          <div className="border rounded-lg p-4">
            <div className="flex items-center mb-2">
              <svg className="w-6 h-6 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-5L9 2H4z" clipRule="evenodd" />
              </svg>
              <h4 className="text-sm font-medium text-gray-900">Populated Excel File</h4>
            </div>
            <p className="text-xs text-gray-500 mb-3">
              Destination file with all mapped data populated
            </p>
            <button
              onClick={() => downloadFile('excel', executionResult?.output_file)}
              disabled={downloading.excel}
              className="w-full px-3 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50"
            >
              {downloading.excel ? 'Downloading...' : 'Download Excel'}
            </button>
          </div>

          {/* Audit Trail */}
          <div className="border rounded-lg p-4">
            <div className="flex items-center mb-2">
              <svg className="w-6 h-6 text-blue-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" clipRule="evenodd" />
              </svg>
              <h4 className="text-sm font-medium text-gray-900">Audit Trail</h4>
            </div>
            <p className="text-xs text-gray-500 mb-3">
              Detailed log of all mapping operations
            </p>
            <button
              onClick={() => downloadFile('audit', executionResult?.audit_file)}
              disabled={downloading.audit}
              className="w-full px-3 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {downloading.audit ? 'Downloading...' : 'Download Audit'}
            </button>
          </div>

          {/* All Files */}
          <div className="border rounded-lg p-4">
            <div className="flex items-center mb-2">
              <svg className="w-6 h-6 text-purple-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clipRule="evenodd" />
              </svg>
              <h4 className="text-sm font-medium text-gray-900">All Files (ZIP)</h4>
            </div>
            <p className="text-xs text-gray-500 mb-3">
              Download all result files in a single ZIP archive
            </p>
            <button
              onClick={() => downloadFile('all', `mapping_results_${jobId}.zip`)}
              disabled={downloading.all}
              className="w-full px-3 py-2 text-sm font-medium text-white bg-purple-600 rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:opacity-50"
            >
              {downloading.all ? 'Downloading...' : 'Download All'}
            </button>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="flex justify-center space-x-4">
        <button
          onClick={onReset}
          className="px-6 py-3 text-gray-700 bg-white border border-gray-300 rounded-md font-medium hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          Start New Mapping
        </button>
        
        <button
          onClick={cleanupJob}
          className="px-6 py-3 text-red-700 bg-red-50 border border-red-200 rounded-md font-medium hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-500"
        >
          Cleanup & Reset
        </button>
      </div>

      {/* Errors List */}
      {executionResult?.errors && executionResult.errors.length > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <h4 className="text-sm font-medium text-yellow-800 mb-2">
            Warnings ({executionResult.errors.length})
          </h4>
          <div className="max-h-32 overflow-y-auto">
            {executionResult.errors.slice(0, 10).map((error, index) => (
              <p key={index} className="text-xs text-yellow-700">{error}</p>
            ))}
            {executionResult.errors.length > 10 && (
              <p className="text-xs text-yellow-600 italic">
                ... and {executionResult.errors.length - 10} more errors
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;
