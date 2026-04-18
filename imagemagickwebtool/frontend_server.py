#!/usr/bin/env python3
"""
Simple HTTP server for Image Mutation Tool frontend
Serves static HTML on port 3000
No Node.js required - pure Python solution
"""

import http.server
import socketserver
import os
import json
from urllib.parse import urlparse
from pathlib import Path

PORT = 3000
HANDLER = http.server.SimpleHTTPRequestHandler

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler with CORS headers"""
    
    def end_headers(self):
        # Add CORS headers to allow requests from localhost:5000
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        """Handle OPTIONS requests"""
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        # Serve advanced-index.html for root path
        if self.path == '/' or self.path == '':
            self.path = '/advanced-index.html'
        
        return super().do_GET()

    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[{self.client_address[0]}] {format % args}")

if __name__ == '__main__':
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Get hostname for network access
    import socket
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "127.0.0.1"
    
    print("\n" + "="*70)
    print("  🎨 Image Mutation Tool - Frontend Server")
    print("="*70)
    print(f"\n📍 Frontend Server Access:")
    print(f"   Local:        http://localhost:{PORT}")
    print(f"   Local IP:     http://{local_ip}:{PORT}")
    print(f"   Network:      http://{hostname}:{PORT}")
    print(f"\n📁 Root directory: {project_dir}")
    print(f"\n✅ Recommended: Use one of the above URLs in your browser")
    print(f"\n⚙️  Backend API Configuration:")
    print(f"   The app will automatically detect the API endpoint")
    print(f"   Backend should be running on port 5000")
    print(f"   Ensure backend is accessible from: http://{local_ip}:5000")
    print(f"\n⚠️  Press Ctrl+C to stop the server\n")
    print("="*70 + "\n")
    
    try:
        # Listen on localhost only (127.0.0.1)
        with socketserver.TCPServer(("127.0.0.1", PORT), CORSRequestHandler) as httpd:
            httpd.allow_reuse_address = True
            print(f"✅ Server running on localhost only (127.0.0.1:{PORT})")
            print(f"✅ Waiting for connections...\n")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped by user")
    except OSError as e:
        if e.errno == 48 or e.errno == 98:
            print(f"\n❌ Error: Port {PORT} is already in use")
            print(f"   Try: lsof -i :{PORT}   (to find what's using it)")
            print(f"   Or kill existing process: kill -9 <PID>")
            print(f"   Or use a different port by editing this script")
        else:
            print(f"\n❌ Error: {e}")
