import React, { useState, useEffect } from 'react';
import { Form, Input, DatePicker, TimePicker, Select, Button, message, Row, Col } from 'antd';
import { useTranslation } from 'react-i18next';
import { useApi } from '../../hooks/useApi';
import { apiService, Place, MatchMakingResponse } from '../../services/api';
import dayjs from 'dayjs';
import type { Dayjs } from 'dayjs';
import { useNavigate } from 'react-router-dom';
import { downloadPDF, getReportFilename } from '../../utils/pdfUtils';

const { Option } = Select;

interface FormValues {
  bride_name: string;
  bride_dob: Dayjs;
  bride_tob: Dayjs;
  bride_place: number;
  groom_name: string;
  groom_dob: Dayjs;
  groom_tob: Dayjs;
  groom_place: number;
}

const MatchMakingForm: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [form] = Form.useForm<FormValues>();
  const [places, setPlaces] = useState<Place[]>([]);
  const [loading, setLoading] = useState(false);

  const { execute: fetchPlaces, loading: placesLoading } = useApi(apiService.getPlaces);
  const { execute: calculateMatchMaking, loading: calculationLoading } = useApi(
    apiService.calculateMatchMaking,
    { 
      successMessage: t('matchmaking.calculationSuccess') || 'Match calculated successfully',
      errorMessage: t('matchmaking.calculationError') || 'Error calculating match'
    }
  );

  const loadPlaces = async () => {
    try {
      setLoading(true);
      const places = await fetchPlaces();
      console.log('DEBUG: places fetched from API:', places);
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

  const onFinish = async (values: any) => {
    try {
      const formattedData = {
        bride_name: values.bride_name,
        bride_dob: values.bride_dob.format('YYYY-MM-DD'),
        bride_tob: values.bride_tob.format('HH:mm'),
        bride_place_id: values.bride_place,
        groom_name: values.groom_name,
        groom_dob: values.groom_dob.format('YYYY-MM-DD'),
        groom_tob: values.groom_tob.format('HH:mm'),
        groom_place_id: values.groom_place
      };
      console.log('formattedData', formattedData);
      console.log('values', values);
      const result = await calculateMatchMaking(formattedData) as MatchMakingResponse;
      navigate(`/matchmaking/result`, { state: { result } });
    } catch (error) {
      console.error('Error calculating match:', error);
    }
  };

  const handleDownloadPDF = async (id: number, language: string) => {
    try {
      const blob = await apiService.getMatchMakingReport(id, language);
      downloadPDF(blob, getReportFilename('matchmaking', language));
    } catch (error) {
      message.error(t('common.errorDownloadingPDF') || 'Error downloading PDF');
    }
  };

  return (
    <Form
      form={form}
      onFinish={onFinish}
      layout="vertical"
      className="max-w-4xl mx-auto p-6"
    >
      <h1 className="text-2xl font-bold mb-6">{t('matchmaking.calculate', 'Match making calculation') as string}</h1>
      <Row gutter={32}>
        <Col xs={24} md={12}>
          <div className="mb-8">
            <h3 className="text-lg font-semibold mb-4">{t('matchmaking.groomInfo', 'Groom Info') as string}</h3>
            <Form.Item
              name="groom_name"
              label={t('matchmaking.name', 'Name') as string}
              rules={[{ required: true, message: t('matchmaking.nameRequired', 'Please enter the name') as string }]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              name="groom_dob"
              label={t('matchmaking.dob', 'Date of Birth') as string}
              rules={[{ required: true, message: t('matchmaking.dobRequired', 'Please enter the date of birth') as string }]}
            >
              <DatePicker className="w-full" />
            </Form.Item>
            <Form.Item
              name="groom_tob"
              label={t('matchmaking.tob', 'Time of Birth') as string}
              rules={[{ required: true, message: t('matchmaking.tobRequired', 'Please enter the time of birth') as string }]}
            >
              <TimePicker className="w-full" format="HH:mm" />
            </Form.Item>
            <Form.Item
              name="groom_place"
              label={t('matchmaking.groomPlaceOfBirth', 'Groom Place of Birth') as string}
              rules={[{ required: true, message: t('matchmaking.placeRequired', 'Please select the place of birth') as string }]}
            >
              <Select
                showSearch
                placeholder={t('matchmaking.selectPlace', 'Select a place') as string}
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
          </div>
        </Col>
        <Col xs={24} md={12}>
          <div className="mb-8">
            <h3 className="text-lg font-semibold mb-4">{t('matchmaking.brideInfo', 'Bride Info') as string}</h3>
            <Form.Item
              name="bride_name"
              label={t('matchmaking.name', 'Name') as string}
              rules={[{ required: true, message: t('matchmaking.nameRequired', 'Please enter the name') as string }]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              name="bride_dob"
              label={t('matchmaking.dob', 'Date of Birth') as string}
              rules={[{ required: true, message: t('matchmaking.dobRequired', 'Please enter the date of birth') as string }]}
            >
              <DatePicker className="w-full" />
            </Form.Item>
            <Form.Item
              name="bride_tob"
              label={t('matchmaking.tob', 'Time of Birth') as string}
              rules={[{ required: true, message: t('matchmaking.tobRequired', 'Please enter the time of birth') as string }]}
            >
              <TimePicker className="w-full" format="HH:mm" />
            </Form.Item>
            <Form.Item
              name="bride_place"
              label={t('matchmaking.bridePlaceOfBirth', 'Bride Place Of Birth') as string}
              rules={[{ required: true, message: t('matchmaking.placeRequired', 'Please select the place of birth') as string }]}
            >
              <Select
                showSearch
                placeholder={t('matchmaking.selectPlace', 'Select a place') as string}
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
          </div>
        </Col>
      </Row>
      <Form.Item style={{ textAlign: 'center' }}>
        <Button
          type="primary"
          htmlType="submit"
          loading={calculationLoading}
          className="w-48"
        >
          {t('matchmaking.calculate', 'Calculate Match') as string}
        </Button>
      </Form.Item>
    </Form>
  );
};

export default MatchMakingForm; 