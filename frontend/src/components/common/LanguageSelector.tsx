import React from 'react';
import { Select } from 'antd';
import { useTranslation } from 'react-i18next';

interface LanguageSelectorProps {
  value: string;
  onChange: (language: string) => void;
}

const LanguageSelector: React.FC<LanguageSelectorProps> = ({ value, onChange }) => {
  const { t } = useTranslation();

  return (
    <Select
      value={value}
      onChange={onChange}
      className="w-28"
      style={{
        background: 'transparent',
        border: 'none',
      }}
      dropdownStyle={{
        borderRadius: '8px',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.08)',
      }}
      options={[
        { value: 'en', label: t('common.english') },
        { value: 'ml', label: t('common.malayalam') },
        { value: 'ta', label: t('common.tamil') },
      ]}
    />
  );
};

export default LanguageSelector; 