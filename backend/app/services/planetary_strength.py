from typing import Dict, Any, List, Tuple
import math

# Constants for planetary strength calculations
EXALTATION_POINTS = {
    "Sun": {"Mesha": 10},  # Exalted in Aries
    "Moon": {"Vrishabha": 10},  # Exalted in Taurus
    "Mars": {"Makara": 10},  # Exalted in Capricorn
    "Mercury": {"Kanya": 10},  # Exalted in Virgo
    "Jupiter": {"Kataka": 10},  # Exalted in Cancer
    "Venus": {"Meena": 10},  # Exalted in Pisces
    "Saturn": {"Tula": 10},  # Exalted in Libra
}

DEBILITATION_POINTS = {
    "Sun": {"Tula": -10},  # Debilitated in Libra
    "Moon": {"Vrischika": -10},  # Debilitated in Scorpio
    "Mars": {"Kataka": -10},  # Debilitated in Cancer
    "Mercury": {"Meena": -10},  # Debilitated in Pisces
    "Jupiter": {"Makara": -10},  # Debilitated in Capricorn
    "Venus": {"Kanya": -10},  # Debilitated in Virgo
    "Saturn": {"Mesha": -10},  # Debilitated in Aries
}

DIG_BALA = {
    "Sun": {"Mesha": 10, "Simha": 10},  # Strong in 1st and 5th
    "Moon": {"Kataka": 10, "Meena": 10},  # Strong in 4th and 12th
    "Mars": {"Mesha": 10, "Vrischika": 10},  # Strong in 1st and 8th
    "Mercury": {"Mithuna": 10, "Kanya": 10},  # Strong in 3rd and 6th
    "Jupiter": {"Dhanu": 10, "Meena": 10},  # Strong in 9th and 12th
    "Venus": {"Vrishabha": 10, "Tula": 10},  # Strong in 2nd and 7th
    "Saturn": {"Makara": 10, "Kumbha": 10},  # Strong in 10th and 11th
}

# Aspect relationships (planets that aspect each other)
ASPECTS = {
    "Sun": ["Mars", "Jupiter", "Saturn"],
    "Moon": ["Mars", "Jupiter", "Saturn"],
    "Mars": ["Sun", "Moon", "Jupiter", "Saturn"],
    "Mercury": ["Jupiter", "Saturn"],
    "Jupiter": ["Sun", "Moon", "Mars", "Mercury", "Saturn"],
    "Venus": ["Saturn"],
    "Saturn": ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus"],
}

PLANET_ICONS = {
    "Sun": "☉",
    "Moon": "☽",
    "Mars": "♂",
    "Mercury": "☿",
    "Jupiter": "♃",
    "Venus": "♀",
    "Saturn": "♄",
}

def calculate_sthana_bala(planet: str, rasi: str) -> float:
    """Calculate Sthana Bala (positional strength) based on sign placement."""
    score = 0.0
    
    # Check exaltation
    if planet in EXALTATION_POINTS and rasi in EXALTATION_POINTS[planet]:
        score += EXALTATION_POINTS[planet][rasi]
    
    # Check debilitation
    if planet in DEBILITATION_POINTS and rasi in DEBILITATION_POINTS[planet]:
        score += DEBILITATION_POINTS[planet][rasi]
    
    return score

def calculate_dig_bala(planet: str, rasi: str) -> float:
    """Calculate Dig Bala (directional strength) based on house position."""
    if planet in DIG_BALA and rasi in DIG_BALA[planet]:
        return DIG_BALA[planet][rasi]
    return 0.0

def calculate_drik_bala(planet: str, planetary_positions: Dict[str, Any]) -> float:
    """Calculate Drik Bala (aspectual strength) based on aspects from other planets."""
    score = 0.0
    
    if planet not in ASPECTS:
        return score
    
    for aspecting_planet in ASPECTS[planet]:
        if aspecting_planet in planetary_positions:
            # Simple aspect calculation - can be enhanced with orb logic
            score += 2.0
    
    return score

