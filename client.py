import socket
import sys
import xor_crypt
import udp_struct
import struct
import parity

BUFSIZE = 64 * 1024


def main():
    # Check command line arguments
    if len(sys.argv) != 3:
        print("[!] Wrong arguments. Usage: python3 {} <server> <port>".format(sys.argv[0]))
        return
    host = sys.argv[1]
    dots = len(host.split('.'))
    if dots != 4:
        print("[!] Invalid address {}".format(host))
        return
    for part in host.split('.'):
        try:
            sub_addr = int(part)
        except ValueError as ve:
            print(ve)
            return
        if 0 > sub_addr > 255:
            print("[!] Invalid address")
            return

    try:
        tcp_port = int(sys.argv[2])
        if 0 > tcp_port > 65535:
            print("[!] Port must be in range 0..65535")
            return
    except ValueError as ve:
        print(ve)
        return

    xcrypt = xor_crypt.XorCrypt()
    decrypt_keys = []
    udpstruct = udp_struct.UdpPacket()
    failed_parity_count = 0
    # Create TCP socket
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as tcpsocket:
        tcpsocket.settimeout(10)
        try:
            tcpsocket.connect((host, tcp_port))
        except (ConnectionError, OverflowError) as conn_err:
            print("[!] Error connecting to {}:{} using TCP".format(host, tcp_port))
            print(conn_err)
            return

        # Start communicating with the server
        tcpsocket.send(b'HELLO ENC PAR MUL\r\n')
        i = 0

        while i < 20:
            key = xcrypt.encryption_keys[i] + '\r\n'
            tcpsocket.send(key.encode('utf-8'))
            i += 1
        tcpsocket.send(b'.\r\n')

        d_recv = tcpsocket.recv(BUFSIZE)
        print(d_recv)
        data_list = d_recv.split(b'\r\n')
        first_msg = data_list[0]
        print("[+] Message from server:", first_msg.decode())
        greeting, cid, udp_port = first_msg.split()
        cid_s = cid.decode('utf-8')
        udp_port = int(udp_port)

        j = 1
        while j < 21:
            decrypt_keys.append(data_list[j])
            print("<Key {}> {}".format(j, data_list[j].decode("utf-8")))
            j += 1

        xcrypt.add_decryption_keys(decrypt_keys)

    if udp_port == "":
        print("[!] Failed to receive UDP port from server.")
        return
    # Create UDP socket
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as udpsocket:
        host_udp = (host, udp_port)
        print("[+] Connecting to {}:{} using UDP".format(host, udp_port))
        crypted_msg = xcrypt.encrypt_mul('HELLO from '+cid_s+'\n')
        udp_msg = udpstruct.pack_udp_packet(crypted_msg, cid)

        for msg in udp_msg:
            udpsocket.sendto(msg, host_udp)

        while True:
            data = udpsocket.recv(BUFSIZE)
            cid, ack, eom, rm, length, content = struct.unpack('!8s2?2H128s', data)
            if 'Wrong' in content.strip(b'\x00').decode('utf-8'):
                print("[+] FAIL!")
                print(content.strip(b'\x00').decode('utf-8'))
                break

            if 'Bye' in content.strip(b'\x00').decode('utf-8') or eom:
                print("[+] Server ending communication")
                print(content.strip(b'\x00').decode('utf-8'))
                break
            parity_ok = True
            total_len = length+rm
            full_msg = content.strip(b'\x00')
            parity_check = parity.check_parity(full_msg)
            if parity_check is not True:
                parity_ok = False
            while rm > 0:
                data = udpsocket.recv(BUFSIZE)
                cid, ack, eom, rm, length, content = struct.unpack('!8s2?2H128s', data)
                full_msg += content.strip(b'\x00')
                parity_check = parity.check_parity(content)
                if parity_check is not True:
                    parity_ok = False

            parity_msg = parity.remove_parity(full_msg)
            content = xcrypt.decrypt_mul(parity_msg, total_len)
            if parity_ok is not True:
                failed_parity_count += 1
                print("Corrupted MSG:", content)
                fail_msg = xcrypt.encrypt_mul('Send again')
                failed_parity = udpstruct.pack_udp_packet(fail_msg, cid, ack=0)
                udpsocket.sendto(failed_parity[0], host_udp)

            else:
                print("RECEIVED WORD LIST", content)
                word_list = content.split()
                word_list.reverse()
                ret_msg = ""
                for word in word_list:
                    ret_msg += word + " "
                ret_msg = ret_msg.rstrip()
                tot_len = len(ret_msg)
                msg_split = [ret_msg[i:i+64] for i in range(0, len(ret_msg), 64)]
                remain = tot_len
                for msg in msg_split:
                    msg_len = len(msg)
                    remain -= msg_len
                    print("SENDING REVERSED MESSAGE", msg)
                    enc_msg = xcrypt.encrypt_mul(msg)
                    ency = enc_msg
                    enc_msg = parity.add_parity(enc_msg)
                    enc_msg_bytes = enc_msg.encode('utf-8')
                    udp_packet = struct.pack('!8s2?2H128s', cid[0:8], 1, 0, remain, msg_len, enc_msg_bytes)
                    udpsocket.sendto(udp_packet, host_udp)


if __name__ == "__main__":
    main()
