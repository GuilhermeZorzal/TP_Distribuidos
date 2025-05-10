import socket
import interface_socket.interface_socket as soc
import json

HOST = "server"
PORT = 50051

tokenCliente = None
cont_pages = 0


def sendMessage(host, port, message):
    # Cria um socket para conexão TCP/IP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Conectando ao servidor {host}:{port}...")

    # Conecta ao servidor no endereço e porta especificados
    client.connect((host, port))

    # Envia os dados para o servidor
    # O método encode() converte a string em bytes para envio
    client.sendall(message.encode())
    resposta = client.recv(1024).decode()

    # Fecha a conexão com o servidor
    client.close()
    return resposta


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
        # Monta o objeto de cadastro como um dicionário
        dados = {
            "nome": nome,
            "apelido": apelido,
            "senha": senha,
            "ccm": ccm,
            "contato": contato
        }
        
        cont_pages = 0
        
        # Serializa o objeto para uma string JSON
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")

        # Aguarda e recebe a resposta do servidor
        resposta = sendMessage(HOST, PORT, ["cadastrar", dados])
        print(f"Resposta do servidor: {resposta}")
        
        tokenCliente = resposta[2].get("tokenCliente")

        # Retorna a resposta do servidor
        return [resposta[0], resposta[1], None]
    except Exception as e:
        # Em caso de erro, exibe a mensagem e retorna o erro
        print(f"Um erro ocorreu: {e}")
        return 0, e


def autenticar(ccm, senha):
    """
    Envia os dados de autenticação para o servidor.

    :param ccm: Documento de identificação (Cadastro de Criatura Mágica)
    :param senha: Senha para autenticação
    :retorno: Resposta do servidor
    """
    try:

        dados = {
            "ccm": ccm,
            "senha": senha
        }
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")
        
        cont_pages = 0

        resposta = sendMessage(HOST, PORT, ["autenticar", dados])
        print(f"Resposta do servidor: {resposta}")
        
        tokenCliente = resposta[2].get("tokenCliente")

        return [resposta[0], resposta[1], None]
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e

def esta_logado():
    """
    Verifica se o usuário está logado.

    :return: True se o usuário estiver logado, False caso contrário
    """
    if tokenCliente is not None:
        return [200, "Usuário está autentificado!"]
    else:
        return [0, "Usuário não está autentificado!"]

def criar_loja(nome_loja, contato, descricao):
    """
    Envia os dados para criar uma loja no servidor.

    :param nome_loja: Nome da loja
    :param contato: Informações de contato da loja
    :param descricao: Descrição da loja
    :return: Resposta do servidor
    """
    try:
        dados = {
            "tokenCliente": tokenCliente,
            "nome_loja": nome_loja,
            "contato": contato,
            "descricao": descricao
        }
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")

        # Resposta do servidor poderia ser o identificador da loja
        resposta = sendMessage(HOST, PORT, ["criar_loja", dados])
        print(f"Resposta do servidor: {resposta}")
        
        return [resposta[0], resposta[1], None]
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e


def criar_anuncio(nome, descricao, categoria, tipo, quantidade):
    """"Cria um anúncio para um produto.
    :param nome: Nome do produto
    :param descricao: Descrição do produto
    :param preco: Preço do produto
    :param categoria: Categoria do produto
    :return: Resposta do servidor
    """
    try:
        dados = {
            "tokenCliente": tokenCliente,
            "nome_servico": nome,
            "descricao_servico": descricao,
            "categoria": categoria,
            "tipo_pagamento": tipo,
            "quantidade": quantidade
        }
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")

        # Resposta do servidor poderia ser o identificador do anúncio
        resposta = sendMessage(HOST, PORT, ["criar_anuncio", dados])
        print(f"Resposta do servidor: {resposta}")

        return [resposta[0], resposta[1], None]
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e


def get_categoria():
    """
    Obtém a lista de categorias disponíveis.

    :return: Resposta do servidor
    """
    try:
        dados = {}

        resposta = sendMessage(HOST, PORT, ["get_categoria", dados])
        print(f"Resposta do servidor: {resposta}")

        return resposta
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e
    
def get_catalago(categorias, idLoja):
    """
    Obtém o catálogo de produtos disponíveis.

    :param categorias: Lista de categorias
    :param idLoja: ID da loja
    :return: Resposta do servidor
    """
    try:
        dados = {
            "pages": cont_pages,
            "categorias": categorias,
            "idLoja": idLoja
        }
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")

        resposta = sendMessage(HOST, PORT, ["get_catalago", dados])
        print(f"Resposta do servidor: {resposta}")

        return resposta
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e

