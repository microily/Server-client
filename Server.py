import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(2)

clients = []
addresses = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message == "/exit":
                index = clients.index(client)
                clients.remove(client)
                client.close()
                address = addresses.pop(index)
                print(f"Пользователь {address} отключен")
            if message:
                print(f"{addresses[clients.index(client)]}: {message.decode('utf-8')}")
                broadcast(message)
            else:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                address = addresses.pop(index)
                print(f"Пользователь {address} отключен")
        except:
            continue

while True:
    print("Ожидание подключения клиента...")
    client_socket, client_address = server_socket.accept()
    print(f"Подключен клиент: {client_address}")
    client_socket.send("Добро пожаловать в чат!".encode('utf-8'))

    addresses.append(client_address)
    clients.append(client_socket)

    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()