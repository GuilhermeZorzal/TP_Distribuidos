import json

def formatar_mensagem(status, mensagem, dados):
    """
    Formata a mensagem de resposta para o cliente.
    
    Args:
        status (int): Código de status da resposta (200 para sucesso, 0 para erro).
        mensagem (str): Mensagem de erro ou sucesso.
        dados (dict): Dados retornados na resposta.
    
    Returns:
        dict: Dicionário formatado com status, mensagem e dados.
    """
    return json.dumps({
        "status": status,
        "mensagem": mensagem,
        "dados": dados
    })
    