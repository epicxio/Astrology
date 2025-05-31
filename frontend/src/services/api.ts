import axios from 'axios';
import { MatchMakingRecord } from '../components/matchmaking/MatchMakingRecord';

// Base URL for API requests
// const BASE_URL = 'http://localhost:5001/api';
const BASE_URL = 'https://astrology-backend.fly.dev/api';

// Create axios instance with base URL
const api = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interfaces for requests and responses
export interface HoroscopeRequest {
    name: string;
    gender: string;
    date_of_birth: string;
    time_of_birth: string;
    place_id: number;
}

export interface MatchMakingRequest {
    bride: {
        name: string;
        gender: string;
        date_of_birth: string;
        time_of_birth: string;
        place_id: number;
    };
    groom: {
        name: string;
        gender: string;
        date_of_birth: string;
        time_of_birth: string;
        place_id: number;
    };
}

export interface HoroscopeResponse {
    id: number;
    name: string;
    gender: string;
    date_of_birth: string;
    time_of_birth: string;
    place_id: number;
    rashi: string;
    nakshatra: string;
    lagna: string;
    planetary_positions: string;
    created_at: string;
    updated_at: string | null;
}

export interface MatchMakingResponse {
    id: number;
    bride_id: number;
    groom_id: number;
    compatibility_score: number;
    details: string;
    created_at: string;
    updated_at: string | null;
}

export interface Place {
    id: number;
    name: string;
    latitude: number;
    longitude: number;
    timezone: string;
}

// API methods
export const apiService = {
    // Places
    getPlaces: async (): Promise<Place[]> => {
        const response = await api.get<Place[]>('/places');
        return response.data;
    },

    // Horoscope
    calculateHoroscope: async (data: HoroscopeRequest): Promise<HoroscopeResponse> => {
        const response = await api.post<HoroscopeResponse>('/horoscope/calculate', data);
        return response.data;
    },

    getHoroscopeReport: async (horoscopeId: number, language: string): Promise<Blob> => {
        const response = await api.get(`/reports/horoscope/${horoscopeId}`, {
            params: { language },
            responseType: 'blob'
        });
        if (response.data.type !== "application/pdf") {
            const text = await response.data.text();
            throw new Error(text || "Server did not return a PDF file.");
        }
        return response.data;
    },

    // Matchmaking
    calculateMatchMaking: async (data: MatchMakingRequest): Promise<MatchMakingResponse> => {
        const response = await api.post<MatchMakingResponse>('/matchmaking/calculate', data);
        return response.data;
    },

    getMatchMakingReport: async (matchId: number, language: string): Promise<Blob> => {
        const response = await api.get(`/reports/matchmaking/${matchId}`, {
            params: { language },
            responseType: 'blob'
        });
        return response.data;
    },

    getMatchMakingRecords: async (): Promise<MatchMakingRecord[]> => {
        const response = await fetch(`${BASE_URL}/matchmaking/`);
        if (!response.ok) throw new Error('Failed to fetch matchmaking records');
        return response.json();
    }
};

export default apiService; 