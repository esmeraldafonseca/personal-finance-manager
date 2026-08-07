from dataclasses import dataclass


# Tipos de movimentação aceites pelo sistema.
INCOME_TYPE = "Receita"
EXPENSE_TYPE = "Despesa"
VALID_TRANSACTION_TYPES = (INCOME_TYPE, EXPENSE_TYPE)

# Categorias sugeridas .
INCOME_CATEGORIES = ["Salário", "Bolsa", "Venda", "Presente", "Trabalho extra", "Outros"]
EXPENSE_CATEGORIES = [
    "Alimentação", "Transporte", "Educação", "Saúde",
    "Internet", "Lazer", "Renda", "Outros",
]


@dataclass
class Transaction:
    """Representa uma movimentação financeira (receita ou despesa)."""

    descricao: str
    tipo: str
    categoria: str
    valor: float
    data: str  # formato esperado: DD/MM/AAAA
    observacao: str = ""
    id: int = None

    def validar(self) -> None:
        """
        Valida os dados do transaction antes de serem persistidos na
        base de dados
          """
        if not self.descricao or not self.descricao.strip():
            raise ValueError("A descrição é obrigatória.")

        if self.tipo not in VALID_TRANSACTION_TYPES:
            raise ValueError("O tipo deve ser 'Receita' ou 'Despesa'.")

        if not self.categoria or not self.categoria.strip():
            raise ValueError("A categoria é obrigatória.")

        try:
            amount_float = float(self.valor)
        except (TypeError, ValueError):
            raise ValueError("O valor deve ser numérico.")

        if amount_float <= 0:
            raise ValueError("O valor deve ser maior que zero.")

        if not self.data or not self.data.strip():
            raise ValueError("A data é obrigatória.")

        # Validação simples do formato DD/MM/AAAA.
        parts = self.data.split("/")
        if len(parts) != 3:
            raise ValueError("A data deve estar no formato DD/MM/AAAA.")

        day, month, year = parts
        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            raise ValueError("A data deve estar no formato DD/MM/AAAA.")

        day_int, month_int = int(day), int(month)
        if not (1 <= day_int <= 31) or not (1 <= month_int <= 12):
            raise ValueError("A data contém day ou mês inválido.")

    def to_tuple(self):
        """Devolve os campos do transaction como tuplo, útil para o SQL."""
        return (self.descricao, self.tipo, self.categoria, float(self.valor), self.data, self.observacao or "")

    @staticmethod
    def from_row(row) -> "Transaction":
        """Cria um objeto Transaction a partir de uma linha da base de dados."""
        return Transaction(
            id=row[0],
            descricao=row[1],
            tipo=row[2],
            categoria=row[3],
            valor=row[4],
            data=row[5],
            observacao=row[6],
        )
