import http.server, sys, urllib.parse
dst = sys.argv[1]
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.urlparse(self.path).query
        d = urllib.parse.parse_qs(q).get('d', [''])[0]
        if d:
            open(dst, 'w', encoding='utf-8', newline='\n').write(d)
            sys.stderr.write('SHRANJENO %d znakov\n' % len(d))
        self.send_response(200); self.send_header('Content-Type','text/plain'); self.end_headers(); self.wfile.write(b'ok')
    def log_message(self, *a): pass
http.server.HTTPServer(('127.0.0.1', 8767), H).serve_forever()
