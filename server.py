import socket
import threading

HOST = '0.0.0.0'  # change this as per wish
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")

clients = {}  # store clients by their usernames
addresses = {}  # store clients by their connection address

#(public messages)
def broadcast(message, sender_conn=None):
    for client in clients.values():
        if client != sender_conn:
            try:
                client.send(message)
            except:
                client.close()
                if client in clients.values():
                    del clients[client]

# (private message)
def send_private_message(sender_conn, recipient_username, message):
    recipient_conn = clients.get(recipient_username)
    if recipient_conn:
        try:
            recipient_conn.send(message)
        except:
            recipient_conn.close()
            del clients[recipient_username]
    else:
        sender_conn.send(f"[ERROR] User {recipient_username} not found.".encode())

# Handle an individual connection
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("Please enter your username: ".encode())
    username = conn.recv(1024).decode().strip()
    clients[username] = conn
    addresses[conn] = addr
    print(f"[USER JOINED] {username} connected.")
    
    try:
        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            if msg.startswith('@'):
                parts = msg[1:].split(' ', 1)
                if len(parts) >= 2:
                    recipient_username, private_message = parts
                    private_message = f"[PRIVATE] {username}: {private_message}"
                    send_private_message(conn, recipient_username, private_message.encode())
                else:
                    conn.send("[ERROR] Invalid private message format. Use @username message.".encode())
            else:
                broadcast(f"[{username}] {msg}".encode(), conn)

    except:
        pass
    finally:
        del clients[username]
        del addresses[conn]
        print(f"[USER LEFT] {username} disconnected.")
        conn.close()

def accept_clients():
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

accept_clients()
