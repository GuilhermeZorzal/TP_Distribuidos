from utils.token import gerar_token
from db.database import addCliente
from objetos import Cliente
import json

def cadastrar(dados):
    try:
        # Cria a instância do cliente com os dados recebidos
        cliente = Cliente(
            nome=dados['nome'],
            apelido=dados['apelido'],
            senha=dados['senha'],
            ccm=dados['ccm'],
            contato=dados['contato']
        )
        
        # Insere o cliente no banco e atualiza o id na instância
        id_cliente = addCliente(cliente)
        if id_cliente is None:
            return 0, "Erro ao cadastrar: cliente não inserido", {}
        
        token = gerar_token(cliente)
        
        return 200, "Cadastro realizado com sucesso", {"tokenCliente": token}
    
    except Exception as e:
        return 0, f"Erro ao cadastrar: {str(e)}", {}