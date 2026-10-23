# MetroRoute AI

**Perencana Rute Transportasi Umum Kota dengan Search dan Sistem Pakar**
Tugas Kecerdasan Buatan: Search Algorithm dan Expert System (rule-based)

**Kelas / nama repository:** `AI-EL10-09`

| Peran | Nama | Branch |
|-------|------|--------|
| Manager / Ketua | Ahmad Nabiil Alfarizi | `main` |
| Dev 1 | Adel Muhammad Suhardin Sirali | `dev-1` |

## 1. Deskripsi

MetroRoute AI membantu menentukan rute tercepat antar stasiun pada jaringan transportasi umum kota contoh (4 jalur, 11 stasiun). Pengguna dapat menandai stasiun yang ditutup, jalur yang gangguan, dan kondisi jam sibuk. Sistem lalu mencari rute, menghitung waktu tempuh termasuk waktu pindah jalur, dan memberi status serta saran perjalanan.

## 2. Tujuan

- Menerapkan algoritma pencarian pada masalah nyata.
- Membandingkan algoritma uninformed (BFS, UCS) dan informed (A*).
- Menerapkan sistem pakar berbasis aturan untuk menafsirkan hasil pencarian.

## 3. Teknologi

- **Python 3.9+**
- **Tkinter**: antarmuka grafis dengan peta jaringan
- **BFS, UCS, A\***: pencarian rute
- **Sistem pakar berbasis aturan**: 9 aturan JIKA-MAKA (R1-R9)

## 4. Cara Kerja Sistem

1. Pengguna memilih stasiun asal, tujuan, algoritma, stasiun ditutup, jalur gangguan, dan jam sibuk.
2. Jaringan dibaca dari `data/jaringan.json`. **Keadaan pencarian** adalah pasangan (stasiun, jalur yang sedang dinaiki), karena pindah jalur memakan waktu.
3. Biaya: antar stasiun = 2 menit/km + 1 menit berhenti; pindah jalur = 5 menit.
4. Algoritma mencari rute, tanpa melewati stasiun tertutup dan tanpa memakai jalur gangguan.
5. Hasil pencarian menjadi **fakta** (ada rute atau tidak, waktu, jumlah pindah jalur, selisih waktu dibanding kondisi normal).
6. Aturan menghasilkan status **LANCAR / PERHATIAN / TERGANGGU** dan saran.
7. Rute digambar di peta dan dijelaskan per jalur.

| Algoritma | Jenis | Menghasilkan | Optimal untuk waktu? |
|-----------|-------|--------------|----------------------|
| BFS | Uninformed | Langkah paling sedikit (stasiun dan pindah jalur dihitung sama) | Tidak selalu |
| UCS | Uninformed | Waktu tempuh tercepat | Ya |
| A* | Informed | Sama dengan UCS, dipandu heuristik | Ya |

Heuristik A*: jarak garis lurus ke tujuan x 2 menit/km. Nilainya tidak pernah melebihi waktu sebenarnya, sehingga A* tetap optimal.

## 5. Peran Kecerdasan Buatan

- **Search:** BFS, UCS, A* menjadi inti pencarian rute.
- **Expert system:** aturan di `expert_system/rules.py` menafsirkan hasil pencarian.

Sistem ini berbasis algoritma dan aturan, **bukan** machine learning.

## 6. Batasan Sistem

- Jaringan adalah model contoh, bukan data transportasi sungguhan.
- Gangguan dimasukkan manual oleh pengguna; tidak ada data waktu nyata.
- Jadwal kedatangan dan waktu tunggu kereta tidak dimodelkan.
- Kapasitas dan tarif tidak dihitung.
- Jam sibuk hanya memberi perkiraan tambahan waktu sekitar 30%.

## 7. Library / Kebutuhan

- Python 3.9 atau lebih baru
- Tkinter (bawaan Python di Windows/macOS; Linux: `sudo apt install python3-tk`)
- `pytest` hanya untuk tes: `pip install -r requirements.txt`

## 8. Cara Pakai

1. Jalankan aplikasi (bagian 9).
2. Pilih **Asal**, **Tujuan**, dan **Algoritma**.
3. (Opsional) Pilih stasiun ditutup (tahan Ctrl untuk lebih dari satu), centang jalur gangguan, atau centang jam sibuk.
4. Klik **Cari Rute**. Status, rute, waktu, dan saran muncul, dan rute ditandai di peta.
5. Klik **Reset** untuk mengosongkan pilihan gangguan.

Skenario yang menarik:
- **Pasar Barat ke Bandara, normal:** LANCAR, 27 menit, langsung tanpa pindah jalur.
- **Pasar Barat ke Bandara, Stasiun Pusat tutup:** PERHATIAN, memutar dengan dua kali pindah jalur (55,4 menit).
- **Bandara ke Taman Kota, Jalur Biru gangguan:** TERGANGGU, tidak ada rute.

## 9. Cara Menjalankan

```bash
pip install -r requirements.txt

python main.py                                   # GUI
python main.py --list                            # daftar id stasiun dan jalur
python main.py --cli --from pasar_barat --to bandara --closed-stations pusat --rush --algo "A*"
python -m pytest                                 # jalankan tes
```

## 10. Struktur Folder

```
MetroRoute-AI/
├── search_algorithm/     # model jaringan dan algoritma pencarian
│   ├── graph.py
│   └── algorithms.py
├── expert_system/        # sistem pakar berbasis aturan
│   ├── rules.py
│   └── engine.py
├── app/gui.py            # antarmuka Tkinter
├── data/jaringan.json    # data stasiun dan jalur
├── tests/                # tes otomatis
├── docs/                 # ANALISIS, GIT_GUIDE, TUTORIAL_ANGGOTA, TUGAS_MANAGER
├── main.py               # titik masuk program
├── README.md
└── requirements.txt
```

Tiap folder kode memiliki `README.md` sendiri.

## 11. Kelompok dan Kontribusi

Kelompok terdiri dari 2 orang. Dev 1 bekerja di branch `dev-1` lalu menggabungkannya ke `main` lewat pull request (lihat `docs/GIT_GUIDE.md`).

- **Manager / Ketua:** model jaringan, alur sistem, repository, sistem pakar (aturan baru R10 dan tesnya), review dan merge, README.
- **Dev 1:** algoritma search, skenario analisis baru di `docs/ANALISIS.md`, dan tesnya.

_Sesuaikan bagian ini dengan riwayat commit yang sebenarnya._

## 12. Transparansi

Proyek ini dikembangkan dengan bantuan asisten AI, lalu dipelajari, diuji, dan disesuaikan oleh penulis.

_AI Course Project: Search Algorithm and Expert System._
