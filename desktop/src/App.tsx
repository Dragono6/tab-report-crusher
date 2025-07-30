import React, { useState } from 'react';
import { invoke } from '@tauri-apps/api/tauri';
import './App.css';
import ModelHub from './components/ModelHub';
import ToleranceControlCenter from './components/ToleranceControlCenter';
import { Model, supportedModels, ToleranceProfile, DroppedFile } from './types';

// Placeholder for the default profile data.
// In the real app, this would be fetched from the local SQLite DB.
const defaultProfile: ToleranceProfile = {
  name: "Manager Default",
  tolerances: {
    "Supply": { type: "percent", value: 10 },
    "Return": { type: "percent", value: 10 },
    "Exhaust": { type: "percent", value: 15 },
    "OA": { type: "percent", value: 5 },
    "Coil_dT": { type: "absolute", value: 2, unit: "F" }
  }
};

function App() {
  const [file, setFile] = useState<DroppedFile | null>(null);
  const [reviewResult, setReviewResult] = useState<any>(null); // To store findings
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [selectedModel, setSelectedModel] = useState<Model>(supportedModels[0]);
  const [apiKey, setApiKey] = useState<string>('');
  const [activeProfile, setActiveProfile] = useState<ToleranceProfile>(defaultProfile);


  const handleDrop = async (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setFile(null);
    setReviewResult(null);
    setError(null);
    setIsProcessing(true);

    if (event.dataTransfer.items) {
      if (event.dataTransfer.items[0].kind === 'file') {
        const droppedFile = event.dataTransfer.items[0].getAsFile() as DroppedFile | null;
        if (droppedFile) {
          setFile(droppedFile);
          try {
            // Send the file path, API key, and model name to the Tauri backend
            const resultJson = await invoke('run_review', {
              filePath: droppedFile.path,
              apiKey: apiKey,
              modelName: selectedModel.id
            });
            setReviewResult(JSON.parse(resultJson as string));
          } catch (e) {
            setError(e as string);
          } finally {
            setIsProcessing(false);
          }
        }
      }
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
  };

  return (
    <div className="container mx-auto p-4 bg-gray-900 text-white min-h-screen">
      <h1 className="text-3xl font-bold mb-4">TAB Report Crusher</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <ModelHub 
          selectedModel={selectedModel}
          setSelectedModel={setSelectedModel}
          apiKey={apiKey}
          setApiKey={setApiKey}
        />
        <ToleranceControlCenter profile={activeProfile} />
      </div>

      <div 
        className="w-full h-64 border-4 border-dashed border-gray-600 rounded-lg flex items-center justify-center text-gray-400"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        {isProcessing ? (
          <p>Processing: {file?.name}...</p>
        ) : file ? (
          <p>File ready for review: {file.name}</p>
        ) : (
          <p>Drag & Drop a PDF or Excel Report Here</p>
        )}
      </div>

      {error && (
        <div className="bg-red-800 text-white p-4 rounded-lg mt-4">
          <h3 className="font-bold">Error</h3>
          <p>{error}</p>
        </div>
      )}

      {reviewResult && reviewResult.findings && (
        <div className="bg-gray-800 p-4 rounded-lg mt-4">
          <h3 className="font-bold text-xl mb-2">Review Findings</h3>
          <ul>
            {reviewResult.findings.map((finding: any, index: number) => (
              <li key={index} className="mb-2 p-2 bg-gray-700 rounded-md">
                <span className="font-bold">Page {finding.page}:</span> {finding.issue}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App; 