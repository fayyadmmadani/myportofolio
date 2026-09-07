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

### Tugas 1

1. Ya, saya menggunakan semantik yang ada pada HTML5. Namun begitu, menurut saya, bisa saja mengabaikan beberapa tag semantik html seperti `<section>`, `<article>`, dan beberapa tag lainnya. Namun ada dua masalah penting yang jarang disadari.
   - Yang pertama dari sisi pengembangan, jika konten-konten sebuah web hanya memakai tag `<div>`, skalabilitas dari website akan sedikit terhambat, terutama jika pengembang berganti tangan. Developer A yang mengembangkan web tersebut mungkin tidak kesulitan dalam melanjutkan pengembangan yang dibutuhkan. Namun jika proyek web tersebut diberi ke Developer B, ia akan terhambat dalam memahami projek secara keseluruhan (untuk konten experience ada di mana, konten projects yang mana, dsb).
   - Lalu yang kedua dari sisi engine, seperti search engine, web browser, screen reader, dan lainnya. Engine-engine tersebut akan kesulitan dalam meng-indeks konten web, seperti menentukan mana konten utama, mana navigasi, hierarki konten konten yang ada, dan sebagainya. Hal ini akan berimplikasi pada kurangnya pengalaman pengguna (User Experience) dan SEO (Search Engine Optimization) untuk website (seperti mudah dicari dari search engine google).

2. Tantangan tata letak yang saya temukan adalah:
   - Navbar pada mobile tidak muat jika dibuat memanjang seperti tampilan desktop, sehingga dibuat tombol hamburger, yakni tombol garis 3 untuk ekspan navigasi yang ada.
   - Ada konten yang urutannya harus disesuaikan, yakni class about.info diberi atribut `display: contents;` agar bisa mengurutkan posisi foto terhadap div about-info tersebut
   - Tuning ukuran margin dan padding yang butuh trial error dalam menentukan nilainya agar sesuai dengan yang diharapkan.

3. Batasan yang ditemukan adalah keterbatasan dalam interaktivitas web, misalnya tidak bisa membuat state di mana section dibuka, kemudian muncul efek visual seperti warna dan garis bawah di navbar. serta juga carousel yang punya state card utama yang sedang dilihat. Kemudian ada keterbatasan dalam mengubah tampilan jika ada data yang ingin ditambah, diupdate, atau dihapus sehingga butuh menyentuh kode secara langsung untuk merubahnya.
   \
   \
   Pada iterasi proyek selanjutnya, saya ingin mengimplementasi efek visual yang bisa disesuaikan dengan kondisi user, misalnya menekan navigasi experience akan menampilkan efek visual tombol experience pada navbar yang memiliki warna berbeda dengan yang lain.

### AI Disclosure

Tools: Claude\
Strategi Prompting:

- Diskusi terkait perencanaan pengembangan, seperti arsitektur kode yang baik (terutama untuk skalabilitas), tag, selector, dan atribut yang bisa digunakan sesuai konteks yang akan diimplementasi, serta evaluasi terhadap kode yang sudah dibuat
- Bagian spesifik yang dibantu: bagaimana implementasi kode yang modular pada django, konten foto profile berbeda posisi pada mobile dan desktop. atribut-atribut yang digunakan untuk kebutuhan spesifik, misal: clamp() untuk mengunci elemen terhadap layar yang dinamis pada browser.
