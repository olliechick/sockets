"""
   channel
   A program for the COSC264-17S2 Assignment
   
   Author: Samuel Pell
   Date Modified: 10/08/17 (DD/MM/YY)
"""

import socket
import select
import sys
from packet import Packet
import random as rand


BIT_ERR_RATE = 0.1


def process_packet(data):
    p = Packet(0,0,0,0,0)
    p.byte_deconversion(data)
    if p.magic_no != 0x497E: #drop if magic number different
        return None
    elif rand.uniform(0, 1) < drop_rate: #drop by random chance
        return None
    elif rand.uniform(0,1) < BIT_ERR_RATE: #create a bit error
        p.data_len += int(rand.uniform(1, 10))
    
    return p.byte_conversion() #return the packets byte conversion


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
    drop_rate = float(args[6])
    
    #Creating sockets to communicate with the outside world
    try:
        sender_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_in.bind(("", sender_in_port))
        sender_in.accept()
    except IOError:
        print("An IO Error occurred trying to create sender_in")
    
    try:
        recv_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recv_in.bind(("", recv_in_port))
        recv_in.accept()
    except IOError:
        print("An IO Error occurred trying to create recv_in")
    
    
    try:
        sender_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_out.bind(("", sender_out_port))
        sender_out.connect(("", sender))
    except IOError:
        print("An IO Error occurred trying to connect to sender")
    
    try:    
        recv_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recv_out.bind(("", recv_out_port))
        recv_out.connect(("", sender))
    except IOError:
        print("An IO Error occurred trying to connect to reciever")


if __name__ == "__main__":
    ##args = sys.argv[1:]
    args = [15645, 15646, 15465, 15466, 17968, 14567, 12]
    main(args)
