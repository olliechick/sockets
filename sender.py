"""
A program to send packets to a channel.
For a COSC264 assignment.

Author: Ollie Chick
Date modified: 20 August 2017
"""

import sys, socket

def main(args):
    
    # Check arguments are valid
    try:
        in_port = int(args[1])
        out_port = int(args[2])
        channel_in_port = int(args[3])
        filename = args[4]
    except:
        print("Usage: {} <in_port> <out_port> <channel_in_port> <filename>".format(args[0]))
        
    # Create sockets
    IP = ''
    
    try:
        socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_in.bind((IP, in_port))
        socket_in.listen(1)
        print("Started socket_in at port", in_port)
    except IOError: #If it fails give up and go home
        sys.exit("An IO Error occurred trying to create socket_in")
    
    try:
        socket_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_out.bind((IP, out_port))
        print("Started socket_out at port", out_port)
    except IOError: #If it fails give up and go home
        sys.exit("An IO Error occurred trying to create socket_out")
        
    # Connect out port to channel sender in port
    try:
        socket_out.connect((IP, channel_in_port))
        print("Connected socket_out to port", channel_in_port)
    except IOError: #If it fails give up and go home
        sys.exit("An IO Error occurred trying to connect socket_out")

    input('Waiting ') #to wait


if __name__ == "__main__":
    #Get arguments from commandline.
    #These should be:
    # two port numbers to use for the two sender sockets s_in and s_out
    # a port number to use for the channel socket c_s_in
    # a file name, indicating the file to send
    args = sys.argv
    
    args = ['', 15630, 15631, 15620, 'data.txt'] #this is just for testing
    
    main(args)