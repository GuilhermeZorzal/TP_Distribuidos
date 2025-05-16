import threading
import socket
import json


def sendMessage(host, port, mensagem):
    """
    Envia uma mensagem para o servidor e retorna a resposta.

    :param host: Endereço do servidor
    :param port: Porta do servidor
    :param mensagem: Mensagem a ser enviada
    :return: Resposta do servidor
    """
    print(f"Conectando ao servidor {host}:{port}...")

    # Cria um socket para conexão TCP/IP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conecta ao servidor no endereço e porta especificados
    print(f"{mensagem}")
    client.connect((host, port))

    mensagem = json.dumps(mensagem)

    # Envia os dados para o servidor
    # O método encode() converte a string em bytes para envio
    client.sendall(mensagem.encode())

    response = client.recv(4096).decode()
    client.close()

    return json.loads(response)


def receiveMessage():
    pass


HOST = "server"
PORT = 50051

tokenCliente = None
cont_pages = 0
data_possui_loja = None
data_meus_pedidos = None
data_pedidos_minha_loja = None
data_catalogo = None


def cadastrar(nome, apelido, senha, ccm, contato):
    """
    Envia os dados de cadastro para o servidor.

    :param nome: Nome da criatura mágica
    :param apelido: Apelido da criatura mágica
    :param senha: Senha para autenticação
    :param ccm: Documento de identificação (Cadastro de Criatura Mágica)
    :param contato: Informações de contato
    :retorno: Resposta do servidor
    """
    try:
        global cont_pages
        global tokenCliente
        cont_pages = 0

        # Monta o objeto de cadastro como um dicionário
        mensagem = {
            "funcao": "cadastrar",
            "dados": {
                "nome": nome,
                "apelido": apelido,
                "senha": senha,
                "ccm": ccm,
                "contato": contato,
            },
        }

        # Aguarda e recebe a resposta do servidor
        resposta = sendMessage(HOST, PORT, mensagem)

        if resposta["status"] == 200:
            tokenCliente = resposta["dados"].get("tokenCliente")

        # Retorna a resposta do servidor
        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        # Em caso de erro, exibe a m cadaensagem e retorna o erro
        print(f"Um erro ocorreu: {e} cadastrar")
        return 0, e, {}


def logout():
    global tokenCliente
    tokenCliente = None
    return [200, "Logout feito com sucesso", {}]


def autenticar(ccm, senha):
    """
    Envia os dados de autenticação para o servidor.

    :param ccm: Documento de identificação (Cadastro de Criatura Mágica)
    :param senha: Senha para autenticação
    :retorno: Resposta do servidor
    """
    global tokenCliente
    global data_possui_loja
    global data_meus_pedidos
    global data_pedidos_minha_loja
    global data_catalogo

    try:
        mensagem = {"funcao": "autenticar", "dados": {"ccm": ccm, "senha": senha}}

        resposta = sendMessage(HOST, PORT, mensagem)

        if resposta["status"] == 200:
            tokenCliente = resposta["dados"].get("tokenCliente")
            print("Threads. Token:", tokenCliente)

            results = {}

            def run_and_store(name, func, *args, **kwargs):
                results[name] = func(*args, **kwargs)

            thread1 = threading.Thread(
                target=run_and_store, args=("minha_loja", get_minha_loja)
            )
            thread2 = threading.Thread(
                target=run_and_store, args=("pedidos", get_pedidos)
            )
            thread3 = threading.Thread(
                target=run_and_store,
                args=("pedidos_minha_loja", get_pedidos_minha_loja),
            )
            thread4 = threading.Thread(
                target=run_and_store, args=("catalogo", get_catalogo)
            )

            thread1.start()
            thread2.start()
            thread3.start()
            thread4.start()

            thread1.join()
            thread2.join()
            thread3.join()
            thread4.join()

            data_possui_loja = results.get("minha_loja")
            data_meus_pedidos = results.get("pedidos")
            data_pedidos_minha_loja = results.get("pedidos_minha_loja")
            data_catalogo = results.get("catalogo")

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e} autenticar")
        return 0, e, {}


def esta_logado():
    """
    Verifica se o usuário está logado.

    :return: True se o usuário estiver logado, False caso contrário
    """
    print("Local", tokenCliente)
    if tokenCliente is not None:
        return [200, "Usuário está autentificado!", {}]
    else:
        return [0, "Usuário não está autentificado!", {}]


