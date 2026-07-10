import ctypes
import math
import os
import tkinter as tk

try:
    # Kita tambahkan '.versi2' di belakangnya untuk menipu dan mereset ingatan Taskbar Windows 11
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "arif.aljabar.transformasi.2d.versi2"
    )
except Exception:
    pass

# LOGIKA ALJABAR LINEAR MANUAL (TANPA LIBRARY INSTAN)

P1 = [0, 0, 1]
P2 = [100, 0, 1]
P3 = [50, 100, 1]


def buat_matriks_translasi(tx, ty):
    return [[1, 0, tx], [0, 1, ty], [0, 0, 1]]


def buat_matriks_skala(sx, sy):
    return [[sx, 0, 0], [0, sy, 0], [0, 0, 1]]


def buat_matriks_rotasi(sudut_derajat):
    rad = math.radians(sudut_derajat)
    cos_theta = math.cos(rad)
    sin_theta = math.sin(rad)
    return [[cos_theta, -sin_theta, 0], [sin_theta, cos_theta, 0], [0, 0, 1]]


def buat_matriks_shear(sh_x, sh_y):
    return [[1, sh_x, 0], [sh_y, 1, 0], [0, 0, 1]]


def buat_matriks_refleksi(ref_x, ref_y):
    # Jika ref_x True, cermin terhadap sumbu X (nilai Y menjadi negatif)
    # Jika ref_y True, cermin terhadap sumbu Y (nilai X menjadi negatif)
    sx = -1 if ref_y else 1
    sy = -1 if ref_x else 1
    return [[sx, 0, 0], [0, sy, 0], [0, 0, 1]]


# --- FUNGSI PERKALIAN MATRIKS 3x3 DENGAN MATRIKS 3x3 ---
def kalikan_matriks_3x3(matA, matB):
    """Menggabungkan 2 matriks transformasi menjadi 1 matriks (M_total = M1 * M2)"""
    hasil = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for baris in range(3):
        for kolom in range(3):
            total = 0
            for k in range(3):
                total += matA[baris][k] * matB[k][kolom]
            hasil[baris][kolom] = total
    return hasil


# --- FUNGSI PERKALIAN MATRIKS 3x3 DENGAN VEKTOR TITIK 3x1 ---
def transformasi_titik(matriks, titik):
    titik_baru = [0, 0, 0]
    for baris in range(3):
        total = 0
        for kolom in range(3):
            total += matriks[baris][kolom] * titik[kolom]
        titik_baru[baris] = total
    return titik_baru



