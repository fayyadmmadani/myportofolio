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

5. Jalankan migrasi database:

```bash
   python manage.py migrate
```

6. Jalankan development server:

```bash
   python manage.py runserver
```

Setelah itu, buka `http://127.0.0.1:8000/` atau `http://localhost:8000` di browser.

### Tugas 2

1. Pertama, browser kirim request ke urls.py milik proyek, kemudian ke urls.py aplikasi terkait dan panggil view yang tepat. Selanjutnya, view akan memanggil model untuk mengambil data yang dibutuhkan, kemudian menyertakan data tersebut ke template yang sesuai. ketika template sudah diisi dengan data dari model, view akan mereturn hasil tersebut sebagai response ke browser milik user.
2. Data sebaiknya disimpan pada model dan tidak langsung di template karena beberapa alasan. Salah satu yang utama adalah separation of concern. Dengan membuatnya di model dan tidak langsung di template, akan membuat template bisa fokus kepada bagaimana data data tersebut akan ditampilkan. Tak hanya itu, dengan menaruh data di model, aplikasi bisa lebih dinamis karena tidak harus menulis data secara langsung (hardcode). Dari sisi maintanability, menghapus data dari database lebih aman daripada langsung dari file kode yang rawan terlewat.
3. makemigrations dan migrate pada Django merupakan sebuah command yang bisa dijalankan pada proyek Django. Kedua command ini berperan dalam sebuah pipeline migrasi database. Perbedaannya terletak pada apa yang dilakukan secara spesifik:
   - makemigrations berfokus dalam mendeteksi perubahan pada model yang sudah ada. Jika terdapat perubahan, maka akan dibuat sebuah file migrasi.
   - migrate adalah yang menjadi eksekutor dalam menerjemahkan operasi-operasi yang berhubungan dengan database langsung ke dalam query database bersangkutan (misal sql).
Contohnya saat menambahkan field baru order pada model Project di project ini, makemigrations mendeteksi perubahan itu dan membuat file migrasi baru (0003_project_order.py), lalu migrate menjalankan file tersebut sehingga kolom order benar-benar ditambahkan ke tabel Project di database.

### AI Disclosure

Tools: Claude\
Strategi Prompting:
- Diskusi terkait style yang menyesuaikan dengan tema aplikasi secara keseluruhan.
- Bertanya seputar konsep dan penerapan yang sesuai pada proyek Django.

Detail Chat: https://claude.ai/share/cfe72149-66f5-4ece-a781-ab52425e564d


