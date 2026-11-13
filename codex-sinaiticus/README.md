# Codex Sinaiticus — Atlas Interlinear

[**Buka pembaca daring**](https://leonashr.github.io/ghs-digital/codex-sinaiticus/) · [**Unduh versi offline lengkap**](https://leonashr.github.io/ghs-digital/codex-sinaiticus/Codex-Sinaiticus-complete.zip) · [Sumber transkripsi resmi](https://github.com/itsee-birmingham/codex-sinaiticus) · [Scan manuskrip resmi](https://codexsinaiticus.org/en/manuscript.aspx)

## Cakupan dan metode

Pembaca ini menyajikan **seluruh unit ayat yang masih terlestarikan** dalam XML v1.95 Codex Sinaiticus Project / ITSEE, bukan ayat demonstrasi dan bukan teks Alkitab modern. Build terakhir mengindeks **63 kelompok teks, 21.882 unit ayat, 390.178 token Yunani**. Kelompok teks meliputi fragmen, Kitab-kitab Septuaginta yang terlestarikan, Perjanjian Baru, Surat Barnabas, Gembala Hermas, dan kelompok tambahan. Angka kelompok **bukan** jumlah kitab kanonik. Manuskrip memiliki lacuna; teks yang hilang tidak ditambahkan.

Teks Yunani mengikuti transkripsi XML dan urutan token, dengan penggabungan segmen kata yang terbelah oleh pembungkusan baris. Pilihan koreksi yang ditampilkan bukan edisi kritis baru; varian, pemendekan **nomina sacra**, penomoran Septuaginta, dan kolom/folio harus diperiksa langsung pada citra naskah resmi. Tautan setiap ayat mengarah ke situs resmi (versi situs resmi dapat berbeda dari XML 1.95).

Tabel tiap ayat memuat tulisan Yunani, **transliterasi sederhana** (bukan pelafalan IPA yang direkonstruksi), glosa leksikal Inggris, serta glosa leksikal Indonesia, **hanya untuk bentuk yang telah dianotasi**. Saat ini ada 167 bentuk Yunani dalam kamus awal. Kata lain sengaja diberi **— belum ditinjau**. Ini bukan terjemahan kontekstual lengkap per kata; **tidak boleh** dijadikan sumber tunggal untuk pembacaan teologis atau kritik teks.

## Cara menggunakan

1. Buka [pembaca online](https://leonashr.github.io/ghs-digital/codex-sinaiticus/) menggunakan ponsel atau desktop. Halaman awal Matius 1:1, atau pilih kitab, pasal, dan ayat sendiri.
2. Klik tautan **Verifikasi ayat** / **Folio** pada hasil. Tombol **Muat penampil resmi** mencoba memuat citra dari situs lain; jika diblokir browser, gunakan tautan resmi tersebut.
3. Untuk **tanpa internet**, unduh arsip **Codex-Sinaiticus-complete.zip**, ekstrak, lalu buka **Codex-Sinaiticus-complete.html**. Seluruh teks Yunani disisipkan langsung. Gambar folio tidak ikut disalin.
4. Gunakan **CSV** untuk mengunduh token dari ayat-ayat yang sedang ditampilkan dan melanjutkan pemeriksaan terjemahan.

## Reproduksibilitas

Berkas utama:
- `index.html` — pembaca responsif dengan JS/CSS dan 167 entri kamus awal tertanam.
- `data/manifest.json`, `data/books/b*.json`, `data/quality-report.json` — dihasilkan dari XML resmi dan disimpan bersama SHA-256 sumber.
- `tools/build_corpus.py` — streaming parser.
- `tools/package_corpus.py` — HTML lengkap offline dari JSON yang telah divalidasi.
- `../../.github/workflows/codex-sinaiticus.yml` — pengambilan XML, validasi, ekspor data, arsip offline, dan commit otomatis di GitHub Actions.

**Buat ulang data:** `python tools/build_corpus.py SOURCE.xml data`

**Buat ZIP offline:** `python tools/package_corpus.py data index.html Codex-Sinaiticus-complete.zip`

Unduh `sinaiticus_full_v195.xml` dari repo ITSEE. Proses build tidak mengunggah ulang berkas XML aslinya; hanya JSON turunan. Workflow akan berhenti jika data kelihatan tidak lengkap, dan `data/quality-report.json` mencatat jumlah, hash, serta status tinjauan terjemahan. Pengujian otomatis bersifat **struktural**, bukan penelaahan filologi setiap ayat.

## Atribusi dan batasan penggunaan

**Greek transcription:** Codex Sinaiticus Project; ITSEE, University of Birmingham, https://github.com/itsee-birmingham/codex-sinaiticus. Sumber transkripsi berlisensi **Creative Commons Attribution–NonCommercial–ShareAlike 3.0 (CC BY-NC-SA 3.0)**. Harap gunakan materi turunannya secara **nonkomersial**, sertakan atribusi, dan ikuti kewajiban lisensi serupa. Citra manuskrip **tidak** termasuk dalam arsip ini; hak dan syarat penggunaan citra mengikuti situs aslinya. Proyek pembaca merupakan alat pendidikan dan riset, bukan salinan resmi Codex Sinaiticus Project.
