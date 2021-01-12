import socket
import threading

HOST = '127.0.0.1'
PORT = 44444

nick_name = input("Enter any nick name you want : ")
print("Connecting to the sever")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf8')
            if message == 'NICK':
                client.send(nick_name.encode('utf8'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(nick_name, input(''))
        client.send(message.encode('utf8'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
