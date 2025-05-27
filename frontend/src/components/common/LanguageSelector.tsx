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
      className="w-32"
      options={[
        { value: 'en', label: t('common.english') },
        { value: 'ml', label: t('common.malayalam') },
        { value: 'ta', label: t('common.tamil') },
      ]}
    />
  );
};

export default LanguageSelector; 