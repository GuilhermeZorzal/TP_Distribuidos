import datetime
from db.database import (
    addPedido,
    getPedido   as db_getPedido,
    getPedidos,
    getPedidosLoja,
    delPedido,
    conectar
)
from objetos import Pedido

def realizar_pedido(idCliente, dados):
    try:
        pedido = Pedido(
            data_pedido   = datetime.datetime.utcnow().isoformat(),
            idServico     = dados.get("idServico"),
            estado_pedido = "PENDENTE",
            total         = dados.get("quantidade"),
            nome_cliente  = "",
            idCliente     = idCliente
        )
        new_id = addPedido(pedido)
        if not new_id:
            return 0, "Falha ao criar pedido", {}
        pedido.idPedido = new_id
        return 200, "Pedido criado com sucesso", {"pedido": pedido.__dict__}
    except Exception as e:
        return 0, f"Erro ao criar pedido: {e}", {}

def get_pedido(idCliente, dados):
    pid = dados.get("idPedido")
    pedido = db_getPedido(pid)
    if not pedido:
        return 404, "Pedido não encontrado", {}
    if pedido.idCliente != idCliente:
        return 403, "Usuário não autorizado", {}
    return 200, "Pedido recuperado", {"pedido": pedido.__dict__}

def get_pedidos(idCliente, dados):
    lst = getPedidos(idCliente)
    return 200, "Pedidos do cliente", {"pedidos": lst}

def get_pedidos_minha_loja(idCliente, dados):
    lst = getPedidosLoja(idCliente)
    return 200, "Pedidos da loja", {"pedidos": lst}

def cancelar_pedido(idCliente, dados):
    pid = dados.get("idPedido")
    pedido = db_getPedido(pid)
    if not pedido:
        return 404, "Pedido não encontrado", {}
    if pedido.idCliente != idCliente:
        return 403, "Usuário não autorizado", {}
    ok = delPedido(pid)
    if not ok:
        return 0, "Falha ao cancelar pedido", {}
    return 200, "Pedido cancelado com sucesso", {}

def realizar_pagamento(idCliente, dados):
    pid = dados.get("idPedido")
    pedido = db_getPedido(pid)
    if not pedido:
        return 404, "Pedido não encontrado", {}
    if pedido.idCliente != idCliente:
        return 403, "Usuário não autorizado", {}
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute(
            "UPDATE pedido SET estado_pedido = ? WHERE idPedido = ?",
            ("PAGO", pid)
        )
        con.commit()
        return 200, "Pagamento realizado com sucesso", {}
    except Exception as e:
        con.rollback()
        return 0, f"Erro ao processar pagamento: {e}", {}
    finally:
        con.close()