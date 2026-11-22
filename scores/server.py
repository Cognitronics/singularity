"""Singularity high-score service (Python stdlib only, SQLite).

GET  /api/scores?limit=20        -> {"scores":[{rank,name,mode,score,turns,anchors,inventions,result,date}]}
POST /api/scores  JSON body      -> {"id":..,"rank":..,"scores":[...top list...]}
     {name, mode: "epochal"|"endless", score, turns, anchors, inventions, result}

Stores no IP addresses. A small in-memory limit (per client address, not persisted)
keeps a single visitor from flooding the list.
"""
import json, os, re, sqlite3, time, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DB = os.environ.get('SCORES_DB', '/data/scores.db')
PORT = int(os.environ.get('PORT', '8080'))
MAX_PER_HOUR = 30
lock = threading.Lock()
recent = {}  # client address -> [timestamps], memory only

def db():
    c = sqlite3.connect(DB)
    c.execute('''CREATE TABLE IF NOT EXISTS scores(
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, mode TEXT NOT NULL,
        score INTEGER NOT NULL, turns INTEGER, anchors INTEGER, inventions INTEGER,
        result TEXT, created INTEGER NOT NULL)''')
    try:
        c.execute('ALTER TABLE scores ADD COLUMN diff TEXT')  # added with the difficulty levels
    except sqlite3.OperationalError:
        pass
    return c

def top(c, limit):
    rows = c.execute('SELECT id,name,mode,score,turns,anchors,inventions,result,created,diff FROM scores '
                     'ORDER BY score DESC, created ASC LIMIT ?', (limit,)).fetchall()
    return [dict(id=r[0], rank=i + 1, name=r[1], mode=r[2], score=r[3], turns=r[4], anchors=r[5],
                 inventions=r[6], result=r[7], diff=r[9] or 'hard', date=time.strftime('%Y-%m-%d', time.gmtime(r[8])))
            for i, r in enumerate(rows)]

NAME_OK = re.compile(r"^[\w .,'!?&()-]{1,20}$", re.UNICODE)

def clean(body):
    name = ' '.join(str(body.get('name', '')).split())[:20]
    if not name or not NAME_OK.match(name):
        raise ValueError('name')
    mode = body.get('mode')
    if mode not in ('epochal', 'endless'):
        raise ValueError('mode')
    def num(k, lo, hi):
        v = body.get(k, 0)
        if not isinstance(v, (int, float)) or not lo <= v <= hi:
            raise ValueError(k)
        return int(v)
    result = str(body.get('result', ''))[:12]
    if result not in ('win', 'lose-inst', 'lose-time', 'lose-rival'):
        raise ValueError('result')
    diff = body.get('diff', 'hard')
    if diff not in ('easy', 'normal', 'hard'):
        raise ValueError('diff')
    return (name, mode, num('score', 0, 1_000_000), num('turns', 0, 5000), num('anchors', 0, 10),
            num('inventions', 0, 64), result, diff)

class H(BaseHTTPRequestHandler):
    server_version = 'scores/1'
    def _send(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(b)))
        self.end_headers()
        self.wfile.write(b)
    def log_message(self, *a):  # no access log (would contain addresses)
        pass
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()
    def do_GET(self):
        if not self.path.startswith('/api/scores'):
            return self._send(404, {'error': 'not found'})
        m = re.search(r'limit=(\d+)', self.path)
        limit = max(1, min(100, int(m.group(1)) if m else 20))
        with lock:
            c = db(); out = top(c, limit); c.close()
        self._send(200, {'scores': out})
    def do_POST(self):
        if self.path.rstrip('/') != '/api/scores':
            return self._send(404, {'error': 'not found'})
        n = int(self.headers.get('Content-Length') or 0)
        if n <= 0 or n > 2000:
            return self._send(400, {'error': 'size'})
        client = self.headers.get('X-Real-IP') or self.client_address[0]
        now = time.time()
        with lock:
            ts = [t for t in recent.get(client, []) if now - t < 3600]
            if len(ts) >= MAX_PER_HOUR:
                recent[client] = ts
                return self._send(429, {'error': 'too many'})
            ts.append(now); recent[client] = ts
        try:
            row = clean(json.loads(self.rfile.read(n)))
        except Exception as e:
            return self._send(400, {'error': 'invalid ' + str(e)})
        with lock:
            c = db()
            cur = c.execute('INSERT INTO scores(name,mode,score,turns,anchors,inventions,result,diff,created) '
                            'VALUES(?,?,?,?,?,?,?,?,?)', row + (int(now),))
            c.commit()
            rid = cur.lastrowid
            rank = c.execute('SELECT COUNT(*) FROM scores WHERE score>? OR (score=? AND id<?)',
                             (row[2], row[2], rid)).fetchone()[0] + 1
            out = top(c, 20); c.close()
        self._send(200, {'id': rid, 'rank': rank, 'scores': out})

if __name__ == '__main__':
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    db().close()
    ThreadingHTTPServer(('0.0.0.0', PORT), H).serve_forever()
