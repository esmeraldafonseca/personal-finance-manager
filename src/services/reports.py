from dataclasses import dataclass

from repositories.transaction_repository import TransactionRepository


@dataclass
class MonthlyReport:
    """Estrutura de dados devolvida por generate_monthly_report."""

    month: str
    year: str
    total_income: float
    total_expenses: float
    balance: float
    transaction_count: int
    top_expense_category: str
    highest_income: float
    highest_expense: float


class FinancialReport:
    """Gera relatórios e estatísticas financeiras com base nos movimentos guardados."""

    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def generate_monthly_report(self, month: str, year: str, user_id: int = None) -> MonthlyReport:
        """
        Gera o relatório mensal completo: totais, saldo, número de
        movimentações, categoria com maior despesa, maior receita e
        maior despesa do mês.
        """
        transactions = self.repository.filter_by_month(month, year, user_id=user_id)

        incomes = [t.valor for t in transactions if t.tipo == "Receita"]
        expenses = [t.valor for t in transactions if t.tipo == "Despesa"]

        total_income = sum(incomes)
        total_expenses = sum(expenses)
        balance = total_income - total_expenses

        expenses_by_category = {}
        for t in transactions:
            if t.tipo == "Despesa":
                expenses_by_category[t.categoria] = expenses_by_category.get(t.categoria, 0.00) + t.valor

        top_expense_category = max(expenses_by_category, key=expenses_by_category.get) if expenses_by_category else "-"

        return MonthlyReport(
            month=month,
            year=year,
            total_income=total_income,
            total_expenses=total_expenses,
            balance=balance,
            transaction_count=len(transactions),
            top_expense_category=top_expense_category,
            highest_income=max(incomes) if incomes else 0.0,
            highest_expense=max(expenses) if expenses else 0.0,
        )
