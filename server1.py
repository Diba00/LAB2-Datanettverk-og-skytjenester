from socket import *
import _thread as thread
import time

clients = []

def now():
    #returns the time of day
    
    return time.ctime(time.time())

def handleClient(connection):
    #broadcast(f" Someone has joined the chat", connection)
    username = connection.recv(1024).decode()
    broadcast(f"{username} has joined the chat", connection)
    while True:
    
        data = connection.recv(1024).decode()
    
        broadcast(f"\n{username}: {data}", connection)
        if (data == "exit"):
            clients.remove(connection)
            broadcast(f"From Server: {username} has left the chat", connection)
            connection.close()
            break

def broadcast(message, conn):
    for client in clients:
        if client != conn:
            client.send(message.encode())


def main():
    #creates a server socket, listens for new connections,
    #and spawns a new thread whenever a new connection join
    
    serverPort = 12000
    serverSocket = socket(AF_INET,SOCK_STREAM)
    try:
        serverSocket.bind(('',serverPort))
    except: 
        print("Bind failed. Error : ")
    serverSocket.listen(1)
    print ('The server is ready to receive')
    while True:
        connectionSocket, addr = serverSocket.accept() 
        clients.append(connectionSocket)
        print('Server connected by ', addr) 
        print('at ', now())
        thread.start_new_thread(handleClient, (connectionSocket,)) 
    serverSocket.close()

if __name__ == '__main__':
    main()
