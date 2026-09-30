import http.server
import socketserver
import os
import sys

PORT = 8082
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def serve():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"============================================================")
        print(f"Agricultural Intelligence Platform — Developer Admin Console")
        print(f"Serving at: http://localhost:{PORT}")
        print(f"Serving directory: {DIRECTORY}")
        print(f"Press Ctrl+C to stop.")
        print(f"============================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    serve()
