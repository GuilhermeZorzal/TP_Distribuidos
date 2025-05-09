import socket
import interface_socket.interface_socket as soc

HOST = "server"
PORT = 50051


def enviar_nome(nome):
    try:
        resposta = soc.sendMessage(HOST, PORT, nome)
        return 1, resposta
    except Exception as e:
        print(f"Um erro ocorreu {e}")
        return 0, e
