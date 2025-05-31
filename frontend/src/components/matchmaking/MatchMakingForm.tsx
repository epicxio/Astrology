import React, { useState, useEffect } from 'react';
import { Form, Input, DatePicker, TimePicker, Select, Button, message, Progress } from 'antd';
import { useTranslation } from 'react-i18next';
import { useApi } from '../../hooks/useApi';
import { apiService, Place, MatchMakingResponse } from '../../services/api';
import dayjs from 'dayjs';
import type { Dayjs } from 'dayjs';
import { useNavigate } from 'react-router-dom';
import { downloadPDF, getReportFilename } from '../../utils/pdfUtils';

const { Option } = Select;
const AVATARS = ['🦸‍♂️','🦸‍♀️','🧑‍🎤','🦄','🐼','🦊','🐧','🦋','👽','🧙‍♀️','🦸‍♂️','🧑‍🚀'];

const steps = [
  { key: 'groom_avatar', label: "Pick Groom's Avatar", type: 'avatar' },
  { key: 'groom_name', label: "What's the groom's name?", type: 'text', placeholder: 'Enter groom name' },
  { key: 'groom_dob', label: "Groom's date of birth", type: 'date' },
  { key: 'groom_tob', label: "Groom's time of birth", type: 'time' },
  { key: 'groom_place', label: "Groom's place of birth", type: 'select' },
  { key: 'bride_avatar', label: "Pick Bride's Avatar", type: 'avatar' },
  { key: 'bride_name', label: "What's the bride's name?", type: 'text', placeholder: 'Enter bride name' },
  { key: 'bride_dob', label: "Bride's date of birth", type: 'date' },
  { key: 'bride_tob', label: "Bride's time of birth", type: 'time' },
  { key: 'bride_place', label: "Bride's place of birth", type: 'select' },
  { key: 'review', label: 'Review & Submit', type: 'review' },
];

