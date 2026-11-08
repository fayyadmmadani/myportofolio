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

### Tugas 6

1. REST (Representational State Transfer) adalah gaya arsitektur komunikasi perangkat lunak berbasis protokol HTTP yang berpusat pada pengelolaan resource (sumber daya) menggunakan URI standar dan metode HTTP semantik. Mengembalikan format JSON saja belum cukup untuk disebut RESTful karena JSON hanyalah format representasi data (payload format). Sebuah API baru dapat disebut RESTful jika mematuhi prinsip-prinsip batasan arsitektur REST, antara lain: pemisahan client-server, statelessness (setiap request membawa konteks lengkap tanpa bergantung pada session state di server), antarmuka yang seragam (uniform interface yang memanfaatkan HTTP verbs GET, POST, PUT, PATCH, DELETE sesuai semantiknya), resource-based identification (misalnya `/api/v1/experiences/<id>/`), penggunaan HTTP status code yang tepat (seperti 200, 201, 204, 400, 403, 404), serta kemampuan manipulasi resource melalui representasi data tersebut.

   Perbedaan utama antara PUT dan PATCH terletak pada cakupan pembaruan datanya. **PUT** bersifat penggantian penuh (full replacement/update) dan idempoten, di mana klien harus mengirimkan seluruh representasi objek secara lengkap; field yang tidak disertakan akan dikosongkan atau diisi nilai default. Contoh penggunaannya adalah ketika pengguna mengedit seluruh data profil melalui formulir lengkap di mana semua atribut dikirimkan kembali ke server. Sedangkan **PATCH** bersifat pembaruan parsial (partial update), di mana klien hanya mengirimkan field spesifik yang ingin diubah tanpa mempengaruhi nilai field lainnya pada resource tersebut. Contoh penggunaannya adalah ketika pengguna hanya ingin memperbarui judul atau status experience (misalnya mengubah `title` saja pada modal edit) tanpa perlu mengirimkan ulang tanggal mulai, thumbnail, atau kategori.

2. Serializer pada Django REST Framework berfungsi sebagai jembatan dua arah (two-way converter) antara tipe data kompleks di Django (seperti objek model dan QuerySet) dengan format data primitif yang dapat dirender ke JSON/XML (proses serialisasi), sekaligus mengubah payload JSON dari request menjadi tipe data Python yang tervalidasi sebelum disimpan ke database (proses deserialisasi). Keuntungannya dibandingkan merakit dictionary secara manual dengan `JsonResponse` seperti pada Tutorial 05 adalah:
   - **Validasi Terpusat dan Otomatis**: Serializer secara otomatis memvalidasi tipe data, batasan model (seperti `max_length`, `choices`, format URL), dan field wajib, serta menyediakan validasi tingkat field (`validate_<field>`) dan objek (`validate`) dengan format error terstandarisasi (HTTP 400), tanpa perlu menulis puluhan baris validasi `if-else` manual di dalam view.
   - **Sanitasi dan Transformasi Data Konsisten**: Pembersihan input (seperti `strip_tags` untuk mitigasi XSS) terikat rapi pada siklus validasi serializer, dan field kalkulasi (seperti `SerializerMethodField` untuk `star_count` dan `is_starred`) dapat didefinisikan secara deklaratif.
   - **Pemisahan Tanggung Jawab (Separation of Concerns)**: Logika representasi data terpisah dari logika kontrol di view/controller. View hanya bertugas mengatur alur HTTP dan otorisasi, sementara serializer menangani struktur dan integritas data.
   - **Integrasi Ekosistem DRF**: Serializer mendukung fitur DRF lanjutan seperti Browsable API interaktif, pagination otomatis, serta pembentukan skema OpenAPI/Swagger secara otomatis.

3. **Autentikasi** adalah proses pembuktian identitas pengguna (*who you are*), yaitu memverifikasi kredensial (seperti session cookie atau token) untuk mengidentifikasi apakah request datang dari pengguna yang valid atau pengguna anonim (`request.user`). Sementara itu, **otorisasi** adalah proses penentuan hak akses (*what you are allowed to do*), yaitu memeriksa apakah pengguna yang sudah terautentikasi memiliki izin untuk melakukan tindakan atau mengakses resource tertentu (misalnya memeriksa apakah user adalah Superuser, anggota grup `Editor`, atau pengguna biasa). Hak akses wajib diperiksa di server menggunakan permission class (seperti `IsOwnerOrEditorOrReadOnly`) karena antarmuka web (HTML template dan tombol UI) berada di bawah kendali penuh sisi klien (*client-side*). Menyembunyikan tombol di template hanyalah peningkatan pengalaman pengguna (UX) agar pengguna tidak melihat aksi yang tidak relevan, bukan mekanisme keamanan. Klien mana pun (seperti penyerang menggunakan Postman, curl, skrip Python, atau Console DevTools browser) dapat dengan mudah membuat dan mengirimkan HTTP request mutasi (POST, PATCH, DELETE) langsung ke URL endpoint API tanpa memerlukan tombol di template. Jika server tidak memvalidasi izin dengan permission class, penyerang dapat melewati pembatasan UI tersebut dan memanipulasi data (*Broken Object Level Authorization* / *Privilege Escalation*).

