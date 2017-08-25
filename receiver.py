"""
A program to receive packets from a channel.
For a COSC264 assignment.

Author: Ollie Chick
Date modified: 20 August 2017
"""

import sys, socket, packet, os, select

def main(args):
    
    VALID_MAGIC_NO = 0x497E
    
    # Check arguments are valid
    try:
        in_port = int(args[1])
        out_port = int(args[2])
        channel_in_port = int(args[3])
        filename = args[4]
    except:
        print("Usage: python3 {} <in_port> <out_port> <channel_in_port> <filename>".format(args[0]))
    else:
        for port in [in_port, out_port, channel_in_port]:
            if port < 1024 or port > 64000:
                print("All port numbers should be integers in the range [1024, 64000].")
                return        
            
    # Create sockets
    IP = '127.0.0.1'
    
    try:
        socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_in.bind((IP, in_port))
        socket_in.listen(2)
        print("Started socket_in at port", in_port)
    except IOError: #If it fails give up and go home
        sys.exit("An IO Error occurred trying to create socket_in.")
    
    try:
        socket_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_out.bind((IP, out_port))
        print("Started socket_out at port", out_port)
    except IOError: #If it fails give up and go home
        sys.exit("An IO Error occurred trying to create socket_out.")
        
    # Connect out port to channel sender in port
    try:
        socket_out.connect((IP, channel_in_port))
        print("Connected socket_out to port", channel_in_port)
    except IOError: #If it fails give up and go home
        sys.exit("An IO Error occurred trying to connect socket_out.")
        
    # Check if file exists - commented out for testing purposes
    ##if os.path.isfile(filename):
        ##sys.exit("Error: {} already exists.".format(filename))
        
    # Initialisation
    expected = 0
    file = open(filename, 'w')
    input("Please acknowledge on the channel that you have started the receiver, then press enter.")
    
    socket_in, addr = socket_in.accept()    
        
    # Main loop
    while True:
        print("\n\n\nWaiting...", flush=True)
        readable, _, _ = select.select([socket_in], [], [])
        #got a response
        print('got a response')
        s = readable[0]
        data = s.recv(1024)
        rcvd = packet.Packet()
        rcvd.decode(data)
        if rcvd.magic_no == VALID_MAGIC_NO and rcvd.packet_type == packet.PTYPE_DATA:
            print("Valid packet")
            magic_no = VALID_MAGIC_NO
            packet_type = packet.PTYPE_ACK
            seq_no = rcvd.seq_no
            data_len = 0
            data = ""
            pack = packet.Packet(magic_no, packet_type, seq_no, data_len, data)
            socket_out.send(pack.encode())
            print("Sent reply")
            if rcvd.seq_no == expected:
                expected = 1 - expected
                if rcvd.data_len > 0:
                    file.write(rcvd.data)
                else:
                    #data_len = 0
                    print("WARNING! CLOSING SOCKETS!")
                    file.close()
                    socket_in.close()
                    socket_out.close()
                    return
                    
            
        # else do NOTHING! just go back to the start of the loop

    print("WARNING! CLOSING SOCKETS!")        
    file.close()
    socket_in.close()
    socket_out.close()


if __name__ == "__main__":
    # Get arguments from the command line.
    # These should be:
    # * two port numbers to use for the two receiver sockets r_in and r_out
    # * a port number to use for the channel socket c_r_in
    # * a file name, indicating where the received data should be stored
    args = sys.argv
    
    s_in, s_out, c_s_in, c_s_out, c_r_in, c_r_out, r_in, r_out = packet.get_socket_numbers()    
    args = ['sender.py', r_in, r_out, c_r_in, 'rec.txt'] ##this is just for testing
    
    main(args)