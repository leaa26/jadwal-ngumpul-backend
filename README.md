# Jadwal Ngumpul Backend 💙

Backend API untuk aplikasi koordinasi jadwal kumpul kelompok (anti-wacana). Dibangun menggunakan **Python (Flask)** dan **SQLite** oleh Lea (Sistem Informasi).

## Fitur Backend
- **GET `/schedules`**: Melihat daftar ketersediaan semua anggota kelompok.
- **POST `/schedules`**: Mengatur status ketersediaan anggota (Free = Hijau / Busy = Merah).
- **GET `/best-day`**: Menghitung dan merekomendasikan hari terbaik untuk ngumpul berdasarkan jumlah anggota terbanyak yang *free*.

## Cara Menjalankan
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Jalankan server:
   ```bash
   python app.py
   ```
3. Server aktif di `http://localhost:5000`
