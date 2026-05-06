import React, { useState, useEffect } from 'react';
import { dataAPI } from '../services/api';

const StateDistrictTest = () => {
  const [states, setStates] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [selectedState, setSelectedState] = useState('');
  const [selectedDistrict, setSelectedDistrict] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadStates = async () => {
      try {
        console.log('Loading states...');
        const response = await dataAPI.getStates();
        console.log('States response:', response.data);
        setStates(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Failed to load states:', err);
        setError('Failed to load states: ' + err.message);
        setLoading(false);
      }
    };
    
    loadStates();
  }, []);

  const handleStateSelect = (stateName) => {
    console.log('Selecting state:', stateName);
    setSelectedState(stateName);
    
    const selectedStateObj = states.find(s => s.name === stateName);
    console.log('Found state object:', selectedStateObj);
    
    if (selectedStateObj && selectedStateObj.districts) {
      setDistricts(selectedStateObj.districts);
      console.log('Districts loaded:', selectedStateObj.districts);
    } else {
      setDistricts([]);
      console.log('No districts found for state');
    }
  };

  const handleDistrictSelect = (districtName) => {
    console.log('Selecting district:', districtName);
    setSelectedDistrict(districtName);
  };

  if (loading) {
    return <div className="p-4">Loading states...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>;
  }

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">State/District Selection Test</h2>
      
      {/* States Selection */}
      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">Select State:</label>
        <select 
          value={selectedState} 
          onChange={(e) => handleStateSelect(e.target.value)}
          className="w-full p-2 border rounded"
        >
          <option value="">-- Select State --</option>
          {states.map(state => (
            <option key={state.code} value={state.name}>
              {state.name} ({state.districts.length} districts)
            </option>
          ))}
        </select>
      </div>

      {/* Districts Selection */}
      {selectedState && (
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">
            Select District (from {selectedState}):
          </label>
          <select 
            value={selectedDistrict} 
            onChange={(e) => handleDistrictSelect(e.target.value)}
            className="w-full p-2 border rounded"
          >
            <option value="">-- Select District --</option>
            {districts.map((district, index) => (
              <option key={index} value={district}>
                {district}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Display Selection */}
      {selectedState && selectedDistrict && (
        <div className="bg-green-100 p-4 rounded">
          <h3 className="font-bold mb-2">Current Selection:</h3>
          <p><strong>State:</strong> {selectedState}</p>
          <p><strong>District:</strong> {selectedDistrict}</p>
        </div>
      )}

      {/* Debug Info */}
      <div className="mt-6 bg-gray-100 p-4 rounded">
        <h3 className="font-bold mb-2">Debug Information:</h3>
        <p>States loaded: {states.length}</p>
        <p>Districts available: {districts.length}</p>
        <p>Selected State: {selectedState || 'None'}</p>
        <p>Selected District: {selectedDistrict || 'None'}</p>
      </div>

      {/* Test Buttons */}
      <div className="mt-4 flex gap-2">
        <button 
          onClick={() => handleStateSelect('Tamil Nadu')}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Test Tamil Nadu
        </button>
        <button 
          onClick={() => handleStateSelect('Karnataka')}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Test Karnataka
        </button>
        <button 
          onClick={() => {
            setSelectedState('');
            setSelectedDistrict('');
            setDistricts([]);
          }}
          className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
        >
          Clear All
        </button>
      </div>
    </div>
  );
};

export default StateDistrictTest;