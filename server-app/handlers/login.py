from utils.token import gerar_token
from db.database import conectar, getCliente
from utils.hash import verify_password

def autenticar_cliente(dados):
    conn = conectar()
    cur = conn.cursor()
    try:
        # busca hash e id pelo ccm
        cur.execute(
            "SELECT idCliente, senha FROM cliente WHERE ccm = ?",
            (dados["ccm"],)
        )
        row = cur.fetchone()
        if not row:
            return 0, "CCM ou senha incorretos", {}
        
        id_cliente, stored_hash = row
        # verifica senha
        if not verify_password(stored_hash, dados["senha"]):
            return 0, "CCM ou senha incorretos", {}

        cliente = getCliente(id_cliente)
        if cliente is None:
            return 0, "Erro: cliente não encontrado", {}

        token = gerar_token(cliente)
        print(f"Token gerado: {token}")
        return 200, "Autenticação realizada com sucesso", {"tokenCliente": token}

    except Exception as e:
        return 0, f"Erro ao autenticar: {e}", {}
    finally:
        conn.close()