def get_servico(idServico):
    """
    Obtém os detalhes de um serviço específico.

    :param idServico: ID do serviço
    :return: Resposta do servidor
    """
    try:
        dados = {
            "idServico": idServico
        }
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")

        resposta = sendMessage(HOST, PORT, ["get_servico", dados])
        print(f"Resposta do servidor: {resposta}")

        return resposta
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e

def get_loja(idLoja):
    """
    Obtém os detalhes de uma loja específica.

    :param idLoja: ID da loja
    :return: Resposta do servidor
    """
    try:
        dados = {
            "idLoja": idLoja
        }
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")

        resposta = sendMessage(HOST, PORT, ["get_loja", dados])
        print(f"Resposta do servidor: {resposta}")

        return resposta
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e
    
def get_pedido(idPedido):
    """
    Obtém os detalhes de um pedido específico.

    :param idPedido: ID do pedido
    :return: Resposta do servidor
    """
    try:
        dados = {
            "idPedido": idPedido
        }
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")

        resposta = sendMessage(HOST, PORT, ["get_pedido", dados])
        print(f"Resposta do servidor: {resposta}")

        return resposta
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e

def get_pedidos():
    """
    Obtém a lista de pedidos.

    :return: Resposta do servidor
    """
    try:
        dados = {
            "tokenCliente": tokenCliente
        }
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")
        
        resposta = sendMessage(HOST, PORT, ["get_pedidos", dados])
        print(f"Resposta do servidor: {resposta}")
        
        return resposta
    except Exception as e:  
        print(f"Um erro ocorreu: {e}")
        return 0, e

def get_pedidos_minha_loja():
    """
    Obtém a lista de pedidos da loja do usuário.

    :return: Resposta do servidor
    """
    try:
        dados = {
            "tokenCliente": tokenCliente,
        }
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")
        
        resposta = sendMessage(HOST, PORT, ["get_pedidos_minha_loja", dados])
        print(f"Resposta do servidor: {resposta}")
        
        return resposta
    except Exception as e:  
        print(f"Um erro ocorreu: {e}")
        return 0, e

def cancelar_pedido(idPedido):
    """
    Cancela um pedido específico.

    :param idPedido: ID do pedido
    :return: Resposta do servidor
    """
    try:
        dados = {
            "idPedido": idPedido
        }
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")

        resposta = sendMessage(HOST, PORT, ["cancelar_pedido", dados])
        print(f"Resposta do servidor: {resposta}")

        return [resposta[0], resposta[1], None]
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e

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
        dados = {
            "idServico": idServico,
            "nome_servico": nome,
            "descricao_servico": descricao,
            "categoria": categoria,
            "tipo_pagamento": tipo,
            "quantidade": quantidade
        }
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")

        resposta = sendMessage(HOST, PORT, ["editar_servico", dados])
        print(f"Resposta do servidor: {resposta}")

        return resposta
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e

def ocultar_servico(idServico):
    """
    Oculta um serviço específico.

    :param idServico: ID do serviço
    :return: Resposta do servidor
    """
    try:
        dados = {
            "idServico": idServico
        }
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")

        resposta = sendMessage(HOST, PORT, ["ocultar_servico", dados])
        print(f"Resposta do servidor: {resposta}")

        return [resposta[0], resposta[1], None]
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e

def desocultar_servico(idServico):
    """
    Desoculta um serviço específico.

    :param idServico: ID do serviço
    :return: Resposta do servidor
    """
    try:
        dados = {
            "idServico": idServico
        }
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")

        resposta = sendMessage(HOST, PORT, ["desocultar_servico", dados])
        print(f"Resposta do servidor: {resposta}")

        return [resposta[0], resposta[1], None]
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e

def apagar_servico(idServico):
    """
    Apaga um serviço específico.

    :param idServico: ID do serviço
    :return: Resposta do servidor
    """
    try:
        dados = {
            "idServico": idServico
        }
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")

        resposta = sendMessage(HOST, PORT, ["apagar_servico", dados])
        print(f"Resposta do servidor: {resposta}")

        return [resposta[0], resposta[1], None]
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e

def get_minha_loja():
    """
    Obtém os detalhes da loja do usuário.

    :return: Resposta do servidor
    """
    try:
        dados = {
            "tokenCliente": tokenCliente
        }
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")

        resposta = sendMessage(HOST, PORT, ["get_minha_loja", dados])
        print(f"Resposta do servidor: {resposta}")

        return [resposta[0], resposta[1], None]
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e

def realizar_pedido(idPedido):
    """
    Finalizar um pedido específico.

    :param idPedido: ID do pedido
    :return: Resposta do servidor
    """
    try:
        dados = {
            "idPedido": idPedido
        }
        dados = json.dumps(dados)
        print(f"Enviando dados: {dados}")

        resposta = sendMessage(HOST, PORT, ["realizar_pedido", dados])
        print(f"Resposta do servidor: {resposta}")

        return [resposta[0], resposta[1], None]
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e