#!/usr/bin/env python3

"""
   channel
   A program for the COSC264-17S2 Assignment

   Authors: Samuel Pell and Ollie Chick
   Date Modified: 30 August 2017
"""

import socket, select, sys, packet, random
from packet import Packet, MAGIC_NO, PTYPE_DATA, PTYPE_ACK
from socket_generator import create_sending_socket, create_listening_socket

BIT_ERR_RATE = 0.1


def process_packet(data, drop_rate):
    """
       Process an input packet (as bytes) and randomly drop it or change its
       header. Returns the input packet as bytes.
       Returns the null byte if the input data is the null byte.
    """
    if data == b'':
        return data

    p = Packet()
    p.decode(data)

    if p.magic_no != MAGIC_NO:
        # magic numbers is wrong: drop it
        return None
    elif random.uniform(0, 1) < drop_rate:
        # drop packet by random chance
        return None
    elif random.uniform(0,1) < BIT_ERR_RATE:
        # create a bit error by random chance (increase data len field randomly)
        p.data_len += random.randint(1, 10)

    return p.encode() # return the packet's byte conversion


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
        readable, _, _ = select.select(sockets_to_watch, [], [])

        for s in readable:
            data = s.recv(1024)

            if data == b'':
                # a socket sent out the null byte (indicating it has closed)
                if s == recv_in:
                    # receiver has closed; stop watching it
                    sockets_to_watch.remove(recv_in)
                else:
                    # sender has closed; stop watching it
                    sockets_to_watch.remove(sender_in)

                if len(sockets_to_watch) == 0:
                    # sender and receiver have closed; exit loop
                    print('\nChannel shut down.')
                    return

            elif len(sockets_to_watch) == 2:
                # sender and receiver are both open
                data_to_forward = process_packet(data, drop_rate)

                if data_to_forward != None:
                    # the packet hasn't been dropped

                    if s == sender_in:
                        # came from sender, send to receiver
                        print("sender -> channel -> receiver", end = '\r')
                        recv_out.send(data_to_forward)
                    else:
                        # came from receiver, send to sender
                        print("sender <- channel <- receiver", end = '\r')
                        sender_out.send(data_to_forward)


def main(args):
    """
       Pull the relevant numbers out of the command line arguments, check they
       are valid input, then create the appropriate sockets before entering
       into the main loop
    """
    # Check arguments are valid
    try:
        # Port numbers for this program
        sender_in_port = int(args[1])
        sender_out_port = int(args[2])
        recv_in_port = int(args[3])
        recv_out_port = int(args[4])

        # Port numbers of the sender and reciver
        sender = int(args[5])
        recv = int(args[6])

        # Probability of dropping a packet
        drop_rate = float(args[7])
    except:
        # User inputted wrong number of arguments, or non-ints/floats, etc.
        print("Usage: {} <sender_in_port> <sender_out_port> <recv_in_port> <recv_out_port> <sender> <recv> <drop_rate>".format(args[0]))
        return

    # Check that ports are in the valid range
    for port in [sender_in_port, sender_out_port, recv_in_port, \
                 recv_out_port, sender, recv]:
        if port < 1024 or port > 64000:
            print("All port numbers should be integers in the range [1024, 64000].")
            return

    # Check that the drop rate is between 0 (inclusive) and 1 (exclusive)
    if (drop_rate >= 1) or (drop_rate < 0):
        print("drop_rate should be in the range [0, 1).")
        return

    # Create in sockets
    sender_in = create_listening_socket(sender_in_port)
    recv_in = create_listening_socket(recv_in_port)
    if None in [sender_in, recv_in]:
        sys.exit("One of the in sockets failed to be created.")

    input("Please start sender and receiver then press enter.")

    # Create out sockets and connect them
    sender_out = create_sending_socket(sender_out_port, sender)
    recv_out = create_sending_socket(recv_out_port, recv)
    if None in [sender_out, recv_out]:
        sys.exit("One of the out sockets failed to be created.")

    # Accept incomming connections to sender_in and recv_in
    try:
        sender_in, addr = sender_in.accept()
        recv_in, addr = recv_in.accept()
    except IOError:
        sys.exit("Error connecting sender_in or recv_in")

    # Enter the main loop
    main_loop(sender_in, sender_out, recv_in, recv_out, drop_rate)

    # Shut down then close all the sockets (then the program)
    sender_in.shutdown(socket.SHUT_RDWR)
    sender_in.close()
    sender_out.shutdown(socket.SHUT_RDWR)
    sender_out.close()
    recv_in.shutdown(socket.SHUT_RDWR)
    recv_in.close()
    recv_out.shutdown(socket.SHUT_RDWR)
    recv_out.close()


if __name__ == "__main__":
    # Get arguments from the command line.
    # These should be:
    # * four port numbers to use for the sockets c_s_in, c_s_out, c_r_in, and c_r_out
    # * the port number where the socket s_in should be found
    # * the port number where the socket r_in should be found
    # * a packet loss rate P such that 0 <= P < 1

    args = sys.argv
    main(args)