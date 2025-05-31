import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import HoroscopeResultGenZ from './HoroscopeResultGenZ';

const avatars = [
  '🦄', '🐉', '👽', '🧑‍🎤', '🦸‍♂️', '🧙‍♀️', '🐼', '🦊', '🐧', '🦋', '🌈', '💫'
];

const steps = [
  { key: 'name', label: "What's your name?", icon: '🧑‍🦱', type: 'text', placeholder: 'Enter your name' },
  { key: 'gender', label: "What's your gender?", icon: '♀️', type: 'select', options: ['Male', 'Female', 'Other'] },
  { key: 'dob', label: 'When were you born?', icon: '🗓️', type: 'date' },
  { key: 'tob', label: 'What time?', icon: '⏰', type: 'time' },
  { key: 'place_id', label: 'Where were you born?', icon: '📍', type: 'place', placeholder: 'Select place of birth' },
];

export default function HoroscopeFormGenZ() {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState({});
  const [avatar, setAvatar] = useState(avatars[0]);
  const [submitted, setSubmitted] = useState(false);
  const [places, setPlaces] = useState([]);
  const [placesLoading, setPlacesLoading] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (steps[step]?.type === 'place' && places.length === 0) {
      setPlacesLoading(true);
      apiService.getPlaces()
        .then((data) => setPlaces(data))
        .catch(() => setPlaces([]))
        .finally(() => setPlacesLoading(false));
    }
  }, [step]);

  const handleNext = async () => {
    if (step < steps.length - 1) {
      setStep(step + 1);
    } else {
      setLoading(true);
      setError(null);
      setSubmitted(true);
      try {
        // Prepare data for API
        const payload = {
          name: form.name,
          gender: form.gender,
          date_of_birth: form.dob,
          time_of_birth: form.tob,
          place_id: form.place_id,
        };
        const res = await apiService.calculateHoroscope(payload);
        setResult(res);
      } catch (err) {
        setError('Failed to calculate horoscope. Please try again.');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleBack = () => {
    if (step > 0) setStep(step - 1);
  };

  const handleChange = (key, value) => {
    setForm({ ...form, [key]: value });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#f6f7fb] transition-colors duration-500">
      <div className="backdrop-blur-lg bg-[#e7eaf3] dark:bg-black/30 rounded-3xl shadow-2xl p-8 w-full max-w-md flex flex-col items-center border border-white/20">
        {/* Avatar Picker */}
        <div className="flex flex-col items-center mb-6">
          <div className="text-5xl mb-2 cursor-pointer animate-bounce">
            {avatar}
          </div>
          <div className="flex flex-wrap gap-2 justify-center">
            {avatars.map((a) => (
              <button
                key={a}
                className={`text-2xl p-1 rounded-full hover:bg-white/20 focus:outline-none ${avatar === a ? 'ring-2 ring-pink-400' : ''}`}
                onClick={() => setAvatar(a)}
                aria-label={`Pick avatar ${a}`}
              >
                {a}
              </button>
            ))}
          </div>
        </div>
        {/* Progress Bar */}
        <div className="w-full h-2 bg-white/20 rounded-full mb-6">
          <div
            className="h-2 rounded-full bg-gradient-to-r from-pink-400 via-blue-400 to-purple-400 transition-all duration-500"
            style={{ width: `${((step + 1) / steps.length) * 100}%` }}
          />
        </div>
        {/* Conversational Stepper */}
        {!submitted ? (
          <div className="w-full flex flex-col items-center animate-fade-in">
            <div className="text-lg font-semibold mb-4 flex items-center gap-2">
              <span className="text-2xl">{steps[step].icon}</span>
              {steps[step].label.replace('name', form.name || 'you')}
            </div>
            {/* Input Field */}
            {steps[step].type === 'text' && (
              <input
                type="text"
                className="w-full p-3 rounded-xl bg-white/20 text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-pink-400 mb-4"
                placeholder={steps[step].placeholder}
                value={form[steps[step].key] || ''}
                onChange={e => handleChange(steps[step].key, e.target.value)}
                autoFocus
              />
            )}
            {steps[step].type === 'select' && (
              <select
                className="w-full p-3 rounded-xl bg-white/20 text-black focus:outline-none focus:ring-2 focus:ring-blue-400 mb-4"
                value={form[steps[step].key] || ''}
                onChange={e => handleChange(steps[step].key, e.target.value)}
              >
                <option value="" disabled>Select gender</option>
                {steps[step].options.map(opt => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
            )}
            {steps[step].type === 'date' && (
              <input
                type="date"
                className="w-full p-3 rounded-xl bg-white/20 text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-400 mb-4"
                value={form[steps[step].key] || ''}
                onChange={e => handleChange(steps[step].key, e.target.value)}
              />
            )}
            {steps[step].type === 'time' && (
              <input
                type="time"
                className="w-full p-3 rounded-xl bg-white/20 text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-400 mb-4"
                value={form[steps[step].key] || ''}
                onChange={e => handleChange(steps[step].key, e.target.value)}
              />
            )}
            {steps[step]?.type === 'place' && (
              <select
                className="w-full p-3 rounded-xl bg-white/20 text-black focus:outline-none focus:ring-2 focus:ring-blue-400 mb-4"
                value={form['place_id'] || ''}
                onChange={e => handleChange('place_id', e.target.value)}
                disabled={placesLoading}
              >
                <option value="" disabled>{placesLoading ? 'Loading places...' : 'Select place of birth'}</option>
                {places.map(place => (
                  <option key={place.id} value={place.id}>{place.name}</option>
                ))}
              </select>
            )}
            {/* Navigation Buttons */}
            <div className="flex w-full justify-between mt-2">
              <button
                className="px-4 py-2 rounded-xl bg-white/10 text-white hover:bg-white/20 transition disabled:opacity-30"
                onClick={handleBack}
                disabled={step === 0}
              >
                ⬅️ Back
              </button>
              <button
                className="px-6 py-2 rounded-xl bg-gradient-to-r from-pink-500 to-blue-500 text-white font-bold shadow-lg hover:scale-105 active:scale-95 transition-all duration-200 animate-glow"
                onClick={handleNext}
                disabled={!form[steps[step].key]}
              >
                {step === steps.length - 1 ? '🌟 Calculate Horoscope' : 'Next ➡️'}
              </button>
            </div>
          </div>
        ) : loading ? (
          <div className="w-full flex flex-col items-center animate-fade-in">
            <div className="text-3xl mb-4 animate-bounce">🔮</div>
            <div className="text-xl font-bold mb-2">All set, {form.name || 'friend'}!</div>
            <div className="text-lg text-white/80 mb-4">Your horoscope is being calculated...</div>
          </div>
        ) : result ? (
          <HoroscopeResultGenZ result={result} avatar={avatar} />
        ) : error ? (
          <div className="w-full flex flex-col items-center animate-fade-in">
            <div className="text-3xl mb-4">⚠️</div>
            <div className="text-xl font-bold mb-2 text-red-400">{error}</div>
            <button className="mt-4 px-4 py-2 rounded-xl bg-gradient-to-r from-pink-500 to-blue-500 text-white font-bold shadow-lg" onClick={() => setSubmitted(false)}>Try Again</button>
          </div>
        ) : null}
      </div>
      {/* Animations */}
      <style jsx>{`
        .animate-fade-in {
          animation: fadeIn 0.7s;
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-glow {
          box-shadow: 0 0 16px 2px #a21caf88, 0 0 32px 4px #2563eb55;
        }
      `}</style>
    </div>
  );
} 