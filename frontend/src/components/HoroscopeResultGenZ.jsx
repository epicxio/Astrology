import React, { useState, useEffect, useRef } from 'react';
import { apiService } from '../services/api';
import { downloadPDF, getReportFilename } from '../utils/pdfUtils';
import { Modal } from 'antd';
import PlanetaryStrengthCard from './horoscope/PlanetaryStrengthCard';

const PLANET_ORDER = [
  'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu', 'Ascendant'
];
const PLANET_ICONS = {
  Sun: '☉',
  Moon: '☽',
  Mars: '♂',
  Mercury: '☿',
  Jupiter: '♃',
  Venus: '♀',
  Saturn: '♄',
  Rahu: '☊',
  Ketu: '☋',
  Ascendant: '↑',
};
const PLANET_LABELS = {
  Sun: 'Sun (Surya)',
  Moon: 'Moon (Chandra)',
  Mars: 'Mars (Mangala)',
  Mercury: 'Mercury (Budha)',
  Jupiter: 'Jupiter (Guru)',
  Venus: 'Venus (Shukra)',
  Saturn: 'Saturn (Shani)',
  Rahu: 'Rahu (North Node)',
  Ketu: 'Ketu (South Node)',
  Ascendant: 'Ascendant (Lagna)',
};
const FIELD_TOOLTIPS = {
  dms: 'Absolute position in the zodiac (DMS)',
  dms_in_sign: 'Degree within the current sign',
  rasi: 'Zodiac sign (Vedic)',
  rasi_lord: 'Ruler of the sign',
  nakshatra: 'Lunar mansion',
  nakshatra_lord: 'Ruler of the nakshatra',
  retrograde: 'Is the planet in retrograde motion? (℞)',
};
const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'ml', label: 'Malayalam' },
  { code: 'ta', label: 'Tamil' },
];

