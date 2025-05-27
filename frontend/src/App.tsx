import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import AppLayout from './components/layout/AppLayout';
import HoroscopeForm from './components/horoscope/HoroscopeForm';
import MatchMakingForm from './components/matchmaking/MatchMakingForm';
import HoroscopeResult from './components/horoscope/HoroscopeResult';
import MatchMakingResult from './components/matchmaking/MatchMakingResult';
import RecordsHoroscopePage from './components/records/RecordsHoroscopePage';
import RecordsMatchmakingPage from './components/records/RecordsMatchmakingPage';

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
            <Route path="/" element={<HoroscopeForm />} />
            <Route path="/horoscope" element={<HoroscopeForm />} />
            <Route path="/matchmaking" element={<MatchMakingForm />} />
            <Route path="/horoscope/result" element={<HoroscopeResult />} />
            <Route path="/matchmaking/result" element={<MatchMakingResult />} />
            <Route path="/records/horoscope" element={<RecordsHoroscopePage />} />
            <Route path="/records/matchmaking" element={<RecordsMatchmakingPage />} />
          </Routes>
        </AppLayout>
      </BrowserRouter>
    </ConfigProvider>
  );
};

export default App;
