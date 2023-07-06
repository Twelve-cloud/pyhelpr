#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
httpserver.py: Simple http server just practice http.server module.
"""


from http.server import HTTPServer, BaseHTTPRequestHandler


PORT = 8000
IPV4 = 'localhost'
ADDRESS = (IPV4, PORT)


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'plain/text')
        self.end_headers()
        self.wfile.write(b'Hello from Server!')

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        print(data.decode())
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "OK"}')


server = HTTPServer(ADDRESS, RequestHandler)
server.serve_forever()
