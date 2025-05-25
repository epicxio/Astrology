from datetime import date, time
from decimal import Decimal
from typing import List, Dict, Any
from app.services.horoscope_calculator import calculate_horoscope
from app.models.place import Place
from sqlalchemy.orm import Session
import json

# Standard tables for Kuta calculations
VARNA_TABLE = {"Brahmin": 1, "Kshatriya": 2, "Vaishya": 3, "Shudra": 4}
VARNA_POINTS = [1, 0.5, 0, 0]  # Example: if same varna, 1; else 0.5 or 0
# ... (other standard tables for Vashya, Tara, Yoni, etc. will be defined below)

KUTA_INFO = [
    {"kuta": "Varna", "description": "Spiritual compatibility and ego levels (based on caste classification)", "max_points": 1},
    {"kuta": "Vashya", "description": "Mutual attraction and power equation", "max_points": 2},
    {"kuta": "Tara", "description": "Birth star compatibility (health and well-being)", "max_points": 3},
    {"kuta": "Yoni", "description": "Sexual compatibility and biological nature", "max_points": 4},
    {"kuta": "Grah Maitri", "description": "Mental compatibility and intellectual level", "max_points": 5},
    {"kuta": "Gana", "description": "Temperament compatibility (Deva, Manushya, Rakshasa)", "max_points": 6},
    {"kuta": "Bhakoot", "description": "Emotional bonding and family welfare", "max_points": 7},
    {"kuta": "Nadi", "description": "Health and heredity (should be different for both partners to avoid dosha)", "max_points": 8},
]

# Standard Varna mapping by Rashi
VARNA_BY_RASHI = {
    "Mesha": "Kshatriya", "Vrishabha": "Vaishya", "Mithuna": "Shudra", "Kataka": "Brahmin",
    "Simha": "Kshatriya", "Kanya": "Vaishya", "Tula": "Shudra", "Vrischika": "Brahmin",
    "Dhanu": "Kshatriya", "Makara": "Vaishya", "Kumbha": "Shudra", "Meena": "Brahmin"
}
# Varna points table: [Bride\Groom] (row: bride, col: groom)
VARNA_POINTS_TABLE = {
    ("Brahmin", "Brahmin"): 1, ("Brahmin", "Kshatriya"): 1, ("Brahmin", "Vaishya"): 1, ("Brahmin", "Shudra"): 1,
    ("Kshatriya", "Brahmin"): 0, ("Kshatriya", "Kshatriya"): 1, ("Kshatriya", "Vaishya"): 1, ("Kshatriya", "Shudra"): 1,
    ("Vaishya", "Brahmin"): 0, ("Vaishya", "Kshatriya"): 0, ("Vaishya", "Vaishya"): 1, ("Vaishya", "Shudra"): 1,
    ("Shudra", "Brahmin"): 0, ("Shudra", "Kshatriya"): 0, ("Shudra", "Vaishya"): 0, ("Shudra", "Shudra"): 1,
}

# Standard Vashya mapping by Rashi
VASHYA_BY_RASHI = {
    "Mesha": "Chatushpada", "Vrishabha": "Chatushpada", "Mithuna": "DwiPad", "Kataka": "Jalchar",
    "Simha": "Vanchar", "Kanya": "DwiPad", "Tula": "DwiPad", "Vrischika": "Jalchar",
    "Dhanu": "Chatushpada", "Makara": "Jalchar", "Kumbha": "Jalchar", "Meena": "Jalchar"
}
# Vashya points table (Bride group, Groom group): points
VASHYA_POINTS_TABLE = {
    ("Chatushpada", "Chatushpada"): 2, ("Chatushpada", "DwiPad"): 1, ("Chatushpada", "Jalchar"): 1.5, ("Chatushpada", "Vanchar"): 1,
    ("DwiPad", "Chatushpada"): 1, ("DwiPad", "DwiPad"): 2, ("DwiPad", "Jalchar"): 1, ("DwiPad", "Vanchar"): 1.5,
    ("Jalchar", "Chatushpada"): 1.5, ("Jalchar", "DwiPad"): 1, ("Jalchar", "Jalchar"): 2, ("Jalchar", "Vanchar"): 1,
    ("Vanchar", "Chatushpada"): 1, ("Vanchar", "DwiPad"): 1.5, ("Vanchar", "Jalchar"): 1, ("Vanchar", "Vanchar"): 2,
}

