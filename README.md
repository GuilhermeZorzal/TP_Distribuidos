# Trabalho prático de distribuidos 

Repositório destinado para a construção do trabalho prático de dsitribuidos. 

# Executando com o Docker (Recomendado)

Basta executar o comando `docker compose up --build`

Dependendo da distribuição que você estiver usando, pode ser que o comando seja `docker-compose up --build` (com um hífen)

Note que é necessário executar o build apenas na primeira vez. Nas execuções subsequentes, basta executar `docker compose up` (ou `docker-compose up`)

# Executando sem o Docker

Para executar sem o docker: 
1. Execute `make install` para instalar as dependencias
2. Execute o comando make para executar todos os processos de uma vez

Caso essa opção não esteja funcionando, você pode tentar executar os processos individualmente:
1. Abra um terminal e execute `make name-server` na raiz do projeto 
2. Abra outro terminal e execute `make server` na raiz do projeto 
3. Abra outro terminal e execute `make client` na raiz do projeto 

Os comandos devem ser executados nessa ordem devido à ordem de dependencia entre eles.