# ANTARMUKA GRAFIS (GUI TKINTER) - VERSI LENGKAP TEMA A
class AplikasiTransformasi2D:

    def __init__(self, root):
        self.root = root
        self.root.title("Proyek Aljabar Linear - Transformasi 2D Lengkap")
        self.root.geometry("950x650")

        try:
            folder_sekarang = os.path.dirname(os.path.abspath(__file__))
            alamat_logo = os.path.join(folder_sekarang, "logo.ico")

            self.root.iconbitmap(alamat_logo)
        except Exception:
            pass

        # Offset pusat koordinat di layar canvas
        self.offset_x = 300
        self.offset_y = 300
        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        # Panel Kontrol
        panel = tk.Frame(root, width=320)
        panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=5)

        tk.Label(
            panel,
            text="KONTROL TRANSFORMASI",
            font=("Arial", 12, "bold"),
            pady=5,
        ).pack()

        # 1. Translasi
        tk.Label(
            panel,
            text="--- Translasi (Geser) ---",
            font=("Arial", 9, "bold"),
            fg="blue",
        ).pack()
        self.slider_tx = tk.Scale(
            panel,
            from_=-200,
            to=200,
            orient=tk.HORIZONTAL,
            label="Geser X",
            command=self.update_grafik,
        )
        self.slider_tx.pack(fill=tk.X)
        self.slider_ty = tk.Scale(
            panel,
            from_=-200,
            to=200,
            orient=tk.HORIZONTAL,
            label="Geser Y",
            command=self.update_grafik,
        )
        self.slider_ty.pack(fill=tk.X)

        # 2. Skala
        tk.Label(
            panel,
            text="--- Skala (Perbesaran) ---",
            font=("Arial", 9, "bold"),
            fg="blue",
        ).pack()
        self.slider_skala = tk.Scale(
            panel,
            from_=0.1,
            to=3.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            label="Skala",
            command=self.update_grafik,
        )
        self.slider_skala.set(1.0)
        self.slider_skala.pack(fill=tk.X)

        # 3. Rotasi (SEKARANG SUDAH AKTIF!)
        tk.Label(
            panel, text="--- Rotasi (Putar) ---", font=("Arial", 9, "bold"), fg="blue"
        ).pack()
        self.slider_rotasi = tk.Scale(
            panel,
            from_=0,
            to=360,
            orient=tk.HORIZONTAL,
            label="Sudut (Derajat)",
            command=self.update_grafik,
        )
        self.slider_rotasi.pack(fill=tk.X)

        # 4. Shear (Condong)
        tk.Label(
            panel, text="--- Shear (Condong) ---", font=("Arial", 9, "bold"), fg="blue"
        ).pack()
        self.slider_shear_x = tk.Scale(
            panel,
            from_=-1.5,
            to=1.5,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            label="Shear X",
            command=self.update_grafik,
        )
        self.slider_shear_x.pack(fill=tk.X)

        # 5. Refleksi (Pencerminan)
        tk.Label(
            panel,
            text="--- Refleksi (Cermin) ---",
            font=("Arial", 9, "bold"),
            fg="blue",
        ).pack()
        frame_ref = tk.Frame(panel)
        frame_ref.pack(pady=5)
        self.cek_ref_x = tk.BooleanVar()
        self.cek_ref_y = tk.BooleanVar()
        tk.Checkbutton(
            frame_ref,
            text="Cermin Sumbu X",
            variable=self.cek_ref_x,
            command=self.update_grafik,
        ).pack(side=tk.LEFT)
        tk.Checkbutton(
            frame_ref,
            text="Cermin Sumbu Y",
            variable=self.cek_ref_y,
            command=self.update_grafik,
        ).pack(side=tk.LEFT)

        # Tombol Reset
        tk.Button(
            panel,
            text="RESET SEMUA POSISI",
            command=self.reset_slider,
            bg="#ff4d4d",
            fg="white",
            font=("Arial", 10, "bold"),
            pady=5,
        ).pack(pady=15, fill=tk.X)

        self.update_grafik()

    def reset_slider(self):
        self.slider_tx.set(0)
        self.slider_ty.set(0)
        self.slider_skala.set(1.0)
        self.slider_rotasi.set(0)
        self.slider_shear_x.set(0.0)
        self.cek_ref_x.set(False)
        self.cek_ref_y.set(False)

    def gambar_segitiga(self, p1, p2, p3, warna, garis_putus=False):
        x1, y1 = p1[0] + self.offset_x, p1[1] + self.offset_y
        x2, y2 = p2[0] + self.offset_x, p2[1] + self.offset_y
        x3, y3 = p3[0] + self.offset_x, p3[1] + self.offset_y

        if garis_putus:
            self.canvas.create_polygon(
                x1,
                y1,
                x2,
                y2,
                x3,
                y3,
                outline=warna,
                fill="",
                dash=(4, 4),
                width=2,
            )
        else:
            self.canvas.create_polygon(
                x1, y1, x2, y2, x3, y3, outline="black", fill=warna, width=2
            )

    def update_grafik(self, *args):
        self.canvas.delete("all")

        # 1. Gambar Sumbu Koordinat Utama (Garis Salib)
        self.canvas.create_line(
            0, self.offset_y, 600, self.offset_y, fill="#888888", width=2
        )  # Sumbu X
        self.canvas.create_line(
            self.offset_x, 0, self.offset_x, 600, fill="#888888", width=2
        )  # Sumbu Y

        # 2. Tambahkan Label Huruf "X" dan "Y"
        self.canvas.create_text(
            580,
            self.offset_y - 15,
            text="X",
            font=("Arial", 12, "bold"),
            fill="blue",
        )
        self.canvas.create_text(
            self.offset_x + 15,
            20,
            text="Y",
            font=("Arial", 12, "bold"),
            fill="blue",
        )
        self.canvas.create_text(
            self.offset_x - 10,
            self.offset_y + 12,
            text="0",
            font=("Arial", 9, "bold"),
            fill="#555555",
        )

        # 3. Tambahkan Angka dan Garis Skala (Ticks) setiap kelipatan 50 dan 100
        for i in range(-250, 251, 50):
            if i == 0:
                continue

            # --- Skala pada Sumbu X (Horizontal) ---
            pos_x = self.offset_x + i
            # Garis kecil penanda skala X
            self.canvas.create_line(
                pos_x,
                self.offset_y - 4,
                pos_x,
                self.offset_y + 4,
                fill="#888888",
            )
            # Tampilkan angka jika kelipatan 100 agar tidak terlalu padat/berdesakan
            if i % 100 == 0:
                self.canvas.create_text(
                    pos_x,
                    self.offset_y + 15,
                    text=str(i),
                    font=("Arial", 8),
                    fill="#555555",
                )
                # Garis kisi tipis (grid latar belakang)
                self.canvas.create_line(
                    pos_x, 0, pos_x, 600, fill="#eeeeee", dash=(2, 2)
                )

            # --- Skala pada Sumbu Y (Vertikal) ---
            # Catatan: Pada GUI Canvas, Y negatif ke atas dan Y positif ke bawah.
            # Agar sesuai matematika aljabar linear standar (atas positif, bawah negatif), kita balik label angkanya:
            pos_y = self.offset_y - i
            # Garis kecil penanda skala Y
            self.canvas.create_line(
                self.offset_x - 4,
                pos_y,
                self.offset_x + 4,
                pos_y,
                fill="#888888",
            )
            if i % 100 == 0:
                self.canvas.create_text(
                    self.offset_x - 20,
                    pos_y,
                    text=str(i),
                    font=("Arial", 8),
                    fill="#555555",
                )
                # Garis kisi tipis (grid latar belakang)
                self.canvas.create_line(
                    0, pos_y, 600, pos_y, fill="#eeeeee", dash=(2, 2)
                )

        # 4. Gambar Segitiga Asal (Abu-abu putus-putus)
        self.gambar_segitiga(P1, P2, P3, "gray", garis_putus=True)

        # 5. Ambil semua nilai dari slider GUI
        tx = self.slider_tx.get()
        ty = self.slider_ty.get()
        skala = self.slider_skala.get()
        rotasi = self.slider_rotasi.get()
        shear_x = self.slider_shear_x.get()
        ref_x = self.cek_ref_x.get()
        ref_y = self.cek_ref_y.get()

        # 6. Buat masing-masing matriks transformasi
        mat_T = buat_matriks_translasi(tx, ty)
        mat_S = buat_matriks_skala(skala, skala)
        mat_R = buat_matriks_rotasi(rotasi)
        mat_Sh = buat_matriks_shear(shear_x, 0)
        mat_Ref = buat_matriks_refleksi(ref_x, ref_y)

        # 7. GABUNGKAN MATRIKS MENGGUNAKAN PERKALIAN MATRIKS 3x3
        mat_total = kalikan_matriks_3x3(mat_Ref, mat_S)
        mat_total = kalikan_matriks_3x3(mat_Sh, mat_total)
        mat_total = kalikan_matriks_3x3(mat_R, mat_total)
        mat_total = kalikan_matriks_3x3(mat_T, mat_total)

        # 8. Kalikan matriks total ke masing-masing titik koordinat
        p1_baru = transformasi_titik(mat_total, P1)
        p2_baru = transformasi_titik(mat_total, P2)
        p3_baru = transformasi_titik(mat_total, P3)

        # 9. Gambar Segitiga Baru (Biru)
        self.gambar_segitiga(p1_baru, p2_baru, p3_baru, "#3399ff")


if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiTransformasi2D(root)
    root.mainloop()