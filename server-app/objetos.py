from dataclasses import dataclass
from typing import Optional

# categorias de serviços magicos
categorias = [
    "magia",
    "maldição",
    "ser mistico",
    "proteção",
    "assassinato",
    "invocação",
    "cura",
    "transformação",
    "adivinhação",
    "alquimia",
    "encantamento",
    "necromancia",
    "viagem planar",
    "contrato sombrio",
    "domesticação mágica",
    "bênção divina",
    "ilusão",
    "espionagem etérea",
    "caça a monstros",
    "rompimento de selos"
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
    idLoja: int = 0

@dataclass
class Pedido:
    idPedido: Optional[int] = None
    data_pedido: str = ""
    idServico: int = 0
    estado_pedido: str = "PENDENTE"  # PENDENTE, ANDAMENTO, CONCLUÍDO
    total: float = 0.0
    nome_cliente: str = ""
    idCliente: int = 0
