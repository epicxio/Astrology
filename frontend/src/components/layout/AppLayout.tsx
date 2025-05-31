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
      <Header className="flex justify-between items-center px-6 bg-white/95 backdrop-blur-md border-b border-gray-100 fixed w-full z-50">
        <div className="flex items-center">
          <img src="/astrology-logo.png" alt="Astrology Logo" style={{ height: 55, marginRight: 12, objectFit: 'contain' }} />
          <Menu
            mode="horizontal"
            selectedKeys={[location.pathname]}
            items={menuItems}
            onClick={({ key }) => handleMenuClick(key)}
            className="border-0 bg-transparent"
            style={{ 
              background: 'transparent',
              border: 'none',
              fontSize: '15px',
              fontWeight: 500
            }}
          >
            {menuItems.map((item) => (
              <Menu.Item
                key={item.key}
                className={`relative px-4 py-2 rounded-lg font-medium text-gray-600 hover:text-gray-900 transition-all duration-200
                  ${location.pathname === item.key ? 'text-gray-900' : 'text-gray-600'}
                  hover:bg-gray-50`}
              >
                {item.label}
                {location.pathname === item.key && (
                  <span className="absolute left-1/2 -translate-x-1/2 bottom-0 h-0.5 w-4/5 bg-gray-900 rounded-full"></span>
                )}
              </Menu.Item>
            ))}
          </Menu>
        </div>
        <LanguageSelector
          value={currentLanguage}
          onChange={handleLanguageChange}
        />
      </Header>
      <Content className="pt-16">
        {children}
      </Content>
    </Layout>
  );
};

export default AppLayout; 