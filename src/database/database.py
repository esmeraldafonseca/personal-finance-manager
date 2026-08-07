import os
import sqlite3


class Database:
    """Gere a ligação e a inicialização da base de dados SQLite."""

    def __init__(self, db_name: str = "finance_manager.db"):
       
        current_folder = os.path.dirname(os.path.abspath(__file__))#Garante que a base de dados é sempre criada dentro da pasta database/,
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

        sql_command = """
            CREATE TABLE IF NOT EXISTS movimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                tipo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                valor REAL NOT NULL,
                data TEXT NOT NULL,
                observacao TEXT
            );
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_command)
            self.connection.commit()
        except sqlite3.Error as error:
            raise RuntimeError(f"Erro ao criar a tabela 'movimentos': {error}")

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
