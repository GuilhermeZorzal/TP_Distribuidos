from db.database import addLoja, getLoja
from objetos import Loja
from utils.token import autorizarToken

def criar_loja(dados):
    try:
        # Cria a instância da loja com os dados recebidos
        status, msg, idCliente =  autorizarToken(dados['token'])
        
        if status != 200:
            return status, msg, {}
        
        loja = Loja(
            nome=dados['nome'],
            contato=dados['contato'],
            descricao=dados['descricao'],
            idCliente=idCliente
        )
        print(f"Loja criada: {loja.__dict__}")
        
        id_loja = addLoja(loja)
        
        if id_loja is None:
            return 0, "Erro ao criar a loja: não foi possível inserir no banco", {}
        
        loja.idLoja = id_loja
        
        return 200, "Loja criada com sucesso", loja.__dict__
    
    except Exception as e:
        return 0, f"Erro ao criar loja: {str(e)}", {}


# faça verificar caso o usuario possui uma loja
def tem_loja(dados):
    
    try:
        status, msg, idCliente = autorizarToken(dados['token'])
        if status != 200:
            return status, msg, {}

        loja = getLoja(idCliente=idCliente)
        if loja:
            return 200, "Usuário possui loja", {"resposta": True}
        else:
            return 200, "Usuário não possui loja", {"resposta": False}

    except Exception as e:
        return 0, f"Erro ao verificar loja: {e}", {}
    
def get_loja(dados):
    try:
        idLoja = dados['idLoja']
        loja = getLoja(idLoja=idLoja)
        if loja:
            return 200, "Loja encontrada", loja.__dict__
        else:
            return 0, "Loja não encontrada", {}
    
    except Exception as e:
        return 0, f"Erro ao obter loja: {e}", {}
    