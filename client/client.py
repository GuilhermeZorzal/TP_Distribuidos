import json
import socket

import jwt
import interface_socket.interface_socket as soc

CATEGORIAS = [
    "magia",
    "maldição",
    "ser mistico",
    "proteção",
    "assassinato",
    "invocação",
    "cura",
    "transformação",
    "adivinhação",
    "alquimia",
    "encantamento",
    "necromancia",
    "viagem planar",
    "contrato sombrio",
    "domesticação mágica",
    "bênção divina",
    "ilusão",
    "espionagem etérea",
    "caça a monstros",
    "rompimento de selos",
]

HOST = "server"
PORT = 50051

# Tokens:
# 1 - eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiaWF0IjoxNzQ3MjQzNDQxLCJuYmYiOjE3NDcyNDM0NDEsImV4cCI6MTc0NzQxNjI0MSwiYXBlbGlkbyI6IkFydGh1ciJ9.Iyl06siQizb_N7qnEUBSQl6BPcFRZCyS0nNDgfrUlBo
# 2 - eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiaWF0IjoxNzQ3MjQzNDYxLCJuYmYiOjE3NDcyNDM0NjEsImV4cCI6MTc0NzQxNjI2MSwiYXBlbGlkbyI6IlpvcnphbCJ9.vlifaQcUOOq6GolgPz6LrD7wVk-XUnzGg0atobk8aM8
# 3 - eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiaWF0IjoxNzQ3MjQzOTg3LCJuYmYiOjE3NDcyNDM5ODcsImV4cCI6MTc0NzQxNjc4NywiYXBlbGlkbyI6IkR1ZGEifQ.OPAjvZBnv6bPtGUSwlRhPwv3QGbp1_aeBgoU3aNwPu4
# 4 - eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiaWF0IjoxNzQ3MjQ4NjkyLCJuYmYiOjE3NDcyNDg2OTIsImV4cCI6MTc0NzQyMTQ5MiwiYXBlbGlkbyI6ImFwZWxpZG8ifQ.ksKmpoxxgrD81eiTEANUQVPzF9UC8DhTwuMdjdrzLTQ

# Cadastro:
# cadastrar nome apelido senha ccm contato
# nome TEXT NOT NULL,
# apelido TEXT NOT NULL,
# senha TEXT NOT NULL,
# ccm TEXT UNIQUE NOT NULL,
# contato TEXT NOT NULL

# Autenticação:
# autenticar ccm senha
# autenticar arthur 123
# ccm TEXT UNIQUE NOT NULL,
# senha TEXT NOT NULL

# Loja:
# criar_loja nome contato descricao
# nome TEXT NOT NULL,
# contato TEXT NOT NULL,
# descricao TEXT NOT NULL,
# Token JWT

# get_loja idLoja

# Serviço:
# criar_anuncio nome_servico1 descricao_servico magia tipo_pagamento 10 1
# criar_anuncio Anoes1 descricao proteção tipo_pagamento 10 1
#
# nome_servico TEXT NOT NULL,
# descricao_servico TEXT NOT NULL,
# categoria TEXT NOT NULL,
# tipo_pagamento TEXT NOT NULL,
# quantidade_pagamento REAL NOT NULL,
# esta_visivel BOOLEAN NOT NULL,

# get_servico idServico

# get_categoria

# get_catalogo
# get_catalogo magia cura maldição 1 0
# get_catalogo magia cura maldição 2 0

# Pedido:
# add_pedido idServico quantidade
# idServico INTEGER NOT NULL,
# quantidade INTEGER NOT NULL,

# pagar_pedido idPedido
# pagar_pedido 1 eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiaWF0IjoxNzQ3MjQzOTg3LCJuYmYiOjE3NDcyNDM5ODcsImV4cCI6MTc0NzQxNjc4NywiYXBlbGlkbyI6IkR1ZGEifQ.OPAjvZBnv6bPtGUSwlRhPwv3QGbp1_aeBgoU3aNwPu4

# get_pedido

# get_pedidos

# get_pedidos_minha_loja

# cancelar_pedido idPedido

# Resetar banco de dados:
# reset


def funcao_generica(String, func="cadastrar"):
    String = String.split()
    func = String[0]
    String = String[1:]

    try:
        if func == "cadastrar":
            mensagem = {
                "funcao": func,
                "dados": {
                    "nome": String[0],
                    "apelido": String[1],
                    "senha": String[2],
                    "ccm": String[3],
                    "contato": String[4],
                },
            }

        elif func == "autenticar":
            mensagem = {"funcao": func, "dados": {"ccm": String[0], "senha": String[1]}}

        else:
            if func == "criar_loja":
                mensagem = {
                    "funcao": func,
                    "dados": {
                        "nome": String[0],
                        "contato": String[1],
                        "descricao": String[2],
                    },
                }

            elif func == "tem_loja":
                mensagem = {"funcao": func, "dados": {}}

            elif func == "get_loja":
                mensagem = {"funcao": func, "dados": {"idLoja": String[0]}}

            elif func == "criar_anuncio":
                mensagem = {
                    "funcao": func,
                    "dados": {
                        "nome_servico": String[0],
                        "descricao_servico": String[1],
                        "categoria": String[2],
                        "tipo_pagamento": String[3],
                        "quantidade_pagamento": String[4],
                        "esta_visivel": String[5],
                    },
                }

            elif func == "get_categoria":
                mensagem = {"funcao": func, "dados": {}}

            elif func == "get_catalogo":
                categorias = []
                print(f"String: {String}")

                for cat in String:
                    if cat in CATEGORIAS:
                        categorias.append(cat)

                idLoja = None
                if len(String) > 2:
                    if String[-3] not in categorias:
                        idLoja = String[-3]

                print(f"\nID Loja: {idLoja}")
                print(f"Categorias: {categorias}\n")
                mensagem = {
                    "funcao": func,
                    "dados": {
                        "categorias": categorias,
                        "idLoja": idLoja,
                        "cont_pages": String[-2],
                    },
                }

            elif func == "get_servico":
                mensagem = {"funcao": func, "dados": {"idServico": String[0]}}

            elif func == "add_pedido":
                mensagem = {
                    "funcao": func,
                    "dados": {"idServico": String[0], "quantidade": String[1]},
                }

            elif func == "pagar_pedido":
                mensagem = {"funcao": func, "dados": {"idPedido": String[0]}}

            elif func == "get_pedido":
                mensagem = {"funcao": func, "dados": {"idPedido": String[0]}}

            elif func == "get_pedidos":
                mensagem = {"funcao": func, "dados": {}}

            elif func == "get_pedidos_minha_loja":
                mensagem = {"funcao": func, "dados": {}}

            elif func == "cancelar_pedido":
                mensagem = {"funcao": func, "dados": {"idPedido": String[0]}}

            elif func == "reset":
                mensagem = {"funcao": func, "dados": {}}

            else:
                raise ValueError("Função não reconhecida")

            mensagem["dados"]["token"] = String[-1]

        resposta = soc.sendMessage(HOST, PORT, json.dumps(mensagem))

        return resposta
    except Exception as e:
        print(f"Um erro ocorreu {e}")
        return 0, e
