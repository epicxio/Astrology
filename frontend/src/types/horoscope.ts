export interface Horoscope {
  id: number;
  name: string;
  date_of_birth: string;
  time_of_birth: string;
  place: string;
  rashi: string;
  nakshatra: string;
  lagna: string;
  planetary_positions?: string;
  planetary_strengths?: string | Record<string, {
    sthana_bala: number;
    dig_bala: number;
    drik_bala: number;
    conjunction: number;
    avastha: number;
    navamsa: number;
    total: number;
  }>;
} 