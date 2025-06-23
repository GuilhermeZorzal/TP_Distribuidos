import Pyro5.api
from handlers import cadastro, login, loja, servico, pedido
from db.database import reset_database
from utils.token import autenticar_decorator
from utils.utils import formatar_mensagem_decorator
from db.database import copiar_banco_base, mostrar_tabelas


@Pyro5.api.expose
class Server:
    def __init__(self):
        print("[Servidor] Servidor iniciado.")
        copiar_banco_base()
        # mostrar_tabelas()

    # Funções que não precisam de autenticação
    
    @formatar_mensagem_decorator
    def cadastrar(self, msg):
        dados = msg.get("dados", {})
        return cadastro.cadastrar(dados)

    @formatar_mensagem_decorator
    def autenticar(self, msg):
        dados = msg.get("dados", {})
        return login.autenticar_cliente(dados)

    @formatar_mensagem_decorator
    def get_categoria(self, msg):
        return servico.get_categoria()

    # Funções com autenticação obrigatória
    
    # Lojas
    @formatar_mensagem_decorator
    @autenticar_decorator
    def criar_loja(self, idCliente, dados):
        return loja.criar_loja(dados, idCliente)

    @formatar_mensagem_decorator
    @autenticar_decorator
    def get_minha_loja(self, idCliente):
        return loja.get_minha_loja(idCliente)

    @formatar_mensagem_decorator
    @autenticar_decorator
    def tem_loja(self, idCliente):
        return loja.tem_loja(idCliente)

    @formatar_mensagem_decorator
    @autenticar_decorator
    def get_loja(self, dados):
        return loja.get_loja(dados)

    # Serviços
    @formatar_mensagem_decorator
    @autenticar_decorator
    def criar_anuncio(self, idCliente, dados):
        return servico.criar_anuncio(dados, idCliente)

    @formatar_mensagem_decorator
    @autenticar_decorator
    def get_catalogo(self, dados):
        return servico.get_catalogo(dados)

    @formatar_mensagem_decorator
    @autenticar_decorator
    def get_servico(self, dados):
        return servico.get_servico(dados)

    @formatar_mensagem_decorator
    @autenticar_decorator
    def ocultar_servico(self, dados):
        return servico.mudar_estado_servico(dados, 0)

    @formatar_mensagem_decorator
    @autenticar_decorator
    def desocultar_servico(self, dados):
        return servico.mudar_estado_servico(dados, 1)

    @formatar_mensagem_decorator
    @autenticar_decorator
    def deletar_servico(self, idCliente, dados):
        return servico.deletar_servico(dados, idCliente)

    @formatar_mensagem_decorator
    @autenticar_decorator
    def editar_servico(self, idCliente, dados):
        return servico.editar_servico(dados, idCliente)

    # Pedidos
    @formatar_mensagem_decorator
    @autenticar_decorator
    def add_pedido(self, idCliente, dados):
        return pedido.add_pedido(dados, idCliente)

    @formatar_mensagem_decorator
    @autenticar_decorator
    def pagar_pedido(self, idCliente, dados):
        return pedido.pagar_pedido(dados, idCliente)

    @formatar_mensagem_decorator
    @autenticar_decorator
    def get_pedido(self, idCliente, dados):
        return pedido.get_pedido(dados, idCliente)

    @formatar_mensagem_decorator
    @autenticar_decorator
    def get_pedidos(self, idCliente):
        return pedido.get_pedidos(idCliente)

    @formatar_mensagem_decorator
    @autenticar_decorator
    def get_pedidos_minha_loja(self, idCliente):
        return pedido.get_pedidos_minha_loja(idCliente)

    @formatar_mensagem_decorator
    @autenticar_decorator
    def cancelar_pedido(self, idCliente, dados):
        return pedido.cancelar_pedido(dados, idCliente)

    @formatar_mensagem_decorator
    @autenticar_decorator
    def reset(self):
        reset_database()
        return 200, "Banco de dados resetado", {}
