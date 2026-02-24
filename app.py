#!/usr/bin/env python3
import json
import os
import sqlite3
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

ROOT = os.path.dirname(__file__)
DB_PATH = os.path.join(ROOT, 'db', 'kopartner.db')
SCHEMA_PATH = os.path.join(ROOT, 'db', 'schema.sql')
PUBLIC_DIR = os.path.join(ROOT, 'public')


def db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db_conn()
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as schema_file:
        conn.executescript(schema_file.read())
    conn.executemany('INSERT OR IGNORE INTO users(full_name,email,phone,role,password,city) VALUES(?,?,?,?,?,?)', [
        ('Platform Admin', 'admin@kopartner.in', '9990000001', 'admin', 'admin123', 'Delhi'),
        ('Aarav Client', 'client@kopartner.in', '9990000002', 'client', 'client123', 'Mumbai'),
        ('Priya Partner', 'partner@kopartner.in', '9990000003', 'partner', 'partner123', 'Bangalore')
    ])
    conn.executemany('INSERT OR IGNORE INTO services(id,name,price_per_hour,active) VALUES(?,?,?,1)', [
        (1, 'Voice Call Chat', 500), (2, 'Video Call Chat', 1000), (3, 'Movie Companion', 2000), (4, 'Travel Partner', 2000)
    ])
    client = conn.execute("SELECT id FROM users WHERE role='client' LIMIT 1").fetchone()
    partner = conn.execute("SELECT id FROM users WHERE role='partner' LIMIT 1").fetchone()
    if client and partner:
        conn.execute('INSERT OR IGNORE INTO bookings(id,client_id,partner_id,service_id,booking_date,duration_hours,status,notes) VALUES(1,?,?,?,?,?,?,?)',
                     (client['id'], partner['id'], 2, '2026-03-02', 2, 'confirmed', 'First demo booking'))
        conn.execute('INSERT OR IGNORE INTO payouts(id,partner_id,booking_id,amount,status) VALUES(1,?,?,?,?)',
                     (partner['id'], 1, 1600, 'due'))
    conn.commit()
    conn.close()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def _json(self, code, payload):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def _read_json(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length).decode() if length else '{}'
        return json.loads(raw)

    def do_GET(self):
        p = urlparse(self.path).path
        conn = db_conn()
        if p == '/api/services':
            rows = [dict(r) for r in conn.execute('SELECT * FROM services WHERE active=1 ORDER BY id')]
            conn.close(); return self._json(200, rows)
        if p.startswith('/api/client/') and p.endswith('/bookings'):
            cid = p.split('/')[3]
            rows = [dict(r) for r in conn.execute('''SELECT b.*, s.name service_name, u.full_name partner_name FROM bookings b
                JOIN services s ON s.id=b.service_id LEFT JOIN users u ON u.id=b.partner_id WHERE b.client_id=? ORDER BY b.created_at DESC''', (cid,))]
            conn.close(); return self._json(200, rows)
        if p.startswith('/api/partner/') and p.endswith('/bookings'):
            pid = p.split('/')[3]
            rows = [dict(r) for r in conn.execute('''SELECT b.*, s.name service_name, c.full_name client_name FROM bookings b
                JOIN services s ON s.id=b.service_id JOIN users c ON c.id=b.client_id WHERE b.partner_id=? ORDER BY b.created_at DESC''', (pid,))]
            conn.close(); return self._json(200, rows)
        if p.startswith('/api/partner/') and p.endswith('/payouts'):
            pid = p.split('/')[3]
            rows = [dict(r) for r in conn.execute('SELECT * FROM payouts WHERE partner_id=? ORDER BY created_at DESC', (pid,))]
            conn.close(); return self._json(200, rows)
        if p == '/api/admin/overview':
            users = [dict(r) for r in conn.execute('SELECT role, COUNT(*) count FROM users GROUP BY role')]
            bookings = [dict(r) for r in conn.execute('SELECT status, COUNT(*) count FROM bookings GROUP BY status')]
            revenue = conn.execute("SELECT IFNULL(SUM(s.price_per_hour*b.duration_hours),0) total FROM bookings b JOIN services s ON s.id=b.service_id WHERE b.status IN ('confirmed','completed')").fetchone()['total']
            conn.close(); return self._json(200, {'users': users, 'bookings': bookings, 'revenue': revenue})
        if p == '/api/admin/bookings':
            rows = [dict(r) for r in conn.execute('''SELECT b.*, s.name service_name, c.full_name client_name, p.full_name partner_name FROM bookings b
             JOIN services s ON s.id=b.service_id JOIN users c ON c.id=b.client_id LEFT JOIN users p ON p.id=b.partner_id ORDER BY b.created_at DESC''')]
            conn.close(); return self._json(200, rows)
        if p == '/api/admin/users':
            rows = [dict(r) for r in conn.execute('SELECT id,full_name,email,phone,role,city,created_at FROM users ORDER BY created_at DESC')]
            conn.close(); return self._json(200, rows)
        conn.close()
        return super().do_GET()

    def do_POST(self):
        p = urlparse(self.path).path
        body = self._read_json()
        conn = db_conn()
        if p == '/api/auth/login':
            u = conn.execute('SELECT id,full_name,email,role,city,password FROM users WHERE email=?', (body.get('email'),)).fetchone()
            conn.close()
            if not u or u['password'] != body.get('password'):
                return self._json(401, {'error': 'Invalid credentials'})
            return self._json(200, {'user': {k: u[k] for k in ['id', 'full_name', 'email', 'role', 'city']}})
        if p == '/api/bookings':
            cur = conn.execute('INSERT INTO bookings(client_id,service_id,booking_date,duration_hours,notes) VALUES(?,?,?,?,?)',
                               (body['client_id'], body['service_id'], body['booking_date'], body['duration_hours'], body.get('notes', '')))
            bid = cur.lastrowid
            conn.commit()
            row = dict(conn.execute('SELECT * FROM bookings WHERE id=?', (bid,)).fetchone())
            conn.close(); return self._json(201, row)
        conn.close()
        self._json(404, {'error': 'Not found'})

    def do_PATCH(self):
        p = urlparse(self.path).path
        if p.startswith('/api/admin/bookings/'):
            bid = p.split('/')[-1]
            body = self._read_json()
            conn = db_conn()
            conn.execute('UPDATE bookings SET status=COALESCE(?,status), partner_id=COALESCE(?,partner_id) WHERE id=?',
                         (body.get('status'), body.get('partner_id'), bid))
            conn.commit()
            row = dict(conn.execute('SELECT * FROM bookings WHERE id=?', (bid,)).fetchone())
            conn.close(); return self._json(200, row)
        self._json(404, {'error': 'Not found'})


if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT, 'db'), exist_ok=True)
    init_db()
    port = int(os.environ.get('PORT', '3000'))
    print(f'Server running at http://localhost:{port}')
    ThreadingHTTPServer(('0.0.0.0', port), Handler).serve_forever()
