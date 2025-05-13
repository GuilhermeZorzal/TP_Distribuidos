import socket
import json

HOST = "localhost"
PORT = 5123


def sendMessage(host, port, mensagem):
    """
    Envia uma mensagem para o servidor e retorna a resposta.

    :param host: Endereço do servidor
    :param port: Porta do servidor
    :param mensagem: Mensagem a ser enviada
    :return: Resposta do servidor
    """
    print(f"Conectando ao servidor {host}:{port}...")
    
    # Cria um socket para conexão TCP/IP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conecta ao servidor no endereço e porta especificados
    print(f"{mensagem}")
    client.connect((host, port))
    

    mensagem = json.dumps(mensagem)

    # Envia os dados para o servidor
        # O método encode() converte a string em bytes para envio
    client.sendall(mensagem.encode())

    response = client.recv(4096).decode()
    client.close()

    return json.loads(response)


def receiveMessage():
    pass
