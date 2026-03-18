# README — Block Cipher Sederhana (CBC XOR + Substitute + Rotate)

## Deskripsi

Program ini merupakan implementasi **block cipher simetris sederhana** menggunakan Python tanpa library eksternal. Sistem ini menggabungkan tiga operasi utama:

* **CBC XOR (Cipher Block Chaining)**
* **Substitution (XOR dengan key)**
* **Bit Rotation (Left & Right)**

Setiap karakter diproses sebagai blok berukuran **1 byte (8-bit)** dan dienkripsi secara berantai menggunakan mode CBC.

Selain itu, sistem menerapkan **format-preserving encryption (FPE)**:

* Huruf tetap menjadi huruf
* Angka tetap menjadi angka
* Simbol tidak berubah

---

## Fitur Utama

* Enkripsi dan dekripsi teks
* Mode operasi: **CBC (Cipher Block Chaining)**
* Operasi kriptografi:

  * XOR (CBC + Key)
  * Substitusi berbasis key
  * Rotasi bit
* Representasi output:

  * Teks (format-preserving)
  * Desimal
  * Biner
  * Hexadecimal
* Validasi input (plaintext, key, ciphertext)

---

## Spesifikasi Teknis

| Komponen   | Nilai                   |
| ---------- | ----------------------- |
| Block size | 1 byte (8-bit)          |
| Mode       | CBC                     |
| IV         | 170 (10101010) [fixed]  |
| Operasi    | XOR, Substitute, Rotate |
| Key        | String (berulang)       |

---

## Cara Kerja Enkripsi

Untuk setiap karakter plaintext:

1. **Konversi ke ASCII (8-bit)**
2. **CBC XOR**

   ```
   blok = plaintext_byte XOR previous_cipher
   ```
3. **Substitute (XOR dengan key)**

   ```
   blok = blok XOR key_byte
   ```
4. **Rotate Left (1 bit)**
5. **Simpan sebagai ciphertext**
6. **Format-Preserving Shift**

   * Menggeser karakter berdasarkan nilai byte hasil enkripsi

---

## Cara Kerja Dekripsi

Untuk setiap blok ciphertext:

1. **Rotate Right**
2. **Reverse Substitute (XOR key)**
3. **Reverse CBC**

   ```
   blok = blok XOR previous_cipher
   ```
4. **Format-Preserving Reverse Shift**

   * Mengembalikan karakter ke bentuk semula

---

## Struktur Program

* `rotate_left()` → rotasi bit kiri
* `rotate_right()` → rotasi bit kanan
* `fpe_shift()` → format-preserving encryption
* `encrypt()` → proses enkripsi utama
* `decrypt()` → proses dekripsi utama
* `menu_enkripsi()` → antarmuka enkripsi
* `menu_dekripsi()` → antarmuka dekripsi

---

## Cara Menjalankan

1. Pastikan Python sudah terinstall
2. Jalankan program:

   ```
   python nama_file.py
   ```
3. Pilih menu:

   * `1` → Enkripsi
   * `2` → Dekripsi
   * `0` → Keluar

---

## Contoh Penggunaan

### Enkripsi

Input:

```
Plaintext : Halo123
Key       : kunci
```

Output:

* Ciphertext (teks)
* Ciphertext (desimal)
* Ciphertext (biner)
* Ciphertext (hex)

---

### Dekripsi

Input:

```
Ciphertext (teks) : hasil_enkripsi
Ciphertext (hex)  : hasil_hex
Key               : kunci
```

Output:

```
Plaintext asli
```

---

## Kelebihan

* Mudah dipahami (cocok untuk pembelajaran)
* Tidak menggunakan library eksternal
* Menjaga format karakter (FPE)
* Menggunakan chaining (lebih aman dari ECB)

---

## Keterbatasan

* **Block size kecil (8-bit)** → rentan analisis
* **IV statis** → tidak aman untuk penggunaan nyata
* **Tidak tahan terhadap serangan kriptografi modern**
* **Tidak ada padding atau autentikasi**

---

## Tujuan

Program ini dibuat untuk:

* Memahami konsep dasar **block cipher**
* Mempelajari **mode CBC**
* Melihat kombinasi operasi sederhana dalam kriptografi

---

## Catatan

Implementasi ini **bukan untuk keamanan nyata**, hanya untuk edukasi dan eksperimen konsep kriptografi dasar.
