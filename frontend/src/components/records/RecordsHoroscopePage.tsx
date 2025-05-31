import React, { useEffect, useState } from 'react';
import { Button, Image, Modal, Tooltip } from 'antd';
import axios from 'axios';
import { InfoCircleOutlined } from '@ant-design/icons';
import PlanetaryStrengthCard from '../horoscope/PlanetaryStrengthCard';

interface HoroscopeRecord {
  id: number;
  name: string;
  date_of_birth: string;
  time_of_birth: string;
  place_name: string;
  rashi: string;
  nakshatra: string;
  lagna: string;
  created_at: string;
  chart_image?: string;
  planetary_positions?: any;
  planetary_strengths?: any;
  showStrengths?: boolean;
}

const AVATARS = ['🦄','🦋','🐼','🦊','🐧','👽','🧙‍♀️','🦸‍♂️','🧑‍🚀','🦸‍♀️','🧑‍🎤'];

const RecordsHoroscopePage: React.FC = () => {
  const [data, setData] = useState<HoroscopeRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalRecord, setModalRecord] = useState<HoroscopeRecord | null>(null);

  useEffect(() => {
    setLoading(true);
    axios.get('/api/horoscope/')
      .then(res => setData(res.data))
      .finally(() => setLoading(false));
  }, []);

  const renderPlanetaryTable = (positions: any) => (
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
          {Object.entries(positions).map(([planet, details]: any, idx) => (
            <tr key={planet} className="border-b border-gray-200 text-gray-900 hover:bg-blue-50 transition">
              <td className="p-2 font-semibold">{planet}</td>
              <td className="p-2">{details.dms}</td>
              <td className="p-2">{details.dms_in_sign}</td>
              <td className="p-2">{details.rasi}</td>
              <td className="p-2">{details.rasi_lord}</td>
              <td className="p-2">{details.nakshatra}</td>
              <td className="p-2">{details.nakshatra_lord}</td>
              <td className="p-2">{details.retrograde ? '℞' : ''}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#f6f7fb] p-2 animate-fade-in">
      <div className="w-full max-w-5xl bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl p-4 sm:p-8 flex flex-col items-center">
        <h1 className="text-2xl font-bold text-black mb-6 tracking-tight">Horoscope Records</h1>
        <div className="w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {data.length === 0 && (
            <div className="text-gray-500 col-span-full text-center">No records found.</div>
          )}
          {data.map((record, idx) => (
            <div
              key={record.id}
              className={
                "bg-white/80 backdrop-blur-xl rounded-2xl shadow-xl p-6 flex flex-col gap-3 border border-pink-300/40 relative transition-all duration-200 hover:scale-105"
              }
            >
              <div className="flex items-center gap-2 mb-2">
                {record.chart_image ? (
                  <Image
                    width={40}
                    src={`/api/horoscope/chart/south/${record.id}`}
                    alt="Chart"
                    className="rounded shadow"
                  />
                ) : (
                  <span className="text-3xl drop-shadow-lg">{AVATARS[idx % AVATARS.length]}</span>
                )}
                <span className="font-bold text-lg text-black tracking-tight">{record.name}</span>
                {record.planetary_positions && (
                  <Tooltip title="View Planetary Positions">
                    <Button
                      shape="circle"
                      icon={<span role="img" aria-label="planet">🪐</span>}
                      size="small"
                      className="ml-2 bg-blue-400/80 text-white hover:bg-blue-500 border-none shadow"
                      onClick={() => setModalRecord(record)}
                    />
                  </Tooltip>
                )}
                {record.planetary_strengths && (
                  <Tooltip title="View Planetary Strengths">
                    <Button
                      shape="circle"
                      icon={<span role="img" aria-label="strength">📊</span>}
                      size="small"
                      className="ml-2 bg-green-400/80 text-white hover:bg-green-500 border-none shadow"
                      onClick={() => setModalRecord({ ...record, showStrengths: true })}
                    />
                  </Tooltip>
                )}
              </div>
              <div className="flex flex-wrap gap-2 text-gray-700 text-sm">
                <span className="bg-white rounded px-2 py-1">DOB: {record.date_of_birth}</span>
                <span className="bg-white rounded px-2 py-1">TOB: {record.time_of_birth}</span>
                <span className="bg-white rounded px-2 py-1">Place: {record.place_name}</span>
              </div>
              <div className="flex flex-wrap gap-2 text-gray-700 text-sm">
                <span className="bg-white rounded px-2 py-1">Rashi: <span className="font-bold text-pink-500">{record.rashi}</span></span>
                <span className="bg-white rounded px-2 py-1">Nakshatra: <span className="font-bold text-pink-500">{record.nakshatra}</span></span>
                <span className="bg-white rounded px-2 py-1">Lagna: <span className="font-bold text-pink-500">{record.lagna}</span></span>
              </div>
              <span className="text-xs text-gray-500 mt-1">Created: {new Date(record.created_at).toLocaleDateString()}</span>
            </div>
          ))}
        </div>
      <Modal
          open={!!modalRecord}
          onCancel={() => setModalRecord(null)}
          title={modalRecord ? (modalRecord.showStrengths ? `Planetary Strengths for ${modalRecord.name}` : `Planetary Positions for ${modalRecord.name}`) : ''}
        footer={null}
        width={800}
          className="backdrop-blur-xl"
      >
          {modalRecord && modalRecord.showStrengths && modalRecord.planetary_strengths && (
            <div className="space-y-6 mt-2">
              {Object.entries(typeof modalRecord.planetary_strengths === 'string' ? JSON.parse(modalRecord.planetary_strengths) : modalRecord.planetary_strengths).map(([planet, data]: [string, any]) => (
                <PlanetaryStrengthCard
                  key={planet}
                  planet={planet}
                  strengths={data}
                  planetaryPositions={modalRecord.planetary_positions}
                />
              ))}
            </div>
          )}
          {modalRecord && !modalRecord.showStrengths && modalRecord.planetary_positions && renderPlanetaryTable(
            typeof modalRecord.planetary_positions === 'string'
              ? JSON.parse(modalRecord.planetary_positions)
              : modalRecord.planetary_positions
          )}
      </Modal>
      </div>
    </div>
  );
};

export default RecordsHoroscopePage; 