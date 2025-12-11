# Rickard-Diagram-App
Aplikasi ini mengimplementasikan diagram klasifikasi sesar menurut model Rickard (1972) menggunakan proyeksi diamond (layang-layang).
Pengguna dapat memasukkan nilai:

- Dip
- Pitch / Rake

Aplikasi kemudian akan:

1. Mengonversi sudut menjadi koordinat pada diagram diamond
2. Menentukan sektor (1–22)
3. Menampilkan nama sesar sesuai sektor

Menggambar diagram lengkap:

1. Diagram Rickard (1972)
2. garis sektor
3. nomor sektor
4. titik lokasi klasifikasi
5. Menyediakan tombol Download PNG untuk menyimpan plot

Proyek ini dibuat dengan Python, Matplotlib, dan Streamlit.

Cara menjalankan: 
1. Install dependensi: pip install streamlit matplotlib numpy
2. Jalankan aplikasi: streamlit run app.py
3. rickard-fault-classification/

├── app.py                 # Aplikasi Streamlit utama
├── rickard_plot.py        # Fungsi perhitungan + plotting diamond
├── README.md              # Dokumentasi
└── assets/
    └── (opsional) gambar-gambar pendukung
