import React, { useState } from 'react';
import { Layout, Menu, Space } from 'antd';
import { useTranslation } from 'react-i18next';
import { useNavigate, useLocation } from 'react-router-dom';
import LanguageSelector from '../common/LanguageSelector';

const { Header, Content } = Layout;

interface AppLayoutProps {
  children: React.ReactNode;
}

const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();
  const [currentLanguage, setCurrentLanguage] = useState('en');

  const menuItems = [
    {
      key: '/horoscope',
      label: t('common.horoscope', 'Horoscope') as string,
    },
    {
      key: '/matchmaking',
      label: t('common.matchmaking', 'Match Making') as string,
    },
    {
      key: 'records',
      label: t('common.records', 'Records') as string,
      children: [
        {
          key: '/records/horoscope',
          label: t('common.horoscopeRecord', 'Horoscope Records') as string,
        },
        {
          key: '/records/matchmaking',
          label: t('common.matchmakingRecord', 'Matchmaking Records') as string,
        },
      ],
    },
  ];

  const handleMenuClick = (key: string) => {
    navigate(key);
  };

  const handleLanguageChange = (language: string) => {
    setCurrentLanguage(language);
  };

  return (
    <Layout className="min-h-screen">
      <Header className="flex justify-between items-center px-6 bg-white shadow">
        <div className="flex items-center">
          <h1 className="text-xl font-bold text-gray-800 mr-8">
            {t('common.welcome')}
          </h1>
          <Menu
            mode="horizontal"
            selectedKeys={[location.pathname]}
            items={menuItems}
            onClick={({ key }) => handleMenuClick(key)}
            className="border-0"
          />
        </div>
        <Space>
          <LanguageSelector
            value={currentLanguage}
            onChange={handleLanguageChange}
          />
        </Space>
      </Header>
      <Content className="p-6">{children}</Content>
    </Layout>
  );
};

export default AppLayout; 