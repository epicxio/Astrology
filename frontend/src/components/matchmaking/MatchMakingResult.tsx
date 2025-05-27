import React, { useState } from 'react';
import { Card, Button, message } from 'antd';
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

const MatchMakingResult: React.FC = () => {
  const { t } = useTranslation();
  const location = useLocation();
  const navigate = useNavigate();
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [loading, setLoading] = useState(false);

  const result = location.state?.result as MatchMakingResult;

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
      const blob = await apiService.getMatchMakingReport(result.id, currentLanguage);
      downloadPDF(blob, getReportFilename('matchmaking', currentLanguage));
      message.success(t('matchmaking.downloadSuccess') || 'PDF downloaded successfully');
    } catch (error) {
      console.error('Error downloading PDF:', error);
      message.error(t('common.errorDownloadingPDF') || 'Error downloading PDF');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">{t('matchmaking.result') || 'Matchmaking Result'}</h1>
        <LanguageSelector value={currentLanguage} onChange={setCurrentLanguage} />
      </div>

      <Card className="mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Bride's Information */}
          <div>
            <h2 className="text-xl font-semibold mb-4">{t('matchmaking.brideInfo') || "Bride's Information"}</h2>
            <div className="space-y-2">
              <p><strong>{t('matchmaking.name') || 'Name'}:</strong> {result.bride_name}</p>
              <p><strong>{t('matchmaking.dob') || 'Date of Birth'}:</strong> {result.bride_dob}</p>
              <p><strong>{t('matchmaking.tob') || 'Time of Birth'}:</strong> {result.bride_tob}</p>
              <p><strong>Rasi:</strong> {result.bride_horoscope?.rashi}</p>
              <p><strong>Nakshatra:</strong> {result.bride_horoscope?.nakshatra}</p>
            </div>
          </div>

          {/* Groom's Information */}
          <div>
            <h2 className="text-xl font-semibold mb-4">{t('matchmaking.groomInfo') || "Groom's Information"}</h2>
            <div className="space-y-2">
              <p><strong>{t('matchmaking.name') || 'Name'}:</strong> {result.groom_name}</p>
              <p><strong>{t('matchmaking.dob') || 'Date of Birth'}:</strong> {result.groom_dob}</p>
              <p><strong>{t('matchmaking.tob') || 'Time of Birth'}:</strong> {result.groom_tob}</p>
              <p><strong>Rasi:</strong> {result.groom_horoscope?.rashi}</p>
              <p><strong>Nakshatra:</strong> {result.groom_horoscope?.nakshatra}</p>
            </div>
          </div>
        </div>
      </Card>

      <Card className="mb-6">
        <h2 className="text-xl font-semibold mb-4">Guna Milan Analysis</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full border text-center">
            <thead className="bg-blue-900 text-white">
              <tr>
                <th className="px-4 py-2">Kuta</th>
                <th className="px-4 py-2">Bride Value</th>
                <th className="px-4 py-2">Groom Value</th>
                <th className="px-4 py-2">Area of Life</th>
                <th className="px-4 py-2">Points</th>
                <th className="px-4 py-2">Maximum</th>
              </tr>
            </thead>
            <tbody>
              {result.guna_table.map((row, idx) => (
                <tr key={idx} className="border-b">
                  <td className="px-4 py-2 font-semibold">{row.kuta}</td>
                  <td className="px-4 py-2">{row.bride_value}</td>
                  <td className="px-4 py-2">{row.groom_value}</td>
                  <td className="px-4 py-2">{row.description}</td>
                  <td className="px-4 py-2">{row.points}</td>
                  <td className="px-4 py-2">{row.max_points}</td>
                </tr>
              ))}
              <tr className="font-bold">
                <td colSpan={4} className="px-4 py-2 text-right">Total</td>
                <td className="px-4 py-2">{result.total_points}</td>
                <td className="px-4 py-2">{result.max_points}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>

      <Card className="mb-6">
        <h2 className="text-xl font-semibold mb-4">Compatibility Analysis</h2>
        <div className="space-y-4">
          <p>{result.compatibility_analysis}</p>
        </div>
      </Card>

      <div className="mt-6 flex justify-center">
        <Button
          type="primary"
          onClick={handleDownloadPDF}
          loading={loading}
        >
          {t('matchmaking.downloadPDF') || 'Download PDF'}
        </Button>
      </div>
    </div>
  );
};

export default MatchMakingResult; 