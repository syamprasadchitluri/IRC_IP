# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


#This module contains the socket connection
import socket
import threading #for multiple process


host = '127.0.0.1' #localhost
port = 64500  #use any available port less than 65535

#starting the server
#AF_INET is for the type of addresses that makes connection (Internet) and SOCK_STREAM is for tcp connections
#AF_INET is for the type of addresses that makes connection (Internet) and SOCK_STREAM is for tcp connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port)) #server is binding
server.listen() #now its in listening mode


instructions = '\nApplication Menu:\n' \
               '1.menu (Navigates to the Main Menu)\n' \
               '2.list (It will provide you the lists available rooms)\n' \
               '3.create roomname - Usage "create IPProject" (This command will create a new room)\n' \
               '4.join roomname - Usage "join IPProject" (This command helps you to join the room)\n' \
               '5.switch roomname - Usage "switch IPProject" (This command will switch you to another room)\n' \
               '6.leave (This command will let you leave from the current room) \n' \
               '7.personal message - Usage "personal Name_of_reciever hello" (sends personal message)\n' \
               '8.exit (exits the client app)\n'


#now create a empty list and dict for data storage
clients = []
user_names = []
roomdetails = {}
users = {}
usersInRoom = {}

#to broadcast the message
def broadcast(message, roomname):
    for client in roomdetails[roomname].peoples:
        msg = '['+roomname+'] '+message
        client.send(msg.encode('utf-8'))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
