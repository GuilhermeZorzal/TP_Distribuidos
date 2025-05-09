import socket

# É uma boa ideia usar funcoes mais genericas e encapsuladas pra ficar mais facil de isolar depois quando tiver o middleware: a gente só adapta esse arquivo aqui


def sendMessage(host, port, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Conectando ao servidor {host}:{port}...")

    client.connect((host, port))

    client.sendall(message.encode())
    resposta = client.recv(1024).decode()

    client.close()
    return resposta


def receiveMessage():
    pass