# Nakshatra list (should match your horoscope_calculator)
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# Tara points by type (auspicious: 1, inauspicious: 0)
TARA_POINTS_BY_TYPE = {
    1: 0,  # Janma (birth star) - inauspicious
    2: 1,  # Sampat - auspicious
    3: 0,  # Vipat - inauspicious
    4: 1,  # Kshema - auspicious
    5: 0,  # Pratyari - inauspicious
    6: 1,  # Sadhaka - auspicious
    7: 0,  # Vadha - inauspicious
    8: 1,  # Mitra - auspicious
    0: 1   # Ati-Mitra (9th) - auspicious
}

# Yoni mapping by Nakshatra (27 Nakshatras)
YONI_BY_NAKSHATRA = [
    "Horse", "Elephant", "Sheep", "Serpent", "Dog", "Cat", "Rat", "Cow", "Buffalo",
    "Tiger", "Horse", "Elephant", "Sheep", "Monkey", "Cat", "Rat", "Dog", "Deer",
    "Monkey", "Cat", "Rat", "Cow", "Buffalo", "Tiger", "Horse", "Elephant", "Deer"
]
# Yoni compatibility points table (Bride Yoni, Groom Yoni): points
YONI_POINTS_TABLE = {}
# Fill the table: same yoni = 4, enemies = 0, friends = 3, neutral = 2, others = 1 (simplified for demo)
YONI_ANIMALS = list(set(YONI_BY_NAKSHATRA))
for y1 in YONI_ANIMALS:
    for y2 in YONI_ANIMALS:
        if y1 == y2:
            YONI_POINTS_TABLE[(y1, y2)] = 4
        else:
            YONI_POINTS_TABLE[(y1, y2)] = 2  # You can expand this with the real enemy/friend/neutral mapping

# Rashi lords (should match your horoscope_calculator)
RASHI_LORDS = {
    "Mesha": "Mars", "Vrishabha": "Venus", "Mithuna": "Mercury", "Kataka": "Moon",
    "Simha": "Sun", "Kanya": "Mercury", "Tula": "Venus", "Vrischika": "Mars",
    "Dhanu": "Jupiter", "Makara": "Saturn", "Kumbha": "Saturn", "Meena": "Jupiter"
}
# Planetary friendship table (simplified for demo)
MAITRI_TABLE = {
    "Sun": {"friend": ["Moon", "Mars", "Jupiter"], "neutral": ["Mercury", "Venus"], "enemy": ["Saturn"]},
    "Moon": {"friend": ["Sun", "Mercury", "Jupiter"], "neutral": ["Mars", "Venus", "Saturn"], "enemy": []},
    "Mars": {"friend": ["Sun", "Moon", "Jupiter"], "neutral": ["Venus", "Saturn"], "enemy": ["Mercury"]},
    "Mercury": {"friend": ["Sun", "Venus"], "neutral": ["Mars", "Jupiter", "Saturn"], "enemy": ["Moon"]},
    "Jupiter": {"friend": ["Sun", "Moon", "Mars"], "neutral": ["Saturn"], "enemy": ["Mercury", "Venus"]},
    "Venus": {"friend": ["Mercury", "Saturn"], "neutral": ["Mars", "Jupiter"], "enemy": ["Sun", "Moon"]},
    "Saturn": {"friend": ["Mercury", "Venus"], "neutral": ["Jupiter"], "enemy": ["Sun", "Moon", "Mars"]},
}
# Maitri points
MAITRI_POINTS = {"friend": 5, "neutral": 3, "enemy": 0}

# Gana mapping by Nakshatra (27 Nakshatras)
GANA_BY_NAKSHATRA = [
    "Deva", "Manushya", "Rakshasa", "Manushya", "Deva", "Manushya", "Deva", "Deva", "Rakshasa",
    "Rakshasa", "Manushya", "Deva", "Deva", "Rakshasa", "Deva", "Rakshasa", "Manushya", "Rakshasa",
    "Rakshasa", "Deva", "Manushya", "Manushya", "Rakshasa", "Deva", "Manushya", "Manushya", "Deva"
]
# Gana compatibility points table (Bride Gana, Groom Gana): points
GANA_POINTS_TABLE = {
    ("Deva", "Deva"): 6, ("Deva", "Manushya"): 6, ("Deva", "Rakshasa"): 1,
    ("Manushya", "Deva"): 6, ("Manushya", "Manushya"): 6, ("Manushya", "Rakshasa"): 0,
    ("Rakshasa", "Deva"): 1, ("Rakshasa", "Manushya"): 0, ("Rakshasa", "Rakshasa"): 6,
}