def criar_loja(nome_loja, contato, descricao):
    """
    Envia os dados para criar uma loja no servidor.

    :param nome_loja: Nome da loja
    :param contato: Informações de contato da loja
    :param descricao: Descrição da loja
    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "criar_loja",
            "dados": {
                "tokenCliente": tokenCliente,
                "nome": nome_loja,
                "contato": contato,
                "descricao": descricao,
            },
        }

        # Resposta do servidor poderia ser o identificador da loja
        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], resposta["dados"]["loja"]]

    except Exception as e:
        print(f"Um erro ocorreu: {e} ciar loja")
        return 0, e, {}


def criar_anuncio(nome, descricao, categoria, tipo, quantidade):
    """ "Cria um anúncio para um produto.
    :param nome: Nome do produto
    :param descricao: Descrição do produto
    :param preco: Preço do produto
    :param categoria: Categoria do produto
    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "criar_anuncio",
            "dados": {
                "tokenCliente": tokenCliente,
                "nome_servico": nome,
                "descricao_servico": descricao,
                "categoria": categoria,
                "tipo_pagamento": tipo,
                "quantidade": quantidade,
            },
        }

        # Resposta do servidor poderia ser o identificador do anúncio
        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e} criar_anuncio")
        return 0, e, {}


def get_categoria():
    try:
        mensagem = {
            "funcao": "get_categoria",
            "dados": {
                "tokenCliente": tokenCliente,
            },
        }

        resposta = sendMessage(HOST, PORT, mensagem)
        print("\n\nResposta:", resposta)
        return [
            resposta["status"],
            resposta["mensagem"],
            resposta["dados"]["categorias"],
        ]
    except Exception as e:
        return 0, str(e), {}


def get_catalogo(categorias=[], idLoja=None):
    """
    Obtém o catálogo de produtos disponíveis.
    :param categorias: Lista de categorias

    :param idLoja: ID da loja
    :return: Resposta do servidor
    """
    try:
        global cont_pages

        mensagem = {
            "funcao": "get_catalogo",
            "dados": {
                "tokenCliente": tokenCliente,
                "pages": 0,
                "categorias": categorias,
                "idLoja": idLoja,
            },
        }
        resposta = sendMessage(HOST, PORT, mensagem)

        # FIXME cont_pages += 1
        return [resposta["status"], resposta["mensagem"], resposta["dados"]["servicos"]]
    except Exception as e:
        print(f"Um erro ocorreu: {e} get_catalogo")
        return 0, e, {}


def get_servico(idServico):
    """
    Obtém os detalhes de um serviço específico.

    :param idServico: ID do serviço
    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "get_servico",
            "dados": {"tokenCliente": tokenCliente, "idServico": idServico},
        }

        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], resposta["dados"]["servico"]]
    except Exception as e:
        print(f"Um erro ocorreu: {e} get_servico")
        return 0, e, {}


def get_loja(idLoja):
    """
    Obtém os detalhes de uma loja específica.

    :param idLoja: ID da loja
    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "get_loja",
            "dados": {
                "idLoja": idLoja,
                "tokenCliente": tokenCliente,
            },
        }

        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], resposta["dados"]["loja"]]
    except Exception as e:
        print(f"Um erro ocorreu: {e} get_loja")
        return 0, e, {}


def pagar_pedido(idPedido):
    """
    Obtém os detalhes de um pedido específico.

    :param idPedido: ID do pedido
    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "pagar_pedido",
            "dados": {
                "idPedido": idPedido,
                "tokenCliente": tokenCliente,
            },
        }

        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], resposta["dados"]["pedido"]]
    except Exception as e:
        print(f"Um erro ocorreu: {e} pagar_pedido")
        return 0, e, {}


def get_pedido(idPedido):
    """
    Obtém os detalhes de um pedido específico.

    :param idPedido: ID do pedido
    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "get_pedido",
            "dados": {
                "idPedido": idPedido,
                "tokenCliente": tokenCliente,
            },
        }

        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], resposta["dados"]["pedido"]]
    except Exception as e:
        print(f"Um erro ocorreu: {e} get_pedido")
        return 0, e, {}


def get_pedidos():
    """
    Obtém a lista de pedidos.

    :return: Resposta do servidor
    """
    try:
        mensagem = {"funcao": "get_pedidos", "dados": {"tokenCliente": tokenCliente}}

        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], resposta["dados"]["pedidos"]]
    except Exception as e:
        print(f"Um erro ocorreu: {e} get_pedidoS")
        return 0, e, {}


