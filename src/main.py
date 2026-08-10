"""
Projeto: Sistema de gestão de finanças pessoais
Autora: Esmeralda Fonseca
Monitor: Sebilson Cristovão
"""

import flet as ft

from database.database import Database
from repositories.transaction_repository import TransactionRepository
from services.reports import FinancialReport
from ui.app_layout import AppLayout

def main(page: ft.Page):
    database = Database()
    repository = TransactionRepository(database)
    report_service = FinancialReport(repository)
    AppLayout(page, repository, report_service)

if __name__ == "__main__":
    ft.run(main)

