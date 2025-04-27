import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.patches as patches

def plot_planetary_positions(planetary_positions, filename="horoscope_chart.png"):
    fig, ax = plt.subplots(figsize=(6,6), subplot_kw={'projection': 'polar'})
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi/2.0)
    ax.set_yticklabels([])
    ax.set_xticks(np.linspace(0, 2*np.pi, 12, endpoint=False))
    ax.set_xticklabels([
        "Mesha", "Vrishabha", "Mithuna", "Kataka", "Simha", "Kanya",
        "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"
    ])

    for planet, pos in planetary_positions.items():
        theta = np.deg2rad((360 - pos["longitude"] + 90) % 360)
        ax.plot([theta], [1], 'o', label=planet)
        ax.text(theta, 1.1, planet, ha='center', va='center', fontsize=10)

    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.title("Planetary Positions (Sidereal)")
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    return filename

def plot_south_indian_chart(planetary_positions, filename="south_indian_chart.png", birth_details=None):
    import matplotlib.patches as patches
    rasi_names = [
        "Mesha", "Vrishabha", "Mithuna", "Kataka", "Simha", "Kanya",
        "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"
    ]
    # Classic South Indian 4x4 grid mapping (counterclockwise, starting from bottom left)
    rasi_box_map = [
        (3,0), # 1 Mesha (bottom left)
        (2,0), # 2 Vrishabha (left, 2nd from bottom)
        (1,0), # 3 Mithuna (left, 2nd from top)
        (0,0), # 4 Kataka (top left)
        (0,1), # 5 Simha (top, 2nd from left)
        (0,2), # 6 Kanya (top, 2nd from right)
        (0,3), # 7 Tula (top right)
        (1,3), # 8 Vrischika (right, 2nd from top)
        (2,3), # 9 Dhanu (right, 2nd from bottom)
        (3,3), #10 Makara (bottom right)
        (3,2), #11 Kumbha (bottom, 2nd from right)
        (3,1), #12 Meena (bottom, 2nd from left)
    ]
    asc_rasi = None
    if "Ascendant" in planetary_positions and "rasi" in planetary_positions["Ascendant"]:
        asc_rasi = planetary_positions["Ascendant"]["rasi"]
    else:
        asc_long = planetary_positions["Ascendant"].get("longitude", 0)
        asc_rasi = rasi_names[int(asc_long // 30) % 12]
    asc_index = rasi_names.index(asc_rasi)
    rotated_rasi_names = rasi_names[asc_index:] + rasi_names[:asc_index]
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.axis('off')
    # Draw grid
    for i in range(5):
        ax.plot([i, i], [0, 4], color='black', lw=2)
        ax.plot([0, 4], [i, i], color='black', lw=2)
    # Draw center 2x2 box with dark red border
    ax.add_patch(patches.Rectangle((1, 1), 2, 2, fill=False, edgecolor='#800000', lw=3))
    # Place rasi names and numbers (rotated)
    for idx, (row, col) in enumerate(rasi_box_map):
        ax.text(col + 0.05, 3.95 - row, f"{(idx+asc_index)%12+1}\n{rotated_rasi_names[idx]}", ha='left', va='top', fontsize=11, color='#8B0000')
    # Place planets and Ascendant in boxes (rotated)
    planet_symbols = {
        "Sun": "☉", "Moon": "☽", "Mars": "♂", "Mercury": "☿", "Jupiter": "♃", "Venus": "♀", "Saturn": "♄", "Rahu": "☊", "Ketu": "☋", "Ascendant": "Asc"
    }
    box_planets = {i: [] for i in range(12)}
    for planet, pos in planetary_positions.items():
        rasi_idx = None
        if "rasi" in pos and pos["rasi"] in rasi_names:
            orig_idx = rasi_names.index(pos["rasi"])
            rasi_idx = (orig_idx - asc_index) % 12
        else:
            rasi_idx = (int(pos.get("longitude", 0) // 30) - asc_index) % 12
        symbol = planet_symbols.get(planet, planet)
        box_planets[rasi_idx].append(symbol)
    for idx, (row, col) in enumerate(rasi_box_map):
        planets_here = " ".join(box_planets[idx])
        ax.text(col + 0.5, 3.5 - row, planets_here, ha='center', va='center', fontsize=18)
    # Add birth details in the center 2x2 area if provided
    if birth_details:
        center_text = "\n".join(birth_details)
        ax.text(2, 2, center_text, ha='center', va='center', fontsize=13, color='#800000')
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    return filename 