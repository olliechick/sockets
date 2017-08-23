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

def replant_seed():
    file = open('seed', 'r')
    seed = int(file.read())
    file.close()
    seed += 1
    file = open('seed', 'w')
    file.write(str(seed))
    file.close()
    

def get_socket_numbers():
    #must be in the range [1024, 64000]
    file = open('seed', 'r')
    seed = int(file.read())
    file.close()
    seed = (seed%100)*10
    
    sender_base  = 5000
    channel_base = 2000
    receiver_base= 8000
    
    s_in = sender_base + seed
    s_out = sender_base + 1 + seed
    c_s_in = channel_base + seed
    c_s_out = channel_base + 1 + seed
    c_r_in = channel_base + 2 + seed
    c_r_out = channel_base + 3 + seed
    r_in = receiver_base + seed
    r_out = receiver_base + 1 + seed
    
    return (s_in, s_out, c_s_in, c_s_out, c_r_in, c_r_out, r_in, r_out)
    

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
    
    def __len__(self):
        return len(self.encode(printStuff = False))
        
    
    def encode(self, printStuff = True):
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