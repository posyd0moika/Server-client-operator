import socket
from select import select

"""
    1)Клиет отправляет запрос, чтобы ему выдали номер очереди, 
серевер переадресует номер очереди клиенту. 
    2)Опереатор - человек который, сообщает о готовности серверу и 
сервер со стека даёт нулевой [0] обект оператору 
    3) СЕРВЕР связывает обе части
"""

stack_client = []
tasks = []
to_read = {}
to_write = {}
dict_container = {
    "CC": 0,
    "CD": 0,
    "M": 0,
    "BA": 0
}



def comparison(clien_send_message, addr):
    clien_send_message = clien_send_message.decode("UTF-8").split()

    match clien_send_message:

        case ["client", type_mess] if type_mess in dict_container:
            message = type_mess + str(dict_container[type_mess])
            stack_client.append(message)
            dict_container[type_mess] += 1
            return message.encode("UTF-8")

        case ["operator", *arg]:
            if stack_client:
                return stack_client.pop(0).encode("UTF-8")
            return "no_client".encode("UTF-8")
    return "ERROR".encode("UTF-8")


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind(("localhost", 5003))  # Создали сервер
    server_socket.listen()  # Слушаем соединения

    while True:
        yield ("read", server_socket)  # Возврашаем катретж (Готовы читать)
        client_socket, addr = server_socket.accept()

        print("Connect...", addr)
        tasks.append(client(client_socket, addr))


def client(client_socket, addr):
    while True:
        yield ("read", client_socket)
        try:
            request = client_socket.recv(4096)
            if not request:
                break
            else:
                respons = comparison(request, addr)
                yield ("write", client_socket)
                client_socket.send(respons)
        except ConnectionResetError:
            client_socket.close()
            break

    client_socket.close()
    print(f"Close...{addr}")


def event_loop():
    while any([tasks, to_read, to_write]):

        while not tasks:
            try:
                ready_to_read, ready_to_write, _ = select(to_read, to_write, [])
                for sock in ready_to_read:
                    tasks.append(to_read.pop(sock))
                for sock in ready_to_write:
                    tasks.append(to_write.pop(sock))
            except ValueError:
                pass
        try:
            task = tasks.pop(0)
            reason, sock = next(task)

            if reason == "read":
                to_read[sock] = task
            if reason == "write":
                to_write[sock] = task

        except StopIteration:
            pass


if __name__ == '__main__':
    print("\033[4m\033[37m\033[44m{}\033[0m".format("Hello Server"))
    tasks.append(server())  # True
    event_loop()