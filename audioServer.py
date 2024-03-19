import os
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def serve_directory(directory, port):
    os.chdir(directory)
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

def isServerRunning(port=8512):
    return is_port_in_use(port)

def confirmServerStart(port=8512):
    if isServerRunning(port):
        print(f"Port {port} is already in use.")
        return True
    
    try:
        audio_files_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'Audio Files')
        print(f"Starting server to serve the 'Audio Files' directory on port {port}.")
        thread = threading.Thread(target=serve_directory, args=(audio_files_directory, port), daemon=True)
        thread.start()
        print(f"Serving 'Audio Files' at http://localhost:{port}")
        return True
    except Exception as e:
        print(f"Failed to start the server on port {port}: {e}")
        return False


