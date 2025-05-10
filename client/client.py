import socket
import interface_socket.interface_socket as soc

HOST = "server"
PORT = 50051

idLoja = None
idCliente = None

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

        # Monta a mensagem de cadastro como uma string formatada
        dados = f"{nome}|{apelido}|{senha}|{ccm}|{contato}"
        print(f"Enviando dados: {dados}")


        # Aguarda e recebe a resposta do servidor
            # O tamanho máximo da resposta é de 1024 bytes
            # O método recv() bloqueia até que a resposta seja recebida
            # O método decode() converte os bytes recebidos em uma string
        resposta = sendMessage(HOST, PORT, dados)
        print(f"Resposta do servidor: {resposta}")


        # Retorna a resposta do servidor
        return 1, resposta
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

        dados = f"{ccm}|{senha}"
        print(f"Enviando dados: {dados}")

        # Resposta do servidor poderia ser o identificador do usuário
        idCliente = sendMessage(HOST, PORT, dados)
        print(f"Resposta do servidor: {idCliente}")

        return 1, idCliente
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e


def criar_loja(nome_loja, contato, descricao):
    """
    Envia os dados para criar uma loja no servidor.

    :param nome_loja: Nome da loja
    :param contato: Informações de contato da loja
    :param descricao: Descrição da loja
    :return: Resposta do servidor
    """
    try:
        dados = f"{nome_loja}|{contato}|{descricao}"
        print(f"Enviando dados: {dados}")


        # Resposta do servidor poderia ser o identificador da loja
        idLoja = sendMessage(HOST, PORT, dados)
        print(f"Resposta do servidor: {idLoja}")

        return 1, idLoja
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e

def criar_anuncio(nome, descricao, preco, categoria):
    """"Cria um anúncio para um produto.
    :param nome: Nome do produto
    :param descricao: Descrição do produto
    :param preco: Preço do produto
    :param categoria: Categoria do produto
    :return: Resposta do servidor
    """
    try:
        dados = f"{nome}|{descricao}|{preco}|{categoria}"
        print(f"Enviando dados: {dados}")

        # Resposta do servidor poderia ser o identificador do anúncio
        resposta = sendMessage(HOST, PORT, dados)
        print(f"Resposta do servidor: {resposta}")

        return 1, resposta
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e

# O usuário pode escolher entre os métodos de pagamento disponíveis e a quantidade de parcelas apenas
def get_dados_pagamento(metodo, parcelas):
    """
    Envia os dados de pagamento para o servidor.

    :param metodo: Método de pagamento
    :param parcelas: Número de parcelas
    :return: Resposta do servidor
    """
    try:
        dados = f"{metodo}|{parcelas}"
        print(f"Enviando dados: {dados}")

        resposta = sendMessage(HOST, PORT, dados)
        print(f"Resposta do servidor: {resposta}")
        
        return 1, resposta
    except Exception as e:
        print(f"Um erro ocorreu: {e}")
        return 0, e
    

def get_idCliente():
    """
    Retorna o identificador do cliente e da loja.
    :return: idLoja, idCliente
    """
    dados = f"{idCliente}"
    resposta = sendMessage(HOST, PORT, dados)
    
    return resposta

def get_idLoja():
    """
    Retorna o identificador do cliente e da loja.
    :return: idLoja, idCliente
    """
    dados = f"{idLoja}"
    resposta = sendMessage(HOST, PORT, dados)
    
    return resposta
