# Tutorial untuk Dev 1: MetroRoute AI

Setelah menerima undangan collaborator dari ketua, ikuti urutan ini. Bagianmu adalah **search dan analisis**. Ketua mengerjakan bagian sistem pakar.

Urutannya: Bagian A, B, D, E, F.

Perkiraan waktu: 45-60 menit. Semua perintah diketik di **terminal** (jendela hitam).

Ganti `<username-ketua>` dan `<kode-kelas>` dengan yang diberikan ketua.

---

## Gambaran singkat proyek

MetroRoute AI mencari rute tercepat antar stasiun pada jaringan transportasi umum, dengan pindah jalur sebagai tantangan (5 menit tiap pindah).

1. Jaringan jadi **graf**: stasiun = titik, jalur = garis berbobot waktu.
2. **Search** (BFS, UCS, A*) mencari rute. BFS menghitung langkah, UCS menghitung menit, A* = UCS + petunjuk arah.
3. **Sistem pakar** (aturan JIKA-MAKA) menilai hasil menjadi LANCAR / PERHATIAN / TERGANGGU.
4. **GUI** (Tkinter) menggambar peta dan rutenya.

---

## Bagian A: Persiapan

**A1. Terima undangan.** Buka email atau github.com, klik **Accept invitation**.

**A2. Install Python dan Git** (lewati kalau sudah ada). Cek di terminal:

```
python --version
git --version
```

Kalau error: install Python dari **python.org/downloads** (**centang "Add Python to PATH"**) dan Git dari **git-scm.com**. Tutup dan buka lagi terminal setelahnya.

**A3. Beri tahu Git siapa kamu** (pakai email akun GitHub-mu):

```
git config --global user.name "Nama Lengkapmu"
git config --global user.email "emailgithubmu@contoh.com"
```

**A4. Unduh proyek:**

```
git clone https://github.com/<username-ketua>/<kode-kelas>.git
cd <kode-kelas>
```

**A5. Install kebutuhan dan tes:**

```
pip install -r requirements.txt
python -m pytest
```

Hasil yang diharapkan: `28 passed` (atau `30 passed` kalau ketua sudah menambah aturan R10 sebelum kamu clone).

**A6. Coba aplikasinya:** `python main.py`. Pilih Asal **Pasar Barat**, Tujuan **Bandara**, lalu **Cari Rute**. Lalu pilih **Stasiun Pusat** di daftar "Stasiun ditutup" dan cari lagi. Perhatikan rute, status, dan saran yang berubah.

**A7. Buat branch sendiri** (di terminal, dalam folder proyek):

```
git checkout -b dev-1
```

Cek dengan `git branch`; tanda `*` harus ada di branch milikmu.

---

## Bagian B: Tugas Dev 1 (Search)

**B1. Baca kodenya.** Buka `search_algorithm/algorithms.py` (klik kanan > Open with > Notepad). Tangkap perbedaan ini:

- `bfs`: antrean, yang masuk duluan dicek duluan (langkah paling sedikit).
- `ucs`: `heapq`, selalu mengambil yang **waktunya paling kecil**.
- `astar`: `heapq` juga, tapi berdasarkan **waktu tempuh + perkiraan sisa waktu**.

**B2. Jalankan skenario baru:** Kampus Timur ke Pelabuhan Selatan, Stasiun **Stadion** tutup.

```
python main.py --cli --from kampus_timur --to pelabuhan --closed-stations stadion --algo BFS
python main.py --cli --from kampus_timur --to pelabuhan --closed-stations stadion --algo UCS
python main.py --cli --from kampus_timur --to pelabuhan --closed-stations stadion --algo "A*"
```

Catat **Waktu**, **pindah jalur**, dan **diekspansi**. Hasil yang seharusnya:

| Algoritma | Waktu (menit) | Pindah jalur | Diekspansi |
|-----------|---------------|--------------|------------|
| BFS | 25.0 | 1 | 11 |
| UCS | 25.0 | 1 | 13 |
| A* | 25.0 | 1 | 5 |

Kalau angkamu beda, cek ulang perintahnya dulu.

**B3. Tambahkan ke `docs/ANALISIS.md`.** Buka dengan Notepad. Di tabel "Skenario", cari baris yang diawali `| Bandara -> Taman Kota, Jalur Biru gangguan`. Tepat **di atas** baris itu, tambahkan tiga baris:

