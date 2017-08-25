"""
   channel
   A program for the COSC264-17S2 Assignment
   
   Authors: Samuel Pell and Ollie Chick
   Date Modified: 21 August 2017
"""

import socket
import select
import sys
import packet
import random

BIT_ERR_RATE = 0.1
DROP_RATE = 0
IP = '127.0.0.1'


def process_packet(data):
    """
       Process an input packet (as bytes) and randomly drop it or change its 
       header. Returns the input packet as bytes.
    """
    return data #just for testing - packet errors will be introduced later
    ##p = packet.Packet()
    ##p.decode(data)
    ##print(p.data)
    ##if p.magic_no != 0x497E: #drop if magic number different
        ##return None
    ##elif random.uniform(0, 1) < DROP_RATE: #drop by random chance
        ##return None
    ##elif random.uniform(0,1) < BIT_ERR_RATE: #create a bit error
        ##p.data_len += int(random.uniform(1, 10))
    
    ##return p.encode() #return the packet's byte conversion


def main_loop(sender_in, sender_out, recv_in, recv_out):
    """
       Wait to recieve packets on sender_in and recv_in. When it does,
       process the packet and send it on to either recv_out or sender_out
       respectively. Takes the four socket objects as arguments.
       
       When one of the sockets indicates it has closed it will stop watching it
       and when both sockets have closed it will return None
    """
    sockets_to_watch = [sender_in, recv_in]
    while True:
        print("\n\n\nWaiting...", flush=True)
        readable, _, _ = select.select(sockets_to_watch, [], [])
        print("Got something hopefully")
        
        for s in readable:
            data = s.recv(1024)
            print("Got some data:", data)
            
            if data == b'':
                print("\n\nOne of the sockets sender_in or recv_in has closed")
                if s.getsockname() == recv_in.getsockname():
                    print("It was recv_in")
                    #if recv_in has closed stop watching it
                    sockets_to_watch = [sender_in]
                else:
                    print("It was sender_in")
                    if len(sockets_to_watch) == 2:
                        #if sender_in has closed and recv_in hasn't keep watching
                        #sender in
                        sockets_to_watch = [recv_in]
                    else:
                        #if both sockets have closed. Time to clean up and exit
                        print("Time to go home")
                        return
            else:
                data_to_forward = process_packet(data)
                ##NOT SURE IF THIS PART WORKS
                if data_to_forward != None: #if the packet isn't dropped
                    if s.getsockname() == sender_in.getsockname():
                        #came from sender, send to receiver
                        print("Forwarding data to receiver.")
                        recv_out.send(data_to_forward)
                        print("Sent.")
                    else: #else came from receiver, send to sender
                        print("Forwarding data to sender.")
                        sender_out.send(data_to_forward)
                        print("Sent.")


def main(args):
    """
       Pull the relevant numbers out of the command line arguments, check they
       are valid input, then create the appropriate sockets before entering
       into the main loop
    """
    try:
        #Port numbers for this program
        sender_in_port = int(args[1])
        sender_out_port = int(args[2])
        recv_in_port = int(args[3])
        recv_out_port = int(args[4])
        
        #Port numbers of the sender and reciver
        sender = int(args[5])
        recv = int(args[6])
        
        #Probability of dropping a packet
        DROP_RATE = float(args[7])
    except:
        print("""Usage: python3 {} <sender_in_port> <sender_out_port> <recv_in_port> <recv_out_port> <sender> <recv> <drop_rate>""".format(args[0]))
        return
    
    # Check that ports are in the valid range
    for port in [sender_in_port, sender_out_port, recv_in_port, \
                 recv_out_port, sender, recv]:
        if port < 1024 or port > 64000:
            print("All port numbers should be integers in the range [1024, 64000].")
            return
        
        
    #Check that the drop rate is between 0 and 1
    if (DROP_RATE > 1) or (DROP_RATE < 0): ##CHANGE ME WHEN TESTING FINISHED
        print("drop_rate should be in the range [0, 1).") 
        return
    
    try:
        #Create the socket to be connected to by sender's out port
        sender_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_in.bind((IP, sender_in_port))
        sender_in.listen(100)
        print("Started sender_in at port {}".format(sender_in_port))
    except IOError: #If it fails give up and go home
        sys.exit("An IO Error occurred trying to create sender_in.")
        
    try:
        #Create the socket to be connected to by recievers's out port
        recv_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recv_in.bind((IP, recv_in_port))
        recv_in.listen(100)
        print("Started recv_in at port {}".format(recv_in_port))
    except IOError: #If it fails give up and go home
        sys.exit("An IO Error occurred trying to create recv_in.")
    
    input("Please start sender and receiver then press enter.")
    
    try:
        #Create the socket to connect to sender's in port
        sender_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_out.bind((IP, sender_out_port))
        sender_out.connect((IP, sender))
        print("Started sender_out ")
    except IOError: #If it fails give up and go home
        sys.exit("An IO Error occurred trying to connect to sender at port {}.".format(sender))
    
    try:
        #Create the socket to connect to recievers in port
        recv_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recv_out.bind((IP, recv_out_port))
        recv_out.connect((IP, recv))
        print("Started recv_out")
    except IOError: #If it fails give up and go home
        sys.exit("An IO Error occurred trying to connect to receiver at port {}.".format(recv))
        
        
    sender_in, addr = sender_in.accept()
    recv_in, addr = recv_in.accept()
    
    main_loop(sender_in, sender_out, recv_in, recv_out)
    
    sender_in.close()
    sender_out.close()
    recv_in.close()
    recv_out.close()


if __name__ == "__main__":
    args = sys.argv
    packet.replant_seed()
    s_in, s_out, c_s_in, c_s_out, c_r_in, c_r_out, r_in, r_out = packet.get_socket_numbers()
    args = ['channel.py', c_s_in, c_s_out, c_r_in, c_r_out, s_in, r_in, 1]
    main(args)
