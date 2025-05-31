import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import AppLayout from './components/layout/AppLayout';
import HoroscopeFormGenZ from './components/HoroscopeFormGenZ';
import MatchMakingForm from './components/matchmaking/MatchMakingForm';
import HoroscopeResult from './components/horoscope/HoroscopeResult';
import MatchMakingResult from './components/matchmaking/MatchMakingResult';
import RecordsHoroscopePage from './components/records/RecordsHoroscopePage';
import MatchMakingRecord from './components/matchmaking/MatchMakingRecord';

const App: React.FC = () => {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1890ff',
        },
      }}
    >
      <BrowserRouter>
        <AppLayout>
          <Routes>
            <Route path="/" element={<HoroscopeFormGenZ />} />
            <Route path="/horoscope" element={<HoroscopeFormGenZ />} />
            <Route path="/matchmaking" element={<MatchMakingForm />} />
            <Route path="/horoscope/result" element={<HoroscopeResult />} />
            <Route path="/matchmaking/result" element={<MatchMakingResult />} />
            <Route path="/records/horoscope" element={<RecordsHoroscopePage />} />
            <Route path="/records/matchmaking" element={<MatchMakingRecord />} />
          </Routes>
        </AppLayout>
      </BrowserRouter>
    </ConfigProvider>
  );
};

export default App;
