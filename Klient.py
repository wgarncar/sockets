from socket import *
import socket

s = socket.socket(AF_INET, SOCK_STREAM)
port = 8888
host = socket.gethostname()

s.connect((host, port))
print (bytes(s.recv(1234)).decode())
opcja = input()
s.send(opcja.encode())
if opcja == '2':
    text = input()
    s.send(text.encode())
    priority = input()
    s.send(priority.encode())
if opcja == '3':
    id = input()
    s.send(id.encode())
if opcja == '4':
    priority = input()
    s.send(priority.encode())
print(bytes(s.recv(123)).decode())
s.close()