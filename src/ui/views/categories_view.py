import flet as ft

from ui.views.theme import MEDIUM_GREEN, YELLOW, WHITE, DARK_TEXT, GRAY_TEXT, TITLE_FONT, header, format_kz


def build(app) -> ft.Column:
    """Constrói a vista de Categorias: totais acumulados por categoria (receitas e despesas),
    restrita às movimentações do utilizador atual."""

    expense_totals = app.repo.totals_by_category("Despesa", user_id=app.current_user.id)
    income_totals = app.repo.totals_by_category("Receita", user_id=app.current_user.id)

    return ft.Column(
        [
            header("Categorias", "Totais acumulados por categoria"),
            ft.Container(height=12),
            ft.Row(
                [_block("Despesas por Categoria", expense_totals, YELLOW),
                 _block("Receitas por Categoria", income_totals, MEDIUM_GREEN)],
                spacing=16, expand=True, vertical_alignment=ft.CrossAxisAlignment.START,
            ),
        ],
        expand=True, scroll=ft.ScrollMode.AUTO,
    )


def _block(title: str, data: list, color: str) -> ft.Container:
    rows = [
        ft.Row(
            [ft.Text(cat, size=13, expand=True), ft.Text(format_kz(val), weight=ft.FontWeight.BOLD, color=color)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ) for cat, val in data
    ] or [ft.Text("Sem dados.", color=GRAY_TEXT, size=12)]

    return ft.Container(
        bgcolor=WHITE, border_radius=16, padding=20, expand=True,
        content=ft.Column([ft.Text(title, size=15, weight=ft.FontWeight.BOLD, color=DARK_TEXT,
                                    font_family=TITLE_FONT), ft.Divider(), *rows], spacing=10),
        shadow=ft.BoxShadow(blur_radius=14, color="#0000000F", offset=ft.Offset(0, 4)),
    )
