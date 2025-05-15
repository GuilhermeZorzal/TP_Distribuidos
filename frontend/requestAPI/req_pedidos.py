import socket
import interface_socket.interface_socket as soc
import random

HOST = "server"
PORT = 50051


def enviar_nome(nome):
    try:
        resposta = soc.sendMessage(HOST, PORT, nome)
        return 1, resposta
    except Exception as e:
        print(f"Um erro ocorreu {e} enviar_nome")
        return 0, e


def cadastrarUsuario(nome, apelido, senha, ccm, contato):
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
