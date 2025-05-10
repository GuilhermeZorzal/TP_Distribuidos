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
        print(f"Um erro ocorreu {e}")
        return 0, e


def loja(token):
    # tem que definir o que exatamente o contato vai fazer
    enviar_nome("batata")
    num = random.random()
    if num < 0.3:
        return False, "Voce nao possui uma loja"
    elif num < 0.6:
        if not token:
            return False, "Voce precisa estar autenticado"
    else:
        return True, "cadastro funcionou"


def criaLoja(token, nome, info, descricao):
    # tem que definir o que exatamente o contato vai fazer
    # enviar_nome("batata")
    num = random.random()
    if not token:
        return False, "Voce precisa estar autenticado"
    if num < 0.5:
        return False, "Requisição falhou"
    else:
        return True, "Loja criada com sucesso"
