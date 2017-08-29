"""
Socket generator
   Program to generate sending and listening sockets.
   Authors: Samuel Pell and Ollie Chick
   Date modified: 29 August 2017
"""
import socket

IP = '127.0.0.1'

def create_sending_socket(local_port, remote_port):
    """
       Creates a socket on the local_port and connects it to the
       remote_port socket, then returns that socket.
       If it fails, returns None.
    """
    try:
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_socket.bind((IP, local_port))
        new_socket.connect((IP, remote_port))
    except IOError: 
        new_socket = None

    return new_socket


def create_listening_socket(port):
    """
       Creates a socket to listen on the port given, then returns that socket.
       If it fails, returns None.
    """
    try:
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_socket.bind((IP, port))
        new_socket.listen(1)
    except IOError:
        new_socket = None
        
    return new_socket