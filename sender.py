#!/usr/bin/env python3

"""
   A program to send packets to a channel.
   For a COSC264 assignment.

   Author: Ollie Chick and Samuel Pell
   Date modified: 29 August 2017
"""

import sys, socket, os, select
from packet import Packet, MAGIC_NO, PTYPE_DATA, PTYPE_ACK
from socket_generator import create_sending_socket, create_listening_socket

TIMEOUT = 1 #seconds
FILE_ENCODING = 'utf8'

def inner_loop(socket_out, socket_in, bytes_to_send, next_no):
    """
       Function to continuously send a packet until a valid acknowledgement
       packet is recieved. Returns the number of packets sent from sender to
       achieve successful transmission.
    """
    packets_sent = 0

    while True:
        # Send packet
        socket_out.send(bytes_to_send)
        packets_sent += 1

        # Await a response
        readable, _, _ = select.select([socket_in], [], [], TIMEOUT)

        if readable:
            # got a response
            s = readable[0]
            data = s.recv(1024)

            rcvd = Packet()
            rcvd.decode(data)

            if rcvd.is_valid_ack(next_no):
                # got a valid acknowledgement packet
                next_no = 1 - next_no
                return packets_sent, next_no


def main(args):
    # Check arguments are valid
    try:
        in_port = int(args[1])
        out_port = int(args[2])
        channel_in_port = int(args[3])
        filename = args[4]
    except:
        print("Usage: {} <in_port> <out_port> <channel_in_port> <filename>".format(args[0]))
        return
    
    # Check that ports are in the valid range
    for port in [in_port, out_port, channel_in_port]:
        if port < 1024 or port > 64000:
            print("All port numbers should be integers in the range [1024, 64000].")
            return


    # Create sockets (and connect socket_out)
    socket_in = create_listening_socket(in_port)
    socket_out = create_sending_socket(out_port, channel_in_port)
    if None in [socket_in, socket_out]:
        sys.exit("One of the sockets failed to be created.")

    # Check if file exists
    if not os.path.isfile(filename):
        # file does not exist
        sys.exit("Error: {} does not exist.".format(filename))

    # Initialisation
    next_no = 0
    packets_sent = 0
    exit_flag = False
    file = open(filename, "rb")
    input("Please acknowledge on the channel that you have started the sender, then press enter.")

    # Accept connection from channel
    socket_in, addr = socket_in.accept()
    print("Sending data...")

    # Outer loop
    i = 0
    while not exit_flag:
        # Read 512 bytes from file
        data = file.read(512)

        # Prepare packet
        packet_type = PTYPE_DATA
        seq_no = next_no
        data_len = len(data)
        if data_len == 0:
            exit_flag = True
        pack = Packet(MAGIC_NO, packet_type, seq_no, data_len, data)

        # Inner loop
        bytes_to_send = pack.encode()
        print("Sending datum {}".format(i), end = "\r")
        packets_used, next_no = inner_loop(socket_out, socket_in, bytes_to_send,
                                           next_no)
        packets_sent += packets_used
        i+=1

    # Clean up and close
    file.close()
    socket_in.shutdown(socket.SHUT_RDWR)
    socket_in.close()
    socket_out.shutdown(socket.SHUT_RDWR)
    socket_out.close()
    print("\nData sent.\nPackets sent: {}".format(packets_sent))


if __name__ == "__main__":
    # Get arguments from the command line.
    # These should be:
    # * two port numbers to use for the two sender sockets s_in and s_out
    # * the port number where the socket c_s_in should be found
    # * a file name, indicating the file whose contents should be sent
    
    args = sys.argv
    main(args)