import Pyro5.api
from time import sleep
from Pyro5.errors import NamingError
from serverClass import Server


# Localizar o Name Server
def locate_ns(retries: int = 3) -> Pyro5.client.Proxy:
    for i in range(retries):
        try:
            return Pyro5.api.locate_ns()
        except NamingError as e:
            print(f"[NameServer] Não encontrado, tentativa {i + 1}/{retries}...")
            sleep(0.1)
            
    raise Exception("[Servidor] Não foi possível localizar o Name Server")


def main():
    # daemon = Pyro5.api.Daemon(host="0.0.0.0")
    daemon = Pyro5.api.Daemon(host="oco_do_ogro_server") 

    ns = locate_ns()
    servidor = Server()
    uri = daemon.register(servidor)
    ns.register("servidor", uri) # Registrando o objeto no Name Server com o nome "servidor"

    print("[Servidor] Registrado no Name Server com sucesso.")
    print(f"[Servidor] Object URI: {uri}")
    daemon.requestLoop()


if __name__ == "__main__":
    main()
