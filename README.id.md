# Digital Product Factory

Buat agent AI membuat produk digital yang bisa dipakai, lalu buktikan dengan QA Gate.

## Isi

- `product-qa`: laporan QA offline untuk prompt pack, XLSX, dan ebook EPUB/PDF.
- `prompt-pack-builder`: format prompt terstruktur dengan variabel dan contoh.
- `template-builder`: template XLSX dengan petunjuk serta data contoh.
- `ebook-builder`: ebook EPUB/PDF dengan pemeriksaan navigasi.

## Pengembangan lokal

```sh
python -m unittest discover -s tests -v
python -m product_qa doctor
python scripts/create_examples.py
```

Contoh prompt pack lulus hanya dengan Python. XLSX membutuhkan LibreOffice untuk evaluasi rumus. Ebook membutuhkan Pandoc dan EPUBCheck untuk gerbang rilis.

Lihat README Inggris untuk perintah instalasi dan aturan laporan QA.
