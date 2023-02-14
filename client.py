from socket import *
import select
import sys

#copied the teachers skeleton code for the client


# write server ip and port, and connect
server_ip = "127.0.0.1" #Standard IP adress
server_port = 12000 #Standard port
client_socket = socket(AF_INET,SOCK_STREAM) 
client_socket.connect((server_ip, server_port)) #connects to the client socket with IP addrress and port

while True:

    # we are going to use a select-based approach here because it will help
    # us deal with two inputs (user's input (stdin) and server's messages from socket)
    inputs = [sys.stdin, client_socket]

    # read the select documentations - You pass select three lists: the 
    # first contains all sockets that you might want to try reading; the 
    # second all the sockets you might want to try writing to, and the last 
    # (normally left empty) those that you want to check for errors.
    read_sockets, write_socket, error_socket = select.select(inputs,[],[])

    # we check if the message is either coming from your terminal or 
    # from a server
    for socks in read_sockets:
        if socks == client_socket:

            # receive message from client and display it on the server side 
            # also handle exceptions here if there is no message from the 
            # client, you should exit.
            try:
                data = client_socket.recv(4096).decode("utf-8") #receives 4096 bytes and decodes deom bytes to utf-8 format
                if not data: #when data doesn't get a connection to a server
                    print("Connection to server lost. Exiting...") 
                    break
                if "has left the chat" in data: #when a client has entered the "exit" msg 
                    print(data)
                    break
                print("Received from server ", data)
            except socket.error as e:
                print("Error receiving data from server:", e)
                break
        else:
            # takes inputs from the user
            message = sys.stdin.readline() #msg input

            # send a message to the server
            client_socket.send(message.encode()) 

client_socket.close()
           




#done