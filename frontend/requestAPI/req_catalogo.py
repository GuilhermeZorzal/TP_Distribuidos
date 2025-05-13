import socket
import interface_socket.interface_socket as soc
import random

HOST = "server"
PORT = 50051


def get_catalogo(categorias, idLoja):
    # tem que definir o que exatamente o contato vai fazer
    num = random.random()
    if num < 0.5:
        return False, "cadastro falhou!!"
    else:
        return True, "cadastro funcionou"


def logarUsuario(ccm, senha):
    num = random.random()
    if num < 0.5:
        return None, "Login falhou!!"
    else:
        return "token_brabo", "Login funcionou"
