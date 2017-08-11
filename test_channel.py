import socket
from packet import Packet

HOST = ''
SENDER_PORT = 15633
OUT_PORT = 15620
RECIEVER_PORT = 15640

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
input("Start Sockets?")

print("Starting reciever")
s2.bind(('', RECIEVER_PORT))
s2.listen(1)
print("Started reciever")
print("Starting sender")
s.bind((HOST, SENDER_PORT))
print("Started sender")


input("Send data?")
s.connect((HOST, OUT_PORT))
p = Packet(0x497E, 0, 0, 20, "*"*20)
s.sendall(p.byte_conversion())
print("Data sent")


print("Accepting connections to sender")
conn, addr = s2.accept()
data = conn.recv(1024)

n = Packet(0,0,0,0,0)
n.byte_deconversion(data)
print("Received " + n.data)

s.close()
s2.close()