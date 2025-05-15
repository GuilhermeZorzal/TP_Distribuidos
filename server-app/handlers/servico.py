from db.database import addServico, getLoja, getServicos, getServico
from objetos import Servico, categorias
from utils.token import autorizarToken


def criar_anuncio(dados, idCliente):
    try:
        idLoja = getLoja(idCliente=idCliente).idLoja
        print(f"ID Loja: {idLoja}")
        
        servico = Servico(
            nome_servico=dados['nome_servico'],
            descricao_servico=dados['descricao_servico'],
            categoria=dados['categoria'],
            tipo_pagamento=dados['tipo_pagamento'],
            quantidade_pagamento=dados['quantidade_pagamento'],
            esta_visivel=dados['esta_visivel'],
            idLoja=idLoja
        )
        
        print(f"Serviço criado: {servico.__dict__}")
        
        id_servico = addServico(servico)
        
        if id_servico is None:
            return 0, "Erro ao criar o serviço: não foi possível inserir no banco", {}
        
        servico.idServico = id_servico
        
        return 200, "Serviço criado com sucesso", servico.__dict__
    
    except Exception as e:
        return 0, f"Erro ao criar serviço: {str(e)}", {}

def get_servico(dados):
    try:
        idServico = dados["idServico"]
        servico = getServico(idServico)
        if servico:
            return 200, "Serviço encontrado com sucesso", servico.__dict__
        else:
            return 0, "Serviço não encontrado", {}
    except Exception as e:
        return 0, f"Erro ao buscar serviço: {e}", {}

def get_categoria():
    print(200, "Categorias mostradas com sucesso", {"categorias": categorias})
    return 200, "Categorias mostradas com sucesso", {"categorias": categorias}
    
def get_catalogo(dados):
    try:

        servicos = getServicos(
            categorias=dados['categorias'],
            idLoja=dados['idLoja'],
            cont_pages=int(dados['pages'])
        )
        if not servicos:
            return 0, "Nenhum serviço encontrado", {}
        print(f"Serviços encontrados: {servicos}")
        return 200, "Serviços encontrados com sucesso", servicos
    
    except Exception as e:
        return 0, f"Erro ao buscar serviços: {str(e)}", {}