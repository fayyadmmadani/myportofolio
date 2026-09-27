# My Portofolio

### Nama: Fayyad Mohammad Madani

### NPM: 2506622720

### Kelas: PBP A

## Cara Menjalankan Project

1. Clone repository ini:

```bash
   git clone <url-repo-ini>
   cd myportofolio
```

2. Buat virtual environment:

```bash
   python -m venv env
```

3. Aktifkan virtual environment:

```bash
   env\Scripts\activate
```

Untuk keluar dari virtual environment:

```bash
   deactivate
```

Catatan untuk pengguna macOS/Linux, perintah aktivasinya berbeda: `source env/bin/activate`

4. Install semua dependency yang dibutuhkan:

```bash
   pip install -r requirements.txt
```

5. Buat file `.env` di root project dengan isi berikut:

```env
   PRODUCTION=False
   EDIT_SECRET=<password-bebas>
```

`EDIT_SECRET` adalah password yang diminta setiap kali menambah, mengubah, atau menghapus data.

6. Jalankan migrasi database (sekaligus membuat grup `Editor` secara otomatis):

```bash
   python manage.py migrate
```

7. Buat akun pemilik portofolio (superuser):

```bash
   python manage.py createsuperuser
```

8. Jalankan development server:

```bash
   python manage.py runserver
```

Setelah itu, buka `http://127.0.0.1:8000/` atau `http://localhost:8000` di browser.

### Menetapkan Peran Editor

1. Daftarkan akun baru lewat halaman Register.
2. Login ke `/admin` menggunakan akun superuser.
3. Buka **Users**, pilih akun tersebut, lalu tambahkan ke grup **Editor** pada bagian *Groups* dan simpan.

Akun Editor dapat mengubah data Projects dan Experience, tetapi tidak dapat menambah atau menghapusnya.

### Menjalankan Test

```bash
   python manage.py test
```

### Tugas 4

### AI Disclosure

Tools: Claude\
Strategi Prompting:
- Memberikan dokumen soal Tugas 4 dan meminta analisis selisih antara requirement dengan kondisi repositori saat ini.
- Mendiskusikan pemetaan pekerjaan per branch (feat/auth, feat/experience, feat/projects) sebelum eksekusi, lalu meminta implementasi per branch dan melakukan review, commit, serta merge sendiri.
Bagian Spesifik yang dibantu:
- Perbaikan implementasi Tutorial 4: key context last_login, route toggle_star, komponen tombol star, dan tampilan sesi terakhir login.
- Cara implementasi peran Editor melalui Django Group menggunakan data migration.
- Cara memisahkan logika otorisasi ke helper (is_editor, can_edit, can_create_or_delete) agar dipakai bersama oleh Projects dan Experience.
- Cara menerapkan pembatasan hak akses di sisi server (redirect login dan HTTP 403) serta menyembunyikan tombol aksi sesuai peran di template.
- Cara membuat halaman 403 custom.
- Cara menulis unit test untuk hak akses keempat peran, fitur star, dan keamanan endpoint JSON, serta memperbaiki test lama yang gagal.
