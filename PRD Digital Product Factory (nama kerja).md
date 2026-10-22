# PRD: Digital Product Factory (nama kerja)

Draf 0.1 · 20 Oktober 2026 · Status: untuk ditinjau · Rencana lisensi: MIT

## 1. Ringkasan

Digital Product Factory adalah repo open source berisi skill (instruksi + skrip kecil) untuk AI agent seperti Claude Code, Codex CLI, dan Cursor. Setelah dipasang dengan satu perintah, agent bisa membuat produk digital (ebook, paket prompt, template spreadsheet) dan **memeriksa sendiri apakah hasilnya benar-benar berfungsi** lewat Product QA Gate sebelum menyerahkannya kepada pengguna.

Proyek ini dirilis dengan model hybrid: inti dan README global (Inggris), paket bahasa Indonesia sebagai paket pertama, dan terbuka untuk paket bahasa lain dari kontributor.

Janji satu kalimat (usulan): “Buat agent AI-mu membuat produk digital yang benar-benar jalan, dan buktikan.”

## 2. Latar belakang dan masalah

- Skill untuk agent sedang tumbuh cepat. Repo skill terbesar menunjukkan minat yang sangat besar dari developer.
- Produk digital buatan AI sering asal jadi: file rusak, sisa placeholder, klaim tanpa sumber, rumus spreadsheet yang error, prompt yang tidak pernah diuji.
- Dari pengamatan awal, skill yang ada kebanyakan menyuruh agent *membuat* sesuatu tanpa memeriksa hasilnya. Alat pemeriksa yang ada (linter dan uji pemicu) memeriksa *file skill*, bukan *produk yang dihasilkan*.
- Celah yang dituju: pemeriksaan otomatis atas hasil produk, dengan prinsip bahwa setiap produk harus punya fungsi nyata dan bisa dipakai.

## 3. Tujuan dan non-tujuan

**Tujuan v0.1**

1. Menyediakan tiga skill pembuat produk (ebook, paket prompt, template xlsx) dan satu skill pemeriksa (product-qa).
2. Setiap produk wajib melewati QA Gate. Kegagalan tingkat blocker mencegah agent menyerahkan hasil sebagai “selesai”.
3. Instalasi dari nol dalam kurang dari 5 menit dengan satu perintah.
4. Fondasi komunitas: menambah paket bahasa baru mudah dan terdokumentasi.
5. Siap publik: lolos tujuh lapis pengujian (bagian 10).

**Non-tujuan v0.1**

- Bukan aplikasi, website, atau SaaS. Isinya terutama markdown dan skrip kecil.
- Bukan linter SKILL.md. Alat itu sudah ada; kita memakainya di CI, bukan membangun ulang.
- Tidak menjual atau menjamin penjualan produk.
- Tidak mendukung Notion atau format yang tidak bisa diverifikasi offline.
- Tidak mencakup domain regulasi (pajak, hukum, kesehatan) pada v0.1.
- Bukan marketplace skill.

## 4. Pengguna sasaran

| Persona | Kebutuhan | Cara memakai |
| --- | --- | --- |
| Kreator produk digital | Menghasilkan ebook, prompt pack, dan template yang rapi dan bisa dijual atau dibagikan | Memasang skill, memberi brief ke agent, menerima produk yang sudah lolos QA |
| Developer atau builder indie | Alur kerja agent yang terstruktur dan bisa dipercaya untuk produk non-kode | Memasang, memodifikasi skill, menjalankan QA Gate di CI |
| Kontributor lokal | Menambah paket bahasa dan gaya tulis untuk negaranya | Fork, salin template paket bahasa, kirim PR |

## 5. Cerita pengguna utama

- Sebagai kreator, saya ingin mengetik “buatkan ebook panduan X” dan menerima file EPUB/PDF yang sudah valid, sehingga tidak perlu memeriksa manual.
- Sebagai kreator, saya ingin laporan yang jelas tentang apa yang gagal dan kenapa, supaya saya percaya pada hasilnya.
- Sebagai developer, saya ingin menjalankan QA Gate dari terminal atau CI dengan kode keluar yang jelas.
- Sebagai kontributor, saya ingin menambah paket bahasa tanpa menyentuh inti skill.
- Sebagai pengguna baru, saya ingin memasang dengan satu perintah dan melihat hasil pertama dalam beberapa menit.

## 6. Persyaratan fungsional

