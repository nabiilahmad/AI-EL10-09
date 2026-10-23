# Analisis Perbandingan Algoritma Search (MetroRoute AI)

Data dihasilkan dengan menjalankan BFS, UCS, dan A* pada jaringan di `data/jaringan.json`.
**Diekspansi** = jumlah keadaan (stasiun + jalur) yang dicek sebelum rute ditemukan; makin kecil makin hemat usaha.

| Skenario | Algoritma | Ketemu | Waktu (menit) | Pindah jalur | Diekspansi |
|---|---|---|---|---|---|
| Sekolah -> Bandara, normal | BFS | ya | 41.0 | 1 | 18 |
|  | UCS | ya | 41.0 | 1 | 17 |
|  | A* | ya | 41.0 | 1 | 11 |
| Pasar Barat -> Bandara, normal | BFS | ya | 27.0 | 0 | 10 |
|  | UCS | ya | 27.0 | 0 | 16 |
|  | A* | ya | 27.0 | 0 | 5 |
| Pusat -> Stadion, normal | BFS | ya | 25.2 | 1 | 15 |
|  | UCS | ya | 23.0 | 1 | 18 |
|  | A* | ya | 23.0 | 1 | 6 |
| Pasar Barat -> Bandara, Stasiun Pusat tutup | BFS | ya | 55.4 | 2 | 16 |
|  | UCS | ya | 55.4 | 2 | 16 |
|  | A* | ya | 55.4 | 2 | 16 |
| Bandara -> Taman Kota, Jalur Biru gangguan | BFS | tidak | - | - | 0 |
|  | UCS | tidak | - | - | 0 |
|  | A* | tidak | - | - | 0 |

## Kesimpulan

1. **UCS dan A\* selalu menghasilkan waktu tempuh yang sama** pada seluruh pasangan stasiun, karena keduanya optimal. Heuristik A* (jarak garis lurus x 2 menit/km) tidak pernah melebihi waktu sebenarnya.
2. **A\* paling hemat pengecekan** dalam semua skenario normal, misalnya Pasar Barat ke Bandara: A* 5 keadaan, BFS 10, UCS 16.
3. **BFS tidak selalu menemukan rute tercepat.** BFS menghitung langkah, bukan menit. Dari 110 pasangan stasiun, BFS memberi rute lebih lambat daripada UCS pada 6 pasangan (contoh: Pusat ke Stadion, BFS 25.2 menit, UCS 23.0 menit).
4. **UCS tidak selalu lebih hemat dari BFS.** Pada Pasar Barat ke Bandara, UCS mengecek 16 keadaan dan BFS hanya 10. UCS menjamin waktu tercepat, bukan pengecekan paling sedikit.
5. **Pindah jalur memakan 5 menit**, sehingga rute terbaik dihitung dari total menit, termasuk waktu pindah, bukan hanya jumlah stasiun yang dilewati.
6. **Gangguan mengubah rute dan waktu.** Saat Stasiun Pusat tutup, Pasar Barat ke Bandara harus memutar lewat Terminal Utara dan Kampus Timur dengan dua kali pindah jalur.
7. **Tanpa rute.** Bandara hanya dilayani Jalur Biru, jadi jika Biru gangguan, semua algoritma menyimpulkan tidak ada rute dan sistem pakar menetapkan status TERGANGGU.

## Catatan

Angka berlaku untuk jaringan contoh ini dan belum tentu sama di jaringan lain.
