import os
import sqlite3


class Database:
    """Gere a ligação e a inicialização da base de dados SQLite."""

    def __init__(self, db_name: str = "finance_manager.db"):

        current_folder = os.path.dirname(os.path.abspath(__file__)) 
        self.database_path = os.path.join(current_folder, db_name)

        self.connection = None
        self._connect()
        self._create_tables()

    def _connect(self) -> None:
        """Cria a ligação com o ficheiro SQLite (criando-o se ainda não existir)."""
        try:
            self.connection = sqlite3.connect(self.database_path)

        except sqlite3.Error as error:
            raise RuntimeError(f"Erro ao ligar à base de dados: {error}")

    def _create_tables(self) -> None:
        sql_users = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                primeiro_nome TEXT NOT NULL,
                ultimo_nome TEXT NOT NULL,
                data_nascimento TEXT NOT NULL,
                telefone TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL,
                ativo INTEGER NOT NULL DEFAULT 1,
                criado_em TEXT NOT NULL
            );
        """
        sql_movimentos = """
            CREATE TABLE IF NOT EXISTS movimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                tipo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                valor REAL NOT NULL,
                data TEXT NOT NULL,
                observacao TEXT,
                user_id INTEGER REFERENCES users(id)
            );
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_users)
            cursor.execute(sql_movimentos)
            self.connection.commit()
        except sqlite3.Error as error:
            raise RuntimeError(f"Erro ao criar as tabelas: {error}")


    def get_connection(self) -> sqlite3.Connection:
        """Devolve a ligação ativa à base de dados."""
        if self.connection is None:
            self._connect()
        return self.connection

    def close(self) -> None:
        """Fecha a ligação à base de dados, se estiver aberta."""
        if self.connection:
            self.connection.close()
            self.connection = None
