# Panduan Git Kelompok (2 orang)

Ganti `<kode-kelas>` dengan kode kelasmu (contoh `AI-TE-103`) dan `<username-ketua>` dengan username GitHub ketua.

| Peran | Branch |
|-------|--------|
| Manager / Ketua | `main` |
| Dev 1 | `dev-1` |

## 1. Ketua: buat repository dan unggah proyek (sekali di awal)

1. Di github.com klik **+ > New repository**. Nama: `<kode-kelas>`. **Jangan** centang README, .gitignore, atau license. Klik **Create repository**.
2. Buka terminal di folder proyek (folder yang berisi `main.py`), lalu:

```bash
git config --global user.name "Ahmad Nabiil Alfarizi"
git config --global user.email "email-akun-github@contoh.com"
git init -b main
git add .
git commit -m "Initial commit: MetroRoute AI"
git remote add origin https://github.com/<username-ketua>/<kode-kelas>.git
git push -u origin main
```

3. Di GitHub: **Settings > Collaborators > Add people**, tambahkan Dev 1.

Pembagian file supaya tidak bentrok:
- **Ketua** hanya mengubah `expert_system/rules.py` (aturan R10), `tests/test_manager.py`, dan README.
- **Dev 1** hanya mengubah `docs/ANALISIS.md` dan `tests/test_dev1.py`.

## 2. Dev 1: ambil proyek dan buat branch

```bash
git clone https://github.com/<username-ketua>/<kode-kelas>.git
cd <kode-kelas>
git checkout -b dev-1
```

Kerjakan tugas (lihat `docs/TUTORIAL_ANGGOTA.md`), lalu:

```bash
python -m pytest
git add .
git commit -m "Tambah skenario analisis dan tes (Dev 1)"
git push -u origin dev-1
```

Buka GitHub, klik **Compare & pull request**, lalu **Create pull request**.

## 3. Ketua: kerjakan bagianmu (lihat `docs/TUGAS_MANAGER.md`)

Bagian ketua dikerjakan langsung di `main` dan di-push:

```bash
git add .
git commit -m "Tambah aturan R10 dan tes (Manager)"
git push
```

## 4. Ketua: review dan merge pull request Dev 1

Tab **Pull requests**, baca perubahan, lalu **Merge pull request**. Setelah itu semua anggota:

```bash
git checkout main
git pull
```

## 5. Kalau muncul "This branch has conflicts"

Klik **Resolve conflicts**. Hapus baris `<<<<<<<`, `=======`, `>>>>>>>`, dan **simpan kedua versi** isinya. Lalu **Mark as resolved**, **Commit merge**, dan **Merge pull request**. Dengan pembagian file di atas, konflik seharusnya tidak terjadi.

## 6. Checklist ketua sebelum dikumpulkan

- [ ] Pull request Dev 1 sudah di-merge ke `main`.
- [ ] `python -m pytest` lolos di `main` (34 tes).
- [ ] README: nama anggota, kode kelas, dan jumlah aturan diperbarui (setelah R10, jumlahnya 10; ubah juga tabel di `expert_system/README.md`).
- [ ] Bagian kontribusi README sesuai riwayat commit.
- [ ] Nama repository di GitHub sama dengan kode kelas.
