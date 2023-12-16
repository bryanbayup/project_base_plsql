# project_base_plsql UAS
Pendahuluan
Proyek ini adalah aplikasi manajemen pengguna sederhana yang dibangun dengan menggunakan Flask, PostgreSQL, dan enkripsi password menggunakan AES. Aplikasi ini memungkinkan pengguna untuk membuat akun dengan menyimpan nama pengguna dan kata sandi yang dienkripsi secara aman di database.

syarat menjalankan aplikasi
Pastikan sistem Anda telah memenuhi persyaratan berikut sebelum menginstal proyek ini:
Python 3.x terinstal
PostgreSQL terinstal dan konfigurasi (termasuk pembuatan database)
PIP terinstal

#Instalasi
Clone repositori ini ke sistem Anda:
git clone https://github.com/namapengguna/project_base_plsql.git
cd project_base_plsql

#Buat dan aktifkan lingkungan virtual:
python -m venv venv
source venv/bin/activate  # Untuk Windows gunakan "venv\Scripts\activate"

#Instal dependensi:
pip install -r requirements.txt

#Konfigurasi database:
Buat database PostgreSQL baru
Ganti URL database di file .env dengan URL database PostgreSQL Anda
#Migrasi database:
flask db init
flask db migrate
flask db upgrade
Penggunaan
Jalankan aplikasi:
flask Main.py
Akses aplikasi melalui browser di http://localhost:5000
