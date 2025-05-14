import socket
import sqlite3
import os
import json
from handlers import cadastro, login, loja, servico, pedido
from db.database import conectar, mostrar_tabelas, reset_database
from utils.utils import formatar_mensagem
from utils.token import autorizarToken

HOST = "0.0.0.0"
PORT = 50051

# formato de resposta para o cliente:
# dicionario = {status, mensagem, dados}
# status: 200 = sucesso, 0 = erro
# mensagem: string com a mensagem de erro ou sucesso
# dados: dicionário com os dados retornados


# formato de requisição para o servidor:
# dicionario = {func, dados}
# func: string com o nome da função a ser chamada
# dados: dicionário com os dados a serem passados para a função

def tratar_mensagem(mensagem):
    if "funcao" not in mensagem:
        return formatar_mensagem(0, "Mensagem mal formatada", {})

    func = mensagem.get("funcao")
    dados = mensagem.get("dados", {})

    # Despacha para o handler adequado
    if func == "cadastrar":
        return cadastro.cadastrar(dados)
    elif func == "autenticar":
        return login.autenticar_cliente(dados)
    else:
        try:
            status, msg, idCliente = autorizarToken(dados['token'])
            if status != 200:
                return status, msg, {}
        except Exception as e:
            return 0, f"Erro ao verificar Token: {e}", {}
        
        idCliente = int(idCliente)
        
        if func == "criar_loja":
            return loja.criar_loja(dados, idCliente)
        
        elif func == "tem_loja":
            return loja.tem_loja(idCliente)
        
        elif func == "get_loja":
            return loja.get_loja(dados)
        
        elif func == "criar_anuncio":
            return servico.criar_anuncio(dados, idCliente)
        
        elif func == "get_categoria":
            return servico.get_categoria()
        
        elif func == "get_catalogo":
            return servico.get_catalogo(dados)
        
        elif func == "get_servico":
            return servico.get_servico(dados)
        
        elif func == "add_pedido":
            return pedido.add_pedido(dados, idCliente)
        
        elif func == "pagar_pedido":
            return pedido.pagar_pedido(dados, idCliente)
        
        elif func == "get_pedido":
            return pedido.get_pedido(dados, idCliente)
        
        elif func == "get_pedidos":
            return pedido.get_pedidos(idCliente)
        
        elif func == "get_pedidos_minha_loja":
            return pedido.get_pedidos_minha_loja(idCliente)
        
        elif func == "cancelar_pedido":
            return pedido.cancelar_pedido(dados, idCliente)

        elif func == "reset":
            reset_database()
            return 200, "Banco de dados resetado", {}
        
    print(f"Função não reconhecida: {func}")
    return 0, "Função não reconhecida", {}

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Especifica a qual porta conectar o socket
    server.bind((HOST, PORT))
    server.listen()

    print(f"Servidor ouvindo em {HOST}:{PORT}")
    mostrar_tabelas()
    
    while True:
        # Conn = connection:  é a nova conexão
        # TODO: usar thread aqui
        conn, addr = server.accept()
        print(f"Conexão recebida de {addr}")

        requisicao = conn.recv(1024)
        if not requisicao:
            conn.close()
            continue

        try:
            mensagem_json = requisicao.decode()
            mensagem = json.loads(mensagem_json)
        except json.JSONDecodeError:
            resposta = formatar_mensagem(0, "JSON inválido", {})
            conn.sendall(resposta.encode())
            conn.close()
            continue
        
        status, msg, dados = tratar_mensagem(mensagem)
        resposta = formatar_mensagem(status, msg, dados)
        
        # TODO: isolar as funcoes de sql.
        # - create {table}
        # - select ...
        # -> se encapsular em funcoes fica mais facil de gerenciar
        # O arquivo sqlite.db é o banco de dados: não existe um servico de bando de dados dedicao
        
        mostrar_tabelas()

        conn.sendall(resposta.encode())

        conn.close()


if __name__ == "__main__":
    main()
