import socket

HOST = "127.0.0.1"  
PORT = 6000

def enviar_nome(nome):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Conectando ao servidor {HOST}:{PORT}...")

    client.connect((HOST, PORT))
    
    client.sendall(nome.encode())
    resposta = client.recv(1024).decode()
    
    client.close()
    return resposta
