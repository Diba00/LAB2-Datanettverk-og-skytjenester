from socket import *
import _thread as thread
import time
import sys

#copied the teachers skeleton code for the server

#this is too keep all the newly joined connections! 

all_client_connections = []

def now():
    #returns the time of day

    return time.ctime(time.time())

def handleClient(connection, addr):
    #a client handler function
    #this is where we broadcast everyone that a new client has joined
    # append this to the list for broadcast
    all_client_connections.append(connection)

    # create a message to inform all other clients that a new client has just joined.
    message = f"{addr} has joined the chat room!"
    broadcast(connection, message)

    try: #added a try and except, without this the client that wrote the exit msg would just loop forever with the exit msg

        while True:
            message = connection.recv(2048).decode().strip()   #added strip to remove any leading or trailing whitespace before comparing the message with "exit".
            print(now() + " " + str(addr) + "#  ", message)  #the address and message will pop ut for the other client
    
            if message == "exit": # removed or not, it didnt do anything for me
                print(f"{addr} has left the chat") #when a user enters exit this msg will show
                broadcast(connection, f"{addr} has left the chat") #then that msg is broadcastet to server and the other client
                break  # Break out of the infinite loop
            else:
                broadcast(connection, f"{addr}: {message}") #when the client is not typing "exit" and just writing a normal msg it will be broadcasted and the address and msg will pop up 
    except:
         all_client_connections.remove(connection) #exception code where the connection closes
         connection.close()

def broadcast(connection, message): #broadcast function for all the clients
    print ("Broadcasting")
    for conn in all_client_connections: 
        if conn != connection:
            try:
                conn.send(message.encode())
            except:
                print ("Error sending message to client") #error msg if the connection does not go through
                conn.close()
                all_client_connections.remove(conn)

def main():
    #creates a server socket, listens for new connections,
    #and spawns a new thread whenever a new connection join
    
    serverPort = 12000
    serverSocket = socket(AF_INET,SOCK_STREAM)
    try:
        serverSocket.bind(('',serverPort)) #serversocket from class, to spesifikk port
    except: 
        print("Bind failed. Error : ")
        sys.exit()
    serverSocket.listen(1)
    print ('The server is ready to receive')
    while True:
        connectionSocket, addr = serverSocket.accept() #this accpets the socket connection and returns the client address
        print('Server connected by ', addr) 
        print('at ', now())
        thread.start_new_thread(handleClient, (connectionSocket, addr)) 
    serverSocket.close()

if __name__ == '__main__':
    main()
#done


      