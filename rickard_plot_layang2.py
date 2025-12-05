import math
import matplotlib.pyplot as plt

# =====================================================================
# 22 NAMA SESAR RICKARD 1972
# =====================================================================
FAULT_NAMES = {
    1:"Thrust Slip Fault", 2:"Reverse Slip Fault", 3:"Right Thrust Slip Fault",
    4:"Thrust Right Slip Fault", 5:"Reverse Right Slip Fault",
    6:"Right Reverse Slip Fault", 7:"Right Slip Fault",
    8:"Lag Right Slip Fault", 9:"Right Lag Slip Fault",
    10:"Right Normal Slip Fault", 11:"Normal Right Slip Fault",
    12:"Lag Slip Fault", 13:"Normal Slip Fault",
    14:"Left Lag Slip Fault", 15:"Lag Left Slip Fault",
    16:"Normal Left Slip Fault", 17:"Left Normal Slip Fault",
    18:"Left Slip Fault", 19:"Thrust Left Slip Fault",
    20:"Left Thrust Slip Fault", 21:"Left Reverse Slip Fault",
    22:"Reverse Left Slip Fault"
}


# =====================================================================
# PROYEKSI DIP + PITCH → KOORDINAT RICKARD
# =====================================================================
def rickard_projection(dip, pitch):
    """
    Rumus Rickard:
    X = (pitch/90) * cos(dip)
    Y = (pitch/90) * sin(dip)
    
    Lalu diproyeksikan ke diagram layang-layang Rickard:
        X' = X
        Y' = Y * 1.7    (faktor distorsi vertikal khas diagram Rickard)
    """
    dip_rad = math.radians(dip)
    r = pitch / 90.0
    
    x = r * math.cos(dip_rad)
    y = r * math.sin(dip_rad)

    # Faktor distorsi Rickard (vertical exaggeration)
    y_rickard = y * 1.7

    return x, y_rickard


# =====================================================================
# MENENTUKAN SEKTOR 1–22
# =====================================================================
def get_sector(x, y):
    angle = math.atan2(y, x)
    if angle < 0:
        angle += 2 * math.pi
    sector = int(angle / (2 * math.pi / 22)) + 1
    return 22 if sector > 22 else sector


# =====================================================================
# PLOT DIAGRAM RICKARD (LAYANG-LAYANG)
# =====================================================================
def plot_rickard(x, y, label):

    # Titik sudut diagram Rickard (bentuk layang-layang)
    kite_x = [0, 1, 0, -1, 0]
    kite_y = [1.7, 0, -1.7, 0, 1.7]

    plt.figure(figsize=(7, 9))

    # gambar layang-layang
    plt.plot(kite_x, kite_y, color="black", linewidth=2)

    # garis sumbu tengah
    plt.axhline(0, color="gray", linewidth=0.6)
    plt.axvline(0, color="gray", linewidth=0.6)

    # titik hasil klasifikasi
    plt.scatter(x, y, color="red", s=80)
    plt.text(x + 0.03, y + 0.03, label, fontsize=10)

    plt.title("Rickard Fault Classification Diagram (1972)", fontsize=14)
    plt.xlim(-1.1, 1.1)
    plt.ylim(-2, 2)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True, linestyle="--", alpha=0.25)
    plt.show()


# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    print("=== RICKARD FAULT CLASSIFICATION (1972) ===")
    dip = float(input("Masukkan DIP (0–90): "))
    pitch = float(input("Masukkan PITCH/RAKE (0–90): "))

    x, y = rickard_projection(dip, pitch)
    sector = get_sector(x, y)
    fault = FAULT_NAMES[sector]

    print("\nHASIL:")
    print(f"Sektor      : {sector}")
    print(f"Nama Sesar  : {fault}")
    print(f"Plot XY     : ({round(x,3)}, {round(y,3)})")

    plot_rickard(x, y, fault)
