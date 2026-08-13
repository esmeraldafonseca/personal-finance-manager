from dataclasses import dataclass
from datetime import datetime


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
    """Representa uma movimentação financeira (receita ou despesa) de um utilizador."""

    descricao: str
    tipo: str
    categoria: str
    valor: float
    data: str  # formato esperado: DD/MM/AAAA
    observacao: str = ""
    id: int = None
    user_id: int = None

    def validar(self) -> None:
        """
        Valida os dados do transaction antes de serem persistidos na
        base de dados
          """
        
        self._validar_descricao()

        if self.tipo not in VALID_TRANSACTION_TYPES:
            raise ValueError("O tipo deve ser 'Receita' ou 'Despesa'.")

        if not self.categoria or not self.categoria.strip():
            raise ValueError("A categoria é obrigatória.")

        try:
            valor_float = float(self.valor)
        except (TypeError, ValueError):
            raise ValueError("O valor deve ser numérico.")

        if valor_float <= 0:
            raise ValueError("O valor deve ser maior que zero.")

        self._validar_data()

    def _validar_descricao(self) -> None:
        """Descrição obrigatória, com pelo menos 3 caracteres e não
        composta apenas por dígitos."""
        if not self.descricao or not self.descricao.strip():
            raise ValueError("A descrição é obrigatória.")

        descricao_limpa = self.descricao.strip()

        if len(descricao_limpa) < 3:
            raise ValueError("A descrição deve ter no mínimo 3 caracteres.")

        if descricao_limpa.isdigit():
            raise ValueError("A descrição não pode conter apenas números.")

    def _validar_data(self) -> None:
        """
        Confirma que a data está num formato válido (DD/MM/AAAA) e não
        é futura.
        """
        if not self.data or not self.data.strip():
            raise ValueError("A data é obrigatória.")

        try:
            data_convertida = datetime.strptime(self.data.strip(), "%d/%m/%Y").date()
        except ValueError:
            raise ValueError("A data deve estar no formato DD/MM/AAAA.")

        if data_convertida > datetime.today().date():
            raise ValueError("A data não pode ser uma data futura.")

    def to_tuple(self):
        """Devolve os campos da transação como tuplo, útil para o SQL."""
        return (self.descricao, self.tipo, self.categoria, float(self.valor), self.data,
                self.observacao or "", self.user_id)

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
            user_id=row[7] if len(row) > 7 else None,
        )
