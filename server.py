import socket
import enc_keys
import xor_crypt

BUFSIZE = 128
HOST = ''
TCPPORT = 10000
UDPPORT = 5544
random_words = 'un dos tres quattro cinco qwerty gilgamesh'


def main():
    encrypt_keys = enc_keys.generate_keys()
    decrypt_keys = []

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as tcpsocket:
        tcpsocket.bind((HOST, TCPPORT))
        tcpsocket.listen(1)
        print("Listening TCP connections on port {}".format(TCPPORT))
        conn, client = tcpsocket.accept()
        client_addr, client_port = client
        with conn:
            print("New connection from {}:{}".format(client_addr, client_port))
            conn.recv(BUFSIZE)
            bytes_sent = conn.send(b'Hello user123 5544\r\n')
            print("[+]Info: {} bytes send to client {}".format(bytes_sent, client_addr))
            while True:
                data = conn.recv(BUFSIZE)
                if data == b'.\r\n':
                    conn.send(b'.\r\n')
                    conn.shutdown(socket.SHUT_RDWR)
                    break
                if len(repr(data)) > 0:
                    key = data.strip(b'\r\n')
                    decrypt_keys.insert(0, key)
                    my_key = encrypt_keys.pop(0)
                    conn.send(my_key+b'\r\n')

    decrypt_keys.reverse()
    xcrypt = xor_crypt.XorCrypt(encrypt_keys, decrypt_keys)

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as udpsocket:
        udpsocket.bind((HOST, UDPPORT))
        print("Listening UDP connections on port {}".format(UDPPORT))
        while True:
            data, client_addr = udpsocket.recvfrom(BUFSIZE)
            client_udp_a, client_udp_p = client_addr
            print("Raw data received:\n", data)
            decr_msg = xcrypt.decrypt(data)
            print("Decrypted message:", decr_msg.decode())

            if data == b'.\r\n':
                print("Client ending communication")
                break

#            print("Message from {}:{}(UDP): {}".format(client_udp_a, client_udp_p, repr(data)))
            udpsocket.sendto(b'bye\r\n', client_addr)
            break


if __name__ == "__main__":
    main()

