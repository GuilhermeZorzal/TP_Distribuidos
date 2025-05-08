# Tutorial: Sistema Distribuído Simples com Sockets e PyQt

### Descrição
> Este projeto implementa um sistema distribuído simples usando Python e sockets, com um servidor e um cliente com interface gráfica em PyQt6. O sistema funciona da seguinte maneira: 
> 1. O usuário insere um nome na interface gráfica.
> 2. O cliente se conecta ao servidor e envia esse nome.
> 3. O servidor responde com a mensagem "roi {nome}, né?".
> 4. A interface exibe essa resposta na tela.

## Como Rodar

### Passo 1: Instalar o Docker

> Linux:
1. Instale a Docker Engine (não o Docker Desktop).
2. Execute os seguintes comandos:
```sh
sudo groupadd docker
sudo usermod -aG docker $USER
shutdown --reboot now
```
3. Se for necessário liberar o acesso do seu display para o Docker, execute:
```sh
xhost +local:*
```

### Passo 2: Construir e Executar os Contêineres
Na raiz do projeto, execute os seguintes comandos:

```sh
docker-compose build
docker-compose up
```

Se preferir, você pode executar os contêineres separados para cada servidor em um terminal diferente:

```sh
docker-compose build nome_do_servico
docker-compose up nome_do_servico
```

### Passo 3: Acessar a Interface
Após os contêineres estarem em execução, uma janela será aberta com a interface definida.

## Observações
- O projeto está configurado para rodar utilizando o Docker Compose, o que facilita a execução dos contêineres simultaneamente.

- Certifique-se de que o Docker e o Docker Compose estão corretamente instalados no seu sistema antes de rodar os contêineres.

- Você pode conferir mais sobre a instalação e uso do Docker bem como outro exemplo do uso de Sockets no tutorial feito pelo monitor Henrique em 2024: [Tutorial Docker](https://github.com/piface314/ccf355-template-docker/tree/main)