import socket
import sys
import enc_keys


BUFSIZE = 128
program_name = "client"


def main():
    # Check command line arguments
    if len(sys.argv) < 3:
        print("[!] Wrong arguments. Usage: python3 {}.py <server> <port>".format(program_name))
        return

    host = sys.argv[1]
    print(host)
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
    my_keys = enc_keys.generate_keys()
    server_keys = []

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0) as tcpsocket:
        tcpsocket.settimeout(5.0)
        try:
            tcpsocket.connect((host, tcp_port))
        except ConnectionError as conn_err:
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
                for key in my_keys:
                    tcpsocket.send(key+b'\r\n')
                    d_recv = tcpsocket.recv(BUFSIZE)
                    s_key = d_recv.strip(b'\r\n')
                    server_keys.append(s_key)
                tcpsocket.send(b'.\r\n')
                print("[+] Received {} keys from server".format(len(server_keys)))
            d_recv = tcpsocket.recv(BUFSIZE)

        else:
            print("[+] Ending TCP communicaion")

    if udp_port == "":
        print("[!] Failed to receive UDP port from server.")
        return

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=0) as udpsocket:
        host_udp = (host, udp_port)
        print("[-] Connecting to {}:{} using UDP".format(host, udp_port))
        try:
            udpsocket.sendto(b'Hello from UDP', host_udp)

        except ConnectionError:
            pass

        data = udpsocket.recv(BUFSIZE)
        print(data.decode(encoding="utf-8"))
        if data == b'bye\r\n':
            print("[+] Server ending communication")
            udpsocket.sendto(b'.\r\n', host_udp)


if __name__ == "__main__":
    main()
