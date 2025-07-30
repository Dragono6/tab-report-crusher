import React, { useState, useEffect } from 'react';
import { Store } from 'tauri-plugin-store-api';
import { Model, supportedModels } from '../types';

// Create a new store instance
const store = new Store('.settings.dat');

interface ModelHubProps {
  selectedModel: Model;
  setSelectedModel: (model: Model) => void;
  apiKey: string;
  setApiKey: (key: string) => void;
}

const ModelHub: React.FC<ModelHubProps> = ({ selectedModel, setSelectedModel, apiKey, setApiKey }) => {
  useEffect(() => {
    // Load the saved API key when the component mounts
    const loadApiKey = async () => {
      const savedKey = await store.get<string>('apiKey');
      if (savedKey) {
        setApiKey(savedKey);
      }
    };
    loadApiKey();
  }, [setApiKey]);

  const handleApiKeyChange = async (newKey: string) => {
    setApiKey(newKey);
    // Save the API key to the store whenever it changes
    await store.set('apiKey', newKey);
    await store.save(); // Persist the store to disk
  };

  const handleModelChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const modelId = event.target.value;
    const model = supportedModels.find(m => m.id === modelId);
    if (model) {
      setSelectedModel(model);
    }
  };

  return (
    <div className="bg-gray-800 p-4 rounded-lg mb-4">
      <h2 className="text-xl font-bold mb-2">Model Hub</h2>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="model-select" className="block text-sm font-medium text-gray-300 mb-1">
            Select AI Model
          </label>
          <select
            id="model-select"
            value={selectedModel.id}
            onChange={handleModelChange}
            className="w-full bg-gray-700 border border-gray-600 rounded-md p-2 text-white focus:ring-blue-500 focus:border-blue-500"
          >
            {supportedModels.map(model => (
              <option key={model.id} value={model.id}>
                {model.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="api-key-input" className="block text-sm font-medium text-gray-300 mb-1">
            API Key
          </label>
          <input
            type="password"
            id="api-key-input"
            value={apiKey}
            onChange={(e) => handleApiKeyChange(e.target.value)}
            placeholder="Enter your API key"
            className="w-full bg-gray-700 border border-gray-600 rounded-md p-2 text-white focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>
    </div>
  );
};

export default ModelHub; 