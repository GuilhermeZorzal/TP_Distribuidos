import sqlite3
import os
from objetos import Cliente, Loja, Servico, Pedido
from handlers.pedido import calcular_tempo_chegada, verificar_entrega

FILE = "./db/sqlite.db"


def conectar():
    if not os.path.exists("./db"):
        os.makedirs("./db")
    return sqlite3.connect(FILE)


def mostrar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = cursor.fetchall()

    print("Tabelas encontradas:")
    for tabela in tabelas:
        nome_tabela = tabela[0]
        print(f"- {nome_tabela.upper()}")

        # Exibe os dados de cada tabela
        cursor.execute(f"SELECT * FROM {nome_tabela}")
        linhas = cursor.fetchall()
        print("Dados:")
        for linha in linhas:
            print(linha)
        print("-" * 40)
    print("-" * 40)
    print("\n\n")
    conn.close()


def getCliente(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM cliente WHERE idCliente = ?", (id,))
    row = cur.fetchone()
    con.close()
    if row:
        # Considerando a ordem: idCliente, nome, apelido, senha, ccm, contato
        return Cliente(
            idCliente=row[0],
            nome=row[1],
            apelido=row[2],
            senha=row[3],
            ccm=row[4],
            contato=row[5],
        )
    return None


def addCliente(cliente: Cliente):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO cliente (nome, apelido, senha, ccm, contato) VALUES (?, ?, ?, ?, ?)",
            (
                cliente.nome,
                cliente.apelido,
                cliente.senha,
                cliente.ccm,
                cliente.contato,
            ),
        )
        con.commit()
        cliente.idCliente = cur.lastrowid
        return cliente.idCliente
    except Exception as e:
        print("Erro ao inserir cliente:", e)
        con.rollback()
        return None
    finally:
        con.close()


def getLoja(idCliente: int = None, idLoja: int = None):
    con = conectar()
    cur = con.cursor()

    conditions = []
    params = []
    if idCliente is not None:
        conditions.append("idCliente = ?")
        params.append(idCliente)
    if idLoja is not None:
        conditions.append("idLoja = ?")
        params.append(idLoja)

    if not conditions:
        con.close()
        return None

    # usa OR para procurar por cliente ou loja
    sql = f"SELECT * FROM loja WHERE {' OR '.join(conditions)}"
    cur.execute(sql, params)
    row = cur.fetchone()
    con.close()

    if row:
        return Loja(
            idLoja=row[0],
            nome=row[1],
            contato=row[2],
            descricao=row[3],
            idCliente=row[4],
        )
    return None


def addLoja(loja: Loja):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO loja (nome, contato, descricao, idCliente) VALUES (?, ?, ?, ?)",
            (loja.nome, loja.contato, loja.descricao, loja.idCliente),
        )
        con.commit()
        loja.idLoja = cur.lastrowid
        return loja.idLoja
    except Exception as e:
        print("Erro ao inserir loja:", e)
        con.rollback()
        return None
    finally:
        con.close()


def getServico(idServico):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM servico WHERE idServico = ?", (idServico,))
    row = cur.fetchone()
    con.close()

    if row:
        return Servico(
            idServico=row[0],
            nome_servico=row[1],
            descricao_servico=row[2],
            categoria=row[3],
            tipo_pagamento=row[4],
            quantidade=row[5],
            esta_visivel=bool(row[6]),
            idLoja=row[7],
        )
    return None


def getServicos(
    categorias: list[str] = None,
    idLoja: int = None,
    cont_pages: int = 0,
    page_size: int = 20,
):
    con = conectar()
    cur = con.cursor()

    conditions = []
    params = []

    if idLoja is not None:
        conditions.append("idLoja = ?")
        params.append(idLoja)

    else:
        conditions.append("esta_visivel = 1")

    if categorias:
        placeholders = ",".join("?" for _ in categorias)
        conditions.append(f"categoria IN ({placeholders})")
        params.extend(categorias)

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    offset = cont_pages * page_size
    sql = f"""
        SELECT *
          FROM servico
        {where_clause}
        LIMIT ? OFFSET ?
    """
    params.extend([page_size, offset])

    cur.execute(sql, params)
    rows = cur.fetchall()
    con.close()

    servicos = [
        Servico(
            idServico=row[0],
            nome_servico=row[1],
            descricao_servico=row[2],
            categoria=row[3],
            tipo_pagamento=row[4],
            quantidade=row[5],
            esta_visivel=row[6],
            idLoja=row[7],
        ).__dict__
        for row in rows
    ]
    return servicos


