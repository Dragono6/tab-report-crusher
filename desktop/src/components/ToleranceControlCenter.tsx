import React from 'react';
import { ToleranceProfile, Tolerance } from '../types';

interface ToleranceControlCenterProps {
  profile: ToleranceProfile;
  // TODO: Add props for editing capabilities
}

const ToleranceControlCenter: React.FC<ToleranceControlCenterProps> = ({ profile }) => {
  return (
    <div className="bg-gray-800 p-4 rounded-lg">
      <h2 className="text-xl font-bold mb-2">Tolerance Control Center</h2>
      <p className="text-md text-gray-400 mb-4">Profile: <span className="font-semibold">{profile.name}</span></p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {(Object.entries(profile.tolerances) as [string, Tolerance][]).map(([key, tolerance]) => (
          <div key={key} className="bg-gray-700 p-3 rounded-md">
            <h3 className="font-bold text-lg">{key.replace('_', ' ')}</h3>
            <p className="text-2xl">
              {tolerance.type === 'percent' ? `±${tolerance.value}%` : `±${tolerance.value} ${tolerance.unit || ''}`}
            </p>
          </div>
        ))}
      </div>

      <div className="mt-4">
        <button 
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2"
          // TODO: onClick handler for importing a spec PDF
        >
          Import TAB Spec (PDF)
        </button>
        <button 
          className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
          // TODO: onClick handler for editing the profile (manager only)
        >
          Edit Profile
        </button>
      </div>
    </div>
  );
};

export default ToleranceControlCenter; 