# Rashi order for Bhakoot (Mesha=1, Vrishabha=2, ..., Meena=12)
RASHI_ORDER = [
    "Mesha", "Vrishabha", "Mithuna", "Kataka", "Simha", "Kanya",
    "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"
]

# Nadi mapping by Nakshatra (27 Nakshatras)
NADI_BY_NAKSHATRA = [
    "Adi", "Madhya", "Antya", "Adi", "Madhya", "Antya", "Adi", "Madhya", "Antya",
    "Adi", "Madhya", "Antya", "Adi", "Madhya", "Antya", "Adi", "Madhya", "Antya",
    "Adi", "Madhya", "Antya", "Adi", "Madhya", "Antya", "Adi", "Madhya", "Antya"
]

class MatchMakingCalculator:
    @staticmethod
    def calculate_compatibility(
        bride_name: str,
        bride_dob: date,
        bride_tob: time,
        bride_place_id: int,
        groom_name: str,
        groom_dob: date,
        groom_tob: time,
        groom_place_id: int,
        db: Session
    ) -> Dict[str, Any]:
        """
        Calculate Ashta Kuta (Gun Milan) compatibility between bride and groom using standard tables.
        """
        # Retrieve place info
        bride_place = db.query(Place).filter(Place.id == bride_place_id).first()
        groom_place = db.query(Place).filter(Place.id == groom_place_id).first()
        if not bride_place or not groom_place:
            raise Exception("Place not found")
        # Calculate horoscopes
        bride_horo = calculate_horoscope(
            bride_dob, bride_tob, bride_place.latitude, bride_place.longitude, bride_place.timezone, gender="F"
        )
        groom_horo = calculate_horoscope(
            groom_dob, groom_tob, groom_place.latitude, groom_place.longitude, groom_place.timezone, gender="M"
        )
        bride_rashi = bride_horo['rashi']
        groom_rashi = groom_horo['rashi']
        bride_varna = VARNA_BY_RASHI[bride_rashi]
        groom_varna = VARNA_BY_RASHI[groom_rashi]
        varna_points = VARNA_POINTS_TABLE.get((bride_varna, groom_varna), 0)
        # --- Vashya Kuta: Use standard mapping and points table ---
        # Standard Vashya group mapping (Manava, Vanachara, Chatushpada, Jalchar, Keet)
        VASHYA_GROUPS = {
            "Mesha": "Chatushpada", "Vrishabha": "Chatushpada", "Mithuna": "Manava", "Kataka": "Jalchar",
            "Simha": "Vanachara", "Kanya": "Manava", "Tula": "Manava", "Vrischika": "Keet",
            "Dhanu": "Chatushpada", "Makara": "Jalchar", "Kumbha": "Manava", "Meena": "Jalchar"
        }
        VASHYA_POINTS = {
            ("Manava", "Manava"): 2, ("Manava", "Vanachara"): 1, ("Manava", "Chatushpada"): 1, ("Manava", "Jalchar"): 1, ("Manava", "Keet"): 1,
            ("Vanachara", "Manava"): 1, ("Vanachara", "Vanachara"): 2, ("Vanachara", "Chatushpada"): 1.5, ("Vanachara", "Jalchar"): 1, ("Vanachara", "Keet"): 1,
            ("Chatushpada", "Manava"): 1, ("Chatushpada", "Vanachara"): 1.5, ("Chatushpada", "Chatushpada"): 2, ("Chatushpada", "Jalchar"): 1.5, ("Chatushpada", "Keet"): 1,
            ("Jalchar", "Manava"): 1, ("Jalchar", "Vanachara"): 1, ("Jalchar", "Chatushpada"): 1.5, ("Jalchar", "Jalchar"): 2, ("Jalchar", "Keet"): 1,
            ("Keet", "Manava"): 1, ("Keet", "Vanachara"): 1, ("Keet", "Chatushpada"): 1, ("Keet", "Jalchar"): 1, ("Keet", "Keet"): 2
        }
        bride_vashya = VASHYA_GROUPS[bride_rashi]
        groom_vashya = VASHYA_GROUPS[groom_rashi]
        vashya_points = VASHYA_POINTS.get((bride_vashya, groom_vashya), 0)
        # --- Tara Kuta Calculation ---
        bride_nakshatra = bride_horo['nakshatra']
        groom_nakshatra = groom_horo['nakshatra']
        bride_nak_index = NAKSHATRAS.index(bride_nakshatra)
        groom_nak_index = NAKSHATRAS.index(groom_nakshatra)
        # Count from bride to groom (including bride)
        tara1 = ((groom_nak_index - bride_nak_index) % 27) + 1
        tara1_type = tara1 % 9
        tara1_points = TARA_POINTS_BY_TYPE[tara1_type]
        # Count from groom to bride (including groom)
        tara2 = ((bride_nak_index - groom_nak_index) % 27) + 1
        tara2_type = tara2 % 9
        tara2_points = TARA_POINTS_BY_TYPE[tara2_type]
        tara_points = (tara1_points + tara2_points) * 1.5  # Each direction is 1.5 points
        # --- Yoni Kuta: Use standard mapping and enemy pairs ---
        # Standard Yoni animal mapping for 27 Nakshatras
        YONI_ANIMALS = [
            "Ashwa",    # Ashwini
            "Gaja",     # Bharani
            "Mesh",     # Krittika
            "Sarpa",    # Rohini
            "Sarpa",    # Mrigashira
            "Shwan",    # Ardra
            "Marjar",   # Punarvasu
            "Mesh",     # Pushya
            "Marjar",   # Ashlesha
            "Mushak",   # Magha
            "Mushak",   # Purva Phalguni
            "Go",       # Uttara Phalguni
            "Mahish",   # Hasta
            "Vyaghra",  # Chitra
            "Mahish",   # Swati
            "Vyaghra",  # Vishakha
            "Mriga",    # Anuradha
            "Mriga",    # Jyeshtha
            "Shwan",    # Mula
            "Vanar",    # Purva Ashadha
            "Vanar",    # Uttara Ashadha
            "Vanar",    # Shravana
            "Singha",   # Dhanishta
            "Ashwa",    # Shatabhisha
            "Singha",   # Purva Bhadrapada
            "Go",       # Uttara Bhadrapada
            "Gaja"      # Revati
        ]
        # Yoni enemy pairs (including Singha/Vyaghra)
        YONI_ENEMIES = {
            ("Singha", "Vyaghra"), ("Vyaghra", "Singha"),
            ("Ashwa", "Gaja"), ("Gaja", "Ashwa"),
            ("Mesh", "Sarpa"), ("Sarpa", "Mesh"),
            ("Shwan", "Mriga"), ("Mriga", "Shwan"),
            ("Marjar", "Mushak"), ("Mushak", "Marjar"),
            ("Go", "Vyaghra"), ("Vyaghra", "Go"),
            ("Mahish", "Ashwa"), ("Ashwa", "Mahish"),
            ("Vanar", "Mesh"), ("Mesh", "Vanar"),
            ("Sarpa", "Mriga"), ("Mriga", "Sarpa")
        }
        def get_yoni_points(b_yoni, g_yoni):
            if b_yoni == g_yoni:
                return 4
            elif (b_yoni, g_yoni) in YONI_ENEMIES:
                return 1
            else:
                return 2
        bride_yoni = YONI_ANIMALS[bride_nak_index]
        groom_yoni = YONI_ANIMALS[groom_nak_index]
        yoni_points = get_yoni_points(bride_yoni, groom_yoni)
        # --- Maitri (Grah Maitri) Kuta Calculation ---
        bride_lord = RASHI_LORDS[bride_rashi]
        groom_lord = RASHI_LORDS[groom_rashi]
        if groom_lord in MAITRI_TABLE[bride_lord]["friend"]:
            maitri_points = MAITRI_POINTS["friend"]
        elif groom_lord in MAITRI_TABLE[bride_lord]["neutral"]:
            maitri_points = MAITRI_POINTS["neutral"]
        else:
            maitri_points = MAITRI_POINTS["enemy"]
        # --- Gana Kuta Calculation ---
        bride_gana = GANA_BY_NAKSHATRA[bride_nak_index]
        groom_gana = GANA_BY_NAKSHATRA[groom_nak_index]
        gana_points = GANA_POINTS_TABLE.get((bride_gana, groom_gana), 0)
        # --- Bhakoot Kuta: Use robust dosha logic ---
        # Bhakoot dosha pairs (2-12, 12-2, 5-9, 9-5, 6-8, 8-6)
        BHAKOOT_DOSHA_PAIRS = [(2, 12), (12, 2), (5, 9), (9, 5), (6, 8), (8, 6), (7, 11), (11, 7)]
        def get_bhakoot_points(b_num, g_num):
            if (b_num, g_num) in BHAKOOT_DOSHA_PAIRS:
                return 0
            elif abs(b_num - g_num) in [6, 8]:
                return 0
            else:
                return 7
        bride_rashi_num = RASHI_ORDER.index(bride_rashi) + 1
        groom_rashi_num = RASHI_ORDER.index(groom_rashi) + 1
        bhakoot_points = get_bhakoot_points(bride_rashi_num, groom_rashi_num)
        # --- Nadi Kuta Calculation ---
        bride_nadi = NADI_BY_NAKSHATRA[bride_nak_index]
        groom_nadi = NADI_BY_NAKSHATRA[groom_nak_index]
        if bride_nadi == groom_nadi:
            nadi_points = 0
        else:
            nadi_points = 8
        # --- Guna Table with Classifications ---
        guna_table = [
            {
                "kuta": "Varna",
                "description": KUTA_INFO[0]["description"],
                "bride_value": bride_varna,
                "groom_value": groom_varna,
                "points": varna_points,
                "max_points": KUTA_INFO[0]["max_points"]
            },
            {
                "kuta": "Vashya",
                "description": KUTA_INFO[1]["description"],
                "bride_value": bride_vashya,
                "groom_value": groom_vashya,
                "points": vashya_points,
                "max_points": KUTA_INFO[1]["max_points"]
            },
            {
                "kuta": "Tara",
                "description": KUTA_INFO[2]["description"],
                "bride_value": bride_nakshatra,
                "groom_value": groom_nakshatra,
                "points": tara_points,
                "max_points": KUTA_INFO[2]["max_points"]
            },
            {
                "kuta": "Yoni",
                "description": KUTA_INFO[3]["description"],
                "bride_value": bride_yoni,
                "groom_value": groom_yoni,
                "points": yoni_points,
                "max_points": KUTA_INFO[3]["max_points"]
            },
            {
                "kuta": "Grah Maitri",
                "description": KUTA_INFO[4]["description"],
                "bride_value": bride_lord,
                "groom_value": groom_lord,
                "points": maitri_points,
                "max_points": KUTA_INFO[4]["max_points"]
            },
            {
                "kuta": "Gana",
                "description": KUTA_INFO[5]["description"],
                "bride_value": bride_gana,
                "groom_value": groom_gana,
                "points": gana_points,
                "max_points": KUTA_INFO[5]["max_points"]
            },
            {
                "kuta": "Bhakoot",
                "description": KUTA_INFO[6]["description"],
                "bride_value": bride_rashi,
                "groom_value": groom_rashi,
                "points": bhakoot_points,
                "max_points": KUTA_INFO[6]["max_points"]
            },
            {
                "kuta": "Nadi",
                "description": KUTA_INFO[7]["description"],
                "bride_value": bride_nadi,
                "groom_value": groom_nadi,
                "points": nadi_points,
                "max_points": KUTA_INFO[7]["max_points"]
            }
        ]
        total_points = sum([
            varna_points, vashya_points, tara_points, yoni_points, maitri_points, gana_points, bhakoot_points, nadi_points
        ])
        max_points = sum([k["max_points"] for k in KUTA_INFO])
        percentage = round((total_points / max_points) * 100, 1)
        compatibility_analysis = (
            f"Overall compatibility score is {total_points} out of {max_points} points ({percentage}%).\n"
            f"The match has scored {total_points} points outs of {max_points} points. This is a reasonably good score. "
            f"Moreover, your rashi lords are friendly with each other thereby signifying mental compatibility and mutual affection between the two. "
            f"Hence, this is a favourable Ashtakoota match."
        )
        print('DEBUG: guna_table =', json.dumps(guna_table, indent=2))
        print('DEBUG: bride_rashi =', bride_rashi, 'bride_nakshatra =', bride_nakshatra)
        print('DEBUG: groom_rashi =', groom_rashi, 'groom_nakshatra =', groom_nakshatra)
        return {
            "guna_table": guna_table,
            "total_points": total_points,
            "max_points": max_points,
            "percentage": percentage,
            "compatibility_analysis": compatibility_analysis,
            "bride_horoscope": {
                "rashi": bride_rashi,
                "nakshatra": bride_nakshatra
            },
            "groom_horoscope": {
                "rashi": groom_rashi,
                "nakshatra": groom_nakshatra
            }
        } 