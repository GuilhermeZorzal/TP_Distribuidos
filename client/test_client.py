import unittest
from unittest.mock import patch
import json
from client import cadastrar, autenticar, criar_loja, esta_logado, criar_anuncio, get_categoria, get_catalago, get_servico, get_loja, get_pedido, get_pedidos, get_pedidos_minha_loja, cancelar_pedido, editar_servico, ocultar_servico, desocultar_servico, apagar_servico, get_minha_loja, realizar_pedido

# O código das funções a serem testadas vem do seu código original
# Como exemplo, vamos testar a função 'cadastrar' (mas o processo seria o mesmo para todas as outras funções)

class TestSocketClientFunctions(unittest.TestCase):

    @patch('interface_socket.interface_socket.sendMessage')
    def test_cadastrar_success(self, mock_send_message):
        # Definir a resposta mockada para o servidor
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Cadastro realizado com sucesso",
            "dados": {"tokenCliente": "token_fake"}
        }

        # Simulando os parâmetros para o cadastro
        nome = "Jonas"
        apelido = "Jonny"
        senha = "senha123"
        ccm = "123456789"
        contato = "jonny@mail.com"

        # Chamar a função
        status, mensagem, _ = cadastrar(nome, apelido, senha, ccm, contato)

        # Verificar se a resposta foi correta
        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Cadastro realizado com sucesso")

    @patch('interface_socket.interface_socket.sendMessage')
    def test_autenticar_success(self, mock_send_message):
        # Definir a resposta mockada para o servidor
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Autenticação bem-sucedida",
            "dados": {"tokenCliente": "token_fake"}
        }

        # Simulando os parâmetros de autenticação
        ccm = "123456789"
        senha = "senha123"

        # Chamar a função
        status, mensagem, _ = autenticar(ccm, senha)
        
        
        print("\n\n\n\n\n")

        # Verificar se a resposta foi correta
        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Autenticação bem-sucedida")

    @patch('interface_socket.interface_socket.sendMessage')
    def test_esta_logado_success(self, mock_send_message):
        global tokenCliente
        tokenCliente = "token_fake"

        # Chamar a função
        status, mensagem, _ = esta_logado()

        # Verificar se a resposta foi correta
        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Usuário está autentificado!")

    @patch('interface_socket.interface_socket.sendMessage')
    def test_criar_loja_success(self, mock_send_message):
        # Definir a resposta mockada para o servidor
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Loja criada com sucesso",
            "dados": {"idLoja": 12345}
        }

        # Simulando os parâmetros para criar loja
        nome_loja = "Loja do Jonny"
        contato = "contato@lojajonny.com"
        descricao = "Loja especializada em produtos diversos"

        # Chamar a função
        status, mensagem, _ = criar_loja(nome_loja, contato, descricao)

        # Verificar se a resposta foi correta
        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Loja criada com sucesso")

    @patch('interface_socket.interface_socket.sendMessage')
    def test_get_categoria_success(self, mock_send_message):
        # Definir a resposta mockada para o servidor
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Categorias obtidas com sucesso",
            "dados": {"categorias": ["Categoria 1", "Categoria 2"]}
        }

        # Chamar a função
        status, mensagem, categorias = get_categoria()

        # Verificar se a resposta foi correta
        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Categorias obtidas com sucesso")
        self.assertListEqual(categorias["categorias"], ["Categoria 1", "Categoria 2"])

    @patch('interface_socket.interface_socket.sendMessage')
    def test_get_catalogo_success(self, mock_send_message):
        # Definir a resposta mockada para o servidor
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Catálogo obtido com sucesso",
            "dados": {"servicos": ["Serviço 1", "Serviço 2"]}
        }

        # Simulando os parâmetros para obter o catálogo
        categorias = ["Categoria 1", "Categoria 2"]
        idLoja = 12345

        # Chamar a função
        status, mensagem, dados = get_catalago(categorias, idLoja)

        # Verificar se a resposta foi correta
        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Catálogo obtido com sucesso")
        self.assertListEqual(dados["servicos"], ["Serviço 1", "Serviço 2"])

    @patch('interface_socket.interface_socket.sendMessage')
    def test_get_servico_success(self, mock_send_message):
        # Definir a resposta mockada para o servidor
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Serviço encontrado com sucesso",
            "dados": {"servico": "Serviço de limpeza"}
        }

        # Simulando os parâmetros para obter o serviço
        idServico = 1

        # Chamar a função
        status, mensagem, dados = get_servico(idServico)

        # Verificar se a resposta foi correta
        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Serviço encontrado com sucesso")
        self.assertEqual(dados["servico"], "Serviço de limpeza")

    @patch('interface_socket.interface_socket.sendMessage')
    def test_cancelar_pedido_success(self, mock_send_message):
        # Definir a resposta mockada para o servidor
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Pedido cancelado com sucesso"
        }

        # Simulando os parâmetros para cancelar o pedido
        idPedido = 12345

        # Chamar a função
        status, mensagem, _ = cancelar_pedido(idPedido)

        # Verificar se a resposta foi correta
        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Pedido cancelado com sucesso")
    
    @patch('interface_socket.interface_socket.sendMessage')
    def test_criar_anuncio_success(self, mock_send_message):
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Anúncio criado com sucesso"
        }

        status, mensagem, _ = criar_anuncio("Título", "Descrição", 100.0, "Categoria", 5)

        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Anúncio criado com sucesso")


    @patch('interface_socket.interface_socket.sendMessage')
    def test_get_loja_success(self, mock_send_message):
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Loja obtida com sucesso",
            "dados": {"nome": "Minha Loja"}
        }

        status, mensagem, dados = get_loja(123)

        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Loja obtida com sucesso")
        self.assertEqual(dados["nome"], "Minha Loja")

    @patch('interface_socket.interface_socket.sendMessage')
    def test_get_pedido_success(self, mock_send_message):
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Pedido encontrado com sucesso",
            "dados": {"idPedido": 1}
        }

        status, mensagem, dados = get_pedido(1)

        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Pedido encontrado com sucesso")
        self.assertEqual(dados["idPedido"], 1)

    @patch('interface_socket.interface_socket.sendMessage')
    def test_get_pedidos_success(self, mock_send_message):
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Pedidos obtidos com sucesso",
            "dados": {"pedidos": [1, 2, 3]}
        }

        status, mensagem, dados = get_pedidos()

        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Pedidos obtidos com sucesso")
        self.assertListEqual(dados["pedidos"], [1, 2, 3])

    @patch('interface_socket.interface_socket.sendMessage')
    def test_get_pedidos_minha_loja_success(self, mock_send_message):
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Pedidos da loja obtidos com sucesso",
            "dados": {"pedidos": [10, 20]}
        }

        status, mensagem, dados = get_pedidos_minha_loja()

        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Pedidos da loja obtidos com sucesso")
        self.assertListEqual(dados["pedidos"], [10, 20])

    @patch('interface_socket.interface_socket.sendMessage')
    def test_editar_servico_success(self, mock_send_message):
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Serviço editado com sucesso",
            "dados": {
                "idServico": 1,
                "nome_servico": "Novo título",
                "descricao_servico": "Nova desc",
                "categoria": "Nova categoria",
                "tipo_pagamento": 150.0,
                "quantidade": 10
            }
        }

        status, mensagem, dados = editar_servico(1, "Novo título", "Nova desc", 150.0, "Nova categoria", 10)
        
        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Serviço editado com sucesso")
        self.assertEqual(dados["idServico"], 1)
        self.assertEqual(dados["nome_servico"], "Novo título")
        self.assertEqual(dados["descricao_servico"], "Nova desc")
        self.assertEqual(dados["categoria"], "Nova categoria")
        self.assertEqual(dados["tipo_pagamento"], 150.0)
        self.assertEqual(dados["quantidade"], 10)


    @patch('interface_socket.interface_socket.sendMessage')
    def test_ocultar_servico_success(self, mock_send_message):
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Serviço ocultado com sucesso"
        }

        status, mensagem, _ = ocultar_servico(1)

        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Serviço ocultado com sucesso")

    @patch('interface_socket.interface_socket.sendMessage')
    def test_desocultar_servico_success(self, mock_send_message):
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Serviço desocultado com sucesso"
        }

        status, mensagem, _ = desocultar_servico(1)

        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Serviço desocultado com sucesso")

    @patch('interface_socket.interface_socket.sendMessage')
    def test_apagar_servico_success(self, mock_send_message):
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Serviço apagado com sucesso"
        }

        status, mensagem, _ = apagar_servico(1)

        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Serviço apagado com sucesso")

    @patch('interface_socket.interface_socket.sendMessage')
    def test_get_minha_loja_success(self, mock_send_message):
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Minha loja obtida com sucesso",
            "dados": {"idLoja": 123}
        }

        status, mensagem, dados = get_minha_loja()

        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Minha loja obtida com sucesso")
        print(dados)

    @patch('interface_socket.interface_socket.sendMessage')
    def test_realizar_pedido_success(self, mock_send_message):
        mock_send_message.return_value = {
            "status": 200,
            "mensagem": "Pedido realizado com sucesso",
            "dados": {"idPedido": 321}
        }

        status, mensagem, dados = realizar_pedido(1)

        self.assertEqual(status, 200)
        self.assertEqual(mensagem, "Pedido realizado com sucesso")


# Executando os testes
if __name__ == "__main__":
    unittest.main()
