import React from 'react';
import { TrophyOutlined, StarOutlined } from '@ant-design/icons';

interface PlanetaryStrengthCardProps {
  planet: string;
  strengths: {
    [key: string]: any;
  };
  planetaryPositions: any;
}

const PLANET_ICONS: { [key: string]: string } = {
  Sun: '☉',
  Moon: '☽',
  Mars: '♂',
  Mercury: '☿',
  Jupiter: '♃',
  Venus: '♀',
  Saturn: '♄',
};

const PlanetaryStrengthCard: React.FC<PlanetaryStrengthCardProps> = ({
  planet,
  strengths,
  planetaryPositions,
}) => {
  const getStrengthColor = (score: number) => {
    if (score >= 8) return 'text-green-600';
    if (score >= 5) return 'text-yellow-600';
    if (score >= 0) return 'text-orange-600';
    return 'text-red-600';
  };

  const getStrengthDescription = (type: string, score: number) => {
    switch (type) {
      case 'sthana_bala':
        return `Positional strength in ${planetaryPositions[planet].rasi}`;
      case 'dig_bala':
        return `Directional strength in ${planetaryPositions[planet].rasi}`;
      case 'drik_bala':
        return 'Aspectual strength from other planets';
      case 'conjunction':
        return 'Strength from planetary conjunctions';
      case 'avastha':
        return `Planetary state (${planetaryPositions[planet].retrograde ? 'Retrograde' : 'Direct'})`;
      case 'navamsa':
        return 'Navamsa chart strength';
      default:
        return '';
    }
  };

  function removeScoreFromExplanation(explanation: string) {
    if (!explanation) return '';
    // Remove patterns like 'Sthana Bala: 0.0/10.0. ', 'Drik Bala: 8.0/10.0. ', etc.
    return explanation.replace(/^[A-Za-z ]+: [-+]?[0-9]*\.?[0-9]+\/[0-9]*\.?[0-9]+\. ?/, '');
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 max-w-2xl w-full">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <span className="text-3xl">{PLANET_ICONS[planet]}</span>
          <h2 className="text-2xl font-bold text-gray-800">{planet}</h2>
        </div>
        <div className="flex items-center space-x-2">
          <TrophyOutlined className="text-2xl text-yellow-500" />
          <span className={`text-2xl font-bold ${getStrengthColor(strengths.total)}`}>
            {strengths.total.toFixed(1)}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {[
          ['sthana_bala', 'Sthana Bala', 10],
          ['dig_bala', 'Dig Bala', 10],
          ['drik_bala', 'Drik Bala', 10],
          ['conjunction', 'Conjunction', 5],
          ['avastha', 'Avastha', 5],
          ['navamsa', 'Navamsa', 10],
        ].map(([type, label, max]) => (
          <div key={type} className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="font-semibold text-gray-700 capitalize">{label}</span>
              <div className="flex items-center space-x-1">
                <StarOutlined className="text-yellow-500" />
                {type === 'navamsa' && (strengths[type] === null || strengths[type] === undefined || isNaN(Number(strengths[type]))) ? (
                  <span className="font-bold text-gray-400 flex items-center h-full" style={{minHeight: '1.5em'}}>
                    No Score
                  </span>
                ) : (
                  <span className={`font-bold ${getStrengthColor(strengths[type])}`}>{strengths[type]?.toFixed(1)}<span>{`/${max}`}</span></span>
                )}
              </div>
            </div>
            <p className="text-sm text-gray-600">
              {removeScoreFromExplanation(strengths[`${type}_explanation`])}
            </p>
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-semibold text-gray-800 mb-2">Interpretation</h3>
        <pre className="text-gray-600 whitespace-pre-line" style={{ fontFamily: 'inherit', background: 'none', padding: 0, margin: 0, border: 'none' }}>
          {strengths.summary ||
            (strengths.total >= 8
              ? `${planet} is very strong in this chart, indicating positive influences.`
              : strengths.total >= 5
              ? `${planet} has moderate strength, suggesting balanced influences.`
              : `${planet} is relatively weak, suggesting challenges in its significations.`)}
        </pre>
      </div>
    </div>
  );
};

export default PlanetaryStrengthCard; 