def mudarEstadoServico(idServico, estado):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute(
            "UPDATE servico SET esta_visivel = ? WHERE idServico = ?",
            (1 if estado else 0, idServico),
        )
        con.commit()
        return cur.rowcount > 0
    except Exception as e:
        print("Erro ao atualizar estado do serviço:", e)
        con.rollback()
        return False
    finally:
        con.close()


def addServico(servico: Servico):
    con = conectar()
    cur = con.cursor()
    try:
        nome_servico = getattr(servico, "nome_servico", "")
        cur.execute(
            "INSERT INTO servico (nome_servico, descricao_servico, categoria, tipo_pagamento, quantidade, esta_visivel, idLoja) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                nome_servico,
                servico.descricao_servico,
                servico.categoria,
                servico.tipo_pagamento,
                servico.quantidade,
                servico.esta_visivel,
                servico.idLoja,
            ),
        )
        con.commit()
        servico.idServico = cur.lastrowid
        return servico.idServico
    except Exception as e:
        print("Erro ao inserir serviço:", e)
        con.rollback()
        return None
    finally:
        con.close()


def editarServico(servico: Servico):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute(
            "UPDATE servico SET nome_servico = ?, descricao_servico = ?, categoria = ?, tipo_pagamento = ?, quantidade = ? WHERE idServico = ?",
            (
                servico.nome_servico,
                servico.descricao_servico,
                servico.categoria,
                servico.tipo_pagamento,
                servico.quantidade,
                servico.idServico,
            ),
        )
        con.commit()
        return cur.rowcount > 0
    except Exception as e:
        print("Erro ao atualizar serviço:", e)
        con.rollback()
        return False
    finally:
        con.close()


def delServico(idServico):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM servico WHERE idServico = ?", (idServico,))
        con.commit()
        return cur.rowcount > 0
    except Exception as e:
        print("Erro ao deletar serviço:", e)
        con.rollback()
        return False
    finally:
        con.close()


def getPedido(idPedido):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM pedido WHERE idPedido = ?", (idPedido,))
    row = cur.fetchone()
    con.close()

    if row:
        return Pedido(
            idPedido=row[0],
            data_pedido=row[1],
            data_pagamento=row[2],
            data_entrega=row[3],
            tempo_chegada=calcular_tempo_chegada(row[5], row[2], row[3]),
            idServico=row[4],
            estado_pedido=row[5],
            total=row[6],
            nome_cliente=getCliente(row[7]).nome,
            nome_servico=getServico(row[4]).nome_servico,
            nome_loja=getLoja(idCliente=row[7]).nome,
            idCliente=row[7],
        )
    return None


def getPedidos(idCliente):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM pedido WHERE idCliente = ?", (idCliente,))
    rows = cur.fetchall()
    con.close()

    pedidos = []
    for row in rows:
        print("AAAAAAAAAAAAAAA\n\n", row)
        pedido = Pedido(
            idPedido=row[0],
            data_pedido=row[1],
            data_pagamento=row[2],
            data_entrega=row[3],
            tempo_chegada=calcular_tempo_chegada(row[5], row[2], row[3]),
            idServico=row[4],
            estado_pedido=row[5],
            total=row[6],
            nome_cliente=getCliente(row[7]).nome,
            nome_servico=getServico(row[4]).nome_servico,
            nome_loja=getLoja(idCliente=row[7]).nome,
            idCliente=row[7],
        )
        # se já passou da data de entrega, marca como concluído
        verificar_entrega(pedido)
        pedidos.append(pedido.__dict__)

    return pedidos


def getPedidosLoja(idCliente):
    print("\n\n\n AQUI")
    loja = getLoja(idCliente=idCliente)
    if not loja:
        return []

    con = conectar()
    cur = con.cursor()
    sql = """
        SELECT p.*
          FROM pedido p
          JOIN servico s ON p.idServico = s.idServico
         WHERE s.idLoja = ?
    """
    cur.execute(sql, (loja.idLoja,))
    rows = cur.fetchall()
    con.close()

    pedidos = []
    for row in rows:
        print("****************************\nROW NO BACK", row)
        pedido = Pedido(
            idPedido=row[0],
            data_pedido=row[1],
            data_pagamento=row[2],
            data_entrega=row[3],
            tempo_chegada=calcular_tempo_chegada(row[5], row[2], row[3]),
            idServico=row[4],
            estado_pedido=row[5],
            total=row[6],
            nome_cliente=getCliente(row[7]).nome,
            nome_servico=getServico(row[4]).nome_servico,
            nome_loja=getLoja(idCliente=row[7]).nome,
            idCliente=row[7],
        )
        # se já passou da data de entrega, marca como concluído
        verificar_entrega(pedido)
        pedidos.append(pedido.__dict__)

    return pedidos


