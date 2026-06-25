# HRIS Application (Django MVT + DRF)

**Live Demo:** [https://simple-hris-project-competency.onrender.com](https://simple-hris-project-competency.onrender.com)

Aplikasi *Human Resource Information System* (HRIS) komprehensif yang dibangun menggunakan Django (Python) dengan pendekatan *hybrid* (MVT untuk Antarmuka Web dan Django Rest Framework untuk API). 

Proyek ini telah dikontainerisasi menggunakan **Docker** dan menggunakan **PostgreSQL** sebagai sistem basis datanya.

---

## 🚀 Fitur Utama

1. **Authentication & Role-Based Access Control (RBAC)**
   - Custom User Model berbasis Email.
   - Peran ganda: `HR_ADMIN` (Akses Penuh) dan `EMPLOYEE` (Akses Terbatas/Read-Only Own Data).
2. **Employee Management (CRUD)**
   - Pencatatan profil karyawan terintegrasi dengan akun pengguna.
   - Pencarian cerdas (Server-Side Search & Pagination).
3. **Attendance System (Sistem Absensi Cerdas)**
   - Check-In & Check-Out terpusat melalui API interaktif via `fetch` AJAX.
   - Validasi ketat (Batas Check-In 08:00).
   - Validasi Otomatis Hari Libur Nasional Indonesia (via _library_ `holidays`) dan Hari Libur Akhir Pekan.
4. **Data Analytics & Export**
   - Visualisasi interaktif menggunakan **Chart.js** di Dashboard HR Admin.
   - Export rekap absensi ke `.xlsx` (Excel) dan `.csv` *on-the-fly* secara dinamis tanpa N+1 Query.

---

## 🛠️ Persyaratan Sistem (Prerequisites)
Pastikan sistem operasi Anda (Windows/Mac/Linux) telah terinstal perangkat lunak berikut:
- [Docker & Docker Compose](https://www.docker.com/products/docker-desktop) (Untuk Setup via Docker)
- [Python 3.10+](https://www.python.org/downloads/) dan [PostgreSQL](https://www.postgresql.org/download/) (Untuk Setup Manual Local)

---

## ⚙️ Tutorial 1: Setup Menggunakan Docker (Rekomendasi)

Aplikasi ini menggunakan skrip `entrypoint.sh` untuk otomatisasi migrasi database dan pembuatan akun admin.

1. **Buka Terminal / Command Prompt** dan pastikan Anda berada di direktori proyek ini.
2. **Jalankan Docker Compose**:
   Jalankan perintah berikut untuk mem-build image Docker dan menjalankan kontainer (termasuk PostgreSQL dan Web Server) di latar belakang:
   ```bash
   docker-compose up --build -d
   ```
3. **Proses Setup Otomatis**:
   Tunggu beberapa saat. Docker akan mengunduh _image_, menginstal dependensi, menjalankan migrasi database, dan menyuntikkan akun Superuser/HR_ADMIN (`admin@hr.com`).
4. **Mengecek Status**:
   Anda bisa mengecek log server dengan perintah:
   ```bash
   docker-compose logs -f web
   ```
5. **Akses Aplikasi**:
   Buka *browser* Anda dan kunjungi URL: **`http://localhost:8000/`**

---

## ⚙️ Tutorial 2: Setup Manual Tanpa Docker (Local Development)

Jika Anda tidak menggunakan Docker, ikuti langkah-langkah di bawah ini untuk menjalankan server secara lokal:

### 1. Persiapan Database (PostgreSQL)
- Pastikan PostgreSQL telah berjalan di komputer Anda.
- Buat database baru bernama `hris_db`.
- Buat user bernama `hris_user` dengan password `hris_password` dan berikan akses penuh ke database `hris_db` (Anda juga dapat membuat database default tanpa setting password jika tidak diperlukan).

### 2. Setup Virtual Environment & Instalasi Dependensi
Buka Terminal / Command Prompt di folder proyek:
```bash
# Membuat virtual environment
python -m venv venv

# Mengaktifkan virtual environment (Windows)
venv\Scripts\activate
# Atau mengaktifkan virtual environment (Mac/Linux)
source venv/bin/activate

# Menginstal dependensi
pip install -r requirements.txt
```

### 3. Migrasi Database & Pembuatan Akun Superuser
Pastikan PostgreSQL Anda berjalan, lalu eksekusi perintah berikut untuk membangun struktur tabel:
```bash
python manage.py makemigrations
python manage.py migrate
```

Untuk membuat akun Superuser / HR Admin, jalankan *shell* Django:
```bash
python manage.py shell
```
Kemudian jalankan kode Python berikut di dalam shell tersebut:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser(email='admin@hr.com', password='admin123')
exit()
```

*(Opsional)* Anda juga dapat mengisi data karyawan dummy jika script khusus tersedia (seperti `init_struct.py`).

### 4. Menjalankan Server (Run Server)
Setelah semua setup selesai, jalankan server Django secara lokal:
```bash
python manage.py runserver
```
Server akan berjalan. Akses aplikasi melalui *browser* pada alamat **`http://localhost:8000/`**

---

## 📖 Tutorial 3: Panduan Penggunaan Website

Setelah aplikasi berjalan, berikut adalah langkah-langkah penggunaan dari sisi pengguna (Admin dan Karyawan).

### Langkah 1: Login ke Sistem
1. Akses halaman utama `http://localhost:8000/`.
2. Gunakan kredensial berikut untuk mencoba sistem:
   - **HR Admin (Akses Penuh):** Email: `admin@hr.com` | Password: `admin123`
   - **Karyawan (Akses Terbatas):** Jika Anda menggunakan Docker dan dummy data ter-generate otomatis, silakan coba login dengan
   - `fnarpati@example.com`
   - `galur93@example.net`
   - `rpangestu@example.net` (Password: `password123`). Jika Anda setup manual, Anda perlu menambahkan user Karyawan terlebih dahulu lewat dashboard HR Admin.
3. Klik tombol **Login**.

### Langkah 2: Eksplorasi Beranda (Dashboard)
- **Sebagai HR Admin**: Anda akan melihat **Dashboard Analytics** yang menampilkan metrik jumlah karyawan aktif, total absensi hari ini, serta grafik kehadiran karyawan (Chart.js).
- **Sebagai Karyawan**: Anda hanya akan melihat informasi profil Anda dan status kehadiran pribadi Anda.

### Langkah 3: Manajemen Karyawan (Menu Karyawan)
1. Klik menu **"Karyawan"** di *sidebar* sebelah kiri.
2. **Sebagai HR Admin**: Anda bisa menambah karyawan baru (klik *Tambah Karyawan*), mengedit, menghapus, atau mencari karyawan tertentu di baris pencarian.
3. **Sebagai Karyawan**: Anda hanya dapat melihat informasi kontak rekan kerja (direktori karyawan).

### Langkah 4: Melakukan Absensi (Menu Absensi Personal)
1. Klik menu **"Absensi Personal"** di *sidebar*.
2. **Check-In**: Jika belum absen masuk hari ini (dan jam belum lewat pukul 08:00 pada hari kerja), klik tombol **Check In**.
3. **Check-Out**: Jika sudah Check-In, tombol akan berubah menjadi **Check Out**. Klik untuk mencatat jam pulang setelah bekerja.

### Langkah 5: Manajemen Absensi & Ekspor Laporan (Khusus HR Admin)
1. Klik menu **"Manajemen Absensi"** di *sidebar*.
2. Anda dapat memonitor rekapan aktivitas absensi dari semua karyawan setiap harinya.
3. **Ekspor Data**: Klik tombol **"Export CSV"** atau **"Export Excel"** untuk mengunduh rekapitulasi data absensi ke penyimpanan lokal Anda.

---

## 📡 Referensi Endpoint API (DRF)

| Metode | Endpoint | Keterangan | Akses |
|--------|----------|------------|-------|
| `GET`  | `/api/employees/` | Daftar karyawan | Admin, Employee (Self) |
| `POST` | `/api/employees/` | Tambah karyawan baru | Admin |
| `GET`  | `/api/attendance/` | Laporan absensi harian | Admin, Employee (Self) |
| `POST` | `/api/attendance/check-in/` | Mencatat jam masuk | Employee |
| `POST` | `/api/attendance/check-out/`| Mencatat jam keluar | Employee |
| `GET`  | `/api/attendance/export-excel/` | Mengunduh file `.xlsx` | Admin |
| `GET`  | `/api/attendance/export-csv/` | Mengunduh file `.csv` | Admin |

---
*Proyek ini merupakan demonstrasi arsitektur Clean Code, Modular, dan skalabilitas pada ekosistem Django Framework.*
