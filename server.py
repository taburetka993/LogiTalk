import socket
import threading

clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            msg = conn.recv(1024).decode()
            if msg:
                print(f"[{addr}] {msg}")
                broadcast(msg)
            else:
                remove_client(conn)
                break
        except:
            remove_client(conn)
            break

def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode())
        except:
            remove_client(client)

def remove_client(conn):
    if conn in clients:
        clients.remove(conn)
        print(f"[DISCONNECTED] {conn.getpeername()} disconnected.")
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12345))
    server.listen()
    print("[STARTED] Server is listening on 127.0.0.1:12345")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
