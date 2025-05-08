import socket

HOST = "0.0.0.0"  
PORT = 6000      

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Servidor ouvindo em {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"Conexão recebida de {addr}")

        nome = conn.recv(1024).decode()
        if not nome:
            break
        
        resposta = f"roi {nome}, né?"
        conn.sendall(resposta.encode())

        conn.close()

if __name__ == "__main__":
    main()
