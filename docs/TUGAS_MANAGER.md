# Tugas Manager / Ketua: aturan R10 dan tesnya

Bagian ini dikerjakan ketua di `main`, setelah proyek di-push ke GitHub.

## 1. Baca aturan yang sudah ada

Buka `expert_system/rules.py` dengan Notepad (klik kanan > Open with > Notepad). Perhatikan satu aturan:

```python
Rule("R5", 1, lambda f: f.result.found and (f.result.minutes or 0) > PERJALANAN_LAMA,
     lambda f: f"Perjalanan cukup lama ({f.result.minutes} menit). Siapkan waktu lebih."),
```

Artinya: aturan R5, tingkat 1 (0 LANCAR, 1 PERHATIAN, 2 TERGANGGU). JIKA kondisi (`lambda` pertama) benar, MAKA tampilkan pesan (`lambda` kedua). `f` adalah fakta, misalnya `f.closed_stations` dan `f.result`.

## 2. Tambahkan aturan R10

Tekan **Ctrl + End** untuk ke baris paling bawah. Kamu melihat aturan `R9`, dan di bawahnya satu baris berisi `]`. Tepat **di atas `]`**, tambahkan:

```python
    Rule("R10", 1, lambda f: len(f.closed_stations) >= 2,
         lambda f: f"{len(f.closed_stations)} stasiun ditutup sekaligus. Cek informasi petugas sebelum berangkat."),
```

Pastikan awalnya 4 spasi dan baris R9 di atasnya berakhir dengan koma. Simpan (**Ctrl + S**).

## 3. Coba hasilnya

```
python main.py --cli --from pasar_barat --to bandara --closed-stations pusat,mal_timur
```

Harus muncul saran "2 stasiun ditutup sekaligus...". Dengan satu stasiun saja (`--closed-stations pusat`), saran itu tidak boleh muncul.

## 4. Tambahkan tes

Di Notepad, tempel kode di bawah, lalu **File > Save As**. *Save as type*: **All files**, nama `test_manager.py`, folder `tests`, encoding **UTF-8**.

```python
import os

import pytest

from expert_system import diagnose
from search_algorithm import TransitNetwork

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "jaringan.json")


@pytest.fixture(scope="module")
def net():
    return TransitNetwork.from_json(DATA)


def test_dua_stasiun_tutup_memicu_r10(net):
    d = diagnose(net, "pasar_barat", "bandara", {"pusat", "mal_timur"})
    assert "R10" in d.fired_rules
    assert d.status == "PERHATIAN"


def test_satu_stasiun_tutup_tidak_memicu_r10(net):
    d = diagnose(net, "pasar_barat", "bandara", {"pusat"})
    assert "R10" not in d.fired_rules
```

Jalankan `python -m pytest`. Seharusnya `30 passed`.

## 5. Kirim ke GitHub

```
git add .
git commit -m "Tambah aturan R10 dan tes (Manager)"
git push
```

## 6. Perbarui dokumen

- Di `README.md`: ubah "9 aturan JIKA-MAKA (R1-R9)" menjadi "10 aturan (R1-R10)", dan sebutkan "9 aturan" di bagian lain bila ada.
- Di `expert_system/README.md`: tambahkan baris R10 di tabel (Dua stasiun ditutup atau lebih, PERHATIAN), dan ubah R1-R9 menjadi R1-R10.