def calculate_conjunction_strength(planet: str, planetary_positions: Dict[str, Any]) -> float:
    """Calculate strength from conjunctions with other planets."""
    score = 0.0
    planet_long = planetary_positions[planet]["longitude"]
    
    for other_planet, other_pos in planetary_positions.items():
        if other_planet != planet:
            other_long = other_pos["longitude"]
            # Consider planets conjunct if within 10 degrees
            if abs(planet_long - other_long) <= 10:
                score += 1.0
    
    return score

def calculate_avastha(planet: str, planetary_positions: Dict[str, Any]) -> float:
    """Calculate Avastha (planetary state) strength."""
    score = 0.0
    pos = planetary_positions[planet]
    
    # Check if planet is retrograde
    if pos.get("retrograde", False):
        score -= 2.0
    
    # Add basic state score
    score += 5.0
    
    return score

def calculate_navamsa_strength(planet: str, planetary_positions: Dict[str, Any]) -> float:
    """Calculate Navamsa strength (simplified version)."""
    score = 0.0
    pos = planetary_positions[planet]
    
    # Basic Navamsa calculation (can be enhanced)
    navamsa_position = (pos["longitude"] % 30) / 3.33
    score += navamsa_position
    
    return score

def compute_planet_strengths(planetary_positions: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    results = {}
    for planet, position in planetary_positions.items():
        if planet in ["Rahu", "Ketu", "Ascendant"]:
            continue

        # Sthana Bala
        sthana_bala = calculate_sthana_bala(planet, position["rasi"])
        sthana_bala_max = 10.0
        if sthana_bala > 0:
            sthana_bala_reason = f"The planet is exalted in {position['rasi']}, receiving full positional strength."
        elif sthana_bala < 0:
            sthana_bala_reason = f"The planet is debilitated in {position['rasi']}, resulting in negative positional strength."
        else:
            sthana_bala_reason = f"The planet is in a neutral sign ({position['rasi']}), so it receives no special positional strength."
        sthana_bala_explanation = (
            f"Sthana Bala: {sthana_bala:.1f}/{sthana_bala_max:.1f}. {sthana_bala_reason} "
            f"(Scale: -10.0 to +10.0, where 10.0 is maximum exaltation, -10.0 is maximum debilitation, 0.0 is neutral.)"
        )

        # Dig Bala
        dig_bala = calculate_dig_bala(planet, position["rasi"])
        dig_bala_max = 10.0
        house_val = position.get('house', None)
        if house_val is None or house_val == 'N/A':
            dig_bala_explanation = (
                f"Dig Bala: Not applicable. House placement is not relevant for {planet}, as it is not traditionally assigned in this context."
            )
        elif dig_bala > 0:
            dig_bala_explanation = (
                f"Dig Bala: {dig_bala:.1f}/{dig_bala_max:.1f}. {planet} is in a house that grants full directional strength. "
                f"(Scale: 0.0 to 10.0, where 10.0 is maximum directional strength.)"
            )
        else:
            dig_bala_explanation = (
                f"Dig Bala: {dig_bala:.1f}/{dig_bala_max:.1f}. {planet} is not in a house that grants directional strength. "
                f"(Scale: 0.0 to 10.0, where 10.0 is maximum directional strength.)"
            )

        # Drik Bala
        drik_bala = calculate_drik_bala(planet, planetary_positions)
        drik_bala_max = 10.0
        aspected_by = [p for p in planetary_positions if p != planet]
        if drik_bala > 0:
            drik_bala_reason = f"Receives strong aspects from: {', '.join(aspected_by)}."
        else:
            drik_bala_reason = f"No significant aspects from other planets."
        drik_bala_explanation = (
            f"Drik Bala: {drik_bala:.1f}/{drik_bala_max:.1f}. {drik_bala_reason} "
            f"(Scale: 0.0 to 10.0, where 10.0 is maximum aspectual strength.)"
        )

        # Conjunction
        conjunction = calculate_conjunction_strength(planet, planetary_positions)
        conjunction_max = 5.0
        conjunct_planets = [p for p, pos in planetary_positions.items() if p != planet and abs(pos['longitude'] - position['longitude']) <= 10]
        if conjunct_planets:
            conjunction_explanation = (
                f"Conjunction: {conjunction:.1f}/{conjunction_max:.1f}. Conjunct with: {', '.join(conjunct_planets)}. "
                f"(Conjunctions occur when planets are within 10° of each other, blending their energies.)"
            )
        else:
            conjunction_explanation = (
                f"Conjunction: {conjunction:.1f}/{conjunction_max:.1f}. No conjunctions: {planet} is not within close proximity (10°) to any other planet in this chart. "
                f"(Conjunctions amplify or blend planetary effects.)"
            )

        # Avastha
        avastha = calculate_avastha(planet, planetary_positions)
        avastha_max = 5.0
        avastha_state = 'Retrograde' if position.get('retrograde') else 'Direct'
        avastha_explanation = (
            f"Avastha: {avastha:.1f}/{avastha_max:.1f}. State: {avastha_state}. "
            f"{'Fully functional.' if avastha > 0 else 'Somewhat weak.'} "
            f"(Scale: -2.0 to 5.0, where 5.0 is fully functional, -2.0 is retrograde/weak.)"
        )

        # Navamsa
        navamsa_max = 10.0
        navamsa_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        if planet in navamsa_planets:
            navamsa_val = position.get('navamsa', None)
            if navamsa_val is None or navamsa_val == 'N/A':
                navamsa = None
                navamsa_explanation = f"Navamsa: Not considered for {planet} in classical astrology."
            else:
                navamsa = calculate_navamsa_strength(planet, planetary_positions)
                navamsa_explanation = (
                    f"Navamsa: {navamsa:.1f}/{navamsa_max:.1f}. {planet} is in Navamsa {navamsa_val}. "
                    f"{'Strong in Navamsa.' if navamsa > 0 else 'Weak in Navamsa.'} "
                    f"(Scale: 0.0 to 10.0, where 10.0 is maximum strength in Navamsa.)"
                )
        else:
            navamsa = None
            navamsa_explanation = (
                f"Navamsa is not calculated for {planet}, as it is not traditionally interpreted in classical astrology."
            )

        total = sthana_bala + dig_bala + drik_bala + conjunction + avastha + (navamsa if navamsa is not None else 0.0)

        # --- DETAILED SUMMARY ---
        bullet = PLANET_ICONS.get(planet, "•")
        summary = (
            f"\n{planet} summary:\n"
            f"  {bullet} {sthana_bala_reason}\n"
            f"  {bullet} {'House placement is not relevant.' if house_val is None or house_val == 'N/A' else dig_bala_explanation.split('. ', 1)[1] if '. ' in dig_bala_explanation else dig_bala_explanation}\n"
            f"  {bullet} {drik_bala_reason}\n"
            f"  {bullet} {'No conjunctions.' if not conjunct_planets else f'Conjunct with: {', '.join(conjunct_planets)} (within 10°), blending their energies.'}\n"
            f"  {bullet} State: {avastha_state}. {'Fully functional.' if avastha > 0 else 'Somewhat weak.'}\n"
            f"  {bullet} {'Navamsa is not considered for this planet in classical astrology.' if navamsa_val is None or navamsa_val == 'N/A' else navamsa_explanation.split('. ', 1)[1] if '. ' in navamsa_explanation else navamsa_explanation}\n"
            f"\nOverall, {planet} in this chart: "
            f"{sthana_bala_reason} {dig_bala_explanation} {drik_bala_reason} {conjunction_explanation} {avastha_explanation} {navamsa_explanation}"
        )

        results[planet] = {
            "sthana_bala": sthana_bala,
            "sthana_bala_explanation": sthana_bala_explanation,
            "dig_bala": dig_bala,
            "dig_bala_explanation": dig_bala_explanation,
            "drik_bala": drik_bala,
            "drik_bala_explanation": drik_bala_explanation,
            "conjunction": conjunction,
            "conjunction_explanation": conjunction_explanation,
            "avastha": avastha,
            "avastha_explanation": avastha_explanation,
            "navamsa": navamsa,
            "navamsa_explanation": navamsa_explanation,
            "total": total,
            "summary": summary
        }
    return results 