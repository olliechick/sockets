import socket
import select
import sys
import packet



def main(args):
    chanSenderInPort = args[0]
    chanSenderOutPort = args[1]
    chanRecvInPort = args[2]
    chanRecvOutPort = args[3]
    
    

if __name__ == "main":
    arguments = sys.argv;
    main(arguments[1:])