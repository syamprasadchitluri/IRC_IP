import threading #for multiple process
import socket
import sys

print("This Project copywrites to Siddhartha, Anoop and Syam")
username = input("Enter your Name: ")
threads = []
#To start the connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 64500))

#this function is to recieve and send message from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'U_NAME':
                client.send(username.encode('utf-8'))
            elif message == 'EXIT':
                sys.exit(2)
            else:
                print(message)
        except Exception as e:
            print('Server not responding')
            client.close()
            sys.exit(2)

def write():
    while True:
        message = '{} {}'.format(username, input(''))
        try:
            client.send(message.encode('utf-8'))
        except:
            sys.exit(0)

receive_thread = threading.Thread(target=receive)
receive_thread.start()
threads.append(receive_thread)
write_thread = threading.Thread(target=write)
write_thread.start()
threads.append(write_thread)