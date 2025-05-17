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
print("PORTA", PORT)

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

    func = mensagem["funcao"]
    dados = mensagem.get("dados", {})

    # Handlers que não precisam de autenticação
    no_auth_handlers = {
        "cadastrar": cadastro.cadastrar,
        "autenticar": login.autenticar_cliente,
        "get_categoria": lambda dados: servico.get_categoria(),
    }
    
    if func in no_auth_handlers:
        return no_auth_handlers[func](dados)

    # Autenticação obrigatória
    try:
        status, msg, idCliente = autorizarToken(dados.get("tokenCliente", ""))
        if status != 200:
            return status, msg, {}
    except Exception as e:
        return 0, f"Erro ao verificar Token: {e}", {}

    idCliente = int(idCliente)

    # Handlers que requerem autenticação
    auth_handlers = {
        "criar_loja": lambda d: loja.criar_loja(d, idCliente),
        "get_minha_loja": lambda d: loja.get_minha_loja(idCliente),
        "tem_loja":      lambda d: loja.tem_loja(idCliente),
        "get_loja":      lambda d: loja.get_loja(d),
        "criar_anuncio": lambda d: servico.criar_anuncio(d, idCliente),
        "get_catalogo":  lambda d: servico.get_catalogo(d),
        "get_servico":   lambda d: servico.get_servico(d),
        "ocultar_servico":   lambda d: servico.mudar_estado_servico(d, 0),
        "desocultar_servico": lambda d: servico.mudar_estado_servico(d, 1),
        "deletar_servico":   lambda d: servico.deletar_servico(d, idCliente),
        "editar_servico":    lambda d: servico.editar_servico(d, idCliente),
        "add_pedido":        lambda d: pedido.add_pedido(d, idCliente),
        "pagar_pedido":      lambda d: pedido.pagar_pedido(d, idCliente),
        "get_pedido":        lambda d: pedido.get_pedido(d, idCliente),
        "get_pedidos":       lambda d: pedido.get_pedidos(idCliente),
        "get_pedidos_minha_loja": lambda d: pedido.get_pedidos_minha_loja(idCliente),
        "cancelar_pedido":   lambda d: pedido.cancelar_pedido(d, idCliente),
        "reset":             lambda d: (reset_database(), (200, "Banco de dados resetado", {}))[1],
    }

    handler = auth_handlers.get(func)
    if not handler:
        return formatar_mensagem(0, "Função não reconhecida", {})

    return handler(dados)


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

        print(f"Resposta Servidor: {resposta}")
        # FIXME:
        # if "dados" in resposta:
        #     if "esta_visivel" in resposta["dados"]:
        #         print(f"Mensagem recebida: {type(resposta['dados']['esta_visivel'])}")

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
