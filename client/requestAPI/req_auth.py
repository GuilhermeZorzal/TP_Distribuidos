import socket
import interface_socket.interface_socket as soc
import random

HOST = "server"
PORT = 50051

# Token global. Fica guardado dentro do arquivo de autenticação
token = None


def enviar_nome(nome):
    try:
        resposta = soc.sendMessage(HOST, PORT, nome)
        return 1, resposta
    except Exception as e:
        print(f"Um erro ocorreu {e}")
        return 0, e


def cadastrar(nome, apelido, senha, ccm, contato):
    # tem que definir o que exatamente o contato vai fazer
    num = random.random()
    # enviar_nome("batata")
    if num < 0.5:
        return False, "cadastro falhou!!"
    else:
        return True, "cadastro funcionou"


def autenticar(ccm, senha):
    num = random.random()
    # enviar_nome("batata")
    if num < 0.5:
        return None, "Login falhou!!"
    else:
        global token
        token = "token_brabo"
        return "token_brabo", "Login funcionou"


def esta_logado():
    return 1 if token else 0


def logout():
    global token
    token = None
    return
