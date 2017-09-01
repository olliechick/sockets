"""
   A program to receive packets from a channel.
   For a COSC264 assignment.

   Author: Ollie Chick
   Date modified: 29 August 2017
"""

import sys, socket, os, select
from packet import Packet, MAGIC_NO, PTYPE_DATA, PTYPE_ACK
from socket_generator import create_sending_socket, create_listening_socket

def main(args):
    # Check arguments are valid
    try:
        in_port = int(args[1])
        out_port = int(args[2])
        channel_in_port = int(args[3])
        filename = args[4]
    except:
        print("Usage: {} <in_port> <out_port> <channel_in_port> <filename>".format(args[0]))
    
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
    if os.path.isfile(filename):
        sys.exit("Error: {} already exists.".format(filename))

    # Initialisation
    expected = 0
    file = open(filename, 'w')
    input("Please acknowledge on the channel that you have started the receiver, then press enter.")

    # Accept connection from channel
    socket_in, addr = socket_in.accept()

    # Main loop
    while True:
        readable, _, _ = select.select([socket_in], [], [])
        # got a response
        s = readable[0]
        data = s.recv(1024)
        rcvd = Packet()
        rcvd.decode(data)

        if rcvd.is_valid_data():
            # got a valid data packet
            
            # Prepare an acknowledgement packet and send it
            magic_no = MAGIC_NO
            packet_type = PTYPE_ACK
            seq_no = rcvd.seq_no
            data_len = 0
            data = ""
            pack = Packet(magic_no, packet_type, seq_no, data_len, data)
            socket_out.send(pack.encode())
            print("Sent reply")

            if rcvd.seq_no == expected:
                expected = 1 - expected
                if rcvd.data_len > 0:
                    # has some data
                    file.write(rcvd.data)
                else:
                    # no data - indicates end of file
                    file.close()
                    socket_in.shutdown(socket.SHUT_RDWR)
                    socket_in.close()
                    socket_out.shutdown(socket.SHUT_RDWR)
                    socket_out.close()
                    return


if __name__ == "__main__":
    # Get arguments from the command line.
    # These should be:
    # * two port numbers to use for the two receiver sockets r_in and r_out
    # * the port number where the socket c_r_in should be found
    # * a file name, indicating where the received data should be stored
    
    args = sys.argv
    main(args)