Berikut ini adalah **README.md lengkap** yang dihasilkan berdasarkan struktur proyek dan isi file yang ditemukan:

---

# 🧵 Textile Inventory Backend

Backend API untuk sistem **manajemen inventori tekstil**, dibangun menggunakan **FastAPI** dan **MySQL**.
Aplikasi ini menangani autentikasi pengguna, manajemen produk, pemasok, transaksi masuk/keluar barang, serta dasbor ringkasan stok.

---

## 📚 Daftar Isi

1. [Pendahuluan](#-pendahuluan)
2. [Fitur](#-fitur)
3. [Struktur Proyek](#-struktur-proyek)
4. [Instalasi](#-instalasi)
5. [Konfigurasi](#-konfigurasi)
6. [Menjalankan Aplikasi](#-menjalankan-aplikasi)
7. [API Endpoint](#-api-endpoint)
8. [Dependensi](#-dependensi)
9. [Troubleshooting](#-troubleshooting)
10. [Kontributor](#-kontributor)
11. [Lisensi](#-lisensi)

---

## 🧩 Pendahuluan

Proyek ini merupakan backend service untuk sistem **Textile Inventory Management**, yang berfungsi untuk:

* Mencatat barang masuk dan keluar.
* Mengelola data produk dan pemasok.
* Mengelola autentikasi pengguna (login dan registrasi).
* Menyediakan data ringkasan untuk dashboard.

Dibangun menggunakan **FastAPI**, aplikasi ini mendukung RESTful API yang cepat dan mudah diintegrasikan dengan frontend (misalnya aplikasi berbasis Angular atau React).

---

## ✨ Fitur

✅ Autentikasi pengguna (JWT-based).
✅ CRUD data produk dan pemasok.
✅ Manajemen stok barang masuk dan keluar.
✅ Dasbor statistik stok.
✅ Dukungan CORS untuk integrasi frontend.
✅ Terstruktur dan modular (routers, CRUD, models, utils).

---

## 🗂️ Struktur Proyek

```
textile-inventory-backend/
│
├── main.py                # Entry point aplikasi FastAPI
├── database.py            # Koneksi dan konfigurasi database MySQL
├── crud/                  # Operasi Create, Read, Update, Delete
├── models/                # Definisi model ORM
├── routers/               # Endpoint API (auth, product, supplier, dll)
├── utils/                 # Fungsi utilitas (misalnya hashing, JWT, dll)
├── requirements.txt       # Dependensi proyek
└── .gitignore
```

---

## ⚙️ Instalasi

1. **Kloning repositori ini**

   ```bash
   git clone https://github.com/username/textile-inventory-backend.git
   cd textile-inventory-backend
   ```

2. **Buat virtual environment (disarankan)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate      # Windows
   ```

3. **Instal dependensi**

   ```bash
   pip install -r requirements.txt
   ```

---

## 🔧 Konfigurasi

Buat file `.env` di root proyek dan isi dengan variabel berikut:

```env
DATABASE_URL=mysql+mysqlconnector://user:password@localhost:3306/textile_inventory
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🚀 Menjalankan Aplikasi

Jalankan server menggunakan **Uvicorn**:

```bash
uvicorn main:app --reload
```

Server akan berjalan di:
👉 `http://127.0.0.1:8080`

---

## 📡 API Endpoint

| Kategori      | Endpoint         | Metode              | Deskripsi           |
| ------------- | ---------------- | ------------------- | ------------------- |
| Auth          | `/auth/login`    | POST                | Login pengguna      |
| Auth          | `/auth/register` | POST                | Registrasi pengguna |
| Produk        | `/product/`      | GET/POST/PUT/DELETE | CRUD produk         |
| Supplier      | `/supplier/`     | GET/POST/PUT/DELETE | CRUD supplier       |
| Barang Masuk  | `/incoming/`     | GET/POST            | Catat barang masuk  |
| Barang Keluar | `/outgoing/`     | GET/POST            | Catat barang keluar |
| Dashboard     | `/dashboard/`    | GET                 | Data ringkasan stok |

---

## 📦 Dependensi

Dari `requirements.txt`:

```txt
fastapi[standard]
mysql-connector-python
uvicorn
dotenv
passlib
python-jose[cryptography]
pyjwt
```

---

## 🧰 Troubleshooting

**Masalah koneksi database:**

> Pastikan konfigurasi `DATABASE_URL` benar dan database MySQL aktif.

**Error “Module not found”:**

> Pastikan environment aktif dan semua dependensi sudah diinstal.

**CORS error saat mengakses dari frontend:**

> Pastikan domain frontend (`localhost:4200`) sudah ditambahkan ke daftar `origins` di `main.py`.

---

## 👥 Kontributor

* **Rafah Fajri Juwaeni** (Developer Utama)

---

