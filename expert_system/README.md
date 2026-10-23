# expert_system

Bagian **sistem pakar** MetroRoute AI: menafsirkan hasil pencarian menjadi status **LANCAR / PERHATIAN / TERGANGGU** dan saran perjalanan.

| File | Fungsi |
|------|--------|
| `rules.py` | Fakta dan aturan R1-R9 |
| `engine.py` | `diagnose`: menjalankan search, mengumpulkan fakta, menerapkan aturan, menyusun teks rute |

## Cara kerja

1. `diagnose` menjalankan search dengan gangguan, dan sekali lagi tanpa gangguan sebagai pembanding.
2. Hasilnya menjadi **fakta**: ada rute atau tidak, waktu, jumlah pindah jalur, selisih waktu.
3. Semua aturan dicek terhadap fakta.
4. Status akhir adalah tingkat **paling parah** dari aturan yang cocok (0 LANCAR, 1 PERHATIAN, 2 TERGANGGU).

## Daftar aturan

| Aturan | Kondisi | Tingkat |
|--------|---------|---------|
| R1 | Stasiun asal atau tujuan ditutup | TERGANGGU |
| R2 | Tidak ada rute yang bisa dipakai | TERGANGGU |
| R3 | Pindah jalur 2 kali atau lebih | PERHATIAN |
| R4 | Ada gangguan dan waktu lebih lama dari normal | PERHATIAN |
| R5 | Waktu tempuh lebih dari 40 menit | PERHATIAN |
| R6 | Jam sibuk (waktu x 1,3) | PERHATIAN |
| R7 | Perjalanan langsung tanpa pindah jalur | LANCAR |
| R8 | Asal dan tujuan sama | LANCAR |
| R9 | Jaringan normal tanpa gangguan | LANCAR |

## Bentuk aturan

```python
Rule("R5", 1, lambda f: f.result.found and f.result.minutes > 40,
     lambda f: "pesan saran ...")
```

JIKA kondisi (`lambda` pertama) benar, MAKA tampilkan pesan (`lambda` kedua). `f` adalah fakta.

## Contoh

```python
from search_algorithm import TransitNetwork
from expert_system import diagnose

net = TransitNetwork.from_json("data/jaringan.json")
d = diagnose(net, "pasar_barat", "bandara", closed_stations={"pusat"}, rush_hour=True)
print(d.status, d.messages)
```

## Menambah aturan

Tambahkan `Rule(...)` di dalam `RULES` sebelum tanda `]` terakhir (4 spasi di awal, koma di ujung), lalu tambahkan tesnya di `tests/test_expert.py`.
