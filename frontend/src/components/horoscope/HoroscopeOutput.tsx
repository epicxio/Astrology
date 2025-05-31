import React from "react";
import PlanetaryStrengthCard from "./PlanetaryStrengthCard";

type PlanetaryPosition = {
  longitude: number;
  latitude: number;
  distance: number;
  speed: number;
  dms?: string;
  dms_in_sign?: string;
  degree_in_sign?: number;
  rasi?: string;
  rasi_lord?: string;
  nakshatra?: string;
  nakshatra_lord?: string;
  retrograde?: boolean;
};

type Predictions = {
  career?: string;
  health?: string;
  relationships?: string;
  finance?: string;
  bestMatches?: string[];
};

type HoroscopeResultType = {
  id?: number;
  name: string;
  gender: string;
  date_of_birth: string;
  time_of_birth: string;
  place_name: string;
  rashi: string;
  nakshatra: string;
  lagna: string;
  planetary_positions: { [planet: string]: PlanetaryPosition };
  predictions?: Predictions;
  ascendant_long?: number;
  rasi_lord?: string;
  lagna_lord?: string;
  nakshatra_lord?: string;
  planetary_strengths?: {
    [planet: string]: {
      sthana_bala: number;
      dig_bala: number;
      drik_bala: number;
      conjunction: number;
      avastha: number;
      navamsa: number;
      total: number;
    };
  };
};

type HoroscopeOutputProps = {
  result: HoroscopeResultType | null;
};

const PLANET_ICONS: { [planet: string]: string } = {
  Sun: "☉",
  Moon: "☽",
  Mercury: "☿",
  Venus: "♀",
  Mars: "♂",
  Jupiter: "♃",
  Saturn: "♄",
  Ascendant: "↑",
  Rahu: "☊",
  Ketu: "☋"
};

const HoroscopeOutput: React.FC<HoroscopeOutputProps> = ({ result }) => {
  if (!result) return null;

  // Debug: Log the full API response
  console.log('Horoscope API result:', result);
  console.log('planetary_strengths:', result.planetary_strengths);

  // Defensive: check if planetary_strengths is a non-empty object
  const hasStrengths = result.planetary_strengths && Object.keys(result.planetary_strengths).length > 0;

  return (
    <div className="horoscope-output-window" style={{
      border: "1px solid #ccc",
      padding: 24,
      marginTop: 24,
      borderRadius: 8,
      background: "#fafbfc"
    }}>
      <h2>Horoscope Result</h2>
      <ul>
        <li><strong>Name:</strong> {result.name}</li>
        <li><strong>Gender:</strong> {result.gender}</li>
        <li><strong>Date of Birth:</strong> {result.date_of_birth}</li>
        <li><strong>Time of Birth:</strong> {result.time_of_birth}</li>
        <li><strong>Place:</strong> {result.place_name}</li>
        <li><strong>Rashi:</strong> {result.rashi}</li>
        <li><strong>Nakshatra:</strong> {result.nakshatra}</li>
        <li><strong>Lagna:</strong> {result.lagna}</li>
        <li>
          <strong>Ascendant Longitude:</strong>{" "}
          {result.ascendant_long !== undefined
            ? Number(result.ascendant_long).toFixed(4) + "°"
            : "N/A"}
        </li>
      </ul>
      <div style={{ marginBottom: 16, marginTop: 8 }}>
        <strong>Rasi Lord for this chart:</strong> {result.rasi_lord || 'N/A'}<br />
        <strong>Lagna Lord for this chart:</strong> {result.lagna_lord || 'N/A'}<br />
        <strong>Nakshatra Lord for this chart:</strong> {result.nakshatra_lord || 'N/A'}
      </div>

      {/* Planetary Strength Analysis */}
      {hasStrengths && (
        <div className="mt-8">
          <h3 className="text-xl font-bold mb-4">Planetary Strength Analysis</h3>
          <div className="grid grid-cols-1 gap-6">
            {Object.entries(result.planetary_strengths!).map(([planet, strengths]) => {
              // Defensive: ensure strengths is an object with required fields
              if (!strengths || typeof strengths !== 'object' || !('total' in strengths)) {
                return (
                  <div key={planet} style={{ color: 'red' }}>
                    Error: Invalid strengths data for {planet}
                  </div>
                );
              }
              return (
                <PlanetaryStrengthCard
                  key={planet}
                  planet={planet}
                  strengths={strengths}
                  planetaryPositions={result.planetary_positions}
                />
              );
            })}
          </div>
        </div>
      )}
      {!hasStrengths && (
        <div style={{ color: 'red', margin: '16px 0' }}>
          No planetary strengths data available.
        </div>
      )}

      <h3>Predictions</h3>
      <ul>
        <li><strong>Career:</strong> {result.predictions?.career || "N/A"}</li>
        <li><strong>Health:</strong> {result.predictions?.health || "N/A"}</li>
        <li><strong>Relationships:</strong> {result.predictions?.relationships || "N/A"}</li>
        <li><strong>Finance:</strong> {result.predictions?.finance || "N/A"}</li>
        <li>
          <strong>Best Matches:</strong>{" "}
          {result.predictions?.bestMatches?.length
            ? result.predictions.bestMatches.join(", ")
            : "N/A"}
        </li>
      </ul>
      <h3>Planetary Positions</h3>
      {/* Classic Vedic order for planets */}
      {(() => {
        const classicOrder = [
          "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Ascendant", "Rahu", "Ketu"
        ];
        return (
          <table style={{ width: "100%", borderCollapse: "collapse", marginBottom: 24 }}>
            <thead>
              <tr>
                <th>Icon</th>
                <th>Planet</th>
                <th>Positions</th>
                <th>Degree</th>
                <th>Rasi</th>
                <th>Rasi Lord</th>
                <th>Nakshatra</th>
                <th>Nakshatra Lord</th>
                <th>Retrograde</th>
              </tr>
            </thead>
            <tbody>
              {classicOrder.map((planet) => {
                const pos = result.planetary_positions[planet];
                if (!pos) return null;
                return (
                  <tr key={planet}>
                    <td style={{ fontSize: 20, textAlign: 'center' }}>{PLANET_ICONS[planet] || ''}</td>
                    <td>{planet}</td>
                    <td>{pos.dms}</td>
                    <td>{pos.dms_in_sign || (pos.degree_in_sign !== undefined ? pos.degree_in_sign : '')}</td>
                    <td>{pos.rasi}</td>
                    <td>{pos.rasi_lord}</td>
                    <td>{pos.nakshatra}</td>
                    <td>{pos.nakshatra_lord}</td>
                    <td>{pos.retrograde ? "℞" : ""}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        );
      })()}
      {/* South Indian Rasi Chart */}
      {result.id && (
        <div style={{ marginTop: 32, textAlign: 'center' }}>
          <h3>South Indian Style Rasi Chart</h3>
          <img
            src={`http://localhost:5001/api/horoscope/chart/south/${result.id}`}
            alt="South Indian Rasi Chart"
            style={{ maxWidth: 400, width: '100%', border: '2px solid #c9b89a', borderRadius: 8, background: '#fff8e1', margin: '0 auto' }}
          />
        </div>
      )}
    </div>
  );
};

export default HoroscopeOutput; 