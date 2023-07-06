#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
httpclient.py: Simple http client just practice http.client module.
"""


from http.client import HTTPConnection


connection = HTTPConnection('localhost', 8000)

connection.request('GET', 'localhost:8000/')
response = connection.getresponse()
message = response.read()
print(message.decode())

connection.request('POST', 'localhost:8000/', b'Hello from Client!', {'Content-Lenght': '18'})
response = connection.getresponse()
message = response.read()
print(message.decode())
