"""
   Packet
   A class to represent a packet of information.
   
   Author: Samuel Pell
   Date Modified: 11/08/17 (DD/MM/YY)
   
   Contains:
       __init__
       byte_conversion()
       byte_deconversion()
"""
PTYPE_DATA = 0
PTYPE_ACK = 1

class Packet:
    
    def __init__(self, magic_no, packet_type, seq_no, data_len, data):
        self.magic_no = magic_no       #determines if packet is dropped
        self.packet_type = packet_type #either dataPacket or acknowledgementPacket
        self.seq_no = seq_no           #number in the sequence
        self.data_len = data_len       #number of bytes in the data
        self.data = data               #data carried by packet
        
    """Returns the byte representation of the packet"""
    def byte_conversion(self):
        conv = str(self.magic_no)
        conv += str(self.packet_type)
        conv += str(self.seq_no)
        conv += "0" * (len(str(self.data_len)) - 3) + str(self.data_len)
        conv += str(self.data)
        return bytes(conv, "utf-8")
        
    
    """Sets the fields of this packet to that of p"""
    def byte_deconversion(self, p):
        p = str(p)
        p = p[2:-1]
        self.magic_no = int(p[:5])
        self.packet_type = int(p[5])
        self.seq_no = int(p[6])
        self.data_len = int(p[6:9])
        self.data = p[9:]
        