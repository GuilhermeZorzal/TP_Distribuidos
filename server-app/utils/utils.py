import datetime
import json
from objetos import Pedido 

def formatar_mensagem(status, mensagem, dados):
    dados["pedido"] = formatar_pedido(dados)
        
    return json.dumps({
        "status": status,
        "mensagem": mensagem,
        "dados": dados
    })

def formatar_pedido(dados):
    if dados.get("pedido") is None and dados.get("pedidos") is None:
        return False
    
    if dados.get("pedido") is not None:
        formatar_data(dados["pedido"])
        return dados["pedido"]

    if dados.get("pedidos") is not None:
        for pedido in dados["pedidos"]:
            formatar_data(pedido)
        return dados["pedidos"]

    return False

def formatar_data(pedido: Pedido):
    # formato = dia / mes / ano - hora : minuto : segundo
    formato = "%d/%m/%Y - %H:%M:%S"
    
    pedido["data_pedido"] = datetime.datetime.fromisoformat(pedido["data_pedido"]).strftime(formato)

    if pedido["data_pagamento"] != "Esperando pagamento":
        pedido["data_pagamento"] = datetime.datetime.fromisoformat(pedido["data_pagamento"]).strftime(formato)

    if pedido["data_entrega"] != "Esperando pagamento":
        pedido["data_entrega"] = datetime.datetime.fromisoformat(pedido["data_entrega"]).strftime(formato)

    if pedido["tempo_chegada"] != "Esperando pagamento":
        # formato =  dia - hora : minuto : segundo
        formato = "%d - %H:%M:%S"
        pedido["tempo_chegada"] = datetime.datetime.fromisoformat(pedido["tempo_chegada"]).strftime(formato)

def calcular_tempo_chegada(estado_pedido, data_pagamento, data_entrega):
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

def verificar_entrega(pedido: Pedido):
    if pedido.estado_pedido == "ENVIADO":
        entrega = datetime.datetime.fromisoformat(pedido.data_entrega)
        if entrega < datetime.datetime.utcnow():
            pedido.estado_pedido = "CONCLUIDO"
            db.mudarEstadoPedido(int(pedido.idPedido), pedido.estado_pedido)
            return True
    return False
    