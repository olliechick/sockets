"""
   Packet
   A class to represent a packet of information.
   
   Authors: Samuel Pell and Ollie Chick
   Date Modified: 21 August 2017
   
   Contains:
       __init__()
       __repr__()
       __str__()
       encode()
       decode()
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
        pt = 'unknown'
        if self.packet_type == 0:
            pt = 'data'
        elif self.packet_type == 1:
            pt = 'ack'
            
        s =  'Magic number: {}\n'.format(self.magic_no)
        s += 'Packet type: {} ({})\n'.format(self.packet_type, pt)
        s += 'Seq no: {}\n'.format(self.seq_no)
        s += 'Data len: {}\n'.format(self.data_len)
        s += 'Data: "{}"'.format(self.data)
        return(s)
        
    
    def encode(self):
        """Returns the byte representation of the packet"""
        conv = str(self.magic_no)
        conv += str(self.packet_type)
        conv += str(self.seq_no)
        conv += "0" * (3 - len(str(self.data_len))) + str(self.data_len)
        conv += str(self.data)
        print("Encoded {}-{} ({}) successfully.".format(self.packet_type, 
                                                        self.seq_no, 
                                                        self.data_len))
        return bytes(conv, "utf-8")
        
    
    
    def decode(self, data):
        """Sets the fields of this packet to that of data"""
        try:
            print("Attempting to deconvert", data)
            data = data.decode()
            self.magic_no = int(data[:5])
            self.packet_type = int(data[5])
            self.seq_no = int(data[6])
            self.data_len = int(data[7:10])
            self.data = data[10:]
            print('Success! Created: {}'.format(self))
        except:
            print("Error decoding data. Packet is unchanged.")