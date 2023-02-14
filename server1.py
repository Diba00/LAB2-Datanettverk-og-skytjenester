import socket

def broadcast(client_socket, message):
    for sock in client_sockets:
        if sock != client_socket:
            sock.send(message)

def handle_client(client_socket, address):
    while True:
        message = client_socket.recv(1024)
        if not message:
            break
        broadcast(client_socket, message)
    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5000))
server_socket.listen(5)

client_sockets = []

while True:
    client_socket, address = server_socket.accept()
    client_sockets.append(client_socket)
    print("Accepted connection from", address)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
    client_thread.start()
