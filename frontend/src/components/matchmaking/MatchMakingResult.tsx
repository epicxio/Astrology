import React, { useState, useEffect } from 'react';
import { Button, message, Tooltip } from 'antd';
import { useTranslation } from 'react-i18next';
import { useLocation, useNavigate } from 'react-router-dom';
import { apiService } from '../../services/api';
import { downloadPDF, getReportFilename } from '../../utils/pdfUtils';
import LanguageSelector from '../common/LanguageSelector';
/*import json from 'json';*/

interface GunaItem {
  kuta: string;
  description: string;
  points: number;
  max_points: number;
  bride_value: string;
  groom_value: string;
}

interface MatchMakingResult {
  id: number;
  bride_name: string;
  bride_dob: string;
  bride_tob: string;
  groom_name: string;
  groom_dob: string;
  groom_tob: string;
  guna_table: GunaItem[];
  total_points: number;
  max_points: number;
  percentage: number;
  compatibility_analysis: string;
  bride_horoscope: { rashi: string; nakshatra: string };
  groom_horoscope: { rashi: string; nakshatra: string };
}

const GUNA_TOOLTIPS = {
  kuta: 'Aspect of compatibility',
  bride_value: 'Bride\'s value',
  groom_value: 'Groom\'s value',
  description: 'Area of life',
  points: 'Points scored',
  max_points: 'Maximum possible points',
};

const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'ml', label: 'Malayalam' },
  { code: 'ta', label: 'Tamil' },
];

const MatchMakingResult: React.FC = () => {
  const { t } = useTranslation();
  const location = useLocation();
  const navigate = useNavigate();
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const result = location.state?.result as MatchMakingResult;
  const bride_avatar = location.state?.bride_avatar || '🦸‍♀️';
  const groom_avatar = location.state?.groom_avatar || '🦸‍♂️';

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

  console.log('DEBUG: Frontend result =', result);
  if (result) {
    console.log('DEBUG: Frontend guna_table =', result.guna_table);
    console.log('DEBUG: Frontend bride_horoscope =', result.bride_horoscope);
    console.log('DEBUG: Frontend groom_horoscope =', result.groom_horoscope);
  }

  if (!result) {
    navigate('/matchmaking');
    return null;
  }

  const handleDownloadPDF = async () => {
    try {
      setLoading(true);
      setSuccess(false);
      const blob = await apiService.getMatchMakingReport(result.id, currentLanguage);
      downloadPDF(blob, getReportFilename('matchmaking', currentLanguage));
      setSuccess(true);
      message.success(t('matchmaking.downloadSuccess') || 'PDF downloaded successfully');
    } catch (error) {
      console.error('Error downloading PDF:', error);
      message.error(t('common.errorDownloadingPDF') || 'Error downloading PDF');
    } finally {
      setLoading(false);
      setTimeout(() => setSuccess(false), 3000);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#f6f7fb] p-2 animate-fade-in">
      <div className="w-full max-w-2xl bg-[#e7eaf3] rounded-3xl shadow-2xl p-4 sm:p-8 flex flex-col items-center">
        <div className="flex flex-col sm:flex-row gap-6 w-full mb-6 justify-center items-center">
          {/* Groom Card */}
          <div className="flex flex-col items-center bg-white/20 rounded-2xl p-4 shadow-lg w-full sm:w-1/2">
            <div className="text-5xl mb-2">{groom_avatar}</div>
            <div className="font-bold text-lg text-white mb-1">{result.groom_name}</div>
            <div className="text-white/80 text-sm mb-1">DOB: {result.groom_dob}</div>
            <div className="text-white/80 text-sm mb-1">TOB: {result.groom_tob}</div>
            <div className="text-white/80 text-sm mb-1">Rasi: {result.groom_horoscope?.rashi}</div>
            <div className="text-white/80 text-sm">Nakshatra: {result.groom_horoscope?.nakshatra}</div>
          </div>
          {/* Bride Card */}
          <div className="flex flex-col items-center bg-white/20 rounded-2xl p-4 shadow-lg w-full sm:w-1/2">
            <div className="text-5xl mb-2">{bride_avatar}</div>
            <div className="font-bold text-lg text-white mb-1">{result.bride_name}</div>
            <div className="text-white/80 text-sm mb-1">DOB: {result.bride_dob}</div>
            <div className="text-white/80 text-sm mb-1">TOB: {result.bride_tob}</div>
            <div className="text-white/80 text-sm mb-1">Rasi: {result.bride_horoscope?.rashi}</div>
            <div className="text-white/80 text-sm">Nakshatra: {result.bride_horoscope?.nakshatra}</div>
          </div>
        </div>
        {/* Guna Milan Table */}
        <div className="w-full mb-6 overflow-x-auto">
          <div className="text-lg font-semibold mb-2 text-white/80">Guna Milan Analysis</div>
          <div className="min-w-[600px] grid grid-cols-6 gap-2 bg-gradient-to-r from-blue-900/60 to-pink-900/40 rounded-xl p-2 text-white text-xs sm:text-sm">
            <Tooltip title={GUNA_TOOLTIPS.kuta}><div className="font-bold">Kuta</div></Tooltip>
            <Tooltip title={GUNA_TOOLTIPS.bride_value}><div className="font-bold">Bride</div></Tooltip>
            <Tooltip title={GUNA_TOOLTIPS.groom_value}><div className="font-bold">Groom</div></Tooltip>
            <Tooltip title={GUNA_TOOLTIPS.description}><div className="font-bold">Area</div></Tooltip>
            <Tooltip title={GUNA_TOOLTIPS.points}><div className="font-bold">Points</div></Tooltip>
            <Tooltip title={GUNA_TOOLTIPS.max_points}><div className="font-bold">Max</div></Tooltip>
            {result.guna_table.map((row: any, idx: number) => (
              <React.Fragment key={idx}>
                <div className="py-1 font-semibold">{row.kuta}</div>
                <div className="py-1">{row.bride_value}</div>
                <div className="py-1">{row.groom_value}</div>
                <div className="py-1">{row.description}</div>
                <div className="py-1">{row.points}</div>
                <div className="py-1">{row.max_points}</div>
              </React.Fragment>
              ))}
            {/* Totals row */}
            <div className="col-span-4 text-right font-bold py-1">Total</div>
            <div className="py-1 font-bold">{result.total_points}</div>
            <div className="py-1 font-bold">{result.max_points}</div>
          </div>
        </div>
        {/* Compatibility Analysis */}
        <div className="w-full mb-6">
          <div className="text-lg font-semibold mb-2 text-white/80">Compatibility Analysis</div>
          <div className="bg-white/20 rounded-xl p-4 text-white/90 shadow-md text-base sm:text-lg">
            {result.compatibility_analysis}
          </div>
        </div>
        {/* PDF Download */}
        <div className="flex flex-col sm:flex-row items-center gap-2 mt-2">
          <LanguageSelector value={currentLanguage} onChange={setCurrentLanguage} />
        <Button
          type="primary"
          onClick={handleDownloadPDF}
          loading={loading}
            className="rounded-xl px-4 py-2 bg-gradient-to-r from-pink-500 to-blue-500 text-white font-bold hover:scale-105 border-none text-sm sm:text-base"
        >
            {loading ? 'Downloading...' : 'Download PDF'}
        </Button>
        </div>
        {success && <div className="text-green-400 mt-2">PDF downloaded successfully!</div>}
      </div>
    </div>
  );
};

export default MatchMakingResult; 