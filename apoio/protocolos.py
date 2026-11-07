import secrets


_ALFABETO = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


def novo_protocolo() -> str:
    def gerar_parte() -> str:
        return "".join(secrets.choice(_ALFABETO) for _ in range(4))

    return f"ESC-{gerar_parte()}-{gerar_parte()}"