# FIXME deletar tudo
def delPedido(idPedido):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM pedido WHERE idPedido = ?", (idPedido,))
        con.commit()
        return cur.rowcount > 0
    except Exception as e:
        print("Erro ao deletar pedido:", e)
        con.rollback()
        return False
    finally:
        con.close()


def addPedido(pedido: Pedido):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO pedido (data_pedido, data_pagamento, data_entrega, idServico, estado_pedido, total,  idCliente) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                pedido.data_pedido,
                pedido.data_pagamento,
                pedido.data_entrega,
                pedido.idServico,
                pedido.estado_pedido,
                pedido.total,
                pedido.idCliente,
            ),
        )
        con.commit()
        pedido.idPedido = cur.lastrowid
        return pedido.idPedido

    except Exception as e:
        print("Erro ao inserir pedido:", e)
        con.rollback()
        return None
    finally:
        con.close()


def atualizarDatasPedido(idPedido: int, data_pagamento: str, data_entrega: str) -> bool:
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute(
            "UPDATE pedido SET data_pagamento = ?, data_entrega = ? WHERE idPedido = ?",
            (data_pagamento, data_entrega, idPedido),
        )
        con.commit()
        return cur.rowcount > 0
    except Exception as e:
        print("Erro ao atualizar datas do pedido:", e)
        con.rollback()
        return False
    finally:
        con.close()


def mudarEstadoPedido(idPedido, estado):
    if estado != "ENVIADO" and estado != "CONCLUÍDO":
        return False

    con = conectar()
    cur = con.cursor()
    try:
        cur.execute(
            "UPDATE pedido SET estado_pedido = ? WHERE idPedido = ?", (estado, idPedido)
        )
        con.commit()
        return cur.rowcount > 0
    except Exception as e:
        print("Erro ao atualizar status do pedido:", e)
        con.rollback()
        return False
    finally:
        con.close()


def reset_database():
    if os.path.exists(FILE):
        os.remove(FILE)

    criar_banco()


def criar_banco():
    con = conectar()
    cur = con.cursor()

    # Tabela Cliente
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cliente (
        idCliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        apelido TEXT NOT NULL,
        senha TEXT NOT NULL,
        ccm TEXT UNIQUE NOT NULL,
        contato TEXT NOT NULL
    );
    """)

    # Tabela Loja
    cur.execute("""
    CREATE TABLE IF NOT EXISTS loja (
        idLoja INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        contato TEXT NOT NULL,
        descricao TEXT NOT NULL,
        idCliente INTEGER NOT NULL,
        FOREIGN KEY (idCliente) REFERENCES cliente(idCliente)
    );
    """)

    # Tabela Serviço
    cur.execute("""
    CREATE TABLE IF NOT EXISTS servico (
        idServico INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_servico TEXT NOT NULL,
        descricao_servico TEXT NOT NULL,
        categoria TEXT NOT NULL,
        tipo_pagamento TEXT NOT NULL,
        quantidade REAL NOT NULL,
        esta_visivel BOOLEAN NOT NULL,
        idLoja INTEGER NOT NULL,
        FOREIGN KEY (idLoja) REFERENCES loja(idLoja)
    );
    """)

    # Tabela Pedido
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pedido (
        idPedido INTEGER PRIMARY KEY AUTOINCREMENT,
        data_pedido TEXT NOT NULL,
        data_pagamento TEXT NOT NULL,
        data_entrega TEXT NOT NULL,
        idServico INTEGER NOT NULL,
        estado_pedido TEXT NOT NULL,
        total REAL NOT NULL,
        idCliente INTEGER NOT NULL,
        FOREIGN KEY (idServico) REFERENCES servico(idServico),
        FOREIGN KEY (idCliente) REFERENCES cliente(idCliente)
    );
    """)

    con.commit()
    con.close()


criar_banco()
