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

### Tugas 3

1. ModelForm dipilih ketimbang form HTML manual karena beberapa alasan:
   - Integrasi: ModelForm Django otomatis terintegrasi dengan database lewat mapper bawaan Django.
   - Konsistensi: Mengikuti definisi model (models.py), seperti max length, format URL, dsb.
   - Less Boilerplate: dengan ModelForm, akan mengautomisasi widget HTML yang sesuai tipe field. (misal field choices langsung membuat ```<select>```)

   Adapun penggunaan ``` {% csrf_token %} ``` (Cross-Site Request Forgery) merupakan token yang mencegah situs lain memicu request ke situs kita, seperti submit form tambah, ubah, atau hapus data. Request tersebut dapat membuat HTTP request yang sebenarnya tidak ingin dilakukan user situs kita.
2. Ada beberapa alasan kenapa JSON lebih dipilih daripada XML. Antara lain:
   - Ringkas (Less verbose): syntax json fokus kepada format key:value yang sederhana daripada xml yang butuh opening dan closing tag tiap elemen.
   - Native ke JavaScript: mayoritas aplikasi web modern berbasis java script di sisi client, karena JSON sendiri adalah subset dari syntax object pada JavaScript, browser client bisa langsung parsing tanpa parser tambahan (misal XML butuh DOMParser, dsb yang lebih berat)
3. Contoh proses serialization di aplikasi ini ada pada method get_experience_json. alurnya:
   1. Membuat HTTP request GET ke server
   2. Data (dalam python) disimpan pada variabel experiences
   3. Data yang ada di serialize ke JSON
   4. return HTTP response data yang sudah di serialize ke JSON tersebut
   serialization tersebut diperlukan agar browser bisa membaca data tersebut. (format JSON adalah format yang universal sehingga bisa dibaca di client manapun (browser, mobile, dsb))

### AI Disclosure

Tools: Claude\
Strategi Prompting:
- Bertanya seputar konsep dan penerapan yang sesuai pada proyek Django.
Bagian Spesifik yang dibantu:
- Cara implementasi template inheritance
- Cara implementasi create, update, dan delete pada view
- Cara implementasi dan integrasi penggunaan field password untuk create, update, dan delete.
- Cara refactor ke alur serialize dan deserialize dalam mengambil dan mereturn data.

Detail Chat: https://claude.ai/share/f4910087-487d-430f-a065-118b0f5cae01