| ID | Kebutuhan | Prioritas |
| --- | --- | --- |
| FR-1 | Skill `product-qa`: menjalankan pemeriksaan per jenis produk dan menghasilkan laporan (JSON + ringkasan terbaca manusia) | P0 |
| FR-2 | Skill `ebook-builder`: brief, outline, naskah, build ke EPUB dan PDF, lalu wajib lewat QA Gate | P0 |
| FR-3 | Skill `prompt-pack-builder`: paket prompt terstruktur (markdown + JSON), variabel terdeklarasi, contoh input dan output | P0 |
| FR-4 | Skill `template-builder` untuk spreadsheet xlsx dengan sheet petunjuk dan data contoh | P0 |
| FR-5 | Paket bahasa `id` dan `en` (gaya tulis, istilah, format tanggal dan mata uang) terpisah dari inti | P0 |
| FR-6 | Instalasi satu perintah (`npx skills add`) dan kepatuhan pada spesifikasi Agent Skills | P0 |
| FR-7 | Tiga produk contoh jadi di `examples/`, masing-masing lolos QA Gate | P0 |
| FR-8 | CI: `skills-ref validate`, satu linter SKILL.md yang sudah ada, dan tes fungsional | P0 |
| FR-9 | Dukungan template docx | P1 |
| FR-10 | Mode `--live` untuk menguji prompt di beberapa model memakai kunci API milik pengguna sendiri | P1 |
| FR-11 | Perintah `doctor` untuk memeriksa lingkungan (versi Python, alat pendukung) | P1 |
| FR-12 | CONTRIBUTING, template paket bahasa, dan issue pelacak “paket dicari” | P1 |
| FR-13 | Pembungkus MCP untuk QA Gate | P2 |
| FR-14 | Dukungan Notion atau Google Sheets | P2 |

## 7. Spesifikasi Product QA Gate

**Perilaku.** Setelah agent membuat produk, skill menginstruksikan agent menjalankan gate. Jika ada temuan blocker, agent memperbaiki dan menjalankan ulang, maksimal tiga iterasi. Jika masih gagal, agent harus melaporkan sisa masalah dengan jujur dan tidak menyatakan produk “selesai”.

**Keluaran.** Laporan JSON (per pemeriksaan: id, status, tingkat, pesan) dan ringkasan terbaca manusia. Kode keluar 0 jika tidak ada blocker, 1 jika ada.

**Pemeriksaan universal**

| Pemeriksaan | Tingkat |
| --- | --- |
| Tidak ada sisa placeholder (TODO, lorem, `{{...}}`, \[ISI\]) | Blocker |
| File utuh dan bisa dibuka | Blocker |
| Metadata lengkap (judul, penulis, versi, lisensi) | Warning |
| Klaim faktual atau berangka punya sumber | Warning (Blocker untuk domain terbatas) |
| Bahasa sesuai paket bahasa yang dipilih | Warning |
| Aset dan kutipan memiliki lisensi atau atribusi | Warning |

**Ebook**

- Build EPUB dan PDF tanpa error; EPUB lolos validator EPUB (mis. EPUBCheck) (Blocker).
- Daftar isi dan tautan internal berfungsi (Blocker).
- Hierarki heading benar (Warning).
- Panjang sesuai brief dengan toleransi sekitar 20% (Warning).

**Paket prompt**

- Struktur valid dan setiap prompt punya contoh input dan output (Blocker).
- Semua variabel dideklarasikan dan dipakai; tidak ada variabel menggantung (Blocker).
- Opsional `--live`: tiap prompt dijalankan pada minimal dua model dengan tiga input contoh dan dinilai dengan rubrik (Warning).

**Template xlsx**

