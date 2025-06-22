import Pyro5.api
from handlers import cadastro, login, loja, servico, pedido
from db.database import reset_database
from utils.token import autenticar_wrapper




@Pyro5.api.expose
class Server:
    def __init__(self):
        print("[Servidor] Servidor iniciado.")

    # Funções que não precisam de autenticação
    def cadastrar(self, dados):
        return cadastro.cadastrar(dados)

    def autenticar(self, dados):
        return login.autenticar_cliente(dados)

    def get_categoria(self):
        return servico.get_categoria()

    # Funções com autenticação obrigatória
    
    # Lojas
    @autenticar_wrapper
    def criar_loja(self, idCliente, dados):
        return loja.criar_loja(dados, idCliente)

    @autenticar_wrapper
    def get_minha_loja(self, idCliente):
        return loja.get_minha_loja(idCliente)

    @autenticar_wrapper
    def tem_loja(self, idCliente):
        return loja.tem_loja(idCliente)

    @autenticar_wrapper
    def get_loja(self, idCliente, dados):
        return loja.get_loja(dados)

    # Serviços
    @autenticar_wrapper
    def criar_anuncio(self, idCliente, dados):
        return servico.criar_anuncio(dados, idCliente)

    @autenticar_wrapper
    def get_catalogo(self, idCliente, dados):
        return servico.get_catalogo(dados)

    @autenticar_wrapper
    def get_servico(self, idCliente, dados):
        return servico.get_servico(dados)

    @autenticar_wrapper
    def ocultar_servico(self, idCliente, dados):
        return servico.mudar_estado_servico(dados, 0)

    @autenticar_wrapper
    def desocultar_servico(self, idCliente, dados):
        return servico.mudar_estado_servico(dados, 1)

    @autenticar_wrapper
    def deletar_servico(self, idCliente, dados):
        return servico.deletar_servico(dados, idCliente)

    @autenticar_wrapper
    def editar_servico(self, idCliente, dados):
        return servico.editar_servico(dados, idCliente)

    # Pedidos
    @autenticar_wrapper
    def add_pedido(self, idCliente, dados):
        return pedido.add_pedido(dados, idCliente)

    @autenticar_wrapper
    def pagar_pedido(self, idCliente, dados):
        return pedido.pagar_pedido(dados, idCliente)

    @autenticar_wrapper
    def get_pedido(self, idCliente, dados):
        return pedido.get_pedido(dados, idCliente)

    @autenticar_wrapper
    def get_pedidos(self, idCliente):
        return pedido.get_pedidos(idCliente)

    @autenticar_wrapper
    def get_pedidos_minha_loja(self, idCliente):
        return pedido.get_pedidos_minha_loja(idCliente)

    @autenticar_wrapper
    def cancelar_pedido(self, idCliente, dados):
        return pedido.cancelar_pedido(dados, idCliente)

    @autenticar_wrapper
    def reset_database(self, idCliente):
        reset_database()
        return 200, "Banco de dados resetado", {}