const MatchMakingForm: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [places, setPlaces] = useState<Place[]>([]);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(0);
  const [formData, setFormData] = useState<any>({});

  const { execute: fetchPlaces } = useApi(apiService.getPlaces);
  const { execute: calculateMatchMaking } = useApi(
    apiService.calculateMatchMaking,
    { 
      successMessage: t('matchmaking.calculationSuccess') || 'Match calculated successfully',
      errorMessage: t('matchmaking.calculationError') || 'Error calculating match'
    }
  );

  useEffect(() => {
  const loadPlaces = async () => {
    try {
      setLoading(true);
      const places = await fetchPlaces();
      setPlaces(places);
    } catch (error) {
      message.error(t('common.errorLoadingPlaces') || 'Error loading places');
    } finally {
      setLoading(false);
    }
  };
    loadPlaces();
  }, []);

  const next = () => setStep((s) => Math.min(s + 1, steps.length - 1));
  const prev = () => setStep((s) => Math.max(s - 1, 0));

  const handleChange = (key: string, value: any) => {
    setFormData((prev: any) => ({ ...prev, [key]: value }));
  };

  const onFinish = async () => {
    try {
      const formattedData = {
        bride_name: formData.bride_name,
        bride_dob: formData.bride_dob,
        bride_tob: formData.bride_tob,
        bride_place_id: formData.bride_place,
        groom_name: formData.groom_name,
        groom_dob: formData.groom_dob,
        groom_tob: formData.groom_tob,
        groom_place_id: formData.groom_place,
        bride_avatar: formData.bride_avatar,
        groom_avatar: formData.groom_avatar,
      };
      const result = await calculateMatchMaking(formattedData) as MatchMakingResponse;
      navigate(`/matchmaking/result`, { state: { result, bride_avatar: formData.bride_avatar, groom_avatar: formData.groom_avatar } });
    } catch (error) {
      message.error(t('matchmaking.calculationError') || 'Error calculating match');
    }
  };

  // Glassmorphic, animated card
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#f6f7fb] p-2">
      {/* <div className="w-full max-w-md bg-horoscope-grey rounded-3xl shadow-2xl p-8 flex flex-col items-center border border-white/20 animate-fade-in"> */}
      <div className="backdrop-blur-lg bg-[#e7eaf3] dark:bg-black/30 rounded-3xl shadow-2xl p-8 w-full max-w-md flex flex-col items-center border border-white/20">

        <Progress percent={Math.round((step / (steps.length - 1)) * 100)} showInfo={false} className="w-full mb-4" strokeColor="#f472b6" />
        <div className="text-xl font-bold text-black mb-2">{steps[step].label}</div>
        {/* Step content */}
        {steps[step].type === 'avatar' && (
          <div className="flex flex-wrap gap-3 justify-center mb-4">
            {AVATARS.map((a) => (
              <button
                key={a}
                className={`text-4xl p-2 rounded-full border-2 ${formData[steps[step].key] === a ? 'border-pink-400 bg-white/20' : 'border-transparent'} hover:scale-110 transition`}
                onClick={() => handleChange(steps[step].key, a)}
                type="button"
              >
                {a}
              </button>
                ))}
          </div>
        )}
        {steps[step].type === 'text' && (
          <input
            type="text"
            className="w-full p-3 rounded-xl bg-[#f6f7fb] text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-pink-400 mb-4"
            placeholder={steps[step].placeholder}
            value={formData[steps[step].key] || ''}
            onChange={e => handleChange(steps[step].key, e.target.value)}
            autoFocus
          />
        )}
        {steps[step].type === 'date' && (
          <input
            type="date"
            className="w-full p-3 rounded-xl bg-[#f6f7fb] text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-400 mb-4"
            value={formData[steps[step].key] || ''}
            onChange={e => handleChange(steps[step].key, e.target.value)}
            autoFocus
          />
        )}
        {steps[step].type === 'time' && (
          <input
            type="time"
            className="w-full p-3 rounded-xl bg-[#f6f7fb] text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-400 mb-4"
            value={formData[steps[step].key] || ''}
            onChange={e => handleChange(steps[step].key, e.target.value)}
            autoFocus
          />
        )}
        {steps[step].type === 'select' && (
          <select
            className="w-full p-3 rounded-xl bg-[#f6f7fb] text-black focus:outline-none focus:ring-2 focus:ring-blue-400 mb-4"
            value={formData[steps[step].key] || ''}
            onChange={e => handleChange(steps[step].key, e.target.value)}
          >
            <option value="" disabled>Select a place</option>
            {places.map(place => (
              <option key={place.id} value={place.id}>{place.name}</option>
            ))}
          </select>
        )}
        {steps[step].type === 'review' && (
          <div className="w-full text-white/90 mb-4">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-2xl">{formData.groom_avatar}</span>
              <span className="font-bold">{formData.groom_name}</span>
            </div>
            <div className="mb-2">DOB: {formData.groom_dob}, TOB: {formData.groom_tob}, Place: {places.find(p => p.id === formData.groom_place)?.name}</div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-2xl">{formData.bride_avatar}</span>
              <span className="font-bold">{formData.bride_name}</span>
            </div>
            <div>DOB: {formData.bride_dob}, TOB: {formData.bride_tob}, Place: {places.find(p => p.id === formData.bride_place)?.name}</div>
          </div>
        )}
        {/* Stepper navigation */}
        <div className="flex gap-4 w-full justify-between mt-2">
          <Button
            onClick={prev}
            disabled={step === 0}
            className="rounded-xl px-4 py-2 bg-[#f0f1f5] text-gray-700 font-bold hover:bg-pink-400/30 border-none"
          >
            Back
          </Button>
          {step < steps.length - 1 ? (
            <Button
              onClick={next}
              disabled={
                (steps[step].type === 'avatar' && !formData[steps[step].key]) ||
                (steps[step].type === 'text' && !formData[steps[step].key]) ||
                (steps[step].type === 'date' && !formData[steps[step].key]) ||
                (steps[step].type === 'time' && !formData[steps[step].key]) ||
                (steps[step].type === 'select' && !formData[steps[step].key])
              }
              className="rounded-xl px-4 py-2 bg-gradient-to-r from-pink-500 to-blue-500 text-white font-bold hover:scale-105 border-none"
            >
              Next
            </Button>
          ) : (
        <Button
              onClick={onFinish}
              loading={loading}
              className="rounded-xl px-4 py-2 bg-gradient-to-r from-pink-500 to-blue-500 text-white font-bold hover:scale-105 border-none"
            >
              Calculate Match
        </Button>
          )}
        </div>
      </div>
    </div>
  );
};

export default MatchMakingForm; 