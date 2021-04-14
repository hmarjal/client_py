import socket
import sys
import enc_keys
import xor_crypt
import struct

BUFSIZE = 128


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

    cid = ""
    udp_port = ""
    encrypt_keys = enc_keys.generate_keys()
    decrypt_keys = []

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
        tcpsocket.send(b'HELLO ENC\r\n')
        d_recv = tcpsocket.recv(BUFSIZE)

        while d_recv != b'.\r\n':
            if d_recv == b'':
                print("[+] Connection closed by server")
                tcpsocket.shutdown(socket.SHUT_RDWR)
                break
            msg = d_recv.decode(encoding='utf-8').strip()
            if msg and not cid:
                print("[+] Message from server:", msg)
                greeting, cid, udp_port = msg.split()
                udp_port = int(udp_port)
            if cid and udp_port:
                for key in encrypt_keys:
                    tcpsocket.send(key+b'\r\n')
                    d_recv = tcpsocket.recv(BUFSIZE)
                    s_key = d_recv.strip(b'\r\n')
                    s_key_as_bytes = bytes(s_key)
                    decrypt_keys.insert(0, s_key_as_bytes)
                tcpsocket.send(b'.\r\n')
                print("[+] Received {} encryption keys from server".format(len(decrypt_keys)))
            d_recv = tcpsocket.recv(BUFSIZE)

        else:
            print("[+] Ending TCP communicaion")

    if udp_port == "":
        print("[!] Failed to receive UDP port from server.")
        return
    decrypt_keys.reverse()
    xcrypt = xor_crypt.XorMsg(encrypt_keys, decrypt_keys)

    # Create UDP socket
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as udpsocket:
        host_udp = (host, udp_port)
        print("[+] Connecting to {}:{} using UDP".format(host, udp_port))
        crypted_msg = xcrypt.encrypt(b'HELLO from 1234\r\n')
        udpsocket.sendto(crypted_msg, host_udp)
        data = udpsocket.recv(BUFSIZE)

        if data == b'bye\r\n':
            print("[+] Server ending communication")
            udpsocket.sendto(b'.\r\n', host_udp)


if __name__ == "__main__":
    main()