- Tidak ada error rumus (#REF!, #NAME?, #DIV/0!) (Blocker).
- Sel input ditandai jelas, ada sheet petunjuk, ada data contoh (Warning).

## 8. Persyaratan non-fungsional

- **Kepatuhan spesifikasi Agent Skills:** nama skill maksimal 64 karakter, deskripsi maksimal 1024 karakter, SKILL.md di bawah 500 baris, instruksi sebaiknya di bawah sekitar 5000 token, referensi file satu tingkat dari SKILL.md.
- **Portabilitas:** macOS, Linux, dan Windows. Skrip memakai Python 3.10+ dengan dependensi minimal (keputusan final di bagian 16).
- **Keamanan:** tidak ada rahasia di repo, tidak ada perintah destruktif, tidak ada akses jaringan secara default, dependensi dipin ke versi tertentu, izin alat dibuat minimal, ada SECURITY.md dan jalur pelaporan kerentanan.
- **Privasi:** konten pengguna tidak dikirim ke mana pun. Mode `--live` memakai kunci API milik pengguna dan tidak menyimpannya.
- **Lisensi:** MIT untuk kode. Aset contoh memakai lisensi yang jelas.
- **i18n:** paket bahasa terpisah di `packs/`; README tersedia dalam Inggris dan Indonesia.
- **Keandalan:** hasil QA Gate harus deterministik untuk input yang sama pada pemeriksaan non-live.

## 9. Arsitektur dan struktur repo

```
digital-product-factory/
  skills/
    product-qa/            # pemeriksa hasil (pembeda utama)
      SKILL.md
      scripts/
    ebook-builder/
    prompt-pack-builder/
    template-builder/
  packs/
    id/  en/               # gaya tulis dan istilah per bahasa
  examples/                # 3 produk jadi sebagai bukti
  tests/                   # set uji pemicu dan fungsional
  README.md  README.id.md
  CONTRIBUTING.md  SECURITY.md  LICENSE
```

**Alur kerja agent**

1. Pengguna memberi brief produk.
2. Agent memilih skill pembuat yang sesuai (pemicu dari deskripsi skill).
3. Skill memakai paket bahasa yang dipilih.
4. Agent membuat produk.
5. Agent menjalankan `product-qa`.
6. Jika ada blocker, agent memperbaiki lalu mengulang (maksimal 3 kali).
7. Agent menyerahkan produk beserta laporan QA.

## 10. Strategi pengujian dan gerbang rilis

| Lapis | Yang diuji | Lulus jika |
| --- | --- | --- |
| 1. Format | `skills-ref validate` dan satu linter yang sudah ada, di CI | 0 error |
| 2. Pemicu | Per skill: 10 prompt yang harus memicu dan 10 yang tidak, di minimal 2 agent | Minimal 90% benar |
| 3. Hasil fungsional | Pemeriksaan QA per jenis produk | Semua lolos pada 3 produk contoh |
| 4. Nilai tambah | Tugas sama dengan dan tanpa skill, dinilai buta | Skill menang di mayoritas; jika tidak, perbaiki atau buang |
| 5. Instalasi bersih | VM atau mesin baru, `npx skills add`, tiap agent dan OS | Hasil pertama kurang dari 5 menit |
| 6. Keamanan | Rahasia, perintah destruktif, jaringan tak perlu, dependensi | 0 temuan |
| 7. Beta manusia | 3 sampai 5 orang tanpa bantuan | Minimal 3 dari 5 mencapai tujuannya |

**Gerbang rilis v0.1.0:** lapis 1 sampai 6 lulus, tiga produk contoh lolos QA Gate, dan beta manusia memenuhi ambang. Jika ada yang gagal, rilis ditunda.

## 11. Distribusi dan peluncuran

**Kelengkapan sebelum publik**

- README Inggris: satu kalimat janji, GIF sekitar 10 detik, instal satu baris, contoh output, dan bagian “kenapa bukan X”.
- README.id, LICENSE, CONTRIBUTING (termasuk cara menambah paket bahasa), SECURITY.md, badge CI, topics, dan gambar pratinjau sosial.
- Tiga produk contoh sebagai bukti, rilis v0.1.0 dengan changelog.
- Pemberitahuan di README untuk mengunduh hanya dari repo resmi.

**Peluncuran**

- Mulai membangun audiens 1 sampai 2 minggu sebelumnya dengan membagikan proses pembuatan.
- Hari peluncuran: X, Reddit, dan Hacker News untuk jangkauan global; grup developer dan komunitas lokal untuk Indonesia.
- Balas issue dan PR dalam 24 jam. Rilis versi kecil secara rutin untuk menunjukkan proyek aktif.
- Evaluasi pada hari ke-14.

## 12. Metrik keberhasilan

Target berikut adalah hipotesis awal, bukan prediksi. Revisi setelah evaluasi hari ke-14.

| Metrik | Hari ke-14 | Hari ke-90 |
| --- | --- | --- |
| Stars | 300 (stretch: 1.000+) | 1.000 |
| Fork | 30 | 100 |
| Issue atau PR dari non-pembuat | 5 | 20 |
| Paket bahasa dari kontributor luar | 0 | 1 atau lebih |
| Lolos QA pada produk contoh dan produk pengguna | 100% contoh | Laporan kegagalan umum terdokumentasi |

Stars bukan satu-satunya ukuran. Fork, issue dari pengguna, dan kontribusi paket bahasa menunjukkan repo benar-benar dipakai. Sebagai pembanding, repo Indonesia-only yang ditemukan dalam riset awal berada di kisaran ratusan stars, sedangkan repo global yang viral bisa mencapai puluhan hingga ratusan ribu, sering karena audiens pembuatnya yang sudah ada.

## 13. Risiko dan mitigasi

| Risiko | Dampak | Mitigasi |
| --- | --- | --- |
| Kategori skill sudah ramai | Tenggelam | Fokus pada pembeda: QA hasil produk, bukan file skill |
| Konten buatan agent keliru atau mengarang | Produk menyesatkan | Klaim faktual wajib bersumber, ada pemeriksaan sumber, domain regulasi di luar lingkup v0.1 |
| Pelanggaran hak cipta pada konten atau aset | Masalah hukum | Instruksi konten orisinal, atribusi dan lisensi aset diperiksa |
| Skrip berjalan di mesin pengguna | Risiko keamanan | Izin minimal, tanpa jaringan default, dependensi dipin, tinjauan keamanan |
| Salinan palsu atau trojan setelah populer | Pengguna terkena malware | Saluran resmi tegas di README, rilis bertanda tangan atau checksum |
| Tidak punya audiens awal | Peluncuran sepi | Bangun audiens sebelum rilis, ekspektasi realistis |
| Cakupan membengkak | Terlambat rilis | v0.1 dibatasi tiga jenis produk |
| Spesifikasi Agent Skills berubah | Skill rusak | CI memakai validator resmi dan dipantau berkala |
| Beban pemeliharaan | Proyek mandek | Panduan kontribusi jelas, cakupan dijaga ketat |

## 14. Lanskap pesaing dan diferensiasi

- **Alat pemeriksa skill yang sudah ada:** doodle-lint, SkillSeal, skill-testing, skillscore, dan validator resmi skills-ref. Fokusnya file SKILL.md (format, pemicu). Kita memakai salah satunya di CI, tidak bersaing langsung.
- **Koleksi skill populer:** mattpocock/skills adalah contoh skill pack yang fokus pada alur kerja rekayasa perangkat lunak, bukan produk digital.
- **Lokal Indonesia:** awesome-copilot-id adalah koleksi agent, skill, rule, dan prompt untuk developer Indonesia. Bisa menjadi mitra atau acuan.
- **Pembeda kita:** pembuatan produk digital dengan pemeriksaan hasil otomatis, plus model hybrid dengan paket bahasa dari kontributor.
- Jumlah bintang pesaing belum diverifikasi.

## 15. Linimasa dan milestone

Perkiraan sekitar 4 minggu. Ini estimasi, bukan komitmen.

| Minggu | Milestone |
| --- | --- |
| 1 | Keputusan nama dan lingkup, repo kerangka, `product-qa` dan `ebook-builder` |
| 2 | `prompt-pack-builder`, `template-builder`, paket bahasa `id`, CI, mulai lapis 1 sampai 3 |
| 3 | Lapis 4 sampai 6, tiga produk contoh, beta manusia, perbaikan |
| 4 | Dokumentasi, README, GIF, gerbang rilis, rilis v0.1.0 dan peluncuran |

## 16. Pertanyaan terbuka

1. Nama final repo dan hasil pengecekan tabrakan di GitHub, npm, dan PyPI.
2. Bahasa skrip: Python (usulan) atau Node.
3. Format template v0.1: xlsx saja, atau xlsx dan docx.
4. Apakah QA Gate nanti dirilis juga sebagai paket mandiri (pip atau npm)?
5. Platform mana yang sudah dimiliki pemilik proyek untuk membangun audiens (X, LinkedIn, YouTube)?
6. Apakah ada domain konten yang dilarang total pada v0.1?
7. Lisensi untuk produk contoh di `examples/`.

## 17. Referensi

- Spesifikasi Agent Skills: https://agentskills.io/specification
- morluto/rea (acuan distribusi: skill + CLI + MCP, setup dan doctor): https://github.com/morluto/rea
- mattpocock/skills (acuan format skill dan penyebaran): https://github.com/mattpocock/skills
- vacanza/holidays (acuan model kontributor per negara): https://github.com/vacanza/holidays
- doodle-lint: https://pypi.org/project/doodle-lint/
- SkillSeal: https://pypi.org/project/skillseal/
- skill-testing: https://github.com/crashcartlabs/skill-testing
- skillscore: https://pub.dev/packages/skillscore
- awesome-copilot-id: https://github.com/GulajavaMinistudio/awesome-copilot-id
