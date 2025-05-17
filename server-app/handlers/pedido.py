import datetime
import db.database as db
from objetos import Pedido
import random

def add_pedido(dados, idCliente):
    try:
        servico = db.getServico(dados.get("idServico"))
        
        if not servico:
            return 0, "Serviço não encontrado", {}

        if servico.esta_visivel == 0:
            return 0, "Serviço não disponível", {}

        idVendedor = db.getLoja(servico.idLoja).idCliente

        if idCliente == idVendedor:
            return 0, "Não é possível comprar o próprio serviço", {}

        print(f"ID Cliente: {idCliente}\n\nDados do pedido: {dados}")
        
        

        pedido = Pedido(
            data_pedido   = datetime.datetime.utcnow().isoformat(),
            idServico     = dados.get("idServico"),
            total         = int(dados.get("quantidade")) * servico.quantidade,
            nome_cliente = db.getCliente(idCliente).nome,
            nome_servico = servico.nome_servico,
            idCliente    = idCliente,
        )
            
        new_id = db.addPedido(pedido)

        print(f"Pedido criado: {pedido.__dict__}")
        
        if not new_id:
            return 0, "Falha ao criar pedido", {}
        
        pedido.idPedido = new_id
        
        return 200, "Pedido criado com sucesso", {"pedido": pedido.__dict__}
    
    except Exception as e:
        return 0, f"Erro ao criar pedido: {e}", {}

def calcular_tempo_chegada(estado_pedido, data_pagamento, data_entrega):
    # printar tudo
    print(f"Estado do pedido: {estado_pedido}")
    print(f"Data do pagamento: {data_pagamento}")
    print(f"Data da entrega: {data_entrega}")
    if estado_pedido == "PENDENTE":
        return "Esperando pagamento"
    
    elif estado_pedido == "ENVIADO":
        pago = datetime.datetime.fromisoformat(data_pagamento)
        entrega = datetime.datetime.fromisoformat(data_entrega)
        delta = entrega - pago
        return str(delta)
    elif estado_pedido == "CONCLUIDO":
        return "Pedido concluído"
    
    return False    

def verificar_entrega(pedido):
    if pedido.estado_pedido == "ENVIADO":
        entrega = datetime.datetime.fromisoformat(pedido.data_entrega)
        if entrega < datetime.datetime.utcnow():
            pedido.estado_pedido = "CONCLUIDO"
            db.mudarEstadoPedido(int(pedido.idPedido), pedido.estado_pedido)
            return True
    return False

def pagar_pedido(dados, idCliente):
    pid = dados.get("idPedido")
    pedido = db.getPedido(int(pid))
    
    if not pedido:
        return 0, "Pedido não encontrado", {}
    
    if int(pedido.idCliente) != idCliente:
        return 0, "Usuário não autorizado", {}
    
    if pedido.estado_pedido != "PENDENTE":
        return 0, "Pedido já pago", {}
    
    pedido.estado_pedido = "ENVIADO"

    if db.mudarEstadoPedido(int(pid), pedido.estado_pedido):
        pago_em = datetime.datetime.utcnow().isoformat()
        dias = random.randint(1, 5)
        previsto_para = (
            datetime.datetime.utcnow() + datetime.timedelta(minutes=3)
        ).isoformat()

        if db.atualizarDatasPedido(int(pid), pago_em, previsto_para):
            return 200, "Pagamento realizado com sucesso", {"pedido": pedido.__dict__}
        else:
            db.mudarEstadoPedido(int(pid), "PENDENTE")
            return 0, "Falha ao atualizar datas do pedido", {}

    return 0, "Falha ao realizar pagamento", {}



def get_pedido(dados, idCliente):
    pid = dados.get("idPedido")
    
    pedido = db.getPedido(int(pid))
    idVendedor = db.getLoja(idLoja=db.getServico(pedido.idServico).idLoja).idCliente

    
    if not pedido:
        return 0, "Pedido não encontrado", {}
    
    if int(pedido.idCliente) != idCliente and idVendedor != idCliente:
        return 0, "Usuário não autorizado", {}

    verificar_entrega(pedido)

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
