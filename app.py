from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Agar Frontend kelompokmu bisa akses backend ini tanpa masalah CORS
DB_NAME = 'jadwal.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tabel ketersediaan jadwal anggota
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS availability (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            hari TEXT NOT NULL,
            status TEXT NOT NULL -- 'free' (hijau) atau 'busy' (merah)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return jsonify({
        "message": "Backend Aplikasi Jadwal Ngumpul 💙",
        "team_role": "Backend by Lea (Sistem Informasi)",
        "endpoints": {
            "GET /schedules": "Melihat jadwal semua anggota",
            "POST /schedules": "Mengatur status ketersediaan (body: nama, hari, status)",
            "GET /best-day": "Melihat hari terbaik untuk ngumpul (paling banyak yang free)"
        }
    })

# 1. GET: Melihat semua jadwal
@app.route('/schedules', methods=['GET'])
def get_schedules():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM availability')
    rows = cursor.fetchall()
    conn.close()
    
    data = [dict(row) for row in rows]
    return jsonify({"schedules": data})

# 2. POST: Update/Tambah jadwal anggota (Free/Busy)
@app.route('/schedules', methods=['POST'])
def update_schedule():
    req_data = request.get_json()
    if not req_data or not all(k in req_data for k in ('nama', 'hari', 'status')):
        return jsonify({"error": "Data tidak lengkap! Sertakan nama, hari, dan status (free/busy)."}), 400
    
    nama = req_data['nama']
    hari = req_data['hari'].capitalize()
    status = req_data['status'].lower() # 'free' atau 'busy'
    
    if status not in ['free', 'busy']:
        return jsonify({"error": "Status harus 'free' (hijau) atau 'busy' (merah)."}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Cek apakah nama & hari sudah ada, kalau ada update, kalau belum insert
    cursor.execute('SELECT id FROM availability WHERE nama = ? AND hari = ?', (nama, hari))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute('UPDATE availability SET status = ? WHERE nama = ? AND hari = ?', (status, nama, hari))
    else:
        cursor.execute('INSERT INTO availability (nama, hari, status) VALUES (?, ?, ?)', (nama, hari, status))
        
    conn.commit()
    conn.close()
    
    return jsonify({
        "message": f"Jadwal {nama} pada hari {hari} berhasil disimpan sebagai '{status}'!",
        "data": {"nama": nama, "hari": hari, "status": status}
    })

# 3. GET /best-day: Mencari hari terbaik untuk ngumpul
@app.route('/best-day', methods=['GET'])
def get_best_day():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Hitung berapa orang yang 'free' di setiap hari
    cursor.execute('''
        SELECT hari, COUNT(*) as total_free 
        FROM availability 
        WHERE status = 'free' 
        GROUP BY hari 
        ORDER BY total_free DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    results = [{"hari": row[0], "total_free": row[1]} for row in rows]
    best = results[0] if results else None
    
    return jsonify({
        "best_day": best,
        "ranking": results
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
