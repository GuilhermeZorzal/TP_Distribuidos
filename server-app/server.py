import socket
import sqlite3
import os

PORT = 50051
HOST = "0.0.0.0"

FILE = "./db/sqlite.db"


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Especifica a qual porta conectar o socket
    server.bind((HOST, PORT))
    server.listen()

    print(f"Servidor ouvindo em {HOST}:{PORT}")

    while True:
        # Conn = connection:  é a nova conexão
        # TODO: usar thread aqui
        conn, addr = server.accept()
        print(f"Conexão recebida de {addr}")

        nome = conn.recv(1024).decode()
        if not nome:
            break

        # TODO: isolar as funcoes de sql.
        # - create {table}
        # - select ...
        # -> se encapsular em funcoes fica mais facil de gerenciar
        # O arquivo sqlite.db é o banco de dados: não existe um servico de bando de dados dedicao
        connDB = sqlite3.connect(FILE)
        cursor = connDB.cursor()
        try:
            cursor.execute("SELECT * FROM users")
            for row in cursor.fetchall():
                print(row)
        except sqlite3.Error as e:
            print("Erro no db:", e)

        connDB.close()

        resposta = f"roi {nome}, né?"
        conn.sendall(resposta.encode())

        conn.close()


if __name__ == "__main__":
    main()
