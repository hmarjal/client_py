import struct
import parity


class UdpPacket:

    def __init__(self, encryption_keys):
        self.__encryption_keys = encryption_keys[:]

    @staticmethod
    def pack_udp_packet(data: bytes, cid: bytes, ack=False, data_remaining=0, eom=False) -> struct:
        """
        pack_udp_packet
        :param data = payload. payload > 64 bytes is sent over multiple packets
        :param cid = server assigned cliend identification token
        :param ack = Acknow
        :param data_remaining lenght of remaining data
        :param eom last message
        """
        udp_packet = struct.pack('!8s2?2H64s', cid[0:8], ack, eom, data_remaining, data)
        return udp_packet

    @staticmethod
    def unpack_udp_packet(packet):
        pass
