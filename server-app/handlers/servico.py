import db.database as db
from objetos import Servico, categorias
from utils.token import autorizarToken


def criar_anuncio(dados, idCliente):
    try:
        idLoja = db.getLoja(idCliente=idCliente).idLoja
        print(f"ID Loja: {idLoja}")

        servico = Servico(
            nome_servico=dados["nome_servico"],
            descricao_servico=dados["descricao_servico"],
            categoria=dados["categoria"],
            tipo_pagamento=dados["tipo_pagamento"],
            quantidade=dados["quantidade"],
            idLoja=idLoja,
        )

        id_servico = db.addServico(servico)
        
        print(f"Serviço criado: {servico.__dict__}")

        if id_servico is None:
            return 0, "Erro ao criar o serviço: não foi possível inserir no banco", {}

        servico.idServico = id_servico

        return 200, "Serviço criado com sucesso", {"servico": servico.__dict__}

    except Exception as e:
        return 0, f"Erro ao criar serviço: {str(e)}", {}


def get_servico(dados):
    try:
        idServico = dados["idServico"]
        servico = db.getServico(idServico)
        if servico:
            return 200, "Serviço encontrado com sucesso", {"servico": servico.__dict__}
        else:
            return 0, "Serviço não encontrado", {}
    except Exception as e:
        return 0, f"Erro ao buscar serviço: {e}", {}


def get_categoria():
    print(200, "Categorias mostradas com sucesso", {"categorias": categorias})
    return 200, "Categorias mostradas com sucesso", {"categorias": categorias}

def mudar_estado_servico(dados, estado):
    try:
        idServico = dados["idServico"]
        servico = db.getServico(idServico)
        if servico:
            db.mudarEstadoServico(servico, estado)
            servico.esta_visivel = estado
            return 200, "Estado do serviço atualizado com sucesso", {"servico": servico.__dict__}
        else:
            return 0, "Serviço não encontrado", {}
    except Exception as e:
        return 0, f"Erro ao mudar estado do serviço: {e}", {}

def deletar_servico(dados, idCliente):
    try:
        idServico = dados["idServico"]
        servico = db.getServico(idServico)
        if not servico:
            return 0, "Serviço não encontrado", {}
        if servico.idLoja != db.getLoja(idCliente).idLoja:
            return 0, "Usuário não autorizado a deletar este serviço", {}

        db.delServico(servico.idServico)
        return 200, "Serviço deletado com sucesso", {}
    except Exception as e:
        return 0, f"Erro ao deletar serviço: {e}", {}

def get_catalogo(dados):
    try:
        print(f"Dados recebidos: {dados}")
        servicos = db.getServicos(
            categorias=dados["categorias"],
            idLoja=dados["idLoja"],
            cont_pages=int(dados["pages"]),
        )
        if not servicos:
            return 200, "Nenhum serviço encontrado", {"servicos": []}
        print(f"Serviços encontrados: {servicos}")
        return 200, "Serviços encontrados com sucesso", {"servicos": servicos}

    except Exception as e:
        return 0, f"Erro ao buscar serviços: {str(e)}", {}

