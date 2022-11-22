import socket
from time import sleep


def socket_client():
    def _send_message():
        """Отправялет гтовоность сереверу, что готов принимать клиентов.
         Сообщение отправляеться в формате UTF-8"""
        temp = input()
        if temp == "break":
            return "break"
        mess = "operator " + temp
        return mess.encode("UTF-8")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", 5003)  # Подключаем сокет к порту,
    # через который прослушивается сервер
    sock.connect(server_address)  # Конектим оператора к серверу

    print(f"Posible comand:\n break, ready(r)")

    while True:
        mess = _send_message()
        if mess == "break":
            print(f"BREAK")
            break
        sock.send(mess)  # Отправляем сообщение

        data = (sock.recv(4096)).decode()  # Принимаем сообщение
        while data == "no_client":
            print("No client")
            sleep(10)
            sock.send(mess)
            data = (sock.recv(4096)).decode()

        print(data)


if __name__ == '__main__':
    socket_client()