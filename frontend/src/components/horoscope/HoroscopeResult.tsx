import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Card, Button, Space, message } from 'antd';
import { useTranslation } from 'react-i18next';
import LanguageSelector from '../common/LanguageSelector';
import { apiService } from '../../services/api';
import { downloadPDF, getReportFilename } from '../../utils/pdfUtils';

interface HoroscopeResultData {
  id: number;
  name: string;
  gender: string;
  dateOfBirth: string;
  timeOfBirth: string;
  placeOfBirth: string;
  predictions: {
    career?: string;
    health?: string;
    wealth?: string;
    relationships?: string;
    bestMatches?: string[];
    avoidMatches?: string[];
  };
}

const HoroscopeResult: React.FC = () => {
  const { t } = useTranslation();
  const location = useLocation();
  const navigate = useNavigate();
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [result, setResult] = useState<HoroscopeResultData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (location.state?.result) {
      setResult(location.state.result);
      setLoading(false);
    } else {
      navigate('/horoscope');
    }
  }, [location, navigate]);

  const handleDownloadPDF = async () => {
    if (!result) return;

    try {
      const blob = await apiService.getHoroscopeReport(result.id, currentLanguage);
      downloadPDF(blob, getReportFilename('horoscope', currentLanguage));
      message.success(t('horoscope.downloadSuccess') || 'PDF downloaded successfully');
    } catch (error) {
      message.error(t('horoscope.downloadError') || 'Error downloading PDF');
    }
  };

  if (loading || !result) {
    return <div>Loading...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <Card
        title={t('horoscope.resultTitle') || 'Horoscope Results'}
        extra={
          <Space>
            <LanguageSelector
              value={currentLanguage}
              onChange={setCurrentLanguage}
            />
            <Button type="primary" onClick={handleDownloadPDF}>
              {t('common.download')}
            </Button>
          </Space>
        }
      >
        <div className="space-y-6">
          <section>
            <h2 className="text-xl font-semibold mb-4">
              {t('horoscope.personalDetails') || 'Personal Details'}
            </h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="font-medium">{t('common.name')}:</p>
                <p>{result.name}</p>
              </div>
              <div>
                <p className="font-medium">{t('common.gender')}:</p>
                <p>{result.gender}</p>
              </div>
              <div>
                <p className="font-medium">{t('common.dateOfBirth')}:</p>
                <p>{result.dateOfBirth}</p>
              </div>
              <div>
                <p className="font-medium">{t('common.timeOfBirth')}:</p>
                <p>{result.timeOfBirth}</p>
              </div>
              <div>
                <p className="font-medium">{t('common.placeOfBirth')}:</p>
                <p>{result.placeOfBirth}</p>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-xl font-semibold mb-4">
              {t('horoscope.predictions') || 'Predictions'}
            </h2>
            <div className="space-y-4">
              <div>
                <h3 className="font-medium">{t('horoscope.career')}:</h3>
                <p>{result.predictions.career}</p>
              </div>
              <div>
                <h3 className="font-medium">{t('horoscope.health')}:</h3>
                <p>{result.predictions.health}</p>
              </div>
              <div>
                <h3 className="font-medium">{t('horoscope.wealth')}:</h3>
                <p>{result.predictions.wealth}</p>
              </div>
              <div>
                <h3 className="font-medium">{t('horoscope.relationships')}:</h3>
                <p>{result.predictions.relationships}</p>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-xl font-semibold mb-4">
              {t('horoscope.compatibility') || 'Compatibility'}
            </h2>
            <div className="space-y-4">
              <div>
                <h3 className="font-medium">{t('horoscope.bestMatches')}:</h3>
                <ul className="list-disc list-inside">
                  {result.predictions?.bestMatches?.length
                    ? result.predictions.bestMatches.map((match, index) => (
                        <li key={index}>{match}</li>
                      ))
                    : <li>N/A</li>}
                </ul>
              </div>
              <div>
                <h3 className="font-medium">{t('horoscope.avoidMatches')}:</h3>
                <ul className="list-disc list-inside">
                  {result.predictions?.avoidMatches?.length
                    ? result.predictions.avoidMatches.map((match, index) => (
                        <li key={index}>{match}</li>
                      ))
                    : <li>N/A</li>}
                </ul>
              </div>
            </div>
          </section>
        </div>
      </Card>
    </div>
  );
};

export default HoroscopeResult; 