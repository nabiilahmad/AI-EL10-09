# app

Bagian **tampilan (GUI)** MetroRoute AI, dibuat dengan **Tkinter**. GUI hanya menampilkan dan menerima masukan; logika ada di folder lain.

| File | Fungsi |
|------|--------|
| `gui.py` | Jendela aplikasi: pilihan, peta jaringan, dan kotak hasil |

## Menjalankan

```bash
python main.py
```

Tkinter: bawaan Python di Windows dan macOS. Linux: `sudo apt install python3-tk`.

## Isi tampilan

- Pilihan **Asal**, **Tujuan**, **Algoritma**.
- Daftar **Stasiun ditutup** (pilih lebih dari satu dengan Ctrl), kotak centang **Jalur gangguan**, dan **Jam sibuk**.
- Tombol **Cari Rute** dan **Reset**.
- Peta jaringan: tiap jalur berwarna, rute ditandai garis tebal gelap.
- Kotak hasil: status, waktu, rute per jalur, dan saran.

## Arti tampilan peta

| Tampilan | Arti |
|----------|------|
| Garis tebal gelap | Rute yang dipilih |
| Cincin biru | Stasiun asal |
| Cincin hijau | Stasiun tujuan |
| Lingkaran merah dengan X | Stasiun ditutup |

## Cadangan tanpa GUI

```bash
python main.py --cli --from sekolah --to bandara --algo "A*"
```

## Catatan rancangan

GUI memanggil `diagnose` dari `expert_system`, sehingga logika yang sama bisa dites otomatis dan dijalankan lewat CLI tanpa membuka jendela.
