#This python file contains all the functionalities

from main import *

#this function is to instatiate by creating objects
class User:
    def __init__(self, name):
        self.name = name
        self.roomdetails = []
        self.thisRoom = ''


class Room:
    def __init__(self, name):
        self.peoples = []
        self.user_names = []
        self.name = name



#List of available room information is the purpose of this function.
def listOfAllRoomDetails(yourname):
    name = users[yourname]
    print(len(roomdetails))
    if len(roomdetails) == 0:
        name.send('I am sorry, No rooms available to join\n'.encode('utf-8'))
    else:
        reply = "Below is the List of available rooms and members: \n"
        name.send(f'{reply}'.encode('utf-8'))
        for room in roomdetails:
            print(roomdetails[room].name)
            print(roomdetails[room].user_names)
            name.send(f'{roomdetails[room].name}\n'.encode('utf-8'))
            name.send(f'{roomdetails[room].user_names}\n'.encode('utf-8'))


#New rooms can be made with this function.
def CreateRoom(yourname, room_name):
    name = users[yourname]
    user = usersInRoom[yourname]
    if not room_name:
        name.send('Enter a roomname to Create! you have not entered a roomname\n'.encode('utf-8'))
    elif room_name not in roomdetails:
        room = Room(room_name)
        roomdetails[room_name] = room
        room.peoples.append(name)
        room.user_names.append(yourname)
        user.thisRoom = room_name
        user.roomdetails.append(room)
        name.send(f'{room_name} created\n'.encode('utf-8'))
    else:
        if room_name in user.roomdetails:
            name.send('There is already a Room with the same name, please enter another name for the room\n'.encode('utf-8'))


#Joining rooms is the purpose of this function.
def JoinRoom(yourname, room_name):
    name = users[yourname]
    user = usersInRoom[yourname]
    print(len(roomdetails))
    if len(roomdetails) == 0:
        name.send('I am sorry. No rooms are available to join\n'.encode('utf-8'))
    else:
        room = roomdetails[room_name]
        if room_name in user.roomdetails:
            name.send('You are already in the room\n'.encode('utf-8'))
        else:
            room.peoples.append(name)
            room.user_names.append(yourname)
            user.thisRoom = room_name
            user.roomdetails.append(room)
            broadcast(f'{yourname} joined the room', room_name)
            broadcast(f'{yourname} Welcome to the room', room_name)


#Personal communications are sent using this Function.
def PersonalMessage(message):
    args = message.split(" ")
    user = args[2]
    sender = users[args[0]]
    sender.send('Entered personal message function'.encode('utf-8'))
    if user not in users:
        sender.send('User not found\n'.encode('utf-8'))
    else:
        reciever = users[user]
        msg = ' '.join(args[3:])
        reciever.send(f'[personal message] {args[0]}: {msg}'.encode('utf-8'))
        sender.send(f'[personal message] {args[0]}: {msg}'.encode('utf-8'))


#To change to another room, use this function.
def SwitchRoom(yourname, roomname):
    user = usersInRoom[yourname]
    name = users[yourname]
    room = roomdetails[roomname]
    if roomname == user.thisRoom:
        name.send('You are already joined in the room, choose another available room to change\n'.encode('utf-8'))
    elif room not in user.roomdetails:
        name.send('I am sorry, As you are not part of the room, change of room not available\n'.encode('utf-8'))
    else:
        user.thisRoom = roomname
        name.send(f'You are switched to {roomname}\n'.encode('utf-8'))

#The room can be left by using this function.
def LeaveRoom(yourname):
    user = usersInRoom[yourname]
    name = users[yourname]
    if user.thisRoom == '':
        name.send('You are not part of any room\n'.encode('utf-8'))
    else:
        roomname = user.thisRoom
        room = roomdetails[roomname]
        user.thisRoom = ''
        user.roomdetails.remove(room)
        roomdetails[roomname].peoples.remove(name)
        roomdetails[roomname].user_names.remove(yourname)
        broadcast(f'{yourname} left the room\n', roomname)
        name.send('You left the room\n'.encode('utf-8'))
        

#The server/application will exit using this function
def RemoveClient(yourname):
    user_names.remove(yourname)
    client = users[yourname]
    user = usersInRoom[yourname]
    user.thisRoom = ''
    for room in user.roomdetails:
        print(room.name)
        room.peoples.remove(client)
        print(room.peoples)
        room.user_names.remove(yourname)
        print(room.user_names)
        broadcast(f'{yourname} left the room\n', room.name)


#to handle
def handle(client):
    uname=''
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            args = message.split(" ")
            name = users[args[0]]
            uname = args[0]
            if 'menu' in message:
                name.send(instructions.encode('utf-8'))
            elif 'list' in message:
                listOfAllRoomDetails(args[0])
            elif 'create' in message:
                CreateRoom(args[0], ' '.join(args[2:]))
            elif 'join' in message:
                JoinRoom(args[0], ' '.join(args[2:]))
            elif 'leave' in message:
                LeaveRoom(args[0])
            elif 'switch' in message:
                SwitchRoom(args[0], args[2])
            elif 'personal' in message:
                PersonalMessage(message)
            elif 'exit' in message:
                RemoveClient(args[0])
                name.send('EXIT'.encode('utf-8'))
                name.close()
            else:
                if usersInRoom[args[0]].thisRoom == '':
                    name.send('You are not part of any room\n'.encode('utf-8'))
                else:
                    msg = ' '.join(args[1:])
                    broadcast(f'{args[0]}: {msg}',usersInRoom[args[0]].thisRoom)

        except Exception as e:
            print("exception occured ", e)
            index = clients.index(client)
            clients.remove(client)
            client.close()
            print(f'user name is {uname}')
            if uname in user_names:
                RemoveClient(uname)
            if uname in user_names:
                user_names.remove(uname)
            break

#main
def recieve():
    while True:
        client, address = server.accept()
        print(f'connected with {str(address)}\n')
        print(client)
        client.send('U_NAME'.encode('utf-8'))
        yourname = client.recv(1024).decode('utf-8')
        user_names.append(yourname)
        clients.append(client)
        user = User(yourname)
        usersInRoom[yourname] = user
        users[yourname] = client
        print(f'Name of the client is {yourname}\n')
        client.send('\nYou are Connected to the server! Start a convo \n'.encode('utf-8'))
        client.send(instructions.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
print("Copywrites -  Siddhartha, Anoop and Syam")
print('Hello I am Server. Handling Clients...')
recieve()