import React from 'react';
import { Layout as AntLayout, Menu } from 'antd';
import { Link, useLocation } from 'react-router-dom';
import LanguageSelector from './LanguageSelector';

const { Header, Content, Footer } = AntLayout;

interface LayoutProps {
  children: React.ReactNode;
  onLanguageChange: (language: string) => void;
  currentLanguage: string;
}

const AppLayout: React.FC<LayoutProps> = ({
  children,
  onLanguageChange,
  currentLanguage,
}) => {
  const location = useLocation();

  return (
    <AntLayout className="min-h-screen">
      <Header className="flex items-center justify-between bg-white shadow">
        <div className="flex items-center">
          <Link to="/" className="text-xl font-bold text-blue-600">
            Epic-X Horoscope
          </Link>
          <Menu
            mode="horizontal"
            selectedKeys={[location.pathname]}
            className="ml-8 border-0"
          >
            <Menu.Item key="/">
              <Link to="/">Horoscope</Link>
            </Menu.Item>
            <Menu.Item key="/matchmaking">
              <Link to="/matchmaking">Match Making</Link>
            </Menu.Item>
          </Menu>
        </div>
        <LanguageSelector
          value={currentLanguage}
          onChange={onLanguageChange}
        />
      </Header>

      <Content className="p-4 bg-gray-50">
        <div className="min-h-[calc(100vh-64px-70px)]">{children}</div>
      </Content>

      <Footer className="text-center bg-white">
        © {new Date().getFullYear()} Epic-X Horoscope. All rights reserved.
      </Footer>
    </AntLayout>
  );
};

export default AppLayout; 