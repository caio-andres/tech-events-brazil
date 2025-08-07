import hashlib

def calcular_hash(conteudo: bytes) -> str:
    """Retorna SHA256 do conteúdo."""
    return hashlib.sha256(conteudo).hexdigest()