```
| Kampus Timur -> Pelabuhan Selatan, Stasiun Stadion tutup | BFS | ya | 25.0 | 1 | 11 |
|  | UCS | ya | 25.0 | 1 | 13 |
|  | A* | ya | 25.0 | 1 | 5 |
```

Lalu di bagian "Kesimpulan", tambahkan **satu poin dengan kalimatmu sendiri**, misalnya tentang A* yang hanya mengecek 5 keadaan padahal BFS 11. Simpan.

**B4. Tambahkan tes.** Di Notepad, tempel kode di bawah, lalu **File > Save As**. *Save as type*: **All files**, nama `test_dev1.py`, folder `tests`, encoding **UTF-8**.

```python
import os

import pytest

from search_algorithm import ALGORITHMS, TransitNetwork

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "jaringan.json")


@pytest.fixture(scope="module")
def net():
    return TransitNetwork.from_json(DATA)


@pytest.mark.parametrize("name", list(ALGORITHMS))
def test_stadion_tutup_dihindari(net, name):
    r = ALGORITHMS[name](net, "kampus_timur", "pelabuhan", {"stadion"})
    assert r.found
    assert all(s != "stadion" for s, _ in r.path)


def test_ucs_dan_astar_waktu_sama(net):
    ucs = ALGORITHMS["UCS"](net, "kampus_timur", "pelabuhan", {"stadion"})
    astar = ALGORITHMS["A*"](net, "kampus_timur", "pelabuhan", {"stadion"})
    assert ucs.minutes == astar.minutes == 25.0
```

Jalankan `python -m pytest`. Seharusnya `32 passed` (atau `34 passed` kalau ketua sudah menambah R10 sebelum kamu clone). Lanjut ke **Bagian D**.

---

## Bagian D: Kirim pekerjaanmu ke GitHub

Pastikan terminal ada di folder proyek dan di branch milikmu (`git branch`).

**D1. Commit:**

```
git add .
git commit -m "Tambah skenario analisis dan tes (Dev 1)"
```

**D2. Push:**

```
git push -u origin dev-1
```

**D3. Pull Request:** di halaman repository GitHub, klik **Compare & pull request**, beri judul dan deskripsi singkat, lalu **Create pull request**. Kabari ketua untuk me-merge.

---

## Bagian E: Setelah di-merge

```
git checkout main
git pull
```

Setelah pull requestmu dan pekerjaan ketua (R10) sama-sama masuk, `python -m pytest` seharusnya menampilkan `34 passed`.

---

## Bagian F: Persiapan presentasi

Kalian harus bisa menjelaskan **seluruh proyek**. Pastikan bisa menjawab:

1. **Apa AI-nya?** Algoritma search dan sistem pakar berbasis aturan, bukan machine learning.
2. **Beda BFS dan UCS?** BFS menghitung langkah, UCS menghitung waktu (menit).
3. **Kenapa BFS bisa kalah cepat?** Contoh: Pusat ke Stadion, BFS 25,2 menit, UCS 23,0 menit.
4. **Kenapa A\* optimal?** Heuristiknya (jarak garis lurus x 2 menit/km) tidak pernah melebihi waktu sebenarnya.
5. **Kenapa keadaan pencarian = (stasiun, jalur)?** Supaya waktu pindah jalur bisa dihitung.
6. **Apa itu sistem pakar?** Kumpulan aturan JIKA-MAKA yang menilai hasil search.
7. **Batasan?** Jaringan fiktif, gangguan dimasukkan manual, tidak ada jadwal kedatangan.

---

## Kalau ada masalah

| Masalah | Solusi |
|---------|--------|
| `'python' is not recognized` | Install ulang Python dan centang "Add Python to PATH". |
| `'git' is not recognized` | Tutup dan buka lagi terminal. Kalau masih, install Git ulang. |
| `Repository not found` saat clone | Undangan belum di-accept, atau alamatnya salah. |
| `Author identity unknown` | Ulangi langkah A3. |
| Tes gagal setelah menambah kode | Cek 4 spasi di awal baris dan koma di ujung aturan. |
| File tersimpan sebagai `.txt` | Saat Save As, pilih *All files* dan ketik nama lengkap dengan `.py`. |
| `git push` ditolak | Pastikan kamu di branch sendiri (`git branch`), bukan `main`. |
| "This branch has conflicts" | Lihat bagian 4 di `docs/GIT_GUIDE.md`. |
