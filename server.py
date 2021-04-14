import socket

BUFSIZE = 128
HOST = ''
TCPPORT = 10000
UDPPORT = 5544
client_flags = [0x00, 0x01, 0x02, 0x04]


def main():

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0) as tcpsocket:
        tcpsocket.bind((HOST, TCPPORT))
        tcpsocket.listen(1)
        print("Listening TCP connections on port {}".format(TCPPORT))
        conn, client = tcpsocket.accept()
        client_addr, client_port = client
        with conn:
            print("New connection from {}:{}".format(client_addr, client_port))
            while True:
                data = conn.recv(BUFSIZE)

                print("Recv data debug:", data)

                if len(repr(data)) > 0:
                    print("Data received:", repr(data))
                    msg = data.strip().decode(encoding='utf-8')
                    print("Message: ", msg)
                    bytes_sent = conn.send(b'Hello user123 5544\r\n')
                    print("[+]Info: {} bytes send to client {}".format(bytes_sent, client_addr))
                    print("[+]Info: Informing client {} for TCP socket shutdown...".format(client_addr))
                    conn.shutdown(socket.SHUT_RDWR)
                    print("[+]Info: TCP socket closed")
                    break
        tcpsocket.shutdown(socket.SHUT_RDWR)

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=0) as udpsocket:
        udpsocket.bind((HOST, UDPPORT))
        print("Listening UDP connections on port {}".format(UDPPORT))
        while True:
            data, client_addr = udpsocket.recvfrom(BUFSIZE)
            client_udp_a, client_udp_p = client_addr
            if data == b'.\r\n':
                print("Client ending communication")
                break
            print("Message from {}:{}(UDP): {}".format(client_udp_a, client_udp_p, repr(data)))
            udpsocket.sendto(b'bye\r\n', client_addr)
            break


if __name__ == "__main__":
    main()

