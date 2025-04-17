import socket
import threading

HOST = '192.168.1.xxx'  # Replace with server's IP
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Get the username from the user
username = input("Enter your username: ")
client.send(username.encode())

# Receive messages from server (both public and private)
def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg:
                print("\n" + msg)
        except:
            print("[ERROR] Disconnected from server.")
            client.close()
            break

# Send messages to server (public or private)
def send():
    while True:
        msg = input()
        if msg.lower() == 'exit':
            break
        elif msg.startswith('@'):
            # Private message format: @username message
            client.send(msg.encode())
        else:
            # Public message
            client.send(msg.encode())

threading.Thread(target=receive).start()
threading.Thread(target=send).start()
