from utils.token import gerar_token
from db.database import conectar, getCliente
from objetos import Cliente

def autenticar_cliente(dados):
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute(
            "SELECT idCliente FROM cliente WHERE ccm = ? AND senha = ?",
            (dados['ccm'], dados['senha'])
        )
        resultado = cur.fetchone()
        
        if resultado:
            id_cliente = resultado[0]
            cliente = getCliente(id_cliente)
            if cliente is None:
                return 0, "Erro: cliente não encontrado", {}
            
            token = gerar_token(cliente)
            print(f"Token gerado: {token}")
            return 200, "Autenticação realizada com sucesso", {"tokenCliente": token}
        else:
            return 0, "CCM ou senha incorretos", {}
    except Exception as e:
        return 0, f"Erro ao autenticar: {str(e)}", {}
    finally:
        conn.close()