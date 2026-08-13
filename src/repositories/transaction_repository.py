import sqlite3

from database.database import Database
from models.transactions import Transaction


class TransactionRepository:
    """Executa as operações CRUD e consultas SQL sobre a tabela 'movimentos'.
    """

    def __init__(self, database: Database):
        self.database = database

    # CRUD básico
    def add_transaction(self, transaction: Transaction) -> int:
        """Insere um novo movimento na base de dados e devolve o ID gerado."""
        transaction.validar()
        sql = """
            INSERT INTO movimentos
            (descricao, tipo, categoria, valor, data, observacao, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        try:
            connection = self.database.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, transaction.to_tuple())
            connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro ao adicionar movimento: {erro}")

    def list_transactions(self, user_id: int = None) -> list:
        """Devolve os movimentos (de um utilizador, se indicado), da data mais
        recente para a mais antiga."""
        sql = """
            SELECT id, descricao, tipo, categoria, valor, data, observacao, user_id
            FROM movimentos
            {filtro}
            ORDER BY id DESC
        """.format(filtro="WHERE user_id = ?" if user_id is not None else "")
        try:
            cursor = self.database.get_connection().cursor()
            cursor.execute(sql, (user_id,) if user_id is not None else ())
            rows = cursor.fetchall()
            return [Transaction.from_row(row) for row in rows]
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro ao listar movimentos: {erro}")

    def get_transaction_by_id(self, transaction_id: int):
        """Devolve um único movimento pelo seu ID, ou None se não existir."""
        sql = """
            SELECT id, descricao, tipo, categoria, valor, data, observacao, user_id
            FROM movimentos WHERE id = ?
        """
        try:
            cursor = self.database.get_connection().cursor()
            cursor.execute(sql, (transaction_id,))
            row = cursor.fetchone()
            return Transaction.from_row(row) if row else None
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro ao obter movimento: {erro}")

    def update_transaction(self, transaction: Transaction) -> None:
        """Atualiza um movimento existente na base de dados."""
        if transaction.id is None:
            raise ValueError("Não é possível atualizar: nenhum registo selecionado.")

        transaction.validar()

        existing = self.get_transaction_by_id(transaction.id)
        if existing is None:
            raise ValueError("Tentativa de editar uma movimentação inexistente.")

        sql = """
            UPDATE movimentos
            SET descricao = ?, tipo = ?, categoria = ?, valor = ?, data = ?, observacao = ?, user_id = ?
            WHERE id = ?
        """
        try:
            connection = self.database.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, (*transaction.to_tuple(), transaction.id))
            connection.commit()
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro ao atualizar movimentos: {erro}")

    def delete_transaction(self, transaction_id: int) -> None:
        """Remove um movimento da base de dados pelo seu ID."""
        existing = self.get_transaction_by_id(transaction_id)
        if existing is None:
            raise ValueError("Tentativa de remover uma movimentação inexistente.")

        sql = "DELETE FROM movimentos WHERE id = ?"
        try:
            connection = self.database.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, (transaction_id,))
            connection.commit()
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro ao remover movimento: {erro}")

    # Pesquisa e filtros
    def search_transactions(self, text: str, user_id: int = None) -> list:
        """Pesquisa movimentos cuja descrição contenha o texto indicado (parcial)."""
        sql = """
            SELECT id, descricao, tipo, categoria, valor, data, observacao, user_id
            FROM movimentos
            WHERE descricao LIKE ? {filtro}
            ORDER BY id DESC
        """.format(filtro="AND user_id = ?" if user_id is not None else "")
        params = (f"%{text}%",) + ((user_id,) if user_id is not None else ())
        try:
            cursor = self.database.get_connection().cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [Transaction.from_row(row) for row in rows]
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro ao pesquisar transactions: {erro}")

    def filter_by_type(self, transaction_type: str, user_id: int = None) -> list:
        """Devolve apenas movimentos do tipo indicado (Receita ou Despesa)."""
        sql = """
            SELECT id, descricao, tipo, categoria, valor, data, observacao, user_id
            FROM movimentos
            WHERE tipo = ? {filtro}
            ORDER BY id DESC
        """.format(filtro="AND user_id = ?" if user_id is not None else "")
        params = (transaction_type,) + ((user_id,) if user_id is not None else ())
        try:
            cursor = self.database.get_connection().cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [Transaction.from_row(row) for row in rows]
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro ao filtrar por tipo: {erro}")

    def filter_by_category(self, category: str, user_id: int = None) -> list:
        """Devolve apenas movimentos da categoria indicada."""
        sql = """
            SELECT id, descricao, tipo, categoria, valor, data, observacao, user_id
            FROM movimentos
            WHERE categoria = ? {filtro}
            ORDER BY id DESC
        """.format(filtro="AND user_id = ?" if user_id is not None else "")
        params = (category,) + ((user_id,) if user_id is not None else ())
        try:
            cursor = self.database.get_connection().cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [Transaction.from_row(row) for row in rows]
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro ao filtrar por categoria: {erro}")

    def filter_by_month(self, month: str, year: str, user_id: int = None) -> list:
        """Devolve apenas movimentos do mês e ano indicados (ex: month='03', year='2026')."""
        sql = """
            SELECT id, descricao, tipo, categoria, valor, data, observacao, user_id
            FROM movimentos
            WHERE SUBSTR(data, 4, 2) = ? AND SUBSTR(data, 7, 4) = ? {filtro}
            ORDER BY id DESC
        """.format(filtro="AND user_id = ?" if user_id is not None else "")
        params = (month.zfill(2), year) + ((user_id,) if user_id is not None else ())
        try:
            cursor = self.database.get_connection().cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [Transaction.from_row(row) for row in rows]
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro ao filtrar por mês/ano: {erro}")

    def count_transactions(self, user_id: int = None) -> int:
        """Conta o número total de movimentações (de um utilizador, se indicado)."""
        sql = "SELECT COUNT(*) FROM movimentos" + (" WHERE user_id = ?" if user_id is not None else "")
        cursor = self.database.get_connection().cursor()
        cursor.execute(sql, (user_id,) if user_id is not None else ())
        return cursor.fetchone()[0]

    def totals_by_category(self, transaction_type: str = "Despesa", user_id: int = None) -> list:
        """
        Agrupa os valores por categoria (usado no gráfico circular de despesas
        por categoria). Devolve uma lista de tuplos (categoria, total).
        """
        sql = """
            SELECT categoria, SUM(valor) as total
            FROM movimentos
            WHERE tipo = ? {filtro}
            GROUP BY categoria
            ORDER BY total DESC
        """.format(filtro="AND user_id = ?" if user_id is not None else "")
        params = (transaction_type,) + ((user_id,) if user_id is not None else ())
        cursor = self.database.get_connection().cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

    def get_existing_categories(self, user_id: int = None) -> list:
        """Devolve a lista de categorias já usadas nos movimentos (para os filtros)."""
        sql = ("SELECT DISTINCT categoria FROM movimentos"
               + (" WHERE user_id = ?" if user_id is not None else "")
               + " ORDER BY categoria")
        cursor = self.database.get_connection().cursor()
        cursor.execute(sql, (user_id,) if user_id is not None else ())
        return [row[0] for row in cursor.fetchall()]

    def get_existing_years(self, user_id: int = None) -> list:
        """Devolve a lista de anos já usados nos movimentos (para os filtros)."""
        sql = ("SELECT DISTINCT SUBSTR(data, 7, 4) as ano FROM movimentos"
               + (" WHERE user_id = ?" if user_id is not None else "")
               + " ORDER BY ano DESC")
        cursor = self.database.get_connection().cursor()
        cursor.execute(sql, (user_id,) if user_id is not None else ())
        return [row[0] for row in cursor.fetchall() if row[0]]

    # Estatísticas agregadas por utilizador (usadas pelo administrador)
    def totals_by_user(self) -> list:
        """Devolve, para cada user_id, os totais de receitas e despesas.
        Lista de tuplos (user_id, total_receitas, total_despesas)."""
        sql = """
            SELECT user_id,
                   SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE 0 END) AS total_receitas,
                   SUM(CASE WHEN tipo = 'Despesa' THEN valor ELSE 0 END) AS total_despesas
            FROM movimentos
            WHERE user_id IS NOT NULL
            GROUP BY user_id
        """
        cursor = self.database.get_connection().cursor()
        cursor.execute(sql)
        return cursor.fetchall()
