import json
from pathlib import Path
import subprocess
import shutil

from product_qa.doctor import tool_path, java_path
from product_qa.checks import check_product

TARGET_DIR = Path(r"C:\Users\YM\Desktop\PROJECT SERIUS\Digital Product Factory\products\ebook-clothing-brand")
TARGET_DIR.mkdir(parents=True, exist_ok=True)

# 1. Product Metadata
metadata = {
    "title": "Blueprint Membangun Clothing Brand Lokal: Dari Nol Sampai Rilis Koleksi Perdana",
    "author": "Digital Product Factory",
    "version": "1.0.0",
    "license": "CC0-1.0",
}
(TARGET_DIR / "product.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# 2. Comprehensive Book Markdown Content
book_markdown = """---
title: "Blueprint Membangun Clothing Brand Lokal"
subtitle: "Dari Nol Sampai Rilis Koleksi Perdana (Edisi Lengkap + SOP & Checklist)"
author: "Digital Product Factory"
lang: "id"
date: "2026-10-22"
---

# Bab 1: Fondasi Brand, Positioning & DNA Koleksi

Membangun clothing brand yang berumur panjang menuntut kejelasan identitas sejak hari pertama. Di Indonesia, lebih dari delapan puluh persen brand pakaian baru gulung tikar dalam waktu enam bulan pertama. Kegagalan tersebut hampir tidak pernah disebabkan oleh ketiadaan mesin sablon atau penjahit, melainkan oleh ketiadaan diferensiasi yang tajam: mereka menjual produk komoditas tanpa alasan emosional bagi pelanggan untuk memilihnya.

## Tiga Archetype Clothing Brand Kontemporer

Sebelum membeli satu kilogram kain pun, Anda wajib menetapkan di mana spektrum identitas produk Anda akan berpijak:

1. **Streetwear Kontemporer (Heavyweight & Graphic)**: Menekankan potongan boxy modern, bahu turun (drop shoulder), kain bergramasi berat (240–280 gsm), grafis artistik berkonsep, dan sensasi eksklusivitas melalui perilisan berkala dalam jumlah terbatas.
2. **Minimalist Basic Essentials (Lifestyle & Comfort)**: Menghilangkan grafis mencolok. Daya pikat bertumpu seratus persen pada kelembutan bahan katun premium (misalnya combed 24s combed compact atau cotton bamboo), potongan leher yang kokoh, dan kenyamanan pemakaian harian di iklim tropis.
3. **Pakaian Fungsional & Komuter (Utility & Techwear)**: Mengutamakan fungsi mobilitas, saku ergonomis, ketahanan bahan ripstop atau parasut tahan percikan air, serta fleksibilitas bagi pengguna komuter perkotaan.

## Menentukan Unique Selling Proposition (USP)

Pasar kaos oblong sablon di Indonesia sudah sangat jenuh. Untuk menonjol, kombinasikan dua elemen tak terduga yang menjadi ciri khas permanen:
- Contoh: Potongan boxy streetwear dengan eksplorasi motif tenun lokal yang disablon discharge.
- Contoh: Pakaian harian ultra-minimalis dengan garansi tukar baru jika kerah leher melar dalam 100 hari pemakaian.

> **PRO TIP FONDASI:** Jangan mendaftarkan nama brand sebelum memeriksa ketersediaan kelas 25 (Pakaian dan Tutup Kepala) pada Pangkalan Data Kekayaan Intelektual (PDKI). Menghabiskan modal pemasaran pada merek yang sudah memiliki hak paten pihak lain adalah kesalahan fatal yang sering terjadi.

### Checklist Tindakan Bab 1
- [ ] Tentukan satu dari tiga archetype brand utama di atas.
- [ ] Buat moodboard visual 9 gambar (estetika foto, warna dominan, gaya tipografi).
- [ ] Cek ketersediaan nama merek di PDKI dan ketersediaan username media sosial utama.

---

# Bab 2: Ensiklopedia Bahan Kain & Standar Gramasi Kaos

Pemilihan bahan adalah tujuh puluh persen penentu kepuasan pelanggan pakaian. Pelanggan mungkin membeli pertama kali karena melihat foto katalog di media sosial, namun mereka akan membeli kembali dan merekomendasikan brand Anda jika bahan terasa nyaman di kulit setelah dicuci berkali-kali.

## Klasifikasi Rajutan Cotton Combed

Rajutan katun combed diproduksi dengan menyisir serat kapas panjang sehingga menghasilkan permukaan yang rata dan minim bulu:

- **Cotton Combed 30s (140–150 gsm)**: Karakter ringan, sejuk, dan jatuh di badan. Sangat cocok untuk kaos kasual tipis harian di wilayah panas, namun kurang ideal untuk potongan boxy yang membutuhkan siluet kaku.
- **Cotton Combed 24s (175–185 gsm)**: Standar emas pasar distro Indonesia. Memiliki ketebalan seimbang yang tidak menerawang dan tidak membuat gerah. Pilihan paling aman untuk koleksi perdana.
- **Cotton Combed 20s (195–210 gsm)**: Lebih tebal dan padat. Memiliki ketahanan cuci tinggi dan memberikan kesan pakaian berkualitas kokoh.
- **Cotton Combed 16s / Heavyweight (230–260 gsm)**: Sangat tebal, padat, dan kaku. Karakter ini menahan bentuk potongan boxy dan oversized agar tidak jatuh lemas di badan pemakai.

## Bahan Outerwear & Celana

- **Cotton Fleece 330 gsm**: Pilihan utama untuk hoodie dan crewneck premium. Bagian dalam berbulu lembut dan hangat, bagian luar halus untuk media sablon atau bordir.
- **French Terry 280–300 gsm**: Bagian dalam bermotif rajutan melingkar (loop), lebih adem dibanding fleece, sangat cocok untuk iklim Indonesia.
- **Baby Canvas Twill & Ripstop**: Bahan pilihan untuk kemeja pekerja (overshirt) dan celana kargo karena ketahanan gesek dan struktur tenun silang yang kuat.

## Tabel Komparasi Karakteristik Bahan Pakaian

| Nama Bahan | Gramasi Rata-rata | Karakter Handfeel | Ketahanan Cuci | Penggunaan Terbaik |
| :--- | :--- | :--- | :--- | :--- |
| Combed 30s | 140–150 gsm | Lembut, tipis, jatuh | Sedang | Kaos santai harian |
| Combed 24s | 175–185 gsm | Seimbang, padat | Sangat Baik | Kaos standar distro |
| Combed 16s | 230–260 gsm | Tebal, kaku, kokoh | Unggul | Kaos Boxy / Oversized |
| Cotton Bamboo | 150–160 gsm | Sangat lembut, dingin | Baik | Premium basic wear |
| Cotton Fleece | 320–350 gsm | Tebal, bagian dalam bulu | Sangat Baik | Pullover Hoodie / Crewneck |
| Baby Canvas | 240–280 gsm | Bertekstur, kuat | Unggul | Worker Overshirt / Jaket |

## Rahasia Mengatasi Penyusutan Kain (Shrinkage)

Semua serat katun alami pasti mengalami penyusutan antara 2% hingga 4% setelah pencucian pertama kali. Jika Anda membuat kaos berukuran panjang 72 cm, setelah dicuci panjangnya bisa menyusut menjadi 70 cm. 

**Solusi Teknis:** Selalu tambahkan panjang pola sebesar 1,5 hingga 2 cm pada pola potong mentah (potong lebih panjang), atau lakukan proses cuci awal (pre-washed / garment wash) sebelum produk dikemas ke plastik penjualan.

### Checklist Tindakan Bab 2
- [ ] Beli katalog swatch kain asli (handfeel book) dari toko bahan terpercaya.
- [ ] Tentukan kombinasi bahan untuk koleksi perdana (contoh: 2 model Combed 16s, 2 model Combed 24s).
- [ ] Lakukan uji cuci dan ukur penyusutan pada sampel kain sebelum membeli gulungan besar.

---

# Bab 3: Pembuatan Pola Potong & Tech-Pack Konveksi

Bekerja sama dengan konveksi atau pabrik penjahit membutuhkan bahasa instruksi yang baku. Mayoritas miskomunikasi produksi terjadi karena pemilik brand hanya mengirimkan foto dari internet dengan instruksi informal seperti "tolong buatkan seperti ini tapi agak longgar".

## Tiga Siluet Pola Kaos Utama

1. **Regular Fit**: Potongan lurus standar tubuh, sambungan jahitan bahu pas di ujung tulang pundak, lengan jatuh di tengah lengan atas.
2. **Boxy Fit**: Lebar badan dilebarkan (5–8 cm lebih lebar dari regular), jahitan bahu diturunkan (drop shoulder), namun panjang badan dipotong sedikit lebih pendek agar tidak terlihat gombrang ke bawah.
3. **Oversized Fit**: Seluruh dimensi diperbesar secara proporsional: lebar badan, panjang badan, dan panjang lengan hingga mendekati siku.

## Standar Size Chart Brand Dewasa (Toleransi Garment)

Tentukan panduan ukuran resmi Anda sendiri dalam satuan sentimeter. Cantumkan selalu toleransi jahit sebesar ±1 cm:

- **Size S**: Lebar Dada 50 cm | Panjang Badan 68 cm | Panjang Lengan 21 cm
- **Size M**: Lebar Dada 53 cm | Panjang Badan 71 cm | Panjang Lengan 22 cm
- **Size L**: Lebar Dada 56 cm | Panjang Badan 74 cm | Panjang Lengan 24 cm
- **Size XL**: Lebar Dada 60 cm | Panjang Badan 77 cm | Panjang Lengan 25 cm
- **Size XXL**: Lebar Dada 64 cm | Panjang Badan 80 cm | Panjang Lengan 26 cm

## Lembar Kerja Teknis (Tech-Pack) Sederhana

Tech-pack adalah cetak biru satu lembar yang Anda serahkan ke tukang jahit:
- **Tampilan Depan & Belakang**: Sketsa garis hitam-putih posisi sablon, label, dan saku.
- **Spesifikasi Jahit**: Wajib memakai jahit rantai pada pundak, bis leher selebar 1,5 cm dengan bahan rib katun ber-spandex agar tidak mudah melar, serta overdeck tiga jarum pada ujung kelim bawah dan lengan.
- **Daftar Ukuran Lengkap**: Tabel ukuran untuk setiap size yang dipesan.

> **ATURAN PROTOKOL PRODUKSI:** Jangan pernah melakukan produksi massal tanpa membuat proto-sample dan fitting langsung pada tubuh manusia asli. Biaya membuat sample adalah investasi wajib untuk mencegah ratusan potong baju gagal bentuk.

### Checklist Tindakan Bab 3
- [ ] Buat lembar size chart resmi brand Anda.
- [ ] Siapkan dokumen tech-pack 1 lembar untuk setiap artikel yang akan diproduksi.
- [ ] Pesan satu helai sample jahit per model dan uji kenyamanan potongannya.

---

# Bab 4: Teknik Sablon, Bordir & Kualitas Cetak Grafis

Desain yang luar biasa di layar monitor komputer bisa terlihat murahan jika dieksekusi dengan teknik cetak yang salah di atas kain. Kenali karakter kimia dan fisik setiap metode sablon sebelum menentukan jenis cetak.

## Komparasi Metode Sablon Layak Jual

1. **Plastisol Doff (Screenprint)**:
   - *Karakter*: Menggunakan tinta berbasis minyak (PVC) yang dipanaskan pada suhu 160°C. Warna sangat tajam, menutup rapat di atas kain hitam, dan awet bertahun-tahun.
   - *Kelemahan*: Area cetak yang terlalu besar akan terasa tebal dan kaku di dada (efek papan). Tidak boleh disetrika langsung.
2. **Discharge / Cabut Warna**:
   - *Karakter*: Tinta kimia yang membakar warna asli kain katun dan menggantikannya dengan pigmen baru.
   - *Keunggulan Mutlak*: Hasil cetakan menyatu dengan serat kain (zero handfeel), sirkulasi udara tetap lancar dan sangat nyaman dipakai di iklim panas. Hanya bisa bekerja pada katun murni 100% dengan pewarna reaktif.
3. **High Density (HD 3D)**:
   - *Karakter*: Sablon timbul berbentuk balok tegas dengan sudut presisi 90 derajat. Memberikan kesan mewah pada tipografi atau logo kecil di dada.
4. **Direct to Film (DTF)**:
   - *Karakter*: Cetak digital ke lembaran film transfer lalu dipres dengan lem serbuk panas.
   - *Penggunaan*: Sangat efektif untuk desain warna-warni bergradasi tinggi dan kuantiti kecil di bawah 24 pcs. Kurang disarankan untuk grafis berukuran besar karena terasa seperti plastik kedap udara.
5. **Bordir Komputer**:
   - *Penggunaan*: Paling direkomendasikan untuk hoodie, jaket, dan polo shirt. Menghadirkan tekstur benang tiga dimensi yang tahan cuci seumur hidup pakaian.

## Uji Ketahanan Sablon (The 5-Wash Test)

Sebelum menyetujui hasil produksi massal dari vendor sablon, lakukan tes mandiri pada pakaian sampel:
- Cuci menggunakan mesin cuci selama 5 siklus berturut-turut.
- Lakukan peregangan manual pada area bergambar. Tinta sablon yang matang sempurna tidak boleh retak, rontok, ataupun luntur ke bagian kain putih.

### Checklist Tindakan Bab 4
- [ ] Tentukan teknik cetak yang tepat untuk tiap desain (grafis besar: Discharge; logo dada kecil: HD / Bordir).
- [ ] Siapkan file grafis berformat vektor (AI / CDR / PDF) atau bitmap resolusi minimal 300 DPI ukuran asli.
- [ ] Lakukan tes cuci dan tarik pada sample sablon pertama.

---

# Bab 5: Trims, Label & Pengalaman Unboxing Premium

Perbedaan paling mencolok antara kaos murah tanpa merek dengan produk clothing brand bernilai tinggi terletak pada perhatian terhadap detail pelengkap (trims) dan kemasan. Pelanggan merasakan sensasi nilai harga sejak mereka menerima paket dari kurir.

## Aksesoris Wajib Pakaian Berkelas

1. **Main Woven Label (Label Leher)**:
   - Gunakan jenis rajutan Damask High Density dengan kerapatan benang tinggi.
   - Tepi label wajib dipotong menggunakan laser (ultrasonic cut) agar lembut dan tidak menusuk atau membuat gatal kulit leher pelanggan.
2. **Washing Care Label (Label Samping)**:
   - Letakkan di bagian pinggang dalam kiri. Menggunakan bahan satin lembut yang memuat instruksi cara merawat pakaian, komposisi bahan (misal 100% Cotton), dan buatan negara.
3. **Hangtag & Tali Pengikat**:
   - Bahan kertas tebal (Art Carton atau Ivory 350–400 gsm) dengan laminasi doff halus.
   - Sambungkan hangtag ke baju menggunakan tali loop atau peniti labu hitam (bulb pin) di label leher. Jangan menusuk badan kain utama karena dapat merusak rajutan benang.

## Standar Kemasan Penjualan D2C

- **Kemasan Primer**: Plastik ziplock frosted (semi-buram tebal) yang dicetak sablon logo brand Anda. Plastik ini menjaga pakaian tetap higienis dan sering disimpan oleh pelanggan untuk kantong bepergian.
- **Kartu Apresiasi (Thank You Card)**: Kartu ucapan terima kasih dengan pesan personal, kontak layanan pelanggan, dan tautan garansi penukaran ukuran jika baju tidak muat.
- **Stiker Promosi (Bonus Item)**: Sertakan 2 hingga 3 stiker vinyl tahan air berkualitas tinggi. Pelanggan muda senang menempelkan stiker brand pakaian di laptop atau helm mereka, menjadi media promosi gratis yang efektif.
- **Kemasan Pengiriman**: Amplop polymailer plastik berperekat kuat anti-robek dan anti-air untuk melindungi isi paket dari hujan selama proses pengantaran ekspedisi.

### Checklist Tindakan Bab 5
- [ ] Pesan woven label leher damask dan washing tag satin sesuai standar.
- [ ] Rancang desain hangtag dan kartu terima kasih berdimensi proporsional.
- [ ] Siapkan kemasan ziplock frosted dan amplop kurir polymailer.

---

# Bab 6: SOP Quality Control (QC) & Manajemen Vendor

Manajemen produksi yang baik adalah sistem mitigasi risiko. Anda tidak boleh mengasumsikan bahwa konveksi akan memeriksa setiap helai baju dengan teliti sebelum mengirimkannya ke Anda. Pemeriksaan mutu akhir adalah tanggung jawab mutlak pemilik brand.

## Prosedur QC 10 Titik Pemeriksaan Fisik

Lakukan pemeriksaan meja pada setiap helai pakaian sebelum dimasukkan ke dalam plastik ziplock:

1. **Kebersihan Sisa Benang**: Gunting seluruh sisa benang jahit yang menjuntai di ujung lengan, kelim bawah, dan kerah.
2. **Kerapian Kerah**: Pastikan kerah bulat simetris, tidak bergelombang (efek keriting), dan jahitan bis rapi rata.
3. **Pemeriksaan Cacat Kain**: Periksa apakah ada benang putus, serat bergaris, atau bolong jarum pada kain.
4. **Noda Minyak & Tinta**: Pastikan kain bersih dari cipratan oli mesin jahit konveksi dan noda tinta sablon.
5. **Kekuatan Jahitan Pundak & Ketiak**: Tarik perlahan sambungan ketiak untuk memastikan tidak ada jahitan yang melompat (skip stitch).
6. **Ketepatan Posisi Sablon**: Ukur jarak sablon dari kerah leher (standar 5–7 cm ke bawah) dan pastikan gambar tidak miring.
7. **Kelengkapan Label**: Pastikan woven label dan washing tag terpasang dengan arah dan ukuran yang benar.
8. **Pengukuran Sampel Ukuran**: Ambil acak satu helai per size dan ukur lebarnya terhadap panduan size chart resmi.
9. **Penyetrikaan Uap (Steam Ironing)**: Setrika seluruh pakaian hingga lipatan rapi dan uap panas mematikan kerutan kain.
10. **Pemasangan Hangtag & Pelipatan Presisi**: Pasang hangtag dan lipat baju dengan ukuran seragam mengikuti papan lipat.

## Menghadapi Cacat Produksi (Defect Rate)

Dalam industri garmen skala kecil dan menengah, tingkat kecacatan wajar berkisar antara 2% hingga 4%. Buat kesepakatan tertulis di awal dengan vendor konveksi: setiap cacat mayor (bolong kain, sablon pecah parah, ukuran meleset lebih dari toleransi 2 cm) wajib diperbaiki atau dipotong dari sisa pembayaran tagihan akhir.

### Checklist Tindakan Bab 6
- [ ] Cetak lembar formulir QC periksa meja untuk tim kerja Anda.
- [ ] Siapkan gunting benang kecil dan setrika uap.
- [ ] Sepakati batas toleransi cacat dan garansi retur dengan pihak vendor konveksi.

---

# Bab 7: Strategi Peluncuran 'The Drop Method' & Funnel Penjualan

Membuat produk yang bagus hanyalah setengah dari pertempuran. Setengah lainnya adalah memastikan produk tersebut habis terjual dengan margin keuntungan yang sehat. Strategi peluncuran modern tidak lagi menunggu pelanggan datang perlahan, melainkan memusatkan seluruh daya tarik penjualan dalam satu momen pembukaan rilis (metode drop).

## Kalender Peluncuran 4 Minggu

- **Minggu ke-1 (Riset & Teaser Awal)**: Mulai perkenalkan konsep koleksi baru melalui dokumentasi proses: potongan kain, pemilihan palet warna, dan inspirasi desain tanpa memperlihatkan produk utuh.
- **Minggu ke-2 (Seeding Influencer)**: Kirimkan paket koleksi perdana kepada 5–10 kreator mikro yang memiliki gaya berpakaian relevan. Minta mereka memakai baju tersebut dalam aktivitas alami mereka tanpa naskah iklan yang kaku.
- **Minggu ke-3 (Rilis Lookbook Resmi)**: Rilis foto katalog dan lookbook sinematik. Umumkan tanggal dan jam rilis secara tegas, serta tegaskan batas kuantiti stok yang diproduksi untuk menciptakan urgensi yang sehat.
- **Minggu ke-4 (Hari-H Peluncuran)**: Buka penjualan tepat waktu di saluran utama (website atau marketplace resmi). Jalankan kampanye iklan berbayar terarah yang menargetkan audiens yang telah berinteraksi dengan teaser Anda.

## Ekosistem Saluran Penjualan

1. **Marketplace (Shopee / Tokopedia / TikTok Shop)**: Memanfaatkan kemudahan pembayaran dan subsidi gratis ongkos kirim untuk menjaring pelanggan pertama yang belum percaya penuh pada merek baru.
2. **Website Mandiri / Link Toko Digital**: Menjadi rumah jangka panjang brand di mana Anda memegang data kontak pelanggan (email dan nomor WhatsApp) untuk kampanye penjualan koleksi berikutnya tanpa bergantung pada algoritma pihak ketiga.

> **KUNCI RETENSI:** Biaya mendapatkan pelanggan baru lima kali lebih mahal daripada mempertahankan pelanggan yang sudah ada. Berikan pengalaman unboxing yang memukau dan tanggapi setiap keluhan penukaran ukuran dengan cepat dan ramah.

### Checklist Tindakan Bab 7
- [ ] Jadwalkan kalender konten 4 minggu pra-peluncuran.
- [ ] Siapkan daftar 10 micro-influencer target untuk seeding koleksi.
- [ ] Pastikan link toko, metode pembayaran, dan stok inventori siap sebelum jam rilis tiba.

---

# Lampiran: Formulir Pemeriksaan Quality Control (QC Sheet)

Gunakan tabel checklist di bawah ini untuk memeriksa setiap helai pakaian sebelum dikirim ke pelanggan:

| No. Batch | Model Pakaian | Ukuran | Status Jahit | Status Sablon | Kebersihan Kain | Status Trims | Keputusan QC (Pass/Reject) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B01-001 | Boxy Heavy Tee | S | [ ] OK | [ ] OK | [ ] OK | [ ] OK | [ ] LULUS |
| B01-002 | Boxy Heavy Tee | M | [ ] OK | [ ] OK | [ ] OK | [ ] OK | [ ] LULUS |
| B01-003 | Boxy Heavy Tee | L | [ ] OK | [ ] OK | [ ] OK | [ ] OK | [ ] LULUS |
| B01-004 | Boxy Heavy Tee | XL | [ ] OK | [ ] OK | [ ] OK | [ ] OK | [ ] LULUS |
| B01-005 | Pullover Hoodie | L | [ ] OK | [ ] OK | [ ] OK | [ ] OK | [ ] LULUS |

---
*Blueprint Membangun Clothing Brand Lokal v1.0.0 — Diterbitkan oleh Digital Product Factory untuk para perintis dan pelaku bisnis fesyen independen Indonesia.*
"""

md_path = TARGET_DIR / "source.md"
md_path.write_text(book_markdown, encoding="utf-8")
print(f"File sumber Markdown ditulis: {md_path} ({len(book_markdown):,} karakter)")

# 3. Build EPUB 3 via Pandoc
epub_path = TARGET_DIR / "book.epub"
cmd_epub = [
    "pandoc",
    str(md_path),
    "-o",
    str(epub_path),
    "--toc",
    "--toc-depth=2",
    "--epub-chapter-level=1",
]
res_ep = subprocess.run(cmd_epub, capture_output=True, text=True)
if res_ep.returncode != 0:
    print("Error Pandoc EPUB:", res_ep.stderr)
    raise RuntimeError("Pandoc EPUB compilation failed")
print(f"EPUB berhasil dikompilasi di: {epub_path} ({epub_path.stat().st_size:,} bytes)")

# Verify EPUB with EPUBCheck
epubcheck = tool_path("epubcheck")
java = java_path()
chk_res = subprocess.run([java, "-jar", epubcheck, str(epub_path)], capture_output=True, text=True)
print(f"EPUBCheck Status: {'LULUS' if chk_res.returncode == 0 else 'GAGAL'}")
assert chk_res.returncode == 0, f"EPUBCheck gagal: {chk_res.stdout}"

# 4. Build High-End Editorial HTML for PDF Rendering
# High-end typographic CSS for LibreOffice PDF
editorial_css = """
@page {
    size: A4 portrait;
    margin: 24mm 20mm 24mm 20mm;
}
body {
    font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
    color: #1e293b;
    line-height: 1.65;
    font-size: 10.5pt;
    margin: 0;
    padding: 0;
}
.cover-page {
    page-break-after: always;
    background-color: #0f172a;
    color: #ffffff;
    padding: 100px 30px 80px 30px;
    text-align: center;
    border-radius: 4px;
}
.cover-tag {
    display: inline-block;
    background-color: #38bdf8;
    color: #0f172a;
    font-size: 10pt;
    font-weight: bold;
    letter-spacing: 2px;
    padding: 6px 16px;
    border-radius: 20px;
    margin-bottom: 24px;
    text-transform: uppercase;
}
.cover-title {
    font-size: 28pt;
    font-weight: 800;
    line-height: 1.25;
    color: #ffffff;
    margin: 16px 0;
    letter-spacing: -0.5px;
}
.cover-subtitle {
    font-size: 12pt;
    color: #94a3b8;
    max-width: 600px;
    margin: 0 auto 40px auto;
    line-height: 1.5;
}
.cover-meta {
    border-top: 1px solid #334155;
    padding-top: 24px;
    margin-top: 60px;
    font-size: 10pt;
    color: #64748b;
}
h1 {
    page-break-before: always;
    font-size: 19pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 2.5px solid #0284c7;
    padding-bottom: 10px;
    margin-top: 20px;
    margin-bottom: 20px;
}
h2 {
    font-size: 13pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 26px;
    margin-bottom: 10px;
    border-left: 4px solid #38bdf8;
    padding-left: 10px;
}
p {
    margin-bottom: 14px;
    text-align: justify;
}
ul, ol {
    margin-top: 6px;
    margin-bottom: 16px;
    padding-left: 24px;
}
li {
    margin-bottom: 6px;
}
blockquote {
    background-color: #f0f9ff;
    border-left: 4px solid #0284c7;
    padding: 14px 18px;
    margin: 20px 0;
    font-style: normal;
    color: #0369a1;
    border-radius: 0 4px 4px 0;
}
blockquote p {
    margin: 0;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 22px 0;
    font-size: 9.5pt;
}
th {
    background-color: #0f172a;
    color: #ffffff;
    font-weight: bold;
    text-align: left;
    padding: 9px 12px;
    border: 1px solid #0f172a;
}
td {
    padding: 8px 12px;
    border: 1px solid #cbd5e1;
    color: #334155;
}
tr:nth-child(even) td {
    background-color: #f8fafc;
}
hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 32px 0;
}
"""

# Convert markdown body to html via pandoc
cmd_html = ["pandoc", str(md_path), "-t", "html"]
raw_html_body = subprocess.run(cmd_html, capture_output=True, text=True, check=True).stdout

# Build complete standalone HTML
cover_html = """
<div class="cover-page">
    <div class="cover-tag">PLAYBOOK RESMI EDISI 2026</div>
    <div class="cover-title">BLUEPRINT MEMBANGUN<br>CLOTHING BRAND LOKAL</div>
    <div class="cover-subtitle">Panduan Operasional Lengkap: Riset Bahan, Standardisasi Pola, Tech-Pack, Quality Control, hingga Strategi Peluncuran Koleksi Perdana</div>
    <div class="cover-meta">
        Diterbitkan oleh <strong>Digital Product Factory</strong> &bull; Edisi Lengkap + SOP & Checklist Siap Cetak
    </div>
</div>
"""

full_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<title>Blueprint Membangun Clothing Brand Lokal</title>
<style>{editorial_css}</style>
</head>
<body>
{cover_html}
{raw_html_body}
</body>
</html>
"""

html_path = TARGET_DIR / "book_source.html"
html_path.write_text(full_html, encoding="utf-8")

# Convert HTML to PDF via LibreOffice
soffice = tool_path("soffice")
pdf_path = TARGET_DIR / "book.pdf"
conv_cmd = [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(TARGET_DIR), str(html_path)]
subprocess.run(conv_cmd, check=True)

# LibreOffice outputs book_source.pdf
tmp_pdf = TARGET_DIR / "book_source.pdf"
if tmp_pdf.is_file():
    tmp_pdf.replace(pdf_path)

# Clean intermediate HTML
if html_path.is_file():
    html_path.unlink()

print(f"PDF berhasil dikompilasi di: {pdf_path} ({pdf_path.stat().st_size:,} bytes)")

# 5. Run QA Check
report = check_product(TARGET_DIR, "ebook")
print("\n=== HASIL QA CHECK EBOOK ===")
print("Exit Code:", report.exit_code)
for f in report.findings:
    print(f"[{f.status.upper()}] {f.id}: {f.message}")

assert report.exit_code == 0, "QA Check Ebook Gagal!"
print("\nSTATUS EBOOK: 100% PASS - SIAP JUAL!")
