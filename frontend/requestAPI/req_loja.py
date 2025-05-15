import socket
import interface_socket.interface_socket as soc
import random

HOST = "server"
PORT = 50051

CATEGORIAS = [
    "Assassino de aluguel",
    "Mineiração",
    "Carpintaria",
    "Transporte",
    "Outro",
]


def enviar_nome(nome):
    try:
        resposta = soc.sendMessage(HOST, PORT, nome)
        return 1, resposta
    except Exception as e:
        print(f"Um erro ocorreu {e} enviar_nome")
        return 0, e


def get_loja(idLoja):
    # tem que definir o que exatamente o contato vai fazer
    num = random.random()
    if num < 0.3:
        return False, "Voce nao possui uma loja"
    else:
        return True, "cadastro funcionou"


def criar_loja(token, nome, info, descricao):
    # tem que definir o que exatamente o contato vai fazer
    # enviar_nome("batata")
    num = random.random()
    if not token:
        return False, "Voce precisa estar autenticado"
    if num < 0.5:
        return False, "Requisição falhou"
    else:
        return True, "Loja criada com sucesso"


def criar_anuncio(token, nome, descricao, categoria, preco):
    # tem que definir o que exatamente o contato vai fazer
    # enviar_nome("batata")
    num = random.random()
    if not token:
        return False, "Voce precisa estar autenticado"
    if num < 0.5:
        return False, "Requisição falhou"
    else:
        return True, "Loja criada com sucesso"


def get_categoria():
    return CATEGORIAS
