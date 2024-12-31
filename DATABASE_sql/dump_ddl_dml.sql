-- Database: `manajemen_toko`
CREATE DATABASE IF NOT EXISTS `manajemen_toko`;
USE `manajemen_toko`;
CREATE TABLE IF NOT EXISTS `barang_product`
(
    `ID_PRODUK` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `nama_produk` VARCHAR(128) NOT NULL,
    `harga_produk` DECIMAL(10,2) NOT NULL CHECK (`harga_produk` >= 0)
);

CREATE TABLE IF NOT EXISTS `catatan_transaksi`
(
    `ID_transaksi` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `ID_PRODUK` INT NOT NULL,
    `jumlah_barang` INT NOT NULL CHECK (`jumlah_barang` > 0),
    `total_harga` DECIMAL(10,2) NOT NULL CHECK (`total_harga` >= 0),
    `waktu_pembuatan` datetime DEFAULT current_timestamp()
);

ALTER TABLE `catatan_transaksi` ADD FOREIGN KEY (`ID_PRODUK`) REFERENCES `barang_product`(`ID_PRODUK`) ON DELETE CASCADE ON UPDATE CASCADE;