import socket
from packet import Packet, get_socket_numbers

s_in, s_out, c_s_in, c_s_out, c_r_in, c_r_out, r_in, r_out = get_socket_numbers()

HOST = ''
SENDER_PORT = s_in + 3
OUT_PORT = c_s_in
RECIEVER_PORT = r_in

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
s.sendall(p.encode())
print("Data sent")


print("Accepting connections to sender")
conn, addr = s2.accept()
data = conn.recv(1024)

n = Packet(0,0,0,0,0)
n.decode(data)
print("Received " + n.data)


print(s)

input()

p = Packet(0x497E, 0, 1, 20, "k"*20)
s.sendall(p.encode())
print("Data sent")


print("Accepting connections to sender")
conn, addr = s2.accept()
data = conn.recv(1024)

n = Packet(0,0,0,0,0)
n.decode(data)
print("Received " + n.data)

s.close()
s2.close()