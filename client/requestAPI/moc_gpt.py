import random
import uuid
from datetime import datetime


# CSU001: Cadastro de Usuário
def cadastrar(nome, apelido, senha, ccm, contato):
    if random.random() < 0.5:
        return 0, "cadastro falhou!!"
    else:
        return 1, "cadastro funcionou"


# CSU002/1: Login
def logout():
    pass


# CSU002/1: Login
def autenticar(ccm, senha):
    if random.random() < 0.5:
        return 0, "Login falhou!!"
    else:
        return 1, "Login funcionou"


# CSU002/2: Autentifica
def esta_logado():
    return (1, "Token válido") if random.random() > 0.5 else (0, "Token inválido")


# CSU003: Criar Loja
def criar_loja(nome_loja, contato, descricao):
    if random.random() < 0.5:
        return 0, "Falha ao criar loja"
    else:
        return 1, "Loja criada com sucesso"


# CSU004/1: Criar Anúncio de Serviço
def criar_anuncio(
    nome_servico, descricao_servico, categoria, tipo_pagamento, quantidade
):
    if random.random() < 0.5:
        return 0, "Erro ao criar serviço"
    else:
        return 1, "Serviço criado com sucesso"


# CSU004/2: Categoria Serviço
def get_categoria():
    categorias = ["limpeza", "reparo", "consultoria"]
    return 1, "Categorias obtidas com sucesso", categorias


# CSU005, CSU006, CSU013/1: Exibir Catálogo de Serviços
def get_catalogo(categorias=[], idLoja=None):
    servicos = [
        {
            "idServico": str(uuid.uuid4()),
            "nome_servico": f"Servico {random.randint(0, 100)}",
            "descricao_servico": "descriçao",
            "categoria": random.choice(["limpeza", "reparo", "consultoria"]),
            "tipo_pagamento": "maldicoes",
            "quantidade_pagamento": random.randint(1, 10),
            "esta_visivel": True,
            "idLoja": str(uuid.uuid4()),
        }
        for i in range(20)
    ]
    # servicos = ["Batata" for i in range(5)]
    return 1, "Serviços encontrados", servicos


# CSU007: Selecionar Serviço
def get_servico(idServico):
    servico = {
        "idServico": idServico,
        "nome_servico": f"Servico {random.randint(0, 100)}",
        "descricao_servico": "Exemplo de serviço",
        "categoria": "limpeza",
        "tipo_pagamento": "maldicoes",
        "quantidade_pagamento": random.randint(1, 10),
        "esta_visivel": True,
        "idLoja": str(uuid.uuid4()),
    }
    return 1, "Serviço carregado", servico


# CSU010: Visualizar Contato da Loja
def get_loja(idLoja):
    loja = {
        "idLoja": idLoja,
        "nome": "Loja Exemplo",
        "contato": "123456789",
        "descricao": "Descrição exemplo",
        "idCliente": str(uuid.uuid4()),
    }
    return 1, "Loja carregada", loja


# CSU008: Acompanhar Estado de um único Pedido
def get_pedido(idPedido):
    pedido = {
        "idPedido": idPedido,
        "data_pedido": str(datetime.now()),
        "servico": "Serviço Exemplo",
        "nome_cliente": "robson",
        "estado_pedido": random.choice(["registrado", "andamento", "concluido"]),
        "total": random.randint(50, 200),
    }
    return 1, "Pedido carregado", pedido


# CSU012/1: Cliente Visualiza seus próprios Pedidos
def get_pedidos():
    pedidos = [
        {
            "idPedido": str(uuid.uuid4()),
            "data_pedido": str(datetime.now()),
            "servico": "Serviço Exemplo",
            "estado_pedido": "registrado",
            "total": 100,
        }
        for _ in range(random.randint(1, 10))
    ]
    return 1, "Pedidos carregados", pedidos


# CSU012/2 e CSU013/2: Visualizar Pedidos feitos na minha Loja
def get_pedidos_minha_loja():
    pedidos = [
        {
            "idPedido": str(uuid.uuid4()),
            "data_pedido": str(datetime.now()),
            "nome_cliente": "robson",
            "servico": "Serviço Exemplo",
            "estado_pedido": "concluido",
            "total": 150,
        }
        for _ in range(5)
    ]
    return 1, "Pedidos da loja carregados", pedidos


# CSU009: Cancelar Pedido
def cancelar_pedido(idPedido):
    return 1, "Pedido cancelado com sucesso"


# CSU011: Gerenciar Serviços
def editar_servico(
    idServico, nome_servico, descricao_servico, categoria, tipo_pagamento, quantidade
):
    return 1, "Serviço editado com sucesso"


def ocultar_servico(idServico):
    return 1, "Serviço ocultado"


def desocultar_servico(idServico):
    return 1, "Serviço desocultado"


def apagar_servico(idServico):
    return 1, "Serviço apagado"


# CSU013/3: Visualizar Informações da Minha Loja
def get_minha_loja():
    loja = {
        "idLoja": str(uuid.uuid4()),
        "nome": "Minha Loja",
        "contato": "999999999",
        "descricao": "Descrição da loja",
        "idCliente": str(uuid.uuid4()),
    }
    return 1, "Loja do cliente carregada", loja


# CSU014: Realizar Pagamento
def realizar_pedido(idPedido):
    return 1, "Pagamento confirmado"
