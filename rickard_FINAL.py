# file: rickard_diamond_streamlit.py
import math
import io
import streamlit as st
import matplotlib.pyplot as plt

# -------------------------
# Nama sesar (1..22)
# -------------------------
FAULT_NAMES = [
    "Thrust Slip Fault",
    "Reverse Slip Fault",
    "Right Thrust Slip Fault",
    "Thrust Right Slip Fault",
    "Reverse Right Slip Fault",
    "Right Reverse Slip Fault",
    "Right Slip Fault",
    "Lag Right Slip Fault",
    "Right Lag Slip Fault",
    "Right Normal Slip Fault",
    "Normal Right Slip Fault",
    "Lag Slip Fault",
    "Normal Slip Fault",
    "Left Lag Slip Fault",
    "Lag Left Slip Fault",
    "Normal Left Slip Fault",
    "Left Normal Slip Fault",
    "Left Slip Fault",
    "Thrust Left Slip Fault",
    "Left Thrust Slip Fault",
    "Left Reverse Slip Fault",
    "Reverse Left Slip Fault"
]

# -------------------------
# Mapping dip/pitch -> diamond coordinates
# -------------------------
def dip_pitch_to_diamond_xy(dip_deg, pitch, convention="rickard"):
    """
    dip_deg : numeric (degree)
    pitch   : 0..90
    convention:
        - "polar": uses theta = radians(dip_deg)
        - "rickard": uses theta = radians(90 - dip_deg)  (often matches Rickard diagram)
    returns (x, y) on diamond where |x|+|y| <= 1
    """
    # choose theta per convention
    if convention == "polar":
        theta = math.radians(dip_deg)
    else:
        theta = math.radians(90.0 - dip_deg)

    r = max(0.0, min(1.0, pitch / 90.0))

    c = math.cos(theta)
    s = math.sin(theta)
    denom = abs(c) + abs(s)
    t = 0.0 if denom == 0 else 1.0 / denom

    x = r * t * c
    y = r * t * s
    return x, y

# -------------------------
# Sector detection (1..22)
# -------------------------
def xy_to_sector(x, y, n=22):
    ang = math.atan2(y, x)
    if ang < 0:
        ang += 2 * math.pi
    idx = int(ang / (2 * math.pi / n))
    sector = idx + 1
    if sector > n:
        sector = n
    return sector

# -------------------------
# Plot diamond, sectorlines, sector numbers, point and label
# -------------------------
def plot_rickard_diamond(x, y, label=None, show_numbers=True, show_sector_lines=True):
    fig, ax = plt.subplots(figsize=(7,7))

    # diamond boundary
    diamond_x = [0, 1, 0, -1, 0]
    diamond_y = [1, 0, -1, 0, 1]
    ax.plot(diamond_x, diamond_y, color="black", linewidth=1.6)

    # sector lines and optional numbering
    for i in range(22):
        theta = (i / 22) * 2 * math.pi
        c = math.cos(theta); s = math.sin(theta)
        denom = abs(c) + abs(s)
        t = 0 if denom == 0 else 1.0 / denom
        xe, ye = t * c, t * s
        if show_sector_lines:
            ax.plot([0, xe], [0, ye], color="gray", linewidth=0.8)
        if show_numbers:
            # place number a bit inside edge (at 0.9*t)
            nx, ny = 0.9 * t * c, 0.9 * t * s
            sector_num = i + 1
            ax.text(nx, ny, str(sector_num), fontsize=9, ha='center', va='center',
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=0.5))

    # point
    ax.scatter([x], [y], color="red", s=120, zorder=5)
    if label:
        # offset label slightly along radial direction
        theta_p = math.atan2(y, x) if not (x==0 and y==0) else 0.0
        dx = 0.06 * math.cos(theta_p)
        dy = 0.06 * math.sin(theta_p)
        ax.text(x + dx, y + dy, label, fontsize=10, weight='bold',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=1), zorder=6)

    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("X (diamond)")
    ax.set_ylabel("Y (diamond)")
    ax.set_title("🔎 Rickard Fault Classification (1972)")

    # remove default grid (we'll rely on sector lines)
    ax.grid(False)
    return fig

# -------------------------
# STREAMLIT UI
# -------------------------
st.title("🔎 Rickard Fault Classification (1972)")

st.markdown("""
Masukkan **Dip** dan **Pitch/Rake**, lalu pilih **Conventional** atau **Rickard** convention.  
Jika titik masih belum cocok dengan gambar referensimu, ubah *convention* ke opsi lainnya. ✅
""")

col1, col2 = st.columns(2)
with col1:
    dip = st.number_input("Dip (°)", value=30.0, min_value=-180.0, max_value=180.0, step=1.0)
    pitch = st.number_input("Pitch / Rake (0–90°)", value=60.0, min_value=0.0, max_value=90.0, step=1.0)
with col2:
    convention = st.radio("Sudut convention:", ("rickard", "polar"))
    show_numbers = st.checkbox("Tampilkan nomor sektor", value=True)
    show_sector_lines = st.checkbox("Tampilkan garis sektor", value=True)

if st.button("Plot & Klasifikasikan ✅"):
    x, y = dip_pitch_to_diamond_xy(dip, pitch, convention=convention)
    sector = xy_to_sector(x, y, n=22)
    fault_name = FAULT_NAMES[sector-1] if 1 <= sector <= 22 else "Unknown"

    label = f"{fault_name} (S{sector})"
    st.subheader("Hasil")
    st.write(f"**Sector:** {sector}")
    st.write(f"**Fault name:** {fault_name}")
    st.write(f"**Diamond coords:** ({x:.4f}, {y:.4f})  — Convention: **{convention}**")

    fig = plot_rickard_diamond(x, y, label=label, show_numbers=show_numbers, show_sector_lines=show_sector_lines)
    st.pyplot(fig)

    # Download
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches='tight')
    buf.seek(0)
    st.download_button("⬇️ Download PNG", data=buf.getvalue(), file_name="rickard_diamond.png", mime="image/png")
