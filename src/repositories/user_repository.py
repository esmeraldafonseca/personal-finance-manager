import sqlite3
from datetime import datetime

from database.database import Database
from models.user import User, gerar_username_base, gerar_hash_senha


class UserRepository:
    """Executa as operações CRUD sobre a tabela 'users'."""

    def __init__(self, database: Database):
        self.database = database
        self._garantir_admin()

    def _garantir_admin(self) -> None:
        """Cria o utilizador administrador (id 1) na primeira execução, se ainda não existir."""
        if self.get_user_by_id(1) is not None:
            return

        senha_hash = gerar_hash_senha("admin123")
        criado_em = datetime.now().strftime("%d/%m/%Y %H:%M")
        sql = """
            INSERT INTO users (primeiro_nome, ultimo_nome, data_nascimento, telefone, username, senha_hash, ativo, criado_em)
            VALUES (?, ?, ?, ?, ?, ?, 0, ?)
        """
        try:
            connection = self.database.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, ("Admin", "Sistema", "01/01/2000", "900000000", "admin", senha_hash, criado_em))
            connection.commit()
            print("Utilizador admin criado. username: admin | password inicial: admin123 (altere assim que possível)")
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro ao criar o utilizador admin: {erro}")

    def _gerar_username_unico(self, primeiro_nome: str, ultimo_nome: str, data_nascimento: str) -> str:
        """Gera o username automático, acrescentando um sufixo numérico se já existir."""
        base = gerar_username_base(primeiro_nome, ultimo_nome, data_nascimento)
        username = base
        sufixo = 1
        while self.get_user_by_username(username) is not None:
            sufixo += 1
            username = f"{base}{sufixo}"
        return username

    def add_user(self, user: User, senha: str) -> int:
        """Cadastra um novo utilizador (chamado apenas pelo admin). O username é
        gerado automaticamente e apenas o hash da password é guardado."""
        user.validar_cadastro()
        username = self._gerar_username_unico(user.primeiro_nome, user.ultimo_nome, user.data_nascimento)
        senha_hash = gerar_hash_senha(senha)
        criado_em = datetime.now().strftime("%d/%m/%Y %H:%M")

        sql = """
            INSERT INTO users (primeiro_nome, ultimo_nome, data_nascimento, telefone, username, senha_hash, ativo, criado_em)
            VALUES (?, ?, ?, ?, ?, ?, 0, ?)
        """
        try:
            connection = self.database.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, (user.primeiro_nome, user.ultimo_nome, user.data_nascimento,
                                  user.telefone, username, senha_hash, criado_em))
            connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro ao cadastrar utilizador: {erro}")

    def list_users(self) -> list:
        """Devolve todos os utilizadores, ordenados por ID."""
        sql = """
            SELECT id, primeiro_nome, ultimo_nome, data_nascimento, telefone, username, senha_hash, ativo, criado_em
            FROM users
            ORDER BY id ASC
        """
        cursor = self.database.get_connection().cursor()
        cursor.execute(sql)
        return [self._from_row(row) for row in cursor.fetchall()]

    def get_user_by_id(self, user_id: int):
        """Devolve um único utilizador pelo seu ID, ou None se não existir."""
        sql = """
            SELECT id, primeiro_nome, ultimo_nome, data_nascimento, telefone, username, senha_hash, ativo, criado_em
            FROM users WHERE id = ?
        """
        cursor = self.database.get_connection().cursor()
        cursor.execute(sql, (user_id,))
        row = cursor.fetchone()
        return self._from_row(row) if row else None

    def get_user_by_username(self, username: str):
        """Devolve um único utilizador pelo seu username, ou None se não existir."""
        sql = """
            SELECT id, primeiro_nome, ultimo_nome, data_nascimento, telefone, username, senha_hash, ativo, criado_em
            FROM users WHERE username = ?
        """
        cursor = self.database.get_connection().cursor()
        cursor.execute(sql, ((username or "").strip().lower(),))
        row = cursor.fetchone()
        return self._from_row(row) if row else None

    def update_user_data(self, user: User) -> None:
        """Atualiza os dados pessoais de um utilizador (não altera username nem password)."""
        if user.id is None:
            raise ValueError("Não é possível atualizar: nenhum utilizador selecionado.")

        user.validar_cadastro()

        sql = """
            UPDATE users SET primeiro_nome = ?, ultimo_nome = ?, data_nascimento = ?, telefone = ?
            WHERE id = ?
        """
        try:
            connection = self.database.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, (user.primeiro_nome, user.ultimo_nome, user.data_nascimento,
                                  user.telefone, user.id))
            connection.commit()
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro ao atualizar utilizador: {erro}")

    def set_active(self, user_id: int, ativo: bool) -> None:
        """Ativa ou desativa um utilizador. O administrador (id 1) nunca pode ser desativado."""
        if user_id == 1:
            raise ValueError("O utilizador administrador não pode ser desativado.")

        sql = "UPDATE users SET ativo = ? WHERE id = ?"
        try:
            connection = self.database.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, (1 if ativo else 0, user_id))
            connection.commit()
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro ao atualizar estado do utilizador: {erro}")

    def reset_password(self, user_id: int, nova_senha: str) -> None:
        """Redefine a password de um utilizador (feito pelo administrador)."""
        if not nova_senha or len(nova_senha) < 6:
            raise ValueError("A nova password deve ter no mínimo 6 caracteres.")

        senha_hash = gerar_hash_senha(nova_senha)
        sql = "UPDATE users SET senha_hash = ? WHERE id = ?"
        try:
            connection = self.database.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, (senha_hash, user_id))
            connection.commit()
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro ao redefinir password: {erro}")

    @staticmethod
    def _from_row(row) -> User:
        return User(
            id=row[0], primeiro_nome=row[1], ultimo_nome=row[2], data_nascimento=row[3],
            telefone=row[4], username=row[5], senha_hash=row[6], ativo=bool(row[7]), criado_em=row[8],
        )
