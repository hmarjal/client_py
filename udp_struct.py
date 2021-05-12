import struct
import parity


class UdpPacket:

    def __init__(self):
        pass

    @staticmethod
    def pack_udp_packet(data, cid, ack=True, data_remaining=0, eom=True) -> list:
        """
        pack_udp_packet
        :param data = payload. payload > 64 bytes is sent over multiple packets
        :param cid = server assigned cliend identification token
        :param ack = ACK bit
        :param data_remaining length of remaining data
        :param eom last message
        """

        remain = len(data)
        msg_chunks = []
        messages = []
        offset = 0
        while remain > 64:
            # read 64 bytes from payload
            chunk = data[offset:offset+64]
            msg_chunks.append(chunk)
            remain -= 64
            offset += 64
        chunk = data[offset:offset+64]
        msg_chunks.append(chunk)

        for msg in msg_chunks:
            total_len = len(msg)
            # add parity to message
            data_parity = parity.add_parity(msg)
            # pad message to 64 bytes
            #msg = data_parity.ljust(64, b'\x00')
            data_parity = data_parity.encode("utf-8")
            udp_packet = struct.pack('!8s2?2H128s', cid[0:8], ack, eom, data_remaining, total_len, data_parity)
            messages.append(udp_packet)
        return messages

    @staticmethod
    def unpack_udp_packet(packet):
        cid, ack, eom, rm, length, content = struct.unpack('!8s2?2H128s', packet)
        content = content.rstrip(b'\x00')
        return content
