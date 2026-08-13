import flet as ft

from models.transactions import INCOME_TYPE
from ui.views.theme import (
    header, summary_card, format_kz,
    MEDIUM_GREEN, LIGHT_GREEN, YELLOW, WHITE,
    DARK_TEXT, GRAY_TEXT, RED, TITLE_FONT,
)


def build(app) -> ft.Column:
    """Constrói a vista do Dashboard: totais gerais + últimas movimentações do utilizador atual."""

    repo = app.repo
    transactions = repo.list_transactions(user_id=app.current_user.id)
    total_income = sum(t.valor for t in transactions if t.tipo == INCOME_TYPE)
    total_expenses = sum(t.valor for t in transactions if t.tipo != INCOME_TYPE)
    balance = total_income - total_expenses

    cards = ft.Row(
        [
            summary_card("Total de Receitas", format_kz(total_income), ft.Icons.TRENDING_UP, MEDIUM_GREEN),
            summary_card("Total de Despesas", format_kz(total_expenses), ft.Icons.TRENDING_DOWN, YELLOW),
            summary_card("Saldo Final", format_kz(balance), ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED,
                         LIGHT_GREEN if balance >= 0 else RED),
            summary_card("Movimentações", str(len(transactions)), ft.Icons.RECEIPT_LONG_OUTLINED, MEDIUM_GREEN),
        ],
        spacing=16,
    )

    latest = transactions[:5]
    latest_rows = []
    for t in latest:
        color = MEDIUM_GREEN if t.tipo == INCOME_TYPE else YELLOW
        sign = "+" if t.tipo == INCOME_TYPE else "-"
        latest_rows.append(
            ft.Row(
                [
                    ft.Icon(ft.Icons.ARROW_UPWARD if t.tipo == INCOME_TYPE else ft.Icons.ARROW_DOWNWARD,
                            color=color, size=16),
                    ft.Column(
                        [ft.Text(t.descricao, size=12, weight=ft.FontWeight.W_600, color=DARK_TEXT),
                         ft.Text(t.categoria, size=10, color=GRAY_TEXT)],
                        spacing=0, expand=True,
                    ),
                    ft.Text(t.data, size=11, color=GRAY_TEXT),
                    ft.Text(f"{sign}{format_kz(t.valor)}", size=12, weight=ft.FontWeight.BOLD, color=color),
                ],
                spacing=10,
            )
        )
    if not latest_rows:
        latest_rows = [ft.Text("Ainda não existem movimentações registadas.", color=GRAY_TEXT, size=12)]

    latest_transactions = ft.Container(
        bgcolor=WHITE, border_radius=16, padding=20, expand=True,
        content=ft.Column(
            [
                ft.Row(
                    [ft.Text("Últimas Movimentações", size=15, weight=ft.FontWeight.BOLD, color=DARK_TEXT,
                             font_family=TITLE_FONT),
                     ft.TextButton("Ver todas", on_click=lambda e: app.navigate("transactions"))],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Column(latest_rows, spacing=14),
            ],
            spacing=10,
        ),
        shadow=ft.BoxShadow(blur_radius=14, color="#0000000F", offset=ft.Offset(0, 4)),
    )

    return ft.Column(
        [
            header("Dashboard", "Visão geral das suas finanças"),
            ft.Container(height=8),
            cards,
            ft.Container(height=16),
            latest_transactions,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
