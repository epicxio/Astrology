import React, { useState } from 'react';
import { Horoscope } from '../types/horoscope';
import { format } from 'date-fns';
import PlanetaryStrengthCard from './horoscope/PlanetaryStrengthCard';

interface HoroscopeRecordProps {
  horoscope: Horoscope;
  onDownload: (id: number) => void;
}

const HoroscopeRecord: React.FC<HoroscopeRecordProps> = ({ horoscope, onDownload }) => {
  const [showPlanetaryPositions, setShowPlanetaryPositions] = useState(false);
  const [showPlanetaryStrengths, setShowPlanetaryStrengths] = useState(false);

  const formatDate = (date: string) => {
    return format(new Date(date), 'dd/MM/yyyy');
  };

  const formatTime = (time: string) => {
    return format(new Date(`2000-01-01T${time}`), 'hh:mm a');
  };

  const renderPlanetaryStrengthsModal = () => {
    if (!horoscope.planetary_strengths) return null;
    
    const strengths = typeof horoscope.planetary_strengths === 'string' 
      ? JSON.parse(horoscope.planetary_strengths)
      : horoscope.planetary_strengths;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6 max-w-4xl w-full max-h-[80vh] overflow-y-auto">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-semibold">Planetary Strengths</h3>
            <button
              onClick={() => setShowPlanetaryStrengths(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>
          <div className="space-y-6">
            {Object.entries(strengths).map(([planet, data]: [string, any]) => (
              <PlanetaryStrengthCard
                key={planet}
                planet={planet}
                strengths={data}
                planetaryPositions={horoscope.planetary_positions}
              />
            ))}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-4">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-xl font-semibold mb-2">{horoscope.name}</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-gray-600">Date of Birth</p>
              <p className="font-medium">{formatDate(horoscope.date_of_birth)}</p>
            </div>
            <div>
              <p className="text-gray-600">Time of Birth</p>
              <p className="font-medium">{formatTime(horoscope.time_of_birth)}</p>
            </div>
            <div>
              <p className="text-gray-600">Place of Birth</p>
              <p className="font-medium">{horoscope.place}</p>
            </div>
            <div>
              <p className="text-gray-600">Rashi</p>
              <p className="font-medium">{horoscope.rashi}</p>
            </div>
          </div>
        </div>
        <div className="flex space-x-2">
          {horoscope.planetary_positions && (
            <button
              onClick={() => setShowPlanetaryPositions(true)}
              className="p-2 text-blue-600 hover:text-blue-800"
              title="View Planetary Positions"
            >
              <span className="text-xl">★</span>
            </button>
          )}
          {horoscope.planetary_strengths && (
            <button
              onClick={() => setShowPlanetaryStrengths(true)}
              className="p-2 text-green-600 hover:text-green-800"
              title="View Planetary Strengths"
            >
              <span className="text-xl">📊</span>
            </button>
          )}
          <button
            onClick={() => onDownload(horoscope.id)}
            className="p-2 text-gray-600 hover:text-gray-800"
            title="Download PDF"
          >
            <span className="text-xl">↓</span>
          </button>
        </div>
      </div>

      {showPlanetaryPositions && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-semibold">Planetary Positions</h3>
              <button
                onClick={() => setShowPlanetaryPositions(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
            <div className="whitespace-pre-wrap font-mono text-sm">
              {horoscope.planetary_positions}
            </div>
          </div>
        </div>
      )}

      {showPlanetaryStrengths && renderPlanetaryStrengthsModal()}
    </div>
  );
};

export default HoroscopeRecord; 