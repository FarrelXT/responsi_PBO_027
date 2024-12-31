# Program Manajemen Toko Sederhana

## Deskripsi Program
Program Manajemen Toko Sederhana adalah aplikasi berbasis GUI yang dibuat menggunakan Python dan Tkinter. Program ini memungkinkan pengguna untuk mengelola produk dan transaksi dalam sebuah toko. Fitur utama dari program ini meliputi:
- Menambahkan produk baru ke dalam database.
- Menambahkan transaksi baru dengan memilih produk dari daftar.
- Menampilkan daftar transaksi yang telah dilakukan.

## Cara Menjalankan Program
Untuk menjalankan program ini, ikuti langkah-langkah berikut:

1. Pastikan Anda telah menginstal Python di komputer Anda. Program ini dikembangkan menggunakan Python 3.x.
2. Instal pustaka yang diperlukan dengan menjalankan perintah berikut di terminal:
   ```bash
   pip install mysql-connector-python pillow
   ```
3. Pastikan Anda memiliki server MySQL yang berjalan dan buat database dengan struktur yang dijelaskan di bawah ini.
4. Import file `dump_ddl_dml.sql` yang terdapat di folder `DATABASE_sql` ke dalam database `manajemen_toko`.
5. Jalankan file `main_app.py` dengan perintah berikut:
   ```bash
   python main_app.py
   ```

## Struktur Database
Program ini menggunakan database MySQL dengan nama `manajemen_toko`. Berikut adalah struktur database beserta penjelasannya:

### Tabel `barang_product`
| Kolom         | Tipe Data     | Keterangan                        |
|---------------|---------------|-----------------------------------|
| `ID_PRODUK`   | INT           | Primary key, auto-increment       |
| `nama_produk` | VARCHAR(128)  | Nama produk                       |
| `harga_produk`| DECIMAL(10,2) | Harga produk                      |

### Tabel `catatan_transaksi`
| Kolom           | Tipe Data     | Keterangan                                      |
|-----------------|---------------|-------------------------------------------------|
| `ID_transaksi`  | INT           | Primary key, auto-increment                     |
| `ID_PRODUK`     | INT           | Foreign key yang mengacu ke `ID_PRODUK`         |
| `jumlah_barang` | INT           | Jumlah barang yang dibeli                       |
| `total_harga`   | DECIMAL(10,2) | Total harga transaksi                           |
| `waktu_pembuatan`| DATETIME     | Waktu pembuatan transaksi                       |

Setiap tabel memiliki relasi yang jelas untuk memastikan integritas data dalam sistem manajemen toko ini.