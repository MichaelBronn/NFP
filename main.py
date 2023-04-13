import socket
def client(text):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect(('', 8080))
    text = bytes(text, encoding='utf-8')
    sock.send(text)

    sock.close()
def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind(('', 8080))

    sock.listen(5)
    while True:
        try:
            client, address = sock.accept() #проверка на существование соединения

        except KeyboardInterrupt:
            sock.close()
            break

        else:
            result = client.recv(1024)
            client.close()

def main():
    pass


if __name__ == '__main__':
    main()
