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
    "rompimento de selos"
]

HOST = "server"
PORT = 50051

# Tokens: 
# 1 - eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiaWF0IjoxNzQ3MTAwODEyLCJuYmYiOjE3NDcxMDA4MTIsImV4cCI6MTc0NzI3MzYxMiwiYXBlbGlkbyI6ImFwZWxpZG8ifQ.uimVVMjQPGwGm6dSSLeKdYTq8nkOI15l7jekbBH44lY
# 2 - eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiaWF0IjoxNzQ3MTM4MDUzLCJuYmYiOjE3NDcxMzgwNTMsImV4cCI6MTc0NzMxMDg1MywiYXBlbGlkbyI6Im1pY3JvIn0.OBdzAnjyVt-NexafGc4x-H2p8CffTQJZr0yR42XUqGA

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

# Serviço:
# criar_anuncio nome_servico1 descricao_servico magia tipo_pagamento quantidade_pagamento 1
# criar_anuncio Anoes1 descricao proteção tipo_pagamento quantidade_pagamento 1
# 
# nome_servico TEXT NOT NULL,
# descricao_servico TEXT NOT NULL,
# categoria TEXT NOT NULL,
# tipo_pagamento TEXT NOT NULL,
# quantidade_pagamento REAL NOT NULL,
# esta_visivel BOOLEAN NOT NULL,

# get_catalogo
# get_catalogo magia cura maldição 1 0
# get_catalogo magia cura maldição 2 0


# Resetar banco de dados:
# reset

def funcao_generica(String, func = 'cadastrar'):
    String = String.split()
    func = String[0]
    String = String[1:]
        
    try:
        if func == 'cadastrar':
            mensagem = {"funcao": func, "dados": {"nome": String[0], "apelido": String[1], "senha": String[2], "ccm": String[3], "contato": String[4]}}
            
        elif func == "autenticar":
            mensagem = {"funcao": func, "dados": {"ccm": String[0], "senha": String[1]}}
            
        elif func == "criar_loja":
            mensagem = {"funcao": func, "dados": {"nome": String[0], "contato": String[1], "descricao": String[2], "token": String[3]}}
        
        elif func == "tem_loja":
            mensagem = {"funcao": func, "dados": {"token": String[0]}}
        
        elif func == "get_loja":
            mensagem = {"funcao": func, "dados": {"idLoja": String[0]}}
            
        elif func == "criar_anuncio":
            mensagem = {"funcao": func, "dados": {"nome_servico": String[0], "descricao_servico": String[1], "categoria": String[2], "tipo_pagamento": String[3], "quantidade_pagamento": String[4], "esta_visivel": String[5], "token": String[6]}}
            
        elif func == "get_categoria":
            mensagem = {"funcao": func, "dados": {}}
            
        elif func == "get_catalogo":
            categorias=[]
            print(f"String: {String}")
            
            for cat in String:
                if cat in CATEGORIAS:
                    categorias.append(cat)
                    
            idLoja = None
            if len(len(String) > 1):
                if String[-2] not in categorias:
                    idLoja = String[-2]
            
            print(f"\nID Loja: {idLoja}")
            print(f"Categorias: {categorias}\n")
            mensagem = {"funcao": func, "dados": {"categorias":categorias, "idLoja": idLoja, "cont_pages": String[-1]}}
        
        elif func == "get_servico":
            mensagem = {"funcao": func, "dados": {"idServico": String[0]}}
        
        elif func == "get_pedido":
            mensagem = {"funcao": func, "dados": {"idCliente": String[0]}}
        
        elif func == "reset":
            mensagem = {"funcao": func, "dados": {}}
            
        else:
            raise ValueError("Função não reconhecida")
        
        
        resposta = soc.sendMessage(HOST, PORT, json.dumps(mensagem))
        
        return resposta
    except Exception as e:
        print(f"Um erro ocorreu {e}")
        return 0, e
