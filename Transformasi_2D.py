import math


# DATA INPUT: TITIK AWAL SEGITIGA (KOORDINAT HOMOGEN 3x1)
P1 = [0, 0, 1]
P2 = [100, 0, 1]
P3 = [50, 100, 1]



# FUNGSI BUATAN SENDIRI: MATRIKS TRANSFORMASI
def buat_matriks_translasi(tx, ty):
    """Menghasilkan matriks homogen 3x3 untuk pergeseran (translasi)"""
    return [[1, 0, tx], [0, 1, ty], [0, 0, 1]]



# FUNGSI BUATAN SENDIRI: PERKALIAN MATRIKS MANUAL
def transformasi_titik(matriks, titik):
    """Mengalikan matriks 3x3 dengan vektor titik 3x1 menggunakan perulangan (DILARANG PAKAI LIBRARY INSTAN)"""
    titik_baru = [0, 0, 0]

    # Perulangan baris x kolom (Logika Aljabar Linear)
    for baris in range(3):
        total = 0
        for kolom in range(3):
            total += matriks[baris][kolom] * titik[kolom]
        titik_baru[baris] = total

    return titik_baru



# PENGUJIAN DAN VALIDASI DENGAN HITUNGAN KERTAS
# Kita coba geser ke kanan 20 (tx=20) dan ke atas 30 (ty=30)
matriks_T = buat_matriks_translasi(20, 30)

print("--- HASIL PENGUJIAN PROGRAM ---")
print("P1 Baru:", transformasi_titik(matriks_T, P1))
print("P2 Baru:", transformasi_titik(matriks_T, P2))
print("P3 Baru:", transformasi_titik(matriks_T, P3))


# FUNGSI-FUNGSI MATRIKS TRANSFORMASI HOMOGEN 3x3 (TEMA A)
def buat_matriks_skala(sx, sy):
    """Matriks homogen 3x3 untuk skala (perbesaran/perkecilan)"""
    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]

def buat_matriks_shear(sh_x, sh_y):
    """Matriks homogen 3x3 untuk shear (condong)"""
    return [
        [1, sh_x, 0],
        [sh_y, 1, 0],
        [0, 0, 1]
    ]

def buat_matriks_refleksi_x():
    """Matriks homogen 3x3 untuk pencerminan terhadap sumbu X"""
    return [
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ]

def buat_matriks_refleksi_y():
    """Matriks homogen 3x3 untuk pencerminan terhadap sumbu Y"""
    return [
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

def buat_matriks_rotasi(sudut_derajat):
    """Matriks homogen 3x3 untuk rotasi (berlawanan arah jarum jam)"""
    # Ubah sudut dari derajat ke radian karena fungsi math.cos dan math.sin butuh radian
    rad = math.radians(sudut_derajat)
    cos_theta = math.cos(rad)
    sin_theta = math.sin(rad)
    
    return [
        [cos_theta, -sin_theta, 0],
        [sin_theta, cos_theta, 0],
        [0, 0, 1]
    ]


# FUNGSI PERKALIAN MATRIKS 3x3 DENGAN MATRIKS 3x3
# (Penting untuk menggabungkan beberapa transformasi / Rotasi titik acuan)
def kalikan_matriks_3x3(matA, matB):
    """Mengalikan matriks 3x3 dengan matriks 3x3 secara manual tanpa library"""
    hasil = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for baris in range(3):
        for kolom in range(3):
            total = 0
            for k in range(3):
                total += matA[baris][k] * matB[k][kolom]
            hasil[baris][kolom] = total
    return hasil

# Tes perbesar segitiga menjadi 2 kali lipat (sx = 2, sy = 2)
matriks_S = buat_matriks_skala(2, 2)

print("\n--- HASIL PENGUJIAN SKALA (PERBESARAN 2x) ---")
print("P1 Baru:", transformasi_titik(matriks_S, P1))
print("P2 Baru:", transformasi_titik(matriks_S, P2))
print("P3 Baru:", transformasi_titik(matriks_S, P3))