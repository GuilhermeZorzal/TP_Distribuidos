import jwt
import datetime
from db.database import getCliente
from utils.utils import BR

SECRET_KEY = "my_secret"
ALGORITHM  = "HS256"
EXP_DELTA  = datetime.timedelta(days=2)

def gerar_token(cliente):
    now = datetime.datetime.now(BR)
    
    payload = {
        "sub": str(cliente.idCliente),
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "exp": int((now + EXP_DELTA).timestamp()),
        "apelido": cliente.apelido,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token):
    
    if isinstance(token, (bytes, bytearray)):
        token = token.decode("utf-8")
    token = token.strip()
    token = token.strip('"\'')
    if not token:
        return 0, "Token não fornecido", {}
    
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={
                "require": ["exp", "iat", "sub"],
                "verify_exp": True
            },
            leeway=10  # tolerância de 10s para clock skew
        )
        return 200, "Token válido", payload

    except jwt.ExpiredSignatureError:
        return 0, "Token expirado. Faça login novamente.", {}
    except jwt.MissingRequiredClaimError as e:
        return 0, f"Claim ausente: {e.claim}", {}
    except jwt.InvalidTokenError as error:
        return 0, "Token inválido. Verifique suas credenciais.", {}

def protected(token):
    status, msg, payload = decode_token(token)
    return status, msg, payload if status == 200 else {}

def autorizarToken(token):
    status, msg, payload = protected(token)
    
    if status != 200:
        return status, msg, {}
    return 200, "ID do cliente obtido", payload.get("sub")

def authorization(idCliente, token):

    cliente = getCliente(idCliente)
    if cliente is None:
        return 0, "Usuário não encontrado", {}

    status, msg, payload = protected(token)
    if status != 200:
        return status, msg, {}

    if payload.get("sub") != int(idCliente):
        return 0, "Usuário não autorizado", {}

    return 200, "Usuário autorizado", {"cliente": cliente}

# autenticação de funções do servidor
def autenticar_wrapper(func):
    def wrapper(self, *args, **kwargs):
        # Captura o token: pode vir nos kwargs ou como último argumento
        token = kwargs.pop('token', None)

        if not token and args:
            ultimo_arg = args[-1]
            if isinstance(ultimo_arg, str):
                token = ultimo_arg
    
        if not token:
            return 401, "Token não fornecido", {}

        # Verifica o token
        try:
            status, msg, idCliente = autorizarToken(token)
            if status != 200:
                return status, msg, {}
        except Exception as e:
            return 500, f"Erro ao verificar Token: {e}", {}

        # Executa a função original com idCliente incluído
        return func(self, idCliente, *args, **kwargs)

    return wrapper