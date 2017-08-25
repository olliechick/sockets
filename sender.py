"""
A program to send packets to a channel.
For a COSC264 assignment.

Author: Ollie Chick and Samuel Pell
Date modified: 24 August 2017
"""

import sys, socket, os, packet, select

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
        
    # Create sockets
    IP = '127.0.0.1'
    packets_sent = 0
    
    try:
        socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_in.bind((IP, in_port))
        socket_in.listen(2)
        print("Started socket_in at port", in_port)
    except IOError: #If it fails give up and go home
        socket_in.close()
        sys.exit("An IO Error occurred trying to create socket_in.")
    
    try:
        socket_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_out.bind((IP, out_port))
        print("Started socket_out at port", out_port)
    except IOError: #If it fails give up and go home
        socket_in.close()
        socket_out.close()
        sys.exit("An IO Error occurred trying to create socket_out.")
        
    # Connect out port to channel sender in port
    try:
        socket_out.connect((IP, channel_in_port))
        print("Connected socket_out to port", channel_in_port)
    except IOError: #If it fails give up and go home
        socket_in.close()
        socket_out.close()
        sys.exit("An IO Error occurred trying to connect socket_out.")
        
    # Check if file exists
    if not os.path.isfile(filename):
        #file does not exist
        sys.exit("Error: {} does not exist.".format(filename))
       
    # Initialisation 
    next_no = 0
    exit_flag = False
    file = open(filename, "rb")
    input("Please acknowledge on the channel that you have started the sender, then press enter.")
    
    
    socket_in, addr = socket_in.accept()    
    
    # Outer loop
    while True:
        print("\n\n\n")
        # Read 512 bytes from filename
        data = file.read(512)
        print("Read data:", data)
        data = data.decode('utf8')
        
        # Prepare packet
        magic_no = 0x497E
        packet_type = packet.PTYPE_DATA
        seq_no = next_no
        data_len = len(data)
        if data_len == 0:
            exit_flag = True
        pack = packet.Packet(magic_no, packet_type, seq_no, data_len, data)
        print('Packet of length', len(pack))
        
        # Testing
        ##print(pack)
        ##pack_bytes = pack.encode()
        ##print(pack_bytes)
        ##p = packet.Packet(0,0,0,0,0)
        ##p.decode(pack_bytes)
        ##print(p)
        
        
        # Place pack into a buffer, packetBuffer
        ## ?????????
        
        # Inner loop
        return_to_outer_loop = False
        bytes_to_send = pack.encode()
        while True and not return_to_outer_loop:
            # Send packet
            print(socket_out, '= socket_out')
            socket_out.send(bytes_to_send)
            packets_sent += 1
            print("Sent to socket ", socket_out)
            
            # Await a response
            timeout = 3 #seconds
            readable, _, _ = select.select([socket_in], [], [], timeout)
            if readable:
                #got a response
                print('got a response')
                s = readable[0]
                data = s.recv(1024)
                rcvd = packet.Packet()
                rcvd.decode(data)
                if rcvd.magic_no == 0x497E and rcvd.packet_type == packet.PTYPE_ACK \
                   and rcvd.data_len == 0 and rcvd.seq_no == next_no:
                    next_no = 1 - next_no
                    if exit_flag:
                        print("WARNING! CLOSING SOCKETS!")  
                        file.close()
                        socket_in.close()
                        socket_out.close()
                        print(packets_sent, "packets sent.")
                        return
                    else:
                        return_to_outer_loop = True
            else:
                print("No response.")
                

    print("WARNING! CLOSING SOCKETS!")                    
    file.close()
    socket_in.close()
    socket_out.close()


if __name__ == "__main__":
    # Get arguments from the command line.
    # These should be:
    # * two port numbers to use for the two sender sockets s_in and s_out
    # * a port number to use for the channel socket c_s_in
    # * a file name, indicating the file to send
    args = sys.argv
    
    # Available files:
    # Name          Size (characters)
    #
    # data.txt      1473
    # small.txt     6
    
    filename = 'pg4300.txt'

    s_in, s_out, c_s_in, c_s_out, c_r_in, c_r_out, r_in, r_out = packet.get_socket_numbers()        
    args = ['sender.py', s_in, s_out, c_s_in, filename] ##this is just for testing
    
    main(args)
