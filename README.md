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

### Tugas 5

1. Debouncing adalah teknik menunda eksekusi sebuah fungsi sampai event berhenti terjadi selama jeda waktu tertentu. Setiap event baru membatalkan timer sebelumnya (`clearTimeout`) lalu memulai timer baru (`setTimeout`), sehingga fungsi hanya dijalankan sekali setelah pengguna benar-benar berhenti. Teknik ini penting untuk pencarian berbasis AJAX karena tanpa debouncing setiap karakter yang diketik memicu satu request ke server. Mengetik "asisten" berarti tujuh request, padahal hanya hasil terakhir yang dibutuhkan. Akibatnya beban server dan jaringan bertambah, dan respons yang datang tidak berurutan bisa menimpa hasil terbaru dengan hasil lama. Pada halaman Experience, pencarian judul memakai jeda 300 ms dan request lama dibatalkan dengan `AbortController`, sehingga hanya hasil pencarian terbaru yang ditampilkan.

2. `fetch()` bersifat asinkron dan langsung mengembalikan sebuah `Promise`, bukan data responsnya. **`await`** (hanya bisa dipakai di dalam fungsi `async`) membuat eksekusi fungsi menunggu sampai `Promise` tersebut selesai lalu mengembalikan nilainya, sehingga kode asinkron bisa ditulis berurutan seperti kode sinkron dan error bisa ditangkap dengan `try...catch`. Tanpa `await`, variabel akan berisi objek `Promise` yang belum selesai, bukan objek `Response`. Pemanggilan seperti `response.ok` atau `response.json()` akan bernilai `undefined` atau gagal, baris berikutnya langsung berjalan sebelum data tiba, dan error jaringan tidak tertangkap oleh blok `catch` di fungsi tersebut. Contohnya di `fetchExperience`, `await fetch(...)` memastikan status respons diperiksa dulu, lalu `await response.json()` memastikan data sudah ter-parse sebelum kartu dirender.

3. XSS (Cross-Site Scripting) adalah serangan ketika penyerang berhasil menyisipkan kode JavaScript ke halaman web, yang kemudian dijalankan di browser pengguna lain. Pada stored XSS, payload seperti `<img src="x" onerror="alert('XSS!')">` disimpan ke database (misalnya sebagai judul) lalu ikut dieksekusi setiap kali data ditampilkan, sehingga penyerang bisa membaca cookie `csrftoken` dan mengirim request atas nama korban. Template Django aman secara default karena melakukan auto-escaping pada setiap `{{ variabel }}`: karakter `<`, `>`, `&`, `"`, dan `'` diubah menjadi entity sehingga ditampilkan sebagai teks biasa. Saat data ditampilkan lewat AJAX, data JSON disisipkan ke template literal lalu dipasang dengan `innerHTML`, dan proses ini tidak melewati template Django. Browser akan menafsirkan setiap tag HTML di dalam data sebagai kode sungguhan. Karena itu setiap nilai harus di-escape manual (`escapeHtml` atau `textContent`), dan sebagai lapisan tambahan input dibersihkan di server dengan `strip_tags` pada method `clean_<field>` di `ModelForm`.

### AI Disclosure

Tools: Claude\
Strategi Prompting:
- Mendiskusikan keputusan desain sebelum eksekusi: adaptasi field Project yang sudah ada, bagian portofolio yang dikerjakan (Experience, karena Projects sudah dipakai di tutorial), pemetaan branch (`tutorial`, `feat/projects`, `feat/experience`), dan fitur ekstra yang dipilih (filter kategori).
- Bagaimana memperbaiki masalah setelah mengikuti tutorial: form hapus di kartu AJAX yang tidak mengirim `secret` dan unit test lama yang masih mengecek HTML hasil render Django.
- Cara memindahkan `escapeHtml` dan `getCookie` ke `static/js/utils.js` agar dipakai bersama oleh Projects dan Experience.
- Cara mengubah halaman Experience menjadi AJAX: JSON manual dengan `JsonResponse` (termasuk format tanggal di server), state loading/kosong/error, pencarian dengan debouncing, filter kategori, dan modal konfirmasi hapus yang dibuat lewat JavaScript.
- Cara membuat `create_experience_ajax` dengan `@require_POST`, pengecekan peran di view (`can_create_or_delete`), validasi `ModelForm`, status 201/400/403, dan token CSRF lewat header `X-CSRFToken`.
- Cara membersihkan input dengan `strip_tags` pada `clean_title` dan `clean_description`.
- Cara menulis unit test untuk endpoint AJAX (405, 403 per peran, 400, 201), filter pencarian, dan sanitasi XSS.
Keterbatasan AI yang ditemukan:
- Untuk evaluasi, AI tidak dapat menguji tampilan dan interaksi di browser secara langsung, sehingga pengujian fungsional di `runserver` tetap dilakukan secara manual.
