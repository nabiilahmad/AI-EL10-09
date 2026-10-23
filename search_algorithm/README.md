# search_algorithm

Bagian **pencarian rute** MetroRoute AI.

| File | Fungsi |
|------|--------|
| `graph.py` | Model jaringan: stasiun, jalur, biaya waktu, tetangga, heuristik |
| `algorithms.py` | BFS, UCS, A*, dan `segments` (mengelompokkan rute per jalur) |

## Konsep

- **Stasiun** punya posisi (x, y) dalam km. **Jalur** adalah urutan stasiun.
- **Keadaan pencarian** = (stasiun, jalur yang sedang dinaiki). Ini yang membuat pindah jalur bisa dihitung.
- **Biaya (menit):** antar stasiun = 2 x jarak (km) + 1 menit berhenti. Pindah jalur = 5 menit.
- **Gangguan:** stasiun tertutup tidak boleh dimasuki, dan jalur gangguan tidak boleh dinaiki.
- **Tujuan:** keadaan mana pun yang stasiunnya sama dengan stasiun tujuan.

## Algoritma

| Algoritma | Memilih keadaan berikutnya | Hasil |
|-----------|----------------------------|-------|
| BFS | Antrean: yang paling sedikit langkahnya | Langkah paling sedikit (belum tentu tercepat) |
| UCS | Waktu tempuh terkecil | Waktu tercepat |
| A* | Waktu tempuh + perkiraan sisa (heuristik) | Waktu tercepat, pengecekan lebih sedikit |

Heuristik: jarak garis lurus ke tujuan x 2 menit/km. Tidak pernah melebihi waktu sebenarnya, jadi A* tetap optimal.

## Hasil (`SearchResult`)

`path`, `minutes`, `rides` (pindah stasiun), `transfers` (pindah jalur), `expanded`, dan `found`.

## Contoh

```python
from search_algorithm import TransitNetwork, ALGORITHMS

net = TransitNetwork.from_json("data/jaringan.json")
r = ALGORITHMS["A*"](net, "sekolah", "bandara")
print(r.minutes, r.transfers, r.expanded)
```

## Tes

`tests/test_search.py` (`python -m pytest`).
