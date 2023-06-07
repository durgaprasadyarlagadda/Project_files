from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json

DATABASE = 'users.db'

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        form_data = parse_form_data(post_data)

        if self.path == '/signup':
            result = handle_signup(form_data)
        elif self.path == '/signin':
            result = handle_signin(form_data)
        else:
            result = {'error': 'Invalid path'}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = 'File not found'
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

def parse_form_data(data):
    form_data = {}
    items = data.split('&')
    for item in items:
        if '=' in item:
            key, value = item.split('=', 1)
            form_data[key] = value
    return form_data


def handle_signup(form_data):
    return {'message': 'Sign up successful'}

def handle_signin(form_data):
    return {'message': 'Sign in successful'}

def run_server():
    server_address = ('', 5500)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Server started on port 5500')
    httpd.serve_forever()

if __name__ == '__main__':
    conn = sqlite3.connect(DATABASE)
    conn.close()
    run_server()
