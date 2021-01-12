import socket
import threading

HOST = '127.0.0.1'
PORT = 44444

sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sever.bind((HOST, PORT))
sever.listen()

clients = []
nick_names = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nick_names[index]
            print('{} has been disconnected !'.format(nickname))
            broadcast('{} left!'.format(nickname).encode('utf8'))
            nick_names.remove(nickname)
            break


def receive():
    while True:
        # Accept Connection
        client, address = sever.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('utf8'))
        nickname = client.recv(1024).decode('utf8')
        nick_names.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf8'))
        client.send('Connected to server!'.encode('utf8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print(f'Sever {str(HOST)}:{str(PORT)} is listening ...')
receive()
