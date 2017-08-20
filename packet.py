"""
   Packet
   A class to represent a packet of information.
   
   Authors: Samuel Pell and Ollie Chick
   Date Modified: 20 August 2017
   
   Contains:
       __init__()
       __repr__()
       __str__()
       byte_conversion()
       byte_deconversion()
"""
PTYPE_DATA = 0
PTYPE_ACK = 1

class Packet:
    
    def __init__(self, magic_no = 0, packet_type = 0, seq_no = 0, data_len = 0, data = ""):
        self.magic_no = magic_no       #determines if packet is dropped
        self.packet_type = packet_type #either dataPacket or acknowledgementPacket
        self.seq_no = seq_no           #number in the sequence
        self.data_len = data_len       #number of bytes in the data
        self.data = data               #data carried by packet
        
    def __repr__(self):
        return self.__str__() 
    
    def __str__(self):
        s =  'Magic number: {}\n'.format(self.magic_no)
        s += 'Packet type: {}\n'.format(self.packet_type)
        s += 'Seq no: {}\n'.format(self.seq_no)
        s += 'Data len: {}\n'.format(self.data_len)
        s += 'Data: "{}"'.format(self.data)
        return(s)
        
    """Returns the byte representation of the packet"""
    def byte_conversion(self):
        conv = str(self.magic_no)
        conv += str(self.packet_type)
        conv += str(self.seq_no)
        conv += "0" * (3 - len(str(self.data_len))) + str(self.data_len)
        conv += str(self.data)
        return bytes(conv, "utf-8")
        
    
    """Sets the fields of this packet to that of p"""
    def byte_deconversion(self, p):
        p = str(p)
        p = p[2:-1]
        self.magic_no = int(p[:5])
        self.packet_type = int(p[5])
        self.seq_no = int(p[6])
        self.data_len = int(p[7:10])
        self.data = p[10:]
        ##print('\n\nCreated: {}\n\n'.format(self))