def get_pedidos_minha_loja():
    """
    Obtém a lista de pedidos da loja do usuário.

    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "get_pedidos_minha_loja",
            "dados": {"tokenCliente": tokenCliente},
        }

        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], resposta["dados"]["pedidos"]]
    except Exception as e:
        print(f"Um erro ocorreu: {e} get_pedidos_minha_loja")
        return 0, e, {}


def cancelar_pedido(idPedido):
    """
    Cancela um pedido específico.

    :param idPedido: ID do pedido
    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "cancelar_pedido",
            "dados": {
                "idPedido": idPedido,
                "tokenCliente": tokenCliente,
            },
        }

        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e} cancelar_pedido")
        return 0, e, {}


def editar_servico(idServico, nome, descricao, categoria, tipo, quantidade):
    """
    Edita um serviço existente.

    :param idServico: ID do serviço
    :param nome: Nome do produto
    :param descricao: Descrição do produto
    :param categoria: Categoria do produto
    :param tipo: Tipo de pagamento
    :param quantidade: Quantidade disponível
    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "editar_servico",
            "dados": {
                "idServico": idServico,
                "tokenCliente": tokenCliente,
                "nome_servico": nome,
                "descricao_servico": descricao,
                "categoria": categoria,
                "tipo_pagamento": tipo,
                "quantidade": quantidade,
            },
        }

        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], resposta["dados"]]
    except Exception as e:
        print(f"Um erro ocorreu: {e} editar_servico")
        return 0, e, {}


def ocultar_servico(idServico):
    """
    Oculta um serviço específico.

    :param idServico: ID do serviço
    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "ocultar_servico",
            "dados": {
                "idServico": idServico,
                "tokenCliente": tokenCliente,
            },
        }

        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e} ocultar_servico")
        return 0, e, {}


def desocultar_servico(idServico):
    """
    Desoculta um serviço específico.

    :param idServico: ID do serviço
    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "desocultar_servico",
            "dados": {
                "idServico": idServico,
                "tokenCliente": tokenCliente,
            },
        }

        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e} desocultar_servico")
        return 0, e, {}


def apagar_servico(idServico):
    """
    Apaga um serviço específico.

    :param idServico: ID do serviço
    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "deletar_servico",
            "dados": {
                "idServico": idServico,
                "tokenCliente": tokenCliente,
            },
        }

        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e} apagar_servico")
        return 0, e, {}


def get_minha_loja():
    """
    Obtém os detalhes da loja do usuário.

    :return: Resposta do servidor
    """
    try:
        mensagem = {"funcao": "get_minha_loja", "dados": {"tokenCliente": tokenCliente}}

        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], resposta["dados"]["loja"]]

    except Exception as e:
        print(f"Um erro ocorreu: {e} get_minha_loja")
        return 0, e, {}


def criar_pedido(idServico, quantidade):
    """
    Finalizar um pedido específico.

    :param idPedido: ID do pedido
    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "add_pedido",
            "dados": {
                "idServico": idServico,
                "quantidade": quantidade,
                "tokenCliente": tokenCliente,
            },
        }

        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e} criar_pedido")
        return 0, e, {}


def realizar_pedido(idPedido):
    """
    Finalizar um pedido específico.

    :param idPedido: ID do pedido
    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "add_pedido",
            "dados": {
                "idPedido": idPedido,
                "tokenCliente": tokenCliente,
            },
        }

        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e} realizar_pedido")
        return 0, e, {}


def usuario_possui_loja():
    """
    Verifica se o usuário possui uma loja.

    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "tem_loja",
            "dados": {"tokenCliente": tokenCliente},
        }

        resposta = sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], resposta["dados"]["resposta"]]

    except Exception as e:
        print(f"Um erro ocorreu: {e} usuario_possui_loja")
        return 0, e, {}


if __name__ == "__main__":
    # Exemplo de uso
    print(cadastrar("Nome", "Apelido", "Senha", "CCM", "Contato"))
    print(autenticar("CCM", "Senha"))
    # print(criar_loja("Loja", "Contato", "Descricao"))
    # print(criar_anuncio("Produto", "Descricao", "Categoria", "Tipo", 10))
    # print(get_categoria())
    # print(get_catalago())
    # print(get_servico(1))
    # print(get_loja(1))
    # print(get_pedido(1))
    # print(get_pedidos())
    # print(get_pedidos_minha_loja())
    # print(cancelar_pedido(1))
    # print(editar_servico(1, "Produto Editado", "Descricao Editada", "Categoria Editada", "Tipo Editado", 5))
    # print(ocultar_servico(1))
    # print(desocultar_servico(1))
    # print(apagar_servico(1))
