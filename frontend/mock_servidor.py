import socket
import uuid
import threading
import json
import time
import random

# Simulando "banco de dados" com dicionários
clientes = {
    1: {
        "nome": "João Silva",
        "email": "joao@example.com",
        "telefone": "1234567890",
        "endereco": "Rua A, 123",
    },
    2: {
        "nome": "Maria Oliveira",
        "email": "maria@example.com",
        "telefone": "9876543210",
        "endereco": "Rua B, 456",
    },
    3: {
        "nome": "Carlos Souza",
        "email": "carlos@example.com",
        "telefone": "4567891230",
        "endereco": "Rua C, 789",
    },
}

tokens = {1: "abcd1234token", 2: "efgh5678token", 3: "ijkl9012token"}

lojas = {
    1: {"nome": "Loja A", "endereco": "Avenida X, 111", "telefone": "111223344"},
    2: {"nome": "Loja B", "endereco": "Avenida Y, 222", "telefone": "223344556"},
    3: {"nome": "Loja C", "endereco": "Avenida Z, 333", "telefone": "334455667"},
}

servicos = {
    1: {"nome": "Desenvolvimento de Software", "categoria": "TI", "preco": 150},
    2: {"nome": "Design de Logotipo", "categoria": "Design", "preco": 100},
    3: {"nome": "Consultoria Empresarial", "categoria": "Consultoria", "preco": 200},
    4: {"nome": "Manutenção de Computadores", "categoria": "Manutenção", "preco": 80},
}

pedidos = {
    1: {
        "cliente_id": 1,
        "loja_id": 1,
        "servicos": [1, 2],
        "status": "em andamento",
        "data": "2025-05-12",
    },
    2: {
        "cliente_id": 2,
        "loja_id": 2,
        "servicos": [3],
        "status": "concluído",
        "data": "2025-05-10",
    },
    3: {
        "cliente_id": 3,
        "loja_id": 3,
        "servicos": [4],
        "status": "em andamento",
        "data": "2025-05-13",
    },
}

# Categorias de serviços
categorias = ["TI", "Design", "Consultoria", "Manutenção"]


# Contadores para IDs
idCliente_counter = 1
idLoja_counter = 1
idServico_counter = 1
idPedido_counter = 1


# Funções auxiliares
def gerar_token(idCliente, apelido):
    exp = int(time.time()) + 3600
    token = f"token_{idCliente}_{int(time.time())}"
    tokens[token] = {"idCliente": idCliente, "apelido": apelido, "exp": exp}
    return {"idCliente": idCliente, "apelido": apelido, "exp": exp}


def get_token_from_request(dados):
    return dados.get("tokenCliente", {}).get("idCliente")


# Handlers por função
def handle_cadastrar(dados):
    global idCliente_counter
    ccm = dados.get("ccm")
    if ccm in clientes:
        return [0, "Usuário já cadastrado", {}]

    idCliente = idCliente_counter
    idCliente_counter += 1

    clientes[ccm] = {
        "idCliente": idCliente,
        "nome": dados["nome"],
        "apelido": dados["apelido"],
        "senha": dados["senha"],
        "contato": dados["contato"],
    }
    token = gerar_token(idCliente, dados["apelido"])
    return [1, "Cadastro realizado com sucesso", {"tokenCliente": token}]


def handle_autenticar(dados):
    ccm = dados["ccm"]
    senha = dados["senha"]
    user = clientes.get(ccm)

    num = random.random()
    print("Num ", num)
    if num > 0.1:
        # if user and user["senha"] == senha:
        #     token = gerar_token(user["idCliente"], user["apelido"])
        return [1, "Login realizado com sucesso", {"tokenCliente": "Token brabo"}]

    return [0, "Credenciais inválidas", {"num": num}]


def handle_criar_loja(dados):
    global idLoja_counter
    loja = {
        "idLoja": idLoja_counter,
        "nome": "batata",
        "contato": dados["contato"],
        "descricao": dados["descricao"],
        "idCliente": "8",
    }
    lojas[idLoja_counter] = loja
    idLoja_counter += 1
    return [1, "Loja criada com sucesso", {"idLoja": loja["idLoja"]}]


