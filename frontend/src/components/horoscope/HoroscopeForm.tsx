import React, { useState, useEffect } from 'react';
import { Form, Input, DatePicker, TimePicker, Select, Button, message } from 'antd';
import { useTranslation } from 'react-i18next';
import { useApi } from '../../hooks/useApi';
import { apiService, Place } from '../../services/api';
import dayjs from 'dayjs';
import type { Dayjs } from 'dayjs';
import HoroscopeOutput from './HoroscopeOutput';

const { Option } = Select;

interface FormValues {
  name: string;
  gender: string;
  dob: Dayjs;
  tob: Dayjs;
  place_id: number;
}

const HoroscopeForm: React.FC = () => {
  const { t } = useTranslation();
  const [form] = Form.useForm<FormValues>();
  const [places, setPlaces] = useState<Place[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const { execute: calculateHoroscope, loading: calculating } = useApi(
    apiService.calculateHoroscope,
    {
      successMessage: t('horoscope.calculationSuccess') || 'Horoscope calculated successfully',
      errorMessage: t('horoscope.calculationError') || 'Error calculating horoscope'
    }
  );

  const loadPlaces = async () => {
    try {
      setLoading(true);
      const places = await apiService.getPlaces();
      setPlaces(places);
    } catch (error) {
      console.error('Error loading places:', error);
      message.error(t('common.errorLoadingPlaces') || 'Error loading places');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPlaces();
  }, []);

  const onFinish = async (values: FormValues) => {
    try {
      setLoading(true);
      const formattedData = {
        name: values.name,
        gender: values.gender,
        date_of_birth: values.dob.format('YYYY-MM-DD'),
        time_of_birth: values.tob.format('HH:mm:ss'),
        place_id: values.place_id
      };

      const result = await calculateHoroscope(formattedData);
      if (result) {
        setResult(result);
      }
    } catch (error) {
      console.error('Error calculating horoscope:', error);
      message.error(t('common.errorCalculatingHoroscope') || 'Error calculating horoscope');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">{t('horoscope.calculate', 'Horoscope Calculation')}</h1>
      <Form<FormValues>
        form={form}
        layout="vertical"
        onFinish={onFinish}
        className="space-y-4"
      >
        <Form.Item
          name="name"
          label={t('common.name') || 'Name'}
          rules={[{ required: true, message: t('common.nameRequired') || 'Please enter your name' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          name="gender"
          label={t('common.gender') || 'Gender'}
          rules={[{ required: true, message: t('common.genderRequired') || 'Please select your gender' }]}
        >
          <Select>
            <Option value="male">{t('common.male') || 'Male'}</Option>
            <Option value="female">{t('common.female') || 'Female'}</Option>
            <Option value="other">{t('common.other') || 'Other'}</Option>
          </Select>
        </Form.Item>

        <Form.Item
          name="dob"
          label={t('common.dateOfBirth') || 'Date of Birth'}
          rules={[{ required: true, message: t('common.dateOfBirthRequired') || 'Please select your date of birth' }]}
        >
          <DatePicker className="w-full" />
        </Form.Item>

        <Form.Item
          name="tob"
          label={t('common.timeOfBirth') || 'Time of Birth'}
          rules={[{ required: true, message: t('common.timeOfBirthRequired') || 'Please select your time of birth' }]}
        >
          <TimePicker className="w-full" format="HH:mm" />
        </Form.Item>

        <Form.Item
          name="place_id"
          label={t('horoscope.placeOfBirth', 'Place of Birth')}
          rules={[{ 
            required: true, 
            message: t('horoscope.placeRequired') || 'Please select your place of birth' 
          }]}
        >
          <Select
            showSearch
            placeholder={t('horoscope.selectPlace') || 'Select a place'}
            optionFilterProp="children"
            loading={loading}
            filterOption={(input, option) =>
              option?.children?.toString().toLowerCase().includes(input.toLowerCase()) ?? false
            }
          >
            {places.map(place => (
              <Option key={place.id} value={place.id}>
                {place.name}
              </Option>
            ))}
          </Select>
        </Form.Item>

        <Form.Item>
          <Button
            type="primary"
            htmlType="submit"
            loading={calculating}
            className="w-full"
          >
            {t('horoscope.calculate', 'Calculate Horoscope')}
          </Button>
        </Form.Item>
      </Form>
      <HoroscopeOutput result={result} />
    </div>
  );
};

export default HoroscopeForm; 