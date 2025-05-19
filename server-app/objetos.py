from dataclasses import dataclass
from typing import Optional

# categorias de serviços magicos
categorias = [
    'todas',
    'alquimia',
    'assassinato',
    'ataques',
    'cura',
    'espionagem',
    'guarda-costas',
    'magia',
    'mineração',
    'rituais',
    'trabalho',
    'transporte',
    'outros'
]

@dataclass
class Cliente:
    idCliente: Optional[int] = None
    nome: str = ""
    apelido: str = ""
    senha: str = ""
    ccm: str = ""
    contato: str = ""


@dataclass
class Loja:
    idLoja: Optional[int] = None
    nome: str = ""
    contato: str = ""
    descricao: str = ""
    idCliente: int = 0


@dataclass
class Servico:
    idServico: Optional[int] = None
    nome_servico: str = ""
    descricao_servico: str = ""
    categoria: str = ""
    tipo_pagamento: str = ""
    quantidade: float = 0.0
    esta_visivel: bool = True
    apagado: bool = False
    idLoja: int = 0


@dataclass
class Pedido:
    idPedido: Optional[int] = None
    data_pedido: str = ""
    data_pagamento: str = "Esperando pagamento"
    data_entrega: str = "Esperando pagamento"
    tempo_chegada: str = "Esperando pagamento"
    idServico: int = 0
    estado_pedido: str = "PENDENTE"  # PENDENTE, ENVIADO, CONCLUÍDO
    total: float = 0.0
    nome_cliente: str = ""
    nome_servico: str = ""
    nome_loja: str = ""
    idCliente: int = 0