export default function HoroscopeResultGenZ({ result, avatar }) {
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [language, setLanguage] = useState('en');
  const [showModal, setShowModal] = useState(false);
  const confettiRef = useRef(null);

  useEffect(() => {
    // Confetti animation when result is shown
    if (result && typeof window !== 'undefined') {
      import('canvas-confetti').then((confetti) => {
        confetti.default({
          particleCount: 120,
          spread: 80,
          origin: { y: 0.6 },
          colors: ['#a21caf', '#2563eb', '#f472b6', '#facc15', '#38bdf8'],
        });
      });
    }
  }, [result]);

  if (!result) return null;

  const handleDownload = async () => {
    setDownloading(true);
    setError(null);
    setSuccess(false);
    try {
      // Call the backend API
      const blob = await apiService.getHoroscopeReport(result.id, language);

      // Check if the response is a PDF
      if (blob.type !== "application/pdf") {
        // Try to read error message from blob
        const text = await blob.text();
        throw new Error(text || "Server did not return a PDF file.");
      }

      // Use the robust download utility
      downloadPDF(blob, getReportFilename('horoscope', language));
      setSuccess(true);
    } catch (err) {
      // Try to extract error message
      let msg = "Failed to download PDF.";
      if (err instanceof Error) {
        msg = err.message;
      }
      setError(msg);
    } finally {
      setDownloading(false);
      setTimeout(() => setSuccess(false), 3000);
    }
  };

  return (
    <div className="flex flex-col items-center w-full animate-fade-in">
      <div className="text-6xl mb-2">{avatar}</div>
      <div className="text-2xl font-bold mb-2 text-black">{result.name}</div>
      <div className="flex flex-wrap gap-4 justify-center mb-4">
        <div className="rounded-xl px-4 py-2 bg-white/80 text-black shadow">Rashi: <span className="font-bold text-pink-500">{result.rashi}</span></div>
        <div className="rounded-xl px-4 py-2 bg-white/80 text-black shadow">Nakshatra: <span className="font-bold text-pink-500">{result.nakshatra}</span></div>
        <div className="rounded-xl px-4 py-2 bg-white/80 text-black shadow">Lagna: <span className="font-bold text-pink-500">{result.lagna}</span></div>
      </div>
      <div className="w-full max-w-2xl bg-white/80 rounded-2xl p-4 mb-4 shadow-lg flex flex-col items-center">
        <div className="text-lg font-semibold mb-4 text-black">Planetary Positions</div>
        <button
          className="px-4 py-2 rounded-xl bg-gradient-to-r from-pink-500 to-blue-500 text-white font-bold shadow-lg hover:scale-105 active:scale-95 transition-all duration-200 mb-2"
          onClick={() => setShowModal(true)}
        >
          View All Planetary Positions
        </button>
      </div>
      {/* South Indian Rasi Chart - moved above Planetary Strength Analysis */}
      {result.id && (
        <div className="w-full flex flex-col items-center mt-6 mb-2">
          <div className="text-lg font-semibold mb-2 text-black">South Indian Style Rasi Chart</div>
          <img
            src={`/api/horoscope/chart/south/${result.id}`}
            alt="South Indian Rasi Chart"
            className="max-w-xs w-full border-2 border-pink-300 rounded-2xl bg-white/80 shadow-lg"
            style={{ background: '#fff8e1' }}
          />
        </div>
      )}
      {/* Planetary Strength Analysis UI */}
      {result.planetary_strengths && Object.keys(result.planetary_strengths).length > 0 && (
        <div className="w-full max-w-2xl mt-4">
          <h2 className="text-xl font-bold mb-4 text-center text-black">Planetary Strength Analysis</h2>
          <div className="space-y-6">
            {Object.entries(result.planetary_strengths).map(([planet, strengths]) => (
              <PlanetaryStrengthCard
                key={planet}
                planet={planet}
                strengths={strengths}
                planetaryPositions={result.planetary_positions}
              />
            ))}
          </div>
        </div>
      )}
      <Modal
        open={showModal}
        onCancel={() => setShowModal(false)}
        title={`Planetary Positions for ${result.name}`}
        footer={null}
        width={800}
        className="backdrop-blur-xl"
      >
        <div className="overflow-x-auto mt-2">
          <table className="min-w-[500px] w-full text-xs sm:text-sm bg-white rounded-2xl shadow-lg">
            <thead>
              <tr className="bg-gradient-to-r from-blue-500/80 to-pink-400/80 text-white">
                <th className="p-2 font-bold">Planet</th>
                <th className="p-2 font-bold">Positions</th>
                <th className="p-2 font-bold">Degree</th>
                <th className="p-2 font-bold">Rasi</th>
                <th className="p-2 font-bold">Rasi Lord</th>
                <th className="p-2 font-bold">Nakshatra</th>
                <th className="p-2 font-bold">Nakshatra Lord</th>
                <th className="p-2 font-bold">Retrograde</th>
              </tr>
            </thead>
            <tbody>
              {PLANET_ORDER.map((planet) => {
                const pos = result.planetary_positions?.[planet];
                if (!pos) return null;
                return (
                  <tr key={planet} className="border-b border-gray-200 text-gray-900 hover:bg-blue-50 transition">
                    <td className="p-2 font-semibold">{planet}</td>
                    <td className="p-2">{pos.dms}</td>
                    <td className="p-2">{pos.dms_in_sign || (pos.degree_in_sign !== undefined ? pos.degree_in_sign : '')}</td>
                    <td className="p-2">{pos.rasi}</td>
                    <td className="p-2">{pos.rasi_lord}</td>
                    <td className="p-2">{pos.nakshatra}</td>
                    <td className="p-2">{pos.nakshatra_lord}</td>
                    <td className="p-2">{pos.retrograde ? '℞' : ''}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Modal>
      {/* Language Selector and Download Button */}
      <div className="flex flex-col items-center gap-2 mt-2 w-full">
        <div className="flex flex-row items-center justify-center gap-2 w-full">
          <select
            className="rounded-xl px-2 sm:px-3 py-1 sm:py-2 bg-white/80 text-black focus:outline-none focus:ring-2 focus:ring-blue-400 text-sm sm:text-base"
            value={language}
            onChange={e => setLanguage(e.target.value)}
            disabled={downloading}
          >
            {LANGUAGES.map(lang => (
              <option key={lang.code} value={lang.code}>{lang.label}</option>
            ))}
          </select>
        </div>
        <div className="flex justify-center w-full mt-2">
          <button
            className="px-6 py-2 rounded-xl bg-gradient-to-r from-pink-500 to-blue-500 text-white font-bold shadow-lg hover:scale-105 active:scale-95 transition-all duration-200 disabled:opacity-60 text-base"
            onClick={handleDownload}
            disabled={downloading}
            style={{ minWidth: 220 }}
          >
            {downloading ? 'Downloading...' : 'Download PDF Report'}
          </button>
        </div>
      </div>
      {success && <div className="text-green-400 mt-2">PDF downloaded successfully!</div>}
      {error && <div className="text-red-400 mt-2">{error}</div>}
      {/* Confetti canvas (handled by canvas-confetti) */}
      <div ref={confettiRef} />
    </div>
  );
} 