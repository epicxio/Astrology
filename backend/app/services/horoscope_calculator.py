from datetime import date, time, datetime
from typing import Dict, Any
import swisseph as swe
import pytz
from .planetary_strength import compute_planet_strengths

RASHIS = [
    "Mesha", "Vrishabha", "Mithuna", "Kataka", "Simha", "Kanya",
    "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

NAKSHATRA_SPAN = 13 + (20/60)  # 13°20'

RASI_LORDS = {
    "Mesha": "Mars", "Vrishabha": "Venus", "Mithuna": "Mercury", "Kataka": "Moon",
    "Simha": "Sun", "Kanya": "Mercury", "Tula": "Venus", "Vrischika": "Mars",
    "Dhanu": "Jupiter", "Makara": "Saturn", "Kumbha": "Saturn", "Meena": "Jupiter"
}

NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
]

def dms(deg):
    d = int(deg)
    m = int((deg - d) * 60)
    return f"{d}° {m}'"

def calculate_horoscope(
    date_of_birth: date,
    time_of_birth: time,
    latitude: float,
    longitude: float,
    timezone: str,
    gender: str
) -> Dict[str, Any]:
    """
    Calculate horoscope details using Swiss Ephemeris (sidereal/Lahiri).
    """
    # Combine date and time, localize to timezone, then convert to UTC
    dt_naive = datetime.combine(date_of_birth, time_of_birth)
    tz = pytz.timezone(timezone)
    dt_local = tz.localize(dt_naive)
    dt_utc = dt_local.astimezone(pytz.utc)

    # Debug: Print longitude, local and UTC datetime
    print(f"Longitude used: {longitude}")
    print(f"Latitude used: {latitude}")
    print(f"Local datetime: {dt_local}")
    print(f"UTC datetime: {dt_utc}")

    # Calculate Julian Day in UT
    jd_ut = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute/60 + dt_utc.second/3600)
    print(f"Julian Day UT: {jd_ut}")

    # Set sidereal mode to Lahiri
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    # Calculate Moon position (tropical)
    moon_pos = swe.calc_ut(jd_ut, swe.MOON)[0]
    # Get ayanamsa
    ayanamsa = swe.get_ayanamsa_ut(jd_ut)
    # Sidereal longitude
    sid_moon_long = (moon_pos[0] - ayanamsa) % 360

    # Calculate Rashi (zodiac sign) using sidereal longitude
    rashi_index = int(sid_moon_long // 30) % 12
    rashi = RASHIS[rashi_index]

    # Calculate Nakshatra using sidereal longitude
    nakshatra_index = int(sid_moon_long // NAKSHATRA_SPAN)
    nakshatra = NAKSHATRAS[nakshatra_index % 27]

    # Calculate true Lagna (Ascendant) using Swiss Ephemeris
    houses, ascmc = swe.houses_ex(jd_ut, latitude, longitude, b'P')
    ascendant_long = ascmc[0] % 360
    # Convert Ascendant to sidereal (subtract ayanamsa)
    sidereal_ascendant = (ascendant_long - ayanamsa) % 360
    lagna_index = int(sidereal_ascendant // 30) % 12
    lagna = RASHIS[lagna_index]
    print(f"Ascendant longitude (tropical): {ascendant_long}")
    print(f"Ayanamsa: {ayanamsa}")
    print(f"Ascendant longitude (sidereal): {sidereal_ascendant}")
    print(f"Lagna index: {lagna_index}, Lagna: {lagna}")

    # Calculate planets and Rahu (Mean Node) only
    planetary_positions = {}
    for planet, name in zip(
        [swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER, swe.VENUS, swe.SATURN, swe.MEAN_NODE],
        ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu"]
    ):
        pos = swe.calc_ut(jd_ut, planet)[0]
        sid_long = (pos[0] - ayanamsa) % 360
        rasi_index = int(sid_long // 30) % 12
        nakshatra_index = int(sid_long // NAKSHATRA_SPAN)
        deg_in_sign = sid_long % 30
        planetary_positions[name] = {
            "longitude": sid_long,
            "degree": round(sid_long, 4),
            "dms": dms(sid_long),
            "degree_in_sign": round(deg_in_sign, 4),
            "dms_in_sign": dms(deg_in_sign),
            "rasi": RASHIS[rasi_index],
            "rasi_lord": RASI_LORDS[RASHIS[rasi_index]],
            "nakshatra": NAKSHATRAS[nakshatra_index % 27],
            "nakshatra_lord": NAKSHATRA_LORDS[nakshatra_index % 27],
            "retrograde": pos[3] < 0,
            "latitude": pos[1],
            "distance": pos[2],
            "speed": pos[3] if len(pos) > 3 else 0
        }

    # Add Ketu as Rahu + 180°
    rahu_long = planetary_positions["Rahu"]["longitude"]
    ketu_long = (rahu_long + 180) % 360
    ketu_rasi_index = int(ketu_long // 30) % 12
    ketu_nakshatra_index = int(ketu_long // NAKSHATRA_SPAN)
    ketu_deg_in_sign = ketu_long % 30
    planetary_positions["Ketu"] = {
        "longitude": ketu_long,
        "degree": round(ketu_long, 4),
        "dms": dms(ketu_long),
        "degree_in_sign": round(ketu_deg_in_sign, 4),
        "dms_in_sign": dms(ketu_deg_in_sign),
        "rasi": RASHIS[ketu_rasi_index],
        "rasi_lord": RASI_LORDS[RASHIS[ketu_rasi_index]],
        "nakshatra": NAKSHATRAS[ketu_nakshatra_index % 27],
        "nakshatra_lord": NAKSHATRA_LORDS[ketu_nakshatra_index % 27],
        "retrograde": True,
        "latitude": 0,
        "distance": 0,
        "speed": 0
    }

    asc_deg_in_sign = sidereal_ascendant % 30
    asc_rasi_index = int(sidereal_ascendant // 30) % 12
    asc_nakshatra_index = int(sidereal_ascendant // NAKSHATRA_SPAN)
    planetary_positions["Ascendant"] = {
        "longitude": sidereal_ascendant,
        "degree": round(sidereal_ascendant, 4),
        "dms": dms(sidereal_ascendant),
        "degree_in_sign": round(asc_deg_in_sign, 4),
        "dms_in_sign": dms(asc_deg_in_sign),
        "rasi": RASHIS[asc_rasi_index],
        "rasi_lord": RASI_LORDS[RASHIS[asc_rasi_index]],
        "nakshatra": NAKSHATRAS[asc_nakshatra_index % 27],
        "nakshatra_lord": NAKSHATRA_LORDS[asc_nakshatra_index % 27],
        "retrograde": False,
        "latitude": 0,
        "distance": 0,
        "speed": 0
    }

    # Get Rasi Lord (Moon's rasi), Lagna Lord (Ascendant's rasi), Nakshatra Lord (Moon's nakshatra)
    moon = planetary_positions.get("Moon", {})
    asc = planetary_positions.get("Ascendant", {})
    rasi_lord = moon.get("rasi_lord")
    lagna_lord = asc.get("rasi_lord")
    nakshatra_lord = moon.get("nakshatra_lord")

    # Debug: Print lords and ascendant
    print(f"Moon planetary data: {moon}")
    print(f"Ascendant planetary data: {asc}")
    print(f"Rasi Lord: {rasi_lord}")
    print(f"Lagna Lord: {lagna_lord}")
    print(f"Nakshatra Lord: {nakshatra_lord}")
    print(f"Ascendant Longitude: {sidereal_ascendant}")

    # Calculate planetary strengths
    planetary_strengths = compute_planet_strengths(planetary_positions)

    return {
        'rashi': rashi,
        'nakshatra': nakshatra,
        'lagna': lagna,
        'ascendant_long': sidereal_ascendant,
        'planetary_positions': planetary_positions,
        'rasi_lord': rasi_lord,
        'lagna_lord': lagna_lord,
        'nakshatra_lord': nakshatra_lord,
        'planetary_strengths': planetary_strengths
    } 