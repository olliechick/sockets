"""
A program to send packets to a channel.
For a COSC264 assignment.

Author: Ollie Chick and Samuel Pell
Date modified: 29 August 2017
"""

import sys, socket, os, packet, select

MAGIC_NO = 0x497E
IP = '127.0.0.1'
TIMEOUT = 1 #seconds
FILE_ENCODING = 'utf8'

def inner_loop(socket_out, socket_in, bytes_to_send, next_no):
    """
       Function to continuously send a packet until a valid acknowledgement
       packet is recieved. Returns the number of packets sent from sender to
       achieve successful transmission.
    """
    ##print(bytes_to_send)
    packets_sent = 0

    while True:
        # Send packet
        socket_out.send(bytes_to_send)
        ##print("Packet sent...")
        packets_sent += 1

        # Await a response
        readable, _, _ = select.select([socket_in], [], [], TIMEOUT)

        if readable:
            #got a response
            ##print('Response received.')
            s = readable[0]
            data = s.recv(1024)

            rcvd = packet.Packet()
            rcvd.decode(data)

            if rcvd.is_valid_ack(next_no):
                #got a valid acknowledgement packet
                next_no = 1 - next_no
                return packets_sent, next_no
        ##else:
            ##print("No response, retransmitting.")


def main(args):
    # Check arguments are valid
    try:
        in_port = int(args[1])
        out_port = int(args[2])
        channel_in_port = int(args[3])
        filename = args[4]
    except:
        print("Usage: python3 {} <in_port> <out_port> <channel_in_port> <filename>".format(args[0]))
        return
    else:
        for port in [in_port, out_port, channel_in_port]:
            if port < 1024 or port > 64000:
                print("All port numbers should be integers in the range [1024, 64000].")
                return

    packets_sent = 0

    # Create sockets and connect socket_out
    try:
        socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_in.bind((IP, in_port))
        socket_in.listen(2)
        ##print("Started socket_in at port", in_port)
    except IOError: #If it fails give up and go home
        socket_in.close()
        sys.exit("An IO Error occurred trying to create socket_in.")

    try:
        socket_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_out.bind((IP, out_port))
        ##print("Started socket_out at port", out_port)
        socket_out.connect((IP, channel_in_port))
        ##print("Connected socket_out to port", channel_in_port)
    except IOError: #If it fails give up and go home
        socket_in.close()
        socket_out.close()
        sys.exit("An IO Error occurred trying to create and connect socket_out.")


    # Check if file exists
    if not os.path.isfile(filename):
        #file does not exist
        sys.exit("Error: {} does not exist.".format(filename))

    # Initialisation
    next_no = 0
    exit_flag = False
    file = open(filename, "rb")
    input("Please acknowledge on the channel that you have started the sender, then press enter.")

    # Accept connection from channel
    socket_in, addr = socket_in.accept()

    # Outer loop
    while not exit_flag:
        ##print("\n\n\n")
        # Read 512 bytes from file
        data = file.read(512)
        ##print("Read data:", data)
        ##print("Successfully read data.")
        data = data.decode(FILE_ENCODING)

        # Prepare packet
        packet_type = packet.PTYPE_DATA
        seq_no = next_no
        data_len = len(data)
        if data_len == 0:
            exit_flag = True

        pack = packet.Packet(MAGIC_NO, packet_type, seq_no, data_len, data)
        ##print('Packet of length', len(pack))

        # Inner loop
        bytes_to_send = pack.encode()

        packets_used, next_no = inner_loop(socket_out, socket_in, bytes_to_send,
                                           next_no)

        packets_sent += packets_used

    #clean up and close
    ##print("WARNING! CLOSING SOCKETS!")
    file.close()
    socket_in.close()
    socket_out.close()
    print("Packets sent: {}".format(packets_sent))


if __name__ == "__main__":
    # Get arguments from the command line.
    # These should be:
    # * two port numbers to use for the two sender sockets s_in and s_out
    # * a port number to use for the channel socket c_s_in
    # * a file name, indicating the file to send
    args = sys.argv

    filename = 'input'

    s_in, s_out, c_s_in, c_s_out, c_r_in, c_r_out, r_in, r_out = packet.get_socket_numbers() ##just for testing
    args = ['sender.py', s_in, s_out, c_s_in, filename] ##just for testing

    main(args)
