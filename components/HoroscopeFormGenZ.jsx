import React, { useState } from 'react';
import { apiService } from '../services/api';

const avatars = [
  '🦄', '🐉', '👽', '🧑‍🎤', '🦸‍♂️', '🧙‍♀️', '🐼', '🦊', '🐧', '🦋', '🌈', '💫'
];

const steps = [
  { key: 'name', label: "What's your name?", icon: '🧑‍🦱', type: 'text', placeholder: 'Enter your name' },
  { key: 'gender', label: "What's your gender?", icon: '♀️', type: 'select', options: ['Male', 'Female', 'Other'] },
  { key: 'dob', label: 'When were you born?', icon: '🗓️', type: 'date' },
  { key: 'tob', label: 'What time?', icon: '⏰', type: 'time' },
  { key: 'place', label: 'Where were you born?', icon: '📍', type: 'text', placeholder: 'Enter place of birth' },
];

export default function HoroscopeFormGenZ() {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState({});
  const [avatar, setAvatar] = useState(avatars[0]);
  const [submitted, setSubmitted] = useState(false);
  const [places, setPlaces] = useState([]);

  const handleNext = () => {
    if (step < steps.length - 1) setStep(step + 1);
    else setSubmitted(true);
  };

  const handleBack = () => {
    if (step > 0) setStep(step - 1);
  };

  const handleChange = (key, value) => {
    setForm({ ...form, [key]: value });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-900 via-blue-900 to-pink-700 dark:bg-black transition-colors duration-500">
      <div className="backdrop-blur-lg bg-white/10 dark:bg-black/30 rounded-3xl shadow-2xl p-8 w-full max-w-md flex flex-col items-center border border-white/20">
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
                className="w-full p-3 rounded-xl bg-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-pink-400 mb-4"
                placeholder={steps[step].placeholder}
                value={form[steps[step].key] || ''}
                onChange={e => handleChange(steps[step].key, e.target.value)}
                autoFocus
              />
            )}
            {steps[step].type === 'select' && (
              <select
                className="w-full p-3 rounded-xl bg-white/20 text-white focus:outline-none focus:ring-2 focus:ring-blue-400 mb-4"
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
                className="w-full p-3 rounded-xl bg-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-blue-400 mb-4"
                value={form[steps[step].key] || ''}
                onChange={e => handleChange(steps[step].key, e.target.value)}
              />
            )}
            {steps[step].type === 'time' && (
              <input
                type="time"
                className="w-full p-3 rounded-xl bg-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-purple-400 mb-4"
                value={form[steps[step].key] || ''}
                onChange={e => handleChange(steps[step].key, e.target.value)}
              />
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
        ) : (
          <div className="w-full flex flex-col items-center animate-fade-in">
            <div className="text-3xl mb-4">🔮</div>
            <div className="text-xl font-bold mb-2">All set, {form.name || 'friend'}!</div>
            <div className="text-lg text-white/80 mb-4">Your horoscope is being calculated...</div>
            {/* Placeholder for result */}
          </div>
        )}
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