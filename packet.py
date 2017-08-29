"""
   Packet
   A class to represent a packet of information.

   Authors: Samuel Pell and Ollie Chick
   Date Modified: 29 August 2017

   Contains:
       __init__()
       __repr__()
       __str__()
       __len__()
       encode()
       decode()
       is_valid_ack()
"""

PTYPE_DATA = 0
PTYPE_ACK = 1
MAGIC_NO = 0x497E


class Packet:

    def __init__(self, magic_no = 0, packet_type = 0, seq_no = 0, data_len = 0, data = ""):
        self.magic_no = magic_no       #determines if packet is dropped
        self.packet_type = packet_type #either dataPacket or acknowledgementPacket
        self.seq_no = seq_no           #sequence number
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

        s =  'Magic number: 0x{:X}\n'.format(self.magic_no)
        s += 'Packet type: {} ({})\n'.format(self.packet_type, pt)
        s += 'Seq no: {}\n'.format(self.seq_no)
        s += 'Data len: {}\n'.format(self.data_len)
        s += 'Data: "{}"'.format(self.data)
        return(s)


    def __len__(self):
        return len(self.encode())


    def encode(self):
        """Returns the byte representation of the packet"""
        conv = str(self.magic_no)
        conv += str(self.packet_type)
        conv += str(self.seq_no)
        conv += "0" * (3 - len(str(self.data_len))) + str(self.data_len)
        conv += str(self.data)
        return bytes(conv, "utf-8")


    def is_valid_ack(self, next_no):
        """
           Checks if the packet is a valid acknowledgement packet with the
           correct sequence number, next_no.
        """
        valid_magic = self.magic_no == MAGIC_NO
        valid_type = self.packet_type == PTYPE_ACK
        valid_length = self.data_len == 0
        valid_seq_no = self.seq_no == next_no

        return valid_magic and valid_type and valid_length and valid_seq_no


    def decode(self, data):
        """Sets the fields of this packet to that of data"""
        try:
            data = data.decode()
            self.magic_no = int(data[:5])
            self.packet_type = int(data[5])
            self.seq_no = int(data[6])
            self.data_len = int(data[7:10])
            self.data = data[10:]
        except:
            print("Error decoding data. Packet is unchanged.")