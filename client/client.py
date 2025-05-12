import socket
import interface_socket.interface_socket as soc
import json

HOST = "server"
PORT = 50051

tokenCliente = None
cont_pages = 0

def sendMessage(host, port, mensagem):
    """
    Envia uma mensagem para o servidor e retorna a resposta.

    :param host: Endereço do servidor
    :param port: Porta do servidor
    :param mensagem: Mensagem a ser enviada
    :return: Resposta do servidor
    """
    # Cria um socket para conexão TCP/IP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conecta ao servidor no endereço e porta especificados
    client.connect((host, port))

    if isinstance(mensagem, dict):
        mensagem = json.dumps(mensagem)
    
    # Envia os dados para o servidor
        # O método encode() converte a string em bytes para envio
    client.sendall(mensagem.encode())

    response = client.recv(4096).decode()
    client.close()

    return json.loads(response)

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
                "contato": contato
            }
        }

        # Aguarda e recebe a resposta do servidor
        resposta = soc.sendMessage(HOST, PORT, mensagem)

        if resposta["status"] == 200:
            tokenCliente = resposta["dados"].get("tokenCliente")
            
        # Retorna a resposta do servidor
        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        # Em caso de erro, exibe a mensagem e retorna o erro
        print(f"Um erro ocorreu: {e}")
        return 0, e, {}


def autenticar(ccm, senha):
    """
    Envia os dados de autenticação para o servidor.

    :param ccm: Documento de identificação (Cadastro de Criatura Mágica)
    :param senha: Senha para autenticação
    :retorno: Resposta do servidor
    """
    global tokenCliente
    try:
        mensagem = {
            "funcao": "autenticar",
            "dados": {
                "ccm": ccm,
                "senha": senha
            }
        }

        resposta = soc.sendMessage(HOST, PORT, mensagem)

        if resposta["status"] == 200:
            tokenCliente = resposta["dados"].get("tokenCliente")

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e, {}


def esta_logado():
    """
    Verifica se o usuário está logado.

    :return: True se o usuário estiver logado, False caso contrário
    """
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
                "nome_loja": nome_loja,
                "contato": contato,
                "descricao": descricao
            }
        }

        # Resposta do servidor poderia ser o identificador da loja
        resposta = soc.sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e, {}


def criar_anuncio(nome, descricao, categoria, tipo, quantidade):
    """"Cria um anúncio para um produto.
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
                "quantidade": quantidade
            }
        }

        # Resposta do servidor poderia ser o identificador do anúncio
        resposta = soc.sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e, {}


def get_categoria():
    try:
        mensagem = {
            "funcao": "get_categoria",
            "dados": {}
        }

        resposta = soc.sendMessage(HOST, PORT, mensagem)
        return [resposta["status"], resposta["mensagem"], resposta["dados"]]
    except Exception as e:
        return 0, str(e)


def get_catalago(categorias, idLoja):
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
                "pages": cont_pages,
                "categorias": categorias,
                "idLoja": idLoja
            }
        }
        resposta = soc.sendMessage(HOST, PORT, mensagem)

        cont_pages += 1
        return [resposta["status"], resposta["mensagem"], resposta["dados"]]
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
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
            "dados": {
                "idServico": idServico
            }
        }

        resposta = soc.sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], resposta["dados"]]
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
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
                "idLoja": idLoja
            }
        }

        resposta = soc.sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], resposta["dados"]]
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
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
                "idPedido": idPedido
            }
        }

        resposta = soc.sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], resposta["dados"]]
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e, {}


def get_pedidos():
    """
    Obtém a lista de pedidos.

    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "get_pedidos",
            "dados": {
                "tokenCliente": tokenCliente
            }
        }

        resposta = soc.sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], resposta["dados"]]
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e, {}


def get_pedidos_minha_loja():
    """
    Obtém a lista de pedidos da loja do usuário.

    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "get_pedidos_minha_loja",
            "dados": {
                "tokenCliente": tokenCliente
            }
        }

        resposta = soc.sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], resposta["dados"]]
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
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
                "idPedido": idPedido
            }
        }

        resposta = soc.sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e}")
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
                "nome_servico": nome,
                "descricao_servico": descricao,
                "categoria": categoria,
                "tipo_pagamento": tipo,
                "quantidade": quantidade
            }
        }

        resposta = soc.sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], resposta["dados"]]
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
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
                "idServico": idServico
            }
        }

        resposta = soc.sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e}")
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
                "idServico": idServico
            }
        }

        resposta = soc.sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e, {}


def apagar_servico(idServico):
    """
    Apaga um serviço específico.

    :param idServico: ID do serviço
    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "apagar_servico",
            "dados": {
                "idServico": idServico
            }
        }

        resposta = soc.sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e, {}


def get_minha_loja():
    """
    Obtém os detalhes da loja do usuário.

    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "get_minha_loja",
            "dados": {
                "tokenCliente": tokenCliente
            }
        }

        resposta = soc.sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e, {}


def realizar_pedido(idPedido):
    """
    Finalizar um pedido específico.

    :param idPedido: ID do pedido
    :return: Resposta do servidor
    """
    try:
        mensagem = {
            "funcao": "realizar_pedido",
            "dados": {
                "idPedido": idPedido
            }
        }

        resposta = soc.sendMessage(HOST, PORT, mensagem)

        return [resposta["status"], resposta["mensagem"], {}]

    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e, {}
