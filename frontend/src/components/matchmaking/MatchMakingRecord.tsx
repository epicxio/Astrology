import React, { useState, useEffect } from 'react';
import { Button, message } from 'antd';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../../services/api';
import { downloadPDF, getReportFilename } from '../../utils/pdfUtils';

export interface MatchMakingRecord {
  id: number;
  bride_name: string;
  groom_name: string;
  created_at: string;
  percentage: number;
  bride_avatar?: string;
  groom_avatar?: string;
  compatibility?: string;
  remarks?: string;
}

const AVATARS = ['🦸‍♂️','🦸‍♀️','🧑‍🎤','🦄','🐼','🦊','🐧','🦋','👽','🧙‍♀️','🦸‍♂️','🧑‍🚀'];

const MatchMakingRecord: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [records, setRecords] = useState<MatchMakingRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [expanded, setExpanded] = useState<number | null>(null);

  useEffect(() => {
    fetchRecords();
  }, []);

  const fetchRecords = async () => {
    try {
      setLoading(true);
      const data = await apiService.getMatchMakingRecords();
      setRecords(data);
    } catch (error) {
      console.error('Error fetching records:', error);
      message.error(t('common.errorFetchingRecords') || 'Error fetching records');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async (id: number) => {
    try {
      setLoading(true);
      const blob = await apiService.getMatchMakingReport(id, 'en');
      downloadPDF(blob, getReportFilename('matchmaking', 'en'));
      message.success(t('matchmaking.downloadSuccess') || 'PDF downloaded successfully');
    } catch (error) {
      console.error('Error downloading PDF:', error);
      message.error(t('common.errorDownloadingPDF') || 'Error downloading PDF');
    } finally {
      setLoading(false);
    }
  };

  const toggleExpand = (id: number) => {
    setExpanded(expanded === id ? null : id);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#f6f7fb] p-2 animate-fade-in">
      <div className="w-full max-w-5xl bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl p-4 sm:p-8 flex flex-col items-center">
        <h1 className="text-2xl font-bold text-black mb-6 tracking-tight">Matchmaking Records</h1>
        <div className="text-gray-600 text-sm mb-6">English</div>
        <div className="w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {records.length === 0 && (
            <div className="text-gray-500 col-span-full text-center">No records found.</div>
          )}
          {records.map((record, idx) => {
            const isOpen = expanded === record.id;
            const preview = record.remarks ? record.remarks.slice(0, 40) + (record.remarks.length > 40 ? '...' : '') : '';
            return (
              <div
                key={record.id}
                className={`bg-white/80 backdrop-blur-xl rounded-2xl shadow-xl p-6 flex flex-col gap-3 border border-pink-300/40 relative transition-all duration-200 ${isOpen ? 'ring-2 ring-pink-400 scale-105' : 'hover:scale-105'}`}
              >
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-3xl drop-shadow-lg">{record.bride_avatar || AVATARS[(idx*2+1)%AVATARS.length]}</span>
                  <span className="font-bold text-lg text-black tracking-tight">{record.bride_name}</span>
                  <span className="mx-2 text-pink-500 text-2xl font-bold">♥</span>
                  <span className="text-3xl drop-shadow-lg">{record.groom_avatar || AVATARS[(idx*2)%AVATARS.length]}</span>
                  <span className="font-bold text-lg text-black tracking-tight">{record.groom_name}</span>
                </div>
                <div className="flex flex-wrap gap-2 text-gray-700 text-sm">
                  <span className="bg-white rounded px-2 py-1">Date: {new Date(record.created_at).toLocaleDateString()}</span>
                  <span className="bg-white rounded px-2 py-1">Compatibility: <span className="font-bold text-pink-500">{record.percentage}%</span></span>
                  {record.compatibility && <span className="bg-white rounded px-2 py-1">{record.compatibility}</span>}
                </div>
                <Button
                  type="primary"
                  onClick={() => handleDownloadPDF(record.id)}
                  loading={loading}
                  className="rounded-xl px-4 py-2 mt-3 bg-gradient-to-r from-pink-500 to-blue-500 text-white font-bold hover:scale-105 border-none text-sm sm:text-base shadow-lg"
                  icon={<span role="img" aria-label="download">⬇️</span>}
                >
                  Download PDF
                </Button>
                {!isOpen && preview && (
                  <div className="mt-2 flex items-center gap-2">
                    <div className="text-xs text-gray-600 italic truncate">{preview}</div>
                    <button
                      className="text-xs px-2 py-1 rounded bg-pink-400/80 text-white font-semibold hover:bg-pink-500 transition"
                      onClick={() => setExpanded(record.id)}
                    >
                      Read More
                    </button>
                  </div>
                )}
                {isOpen && (
                  <div className="mt-2 p-3 rounded-xl bg-white text-sm text-gray-800 shadow-inner animate-fade-in border border-pink-200">
                    <div className="font-semibold mb-1 text-pink-500">Description / Remarks</div>
                    <div>{record.remarks || 'No additional remarks.'}</div>
                    <button
                      className="mt-2 text-xs px-2 py-1 rounded bg-blue-400/80 text-white font-semibold hover:bg-blue-500 transition"
                      onClick={() => setExpanded(null)}
                    >
                      Hide Details
                    </button>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default MatchMakingRecord; 