def handle_usuario_possui_loja(dados):
    if random.random() < 0.5:
        return [0, "Usuário não possui loja", {}]
    else:
        return [1, "Usuário possui loja", {}]
        return 1, "Usuario possui loja"
    idCliente = dados["tokenCliente"]["idCliente"]
    for loja in lojas.values():
        if loja["idCliente"] == idCliente:
            return [1, "Usuário possui loja", {}]
    return [0, "Usuário não possui loja", {}]


def handle_criar_anuncio(dados):
    global idServico_counter
    servico = {
        "idServico": idServico_counter,
        "nome_servico": dados["nome_servico"],
        "descricao_servico": dados["descricao_servico"],
        "categoria": dados["categoria"],
        "tipo_pagamento": dados["tipo_pagamento"],
        "quantidade_pagamento": dados["quantidade"],
        "esta_visivel": True,
        "idLoja": "8",
    }
    servicos[idServico_counter] = servico
    idServico_counter += 1
    return [1, "Serviço criado com sucesso", {"servico": servico}]


def handle_get_categoria(_):
    return [1, "Categorias recuperadas", {"categorias": categorias}]


def handle_get_catalogo(dados):
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
        for _ in range(4)
    ]

    return [1, "Catálogo recuperado", {"servicos": servicos}]


def handle_get_servico(dados):
    servico = {
        "idServico": "5",
        "nome_servico": f"Servico {random.randint(0, 100)}",
        "descricao_servico": "Exemplo de serviço",
        "categoria": "limpeza",
        "tipo_pagamento": "maldicoes",
        "quantidade_pagamento": random.randint(1, 10),
        "esta_visivel": True,
        "idLoja": str(uuid.uuid4()),
    }
    return [1, "Serviço encontrado", {"servico": servico}]


def handle_get_minha_loja(dados):
    loja = {
        "idLoja": str(uuid.uuid4()),
        "nome": "Minha Loja",
        "contato": "999999999",
        "descricao": "Descrição da loja",
        "idCliente": str(uuid.uuid4()),
    }
    return [1, "Loja do cliente carregada", loja]
    # return [0, "Loja não encontrada", {}]


def handle_get_loja(dados):
    idLoja = dados["idLoja"] if "idLoja" in dados else None
    if not idLoja and "tokenCliente" in dados:
        idCliente = dados["tokenCliente"]["idCliente"]
        for loja in lojas.values():
            if loja["idCliente"] == idCliente:
                return [1, "Minha loja", {"loja": loja}]
        return [0, "Loja não encontrada", {}]
    loja = lojas.get(idLoja)
    if loja:
        return [1, "Loja encontrada", {"loja": loja}]
    return [0, "Loja não encontrada", {}]

    # mensagem = {"funcao": "get_pedidos", "dados": {"tokenCliente": tokenCliente}}


def handle_get_pedido(dados):
    print(dados)

    pedido = {
        "idPedido": "a",
        "data_pedido": str("kdf"),
        "servico": "Serviço Exemplo",
        "nome_cliente": "robson",
        "estado_pedido": random.choice(["registrado", "andamento", "concluido"]),
        "total": random.randint(50, 200),
    }

    if pedido:
        return [1, "Pedido encontrado", {"pedido": pedido}]
    return [0, "Pedido não encontrado", {}]


def handle_get_pedidos(dados):
    print("Handle get pedidos", dados)
    # idCliente = dados["tokenCliente"]["idCliente"]
    # resultado = [p for p in pedidos.values() if p["servico"]["idLoja"] == idCliente]
    resultado = [
        {
            "idPedido": str(uuid.uuid4()),
            "data_pedido": str(datetime.now()),
            "servico": "Serviço Exemplo",
            "estado_pedido": "registrado",
            "total": 100,
        }
        for _ in range(random.randint(1, 10))
    ]
    return [1, "Pedidos encontrados", {"pedidos": resultado}]


