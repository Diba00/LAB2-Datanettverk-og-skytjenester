from socket import *
import sys
import threading

host_name = gethostname()
serverName = gethostbyname(host_name)
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)

try:
    clientSocket.connect((serverName, serverPort))
except:
    print("ConnectionError")
    sys.exit()
       
username = input("Enter your username: ")
clientSocket.send(username.encode())

def receive_message():
    while True:
        received_message = clientSocket.recv(1024).decode()
        if received_message:
            print (received_message)

def send_message():
    while True:
        sentence = input('') #kode fra Islam hvor man kan skrive en mld til server
        clientSocket.send(sentence.encode())
        if (sentence == "exit"):
            clientSocket.close()
        break
    #modifiedSentence = clientSocket.recv(1024)
    #print (modifiedSentence.decode())
    
#clientSocket.close()

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

send_message()

receive_thread.join()

"""
while True:

    #print("1. Send a message")
    #print("2. Play game")
    choice = input("Enter your choice: ")
    if choice == "1":
        message = input("Input message: ")
        clientSocket.send(message.encode())
        if (message == "exit"):
            break
        received_message = clientSocket.recv(1024).decode()
        print (received_message)
    elif choice == "2":
        play_game()
    else:
        print("Invalid option. Please try again.")

clientSocket.close()
"""