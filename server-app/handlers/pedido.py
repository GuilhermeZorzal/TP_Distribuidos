import datetime
import db.database as db
from objetos import Pedido

def add_pedido(dados, idCliente):
    try:
        servico = db.getServico(dados.get("idServico"))
        if not servico:
            return 0, "Serviço não encontrado", {}

        pedido = Pedido(
            data_pedido   = datetime.datetime.utcnow().isoformat(),
            idServico     = dados.get("idServico"),
            total         = int(dados.get("quantidade")) * servico.quantidade,
            nome_cliente= db.getCliente(idCliente).nome,
            idCliente     = idCliente,
        )
        
        new_id = db.addPedido(pedido)

        if not new_id:
            return 0, "Falha ao criar pedido", {}
        
        pedido.idPedido = new_id
        
        return 200, "Pedido criado com sucesso", {"pedido": pedido.__dict__}
    
    except Exception as e:
        return 0, f"Erro ao criar pedido: {e}", {}
    

def pagar_pedido(dados, idCliente):
    pid = dados.get("idPedido")
    pedido = db.getPedido(int(pid))
    
    if not pedido:
        return 0, "Pedido não encontrado", {}
    if int(pedido.idCliente) != idCliente:
        return 0, "Usuário não autorizado", {}
    if pedido.estado_pedido != "PENDENTE":
        return 0, "Pedido já pago", {}
    
    pedido.estado_pedido = "ANDAMENTO"

    if db.mudarEstadoPedido(int(pid), pedido.estado_pedido):
        return 200, "Pagamento realizado com sucesso", {"pedido": pedido.__dict__}
    
    return 0, "Falha ao realizar pagamento", {}

def get_pedido(dados, idCliente):
    pid = dados.get("idPedido")
    print("\n\n", pid, "\n\n")
    pedido = db.getPedido(int(pid))
    
    if not pedido:
        return 0, "Pedido não encontrado", {}
    if int(pedido.idCliente) != idCliente:
        return 0, "Usuário não autorizado", {}
    
    return 200, "Pedido recuperado", {"pedido": pedido.__dict__}

def get_pedidos(idCliente):
    lista = db.getPedidos(idCliente)
    return 200, "Pedidos do cliente", {"pedidos": lista}

def get_pedidos_minha_loja(idCliente):
    lista = db.getPedidosLoja(idCliente)
    return 200, "Pedidos da loja", {"pedidos": lista}

def cancelar_pedido(dados, idCliente):
    pid = dados.get("idPedido")
    pedido = db.getPedido(pid)
    if not pedido:
        return 0, "Pedido não encontrado", {}
    if pedido.idCliente != idCliente:
        return 0, "Usuário não autorizado", {}
    ok = db.delPedido(pid)
    if not ok:
        return 0, "Falha ao cancelar pedido", {}
    return 200, "Pedido cancelado com sucesso", {}
