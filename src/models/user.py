import hashlib
import os
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime

ADMIN_ID = 1
IDADE_MINIMA = 18


@dataclass
class User:
    """Representa um utilizador do sistema (utilizador comum ou administrador)."""

    primeiro_nome: str
    ultimo_nome: str
    data_nascimento: str  # formato esperado: DD/MM/AAAA
    telefone: str
    username: str = ""
    senha_hash: str = ""
    ativo: bool = True
    criado_em: str = ""
    id: int = None

    def validar_cadastro(self) -> None:
        """Valida os dados pessoais do utilizador antes de serem persistidos."""
        self._validar_nome(self.primeiro_nome, "primeiro nome")
        self._validar_nome(self.ultimo_nome, "último nome")
        self._validar_data_nascimento()
        self._validar_telefone()

    def _validar_nome(self, nome: str, rotulo: str) -> None:
        if not nome or not nome.strip():
            raise ValueError(f"O {rotulo} é obrigatório.")
        if len(nome.strip()) < 2:
            raise ValueError(f"O {rotulo} deve ter no mínimo 2 caracteres.")

    def _validar_data_nascimento(self) -> None:
        if not self.data_nascimento or not self.data_nascimento.strip():
            raise ValueError("A data de nascimento é obrigatória.")

        try:
            nascimento = datetime.strptime(self.data_nascimento.strip(), "%d/%m/%Y").date()
        except ValueError:
            raise ValueError("A data de nascimento deve estar no formato DD/MM/AAAA.")

        if nascimento > datetime.today().date():
            raise ValueError("A data de nascimento não pode ser uma data futura.")

        # Verificação simplificada por ano (não considera dia/mês)
        idade_em_anos = datetime.today().year - nascimento.year
        if idade_em_anos < IDADE_MINIMA:
            raise ValueError(f"O utilizador deve ter pelo menos {IDADE_MINIMA} anos.")

    def _validar_telefone(self) -> None:
        telefone = (self.telefone or "").strip()
        if not re.fullmatch(r"9\d{8}", telefone):
            raise ValueError("O número de telefone deve ter 9 dígitos e começar por 9.")


def _normalizar(texto: str) -> str:
    """Remove acentos e caracteres não alfanuméricos, e converte para minúsculas."""
    texto = unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]", "", texto.lower())


def gerar_username_base(primeiro_nome: str, ultimo_nome: str, data_nascimento: str) -> str:
    """Gera o username base: primeiro nome + último nome + dia de nascimento (2 dígitos).
    Ex.: 'João Miguel' nascido a 01/02/1992 -> 'joaomiguel01'."""
    dia = datetime.strptime(data_nascimento.strip(), "%d/%m/%Y").day
    return f"{_normalizar(primeiro_nome)}{_normalizar(ultimo_nome)}{dia:02d}"


def gerar_hash_senha(senha: str) -> str:
    """Gera um hash seguro da password """
    salt = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, 200_000)
    return f"{salt.hex()}${hash_bytes.hex()}"


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Verifica se a password fornecida corresponde ao hash guardado."""
    try:
        salt_hex, hash_hex = (senha_hash or "").split("$")
        salt = bytes.fromhex(salt_hex)
        hash_esperado = bytes.fromhex(hash_hex)
    except (ValueError, AttributeError):
        return False
    hash_calculado = hashlib.pbkdf2_hmac("sha256", (senha or "").encode("utf-8"), salt, 200_000)
    return hash_calculado == hash_esperado
