"""
Projeto: Sistema de gestão de finanças pessoais
Autora: Esmeralda Fonseca
Monitor: Sebilson Cristovão
"""

import flet as ft

from database.database import Database
from repositories.transaction_repository import TransactionRepository
from repositories.user_repository import UserRepository
from services.reports import FinancialReport
from services.auth_service import AuthService
from ui.views.login_view import LoginView


def main(page: ft.Page):
    database = Database()
    transaction_repository = TransactionRepository(database)
    user_repository = UserRepository(database)
    report_service = FinancialReport(transaction_repository)
    auth_service = AuthService(user_repository)

    LoginView(page, auth_service, transaction_repository, user_repository, report_service)


if __name__ == "__main__":
    ft.run(main)
