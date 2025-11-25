#!/usr/bin/env python3
"""
Unified tiny test server to log GET and POST requests and respond to /cc like the device.
Place this file in the same folder as the HTML test page and run it:
  python3 logger_server.py
Open http://localhost:8000/test_xhr.html in your browser.
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import json

HOST = 'localhost'
PORT = 8000

class Handler(SimpleHTTPRequestHandler):
    def log_request_info(self):
        print('---- request start ----')
        print('Path:', self.path)
        print('Headers:')
        for k, v in self.headers.items():
            print(f'  {k}: {v}')
        print('---- request end ----\n')

    def do_GET(self):
        self.log_request_info()
        if self.path.startswith('/cc'):
            qs = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(qs)
            print('Parsed GET params:', params)
            resp = {'result': 1}
            body = json.dumps(resp).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        # Fallback: serve files so test_xhr.html can be loaded
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        # Log headers and read body
        self.log_request_info()
        if self.path.startswith('/cc'):
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length) if length > 0 else b''
            print('Raw POST body bytes:', body)
            try:
                decoded = body.decode('utf-8')
            except Exception:
                decoded = repr(body)
            print('Decoded POST body:', decoded)
            # parse form-encoded body
            params = urllib.parse.parse_qs(decoded)
            print('Parsed POST params:', params)
            resp = {'result': 1}
            out = json.dumps(resp).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(out)))
            self.end_headers()
            self.wfile.write(out)
            return
        return SimpleHTTPRequestHandler.do_POST(self)

if __name__ == '__main__':
    print(f'Serving on http://{HOST}:{PORT}/ (CTRL-C to stop)')
    httpd = HTTPServer((HOST, PORT), Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped')
        httpd.server_close()