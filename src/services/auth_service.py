from models.user import verificar_senha, ADMIN_ID
from repositories.user_repository import UserRepository


class AuthService:
    """Autentica utilizadores por username + password."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def autenticar(self, username: str, senha: str):
        """Devolve o objeto User em caso de sucesso, ou levanta ValueError com a mensagem do erro."""
        username = (username or "").strip().lower()
        if not username or not senha:
            raise ValueError("Preencha o utilizador e a password.")

        user = self.user_repository.get_user_by_username(username)
        if user is None or not verificar_senha(senha, user.senha_hash):
            raise ValueError("Utilizador ou password incorretos.")

        if not user.ativo:
            raise ValueError("Esta conta está desativada. Contacte o administrador.")

        return user

    @staticmethod
    def is_admin(user) -> bool:
        return user is not None and user.id == ADMIN_ID
