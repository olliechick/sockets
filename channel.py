"""
   channel
   A program for the COSC264-17S2 Assignment
   
   Author: Samuel Pell
   Date Modified: 10/08/17 (DD/MM/YY)
"""

import socket
import select
import sys
import packet
import random as rand


BIT_ERR_RATE = 0.1
DROP_RATE = 0


def process_packet(data):
    p = packet.Packet(0,0,0,0,0)
    p.byte_deconversion(data)
    if p.magic_no != 0x497E: #drop if magic number different
        return None
    elif rand.uniform(0, 1) < DROP_RATE: #drop by random chance
        return None
    elif rand.uniform(0,1) < BIT_ERR_RATE: #create a bit error
        p.data_len += int(rand.uniform(1, 10))
    
    return p.byte_conversion() #return the packets byte conversion


def main_loop(sender_in, sender_out, recv_in, recv_out):
    while True:
        readable, _, _ = select.select([sender_in, recv_in], [], [])
        for s in readable:
            conn, addr = s.accept()
            data = conn.recv(1024)
            data_to_forward = process_packet(data)
            if s.getsockname() == sender_in.getsockname(): #came from sender send to reciever
                recv_out.sendall(data_to_forward)
            else: #else send to sender
                sender_out.sendall(data_to_forward)

def main(args):
    #Port numbers for this program
    sender_in_port = int(args[0])
    sender_out_port = int(args[1])
    recv_in_port = int(args[2])
    recv_out_port = int(args[3])
    
    #Port numbers of the sender and reciver
    sender = int(args[4])
    recv = int(args[5])
    
    #Probability of dropping a packet
    DROP_RATE = float(args[6])
    
    #Creating sockets to communicate with the outside world
    try:
        sender_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_in.bind(("", sender_in_port))
        sender_in.listen(1)
        print("Started sender_in")
    except IOError: #If it fails give up and go home
        print("An IO Error occurred trying to create sender_in")
        sys.exit()
        
    try:
        recv_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recv_in.bind(("", recv_in_port))
        recv_in.listen(1)
        print("Started recv_in")
    except IOError:
        print("An IO Error occurred trying to create recv_in")
        sys.exit()
    
    out = input("Please start sender and reciever and then press enter")
    
    try:
        sender_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_out.bind(("", sender_out_port))
        sender_out.connect(("", sender))
        print("Started sender_out")
    except IOError:
        print("An IO Error occurred trying to connect to sender")
        sys.exit()
    
    try:    
        recv_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recv_out.bind(("", recv_out_port))
        recv_out.connect(("", recv))
        print("Started recv_out")
    except IOError:
        print("An IO Error occurred trying to connect to reciever")
        sys.exit()
        
    main_loop()


if __name__ == "__main__":
    ##args = sys.argv[1:]
    args = [15620, 15646, 15465, 15466, 17968, 14567, 12]
    main(args)
