#!/usr/bin/env python3
"""
Simple Frontend HTTP Server

Serves the frontend HTML file over HTTP to avoid CORS issues.
"""

import http.server
import socketserver
import webbrowser
import threading
import time
from pathlib import Path

PORT = 3000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def do_GET(self):
        # Serve the frontend_simple.html as index
        if self.path == '/' or self.path == '/index.html':
            self.path = '/frontend_simple.html'
        return super().do_GET()

def start_server():
    """Start the HTTP server for the frontend."""
    
    # Change to the project directory
    os.chdir('/Users/michaelkim/code/Bernstein')
    
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"🌐 Frontend server running at: http://localhost:{PORT}")
        print(f"📱 Open in browser: http://localhost:{PORT}")
        print(f"🔧 Backend API: http://localhost:8000")
        print(f"✅ CORS issues resolved!")
        print(f"")
        print(f"Press Ctrl+C to stop the server")
        
        # Auto-open browser after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open(f'http://localhost:{PORT}')
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n🛑 Frontend server stopped")

if __name__ == "__main__":
    import os
    start_server()