4. Permintaan yang mengubah data (POST, PUT, PATCH, DELETE) tetap memerlukan token CSRF (`X-CSRFToken`) pada `SessionAuthentication` karena browser secara otomatis melampirkan cookie sesi (`sessionid`) pada setiap HTTP request ke domain yang bersangkutan, termasuk request lintas situs (*cross-origin*). Tanpa token CSRF, aplikasi rentan terhadap serangan CSRF (*Cross-Site Request Forgery*), di mana situs berbahaya yang dikunjungi korban dapat memicu request mutasi data secara diam-diam ke portofolio menggunakan kredensial cookie sesi korban yang masih aktif. Token CSRF berfungsi sebagai rahasia yang tidak dapat dibaca oleh situs pihak ketiga karena aturan *Same-Origin Policy*, sehingga server dapat memastikan bahwa request mutasi tersebut memang sengaja dikirimkan oleh frontend resmi aplikasi kita. Pengujian yang memakai `force_authenticate` tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan karena method `force_authenticate()` sengaja dirancang untuk melewati (*bypass*) seluruh lapisan autentikasi Django, termasuk mekanisme evaluasi middleware `CsrfViewMiddleware` dan pembacaan cookie. Saat memakai `force_authenticate`, objek user langsung ditempelkan ke `request.user` tanpa memproses login session dan tanpa memeriksa token CSRF. Oleh karena itu, pengujian CSRF wajib menggunakan `APIClient(enforce_csrf_checks=True)` bersama metode `client.login()`, yang menjalankan siklus penanganan request secara nyata sehingga dapat membuktikan bahwa permintaan mutasi tanpa header `X-CSRFToken` benar-benar ditolak dengan status HTTP 403 Forbidden.

### AI Disclosure

Tools: Gemini

Strategi Prompting:
- Manajemen Git & Branching Tugas 6: pemilihan strategi merge branch `tutorial` ke `dev` sebagai integrasi Tutorial 07, penyelesaian konflik stash pada `templates/projects.html` ke endpoint DRF yang bersih, dan melanjutkan pengerjaan Tugas 6 di branch `feat/experience`.
- Desain & Migrasi Model: menambahkan relasi many-to-many `starred_by` pada model `Experience` dan mengeksekusi migrasi database `0006_experience_starred_by`.
- Implementasi Serializer & Otorisasi DRF: Bagaimana merancang `ExperienceSerializer` dengan field eksplisit, field kalkulasi star (`star_count`, `is_starred`, `starred_by_names`), sanitasi XSS `strip_tags` pada `validate_title` dan `validate_description`, serta merapikan permission class semantik (`IsOwnerOrReadOnly`, `IsOwnerOrEditorOrReadOnly`).
- Alur Pembangunan API Views & Endpoint: langkah-langkah membangun fungsi API berbasis fungsi (`@api_view`, `SessionAuthentication`) untuk daftar, detail, dan star dengan status HTTP standar (200, 201, 204, 400, 403, 404), serta mendaftarkan routing `/api/v1/experiences/`.
- Migrasi Frontend Experience ke DRF: bagaimana memperbarui `experience.html` dan membuat modal edit `experience_edit_modal.html` agar seluruh aksi CRUD, pencarian, filter kategori, dan star berjalan via `fetch()` tanpa reload halaman dengan feedback pesan toast.
- Pengujian Komprehensif: menyusun test suite `ExperienceAPITest` di `main/tests_api.py` yang mencakup keempat peran, validasi input, sanitasi XSS, verifikasi keutuhan database pada penolakan, serta uji kepatuhan CSRF menggunakan `APIClient(enforce_csrf_checks=True)` dan `.login()`.

Keterbatasan AI yang ditemukan:
- Untuk evaluasi, AI tidak dapat menguji tampilan dan interaksi di browser secara langsung, sehingga pengujian fungsional di `runserver` tetap dilakukan secara manual.
