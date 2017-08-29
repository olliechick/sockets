"""
   channel
   A program for the COSC264-17S2 Assignment

   Authors: Samuel Pell and Ollie Chick
   Date Modified: 29 August 2017
"""

import socket
import select
import sys
import packet
import random

BIT_ERR_RATE = 0.1
IP = '127.0.0.1'
MAGIC_NO = 0x497E

def create_sending_socket(local_port, remote_port):
    """
       Creates a socket on the local_port and connects it to the
       remote_port socket. Exits the program if it fails.
    """
    try:
        #Create the socket to connect to sender's in port
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_socket.bind((IP, local_port))
        new_socket.connect((IP, remote_port))
        ##print("Started sending socket at port {} connected to {}"
              ##.format(local_port, remote_port))
    except IOError: #If it fails give up and go home
        sys.exit("An IO Error occurred trying to create and connect port on {} to {}."
                 .format(local_port, remote_port))

    return new_socket


def create_listening_socket(port):
    """
       Creates a socket to listen on the port given. Exits the program if it
       fails.
    """
    try:
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_socket.bind((IP, port))
        new_socket.listen(1)
        ##print("Started listening socket at port {}".format(port))
    except IOError: #If it fails give up and go home
        sys.exit("An IO Error occurred trying to create socket on {}.".format(port))

    return new_socket


def process_packet(data, drop_rate):
    """
       Process an input packet (as bytes) and randomly drop it or change its
       header. Returns the input packet as bytes. Returns the null byte if the
       input data is the null byte.
    """
    if data == b'':
        return data

    p = packet.Packet()
    p.decode(data)

    if p.magic_no != MAGIC_NO: #drop if magic number different
        return None
    elif random.uniform(0, 1) < drop_rate: #drop by random chance
        ##print("Dropping the packet")
        return None
    elif random.uniform(0,1) < BIT_ERR_RATE: #create a bit error
        ##print("Changing the packet")
        p.data_len += random.randint(1, 10)

    return p.encode() #return the packet's byte conversion


def main_loop(sender_in, sender_out, recv_in, recv_out, drop_rate):
    """
       Wait to recieve packets on sender_in and recv_in. When it does,
       process the packet and send it on to either recv_out or sender_out
       respectively. Takes the four socket objects as arguments.

       When one of the sockets indicates it has closed it will stop watching it
       and when both sockets have closed it will return None
    """
    sockets_to_watch = [sender_in, recv_in]

    while True:
        ##print("\n\nWaiting...", flush=True)
        readable, _, _ = select.select(sockets_to_watch, [], [])

        for s in readable:
            data = s.recv(1024)

            if data == b'': #if the packet sends out the null byte it has closed
                ##print("\nOne of the sockets sender_in or recv_in has closed")
                if s.getsockname() == recv_in.getsockname():
                    ##print("It was recv_in")
                    #if recv_in has closed stop watching it
                    sockets_to_watch = [sender_in]
                else:
                    ##print("It was sender_in")
                    if len(sockets_to_watch) == 2:
                        #if sender_in has closed and recv_in hasn't keep watching
                        #recv_in
                        sockets_to_watch = [recv_in]
                    else:
                        #if both sockets have closed. Time to clean up and exit
                        ##print("Time to go home")
                        return

            elif len(sockets_to_watch) != 1:
                #if both programs are open forward it, if not do nothing
                data_to_forward = process_packet(data, drop_rate)

                if data_to_forward != None:
                    #if the packet isn't dropped

                    if s.getsockname() == sender_in.getsockname():
                        #came from sender, send to receiver
                        ##print("Forwarding data to receiver.")
                        recv_out.send(data_to_forward)
                        ##print("Sent.")
                    else: #else came from receiver, send to sender
                        ##print("Forwarding data to sender.")
                        sender_out.send(data_to_forward)
                        ##print("Sent.")


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
        drop_rate = float(args[7])
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
    if (drop_rate >= 1) or (drop_rate < 0):
        print("drop_rate should be in the range [0, 1).")
        return

    #Create sockets
    sender_in = create_listening_socket(sender_in_port)
    recv_in = create_listening_socket(recv_in_port)

    input("Please start sender and receiver then press enter.")

    sender_out = create_sending_socket(sender_out_port, sender)
    recv_out = create_sending_socket(recv_out_port, recv)

    #Accept incomming connections to sender_in and recv_in
    try:
        sender_in, addr = sender_in.accept()
        recv_in, addr = recv_in.accept()
    except IOError:
        sys.exit("Error connecting sender_in or recv_in")

    #Enter the main loop
    main_loop(sender_in, sender_out, recv_in, recv_out, drop_rate)

    #Now that the main loop has finished close all the sockets
    sender_in.close()
    sender_out.close()
    recv_in.close()
    recv_out.close()


if __name__ == "__main__":
    args = sys.argv
    packet.replant_seed()
    s_in, s_out, c_s_in, c_s_out, c_r_in, c_r_out, r_in, r_out = packet.get_socket_numbers()
    args = ['channel.py', c_s_in, c_s_out, c_r_in, c_r_out, s_in, r_in, 0.05]
    main(args)
