import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MappingConfiguration = ({ uploadedFiles, onConfigurationSet, jobId }) => {
  const [config, setConfig] = useState({
    targetColumn: 71,
    dataColumn: 'CO'
  });
  const [mappingPreview, setMappingPreview] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMappingPreview();
  }, [jobId]);

  const loadMappingPreview = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/mapping-preview/${jobId}`);
      setMappingPreview(response.data);
    } catch (err) {
      console.error('Failed to load mapping preview:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleConfigChange = (field, value) => {
    setConfig(prev => ({ ...prev, [field]: value }));
  };

  const handleContinue = () => {
    onConfigurationSet(config);
  };

  const columnOptions = [
    { value: 70, label: 'Column 70 (BR)' },
    { value: 71, label: 'Column 71 (BS)' },
    { value: 72, label: 'Column 72 (BT)' },
    { value: 73, label: 'Column 73 (BU)' },
    { value: 74, label: 'Column 74 (BV)' },
    { value: 75, label: 'Column 75 (BW)' },
    { value: 80, label: 'Column 80 (CB)' }
  ];

  const dataColumnOptions = [
    { value: 'BR', label: 'BR (Column 70) - Typically Q1 data' },
    { value: 'BS', label: 'BS (Column 71) - Typically Q2 data' },
    { value: 'CO', label: 'CO (Column 93) - Current default' },
    { value: 'BT', label: 'BT (Column 72)' },
    { value: 'BU', label: 'BU (Column 73)' }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Configure Mapping Parameters</h2>
        <p className="text-gray-600">
          Set the target destination column and source data column for the field mapping process.
        </p>
      </div>

      {/* File Summary */}
      <div className="bg-gray-50 rounded-lg p-4">
        <h3 className="text-lg font-medium text-gray-900 mb-3">Uploaded Files</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Object.entries(uploadedFiles).map(([type, fileInfo]) => (
            <div key={type} className="bg-white rounded-md p-3 border">
              <div className="flex items-center">
                <svg className="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                <div>
                  <p className="text-sm font-medium text-gray-900 capitalize">{type} File</p>
                  <p className="text-xs text-gray-500">{fileInfo.filename}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Configuration Form */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Target Column (DESTINATION)
          </label>
          <select
            value={config.targetColumn}
            onChange={(e) => handleConfigChange('targetColumn', parseInt(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            {columnOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <p className="text-xs text-gray-500 mt-1">
            Column in destination file where mapped data will be written
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Data Column (SOURCE)
          </label>
          <select
            value={config.dataColumn}
            onChange={(e) => handleConfigChange('dataColumn', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            {dataColumnOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <p className="text-xs text-gray-500 mt-1">
            Column in source file where data will be read from
          </p>
        </div>
      </div>

      {/* Data Flow Visualization */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-sm font-medium text-blue-800 mb-2">Data Flow</h3>
        <div className="flex items-center justify-center space-x-4">
          <div className="text-center">
            <div className="bg-blue-100 rounded-md px-3 py-2">
              <p className="text-sm font-medium text-blue-800">Source File</p>
              <p className="text-xs text-blue-600">Column {config.dataColumn}</p>
            </div>
          </div>
          <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
          <div className="text-center">
            <div className="bg-green-100 rounded-md px-3 py-2">
              <p className="text-sm font-medium text-green-800">Destination File</p>
              <p className="text-xs text-green-600">Column {config.targetColumn}</p>
            </div>
          </div>
        </div>
        <p className="text-xs text-blue-600 text-center mt-2">
          Source tracking will be added to Column {config.targetColumn + 1}
        </p>
      </div>

      {/* Mapping Preview */}
      {loading ? (
        <div className="bg-gray-50 rounded-lg p-8 text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
          <p className="text-gray-500 mt-2">Loading mapping preview...</p>
        </div>
      ) : mappingPreview ? (
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-medium text-gray-900 mb-3">Mapping Preview</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div className="bg-white rounded-md p-3 border">
              <p className="text-sm font-medium text-gray-900">Total Mappings</p>
              <p className="text-2xl font-bold text-primary-600">{mappingPreview.total_mappings}</p>
            </div>
            
            <div className="bg-white rounded-md p-3 border">
              <p className="text-sm font-medium text-gray-900">Source Sheets</p>
              <p className="text-2xl font-bold text-primary-600">{Object.keys(mappingPreview.source_sheets || {}).length}</p>
            </div>
            
            <div className="bg-white rounded-md p-3 border">
              <p className="text-sm font-medium text-gray-900">Mapping Types</p>
              <p className="text-2xl font-bold text-primary-600">{Object.keys(mappingPreview.mapping_types || {}).length}</p>
            </div>
          </div>

          {/* Sample Mappings */}
          <div className="bg-white rounded-md border overflow-hidden">
            <div className="px-4 py-3 bg-gray-50 border-b">
              <h4 className="text-sm font-medium text-gray-900">Sample Mappings</h4>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Dest Row</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Destination Field</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Source Field</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {mappingPreview.preview?.slice(0, 5).map((mapping, index) => (
                    <tr key={index}>
                      <td className="px-4 py-2 text-sm text-gray-900">{mapping.Dest_Row || mapping.Dest_Row_Number}</td>
                      <td className="px-4 py-2 text-sm text-gray-900">{mapping.Dest_Field || mapping.Dest_Field_Name}</td>
                      <td className="px-4 py-2 text-sm text-gray-900">{mapping.Source_Field || mapping.Source_Field_Name}</td>
                      <td className="px-4 py-2 text-sm text-gray-500">{mapping.Mapping_Type || 'Standard'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
          <p className="text-sm text-yellow-700">Unable to load mapping preview</p>
        </div>
      )}

      {/* Continue Button */}
      <div className="flex justify-center">
        <button
          onClick={handleContinue}
          className="px-8 py-3 bg-primary-600 text-white rounded-md font-medium hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          Continue to Execution
        </button>
      </div>
    </div>
  );
};

export default MappingConfiguration;
