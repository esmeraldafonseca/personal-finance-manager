import flet as ft

from models.transactions import INCOME_TYPE
from ui.views.theme import MEDIUM_GREEN, YELLOW, LIGHT_BG, WHITE, GRAY_TEXT, header, format_kz


def build(app) -> ft.Column:
    """Constrói a vista de Pesquisa dedicada (pesquisa por descrição)."""

    results_column = ft.Column(spacing=10)

    def search(e):
        text = field.value.strip()
        results_column.controls.clear()
        if not text:
            results_column.controls.append(ft.Text("Escreva um termo para pesquisar.", color=GRAY_TEXT))
        else:
            found = app.repo.search_transactions(text)
            if not found:
                results_column.controls.append(ft.Text("Nenhuma movimentação encontrada.", color=GRAY_TEXT))
            for t in found:
                color = MEDIUM_GREEN if t.tipo == INCOME_TYPE else YELLOW
                results_column.controls.append(
                    ft.Container(
                        bgcolor=LIGHT_BG, border_radius=10, padding=12,
                        content=ft.Row(
                            [
                                ft.Column([ft.Text(t.descricao, weight=ft.FontWeight.W_600),
                                           ft.Text(f"{t.categoria} • {t.data}", size=11, color=GRAY_TEXT)],
                                          spacing=2, expand=True),
                                ft.Text(f"{'+' if t.tipo == INCOME_TYPE else '-'}{format_kz(t.valor)}",
                                        color=color, weight=ft.FontWeight.BOLD),
                            ],
                        ),
                    )
                )
        app.page.update()

    field = ft.TextField(
        label="Pesquisar por descrição", hint_text="Ex.: material, supermercado, salário...",
        border_radius=10, filled=True, bgcolor=WHITE, on_submit=search, expand=True,
    )
    button = ft.FilledButton("Pesquisar", icon=ft.Icons.SEARCH,
                              style=ft.ButtonStyle(bgcolor=MEDIUM_GREEN, color=WHITE), on_click=search)

    return ft.Column(
        [
            header("Pesquisar Movimentações", "Encontre movimentações pela descrição, mesmo parcial"),
            ft.Container(height=12),
            ft.Container(
                bgcolor=WHITE, border_radius=16, padding=20,
                content=ft.Column(
                    [ft.Row([field, button], spacing=10), ft.Divider(height=20), results_column],
                    scroll=ft.ScrollMode.AUTO,
                ),
                shadow=ft.BoxShadow(blur_radius=14, color="#0000000F", offset=ft.Offset(0, 4)),
                expand=True,
            ),
        ],
        expand=True,
    )
