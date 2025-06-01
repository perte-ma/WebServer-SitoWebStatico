import sys, signal
import http.server
import socketserver

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/www/index.html')
            self.end_headers()
        else:
            super().do_GET()
    def send_error(self, code, message=None, explain=None):
        if code == 404:
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"""\
            <html>
              <head><title>404 Not Found</title></head>
              <body><h1>404 Not Found</h1></body>
            </html>
            """)
        else:
            super().send_error(code, message, explain)

server = socketserver.ThreadingTCPServer(('127.0.0.1',8080), MyHTTPRequestHandler )

server.daemon_threads = True  
server.allow_reuse_address = True  

def signal_handler(signal, frame):
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
      if( server ):
        server.server_close()
    finally:
      sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    print(f"Server ready to serve on http://127.0.0.1:8080 ...")
    server.serve_forever()
except KeyboardInterrupt:
  pass

server.server_close()