def handle_get_pedidos_minha_loja(dados):
    idCliente = dados["tokenCliente"]["idCliente"]
    minhas_lojas = [l["idLoja"] for l in lojas.values() if l["idCliente"] == idCliente]
    resultado = [p for p in pedidos.values() if p["servico"]["idLoja"] in minhas_lojas]
    return [1, "Pedidos da loja encontrados", {"pedidos": resultado}]


def handle_cancelar_pedido(dados):
    idPedido = dados["idPedido"]
    if idPedido in pedidos:
        pedidos.pop(idPedido)
        return [1, "Pedido cancelado", {}]
    return [0, "Pedido não encontrado", {}]


def handle_editar_servico(dados):
    servico = {
        "idServico": "5",
        "nome_servico": f"Servico {random.randint(0, 100)}",
        "descricao_servico": "Exemplo de serviço",
        "categoria": "limpeza",
        "tipo_pagamento": "maldicoes",
        "quantidade_pagamento": random.randint(1, 10),
        "esta_visivel": True,
        "idLoja": str(uuid.uuid4()),
    }
    return [1, "Serviço atualizado", {"servico": servico}]


def handle_ocultar_servico(dados):
    return [1, "Serviço ocultado", {}]
    return [0, "Serviço não encontrado", {}]


def handle_desocultar_servico(dados):
    return [1, "Serviço desocultado", {}]
    return [0, "Serviço não encontrado", {}]


def handle_apagar_servico(dados):
    return [1, "Serviço apagado", {}]
    return [0, "Serviço não encontrado", {}]


def handle_realizar_pedido(dados):
    global idPedido_counter
    idPedido = idPedido_counter
    idPedido_counter += 1
    pedido = {
        "idPedido": idPedido,
        "data_pedido": time.strftime("%Y-%m-%d"),
        "servico": "batata",
        "nome_cliente": "robson",
        "estado_pedido": "registrado",
        "total": 10,
    }
    pedidos[idPedido] = pedido
    return [1, "Pedido realizado com sucesso", {}]


# Mapeamento das funções
funcoes = {
    "cadastrar": handle_cadastrar,
    "autenticar": handle_autenticar,
    "criar_loja": handle_criar_loja,
    "usuario_possui_loja": handle_usuario_possui_loja,
    "criar_anuncio": handle_criar_anuncio,
    "get_categoria": handle_get_categoria,
    "get_catalogo": handle_get_catalogo,
    "get_servico": handle_get_servico,
    "get_loja": handle_get_loja,
    "get_minha_loja": handle_get_minha_loja,
    "get_pedidos": handle_get_pedidos,
    "get_pedidos_minha_loja": handle_get_pedidos_minha_loja,
    "cancelar_pedido": handle_cancelar_pedido,
    "editar_servico": handle_editar_servico,
    "ocultar_servico": handle_ocultar_servico,
    "desocultar_servico": handle_desocultar_servico,
    "apagar_servico": handle_apagar_servico,
    "realizar_pedido": handle_realizar_pedido,
}


def handle_client(conn, addr):
    try:
        data = conn.recv(4096)
        if not data:
            return

        req = json.loads(data.decode())
        funcao = req.get("funcao")
        dados = req.get("dados", {})

        if funcao not in funcoes:
            resp = [0, "Função inválida", {}]
        else:
            resp = funcoes[funcao](dados)

        conn.sendall(
            json.dumps(
                {
                    "status": 200 if resp[0] == 1 else 0,
                    "mensagem": resp[1],
                    "dados": resp[2],
                }
            ).encode()
        )

    except Exception as e:
        conn.sendall(
            json.dumps(
                {"status": 0, "mensagem": f"Erro no servidor: {e}", "dados": {}}
            ).encode()
        )
    finally:
        conn.close()


def start_server(host="localhost", port=50051):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(10)
    print(f"[SERVIDOR ONLINE] {host}:{port}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    start_server()
