import flet as ft

from models.transactions import INCOME_TYPE
from ui.views.theme import DARK_BG, MEDIUM_GREEN, YELLOW, LIGHT_BG, WHITE, DARK_TEXT, GRAY_TEXT, RED, header, format_kz


def build(app) -> ft.Column:
    """Constrói a vista de Movimentações: pesquisa por descrição + filtro simples por tipo,
    restrita às movimentações do utilizador atual."""

    search_field = ft.TextField(
        hint_text="Pesquisar descrição...", value=app.search_text, width=280,
        prefix_icon=ft.Icons.SEARCH, border_radius=10, filled=True, bgcolor=WHITE,
        on_change=lambda e: _on_search_change(app, e.control.value),
    )
    type_dropdown = ft.Dropdown(
        width=150, value=app.type_filter,
        options=[ft.dropdown.Option("Todos"), ft.dropdown.Option("Receita"), ft.dropdown.Option("Despesa")],
        on_select=lambda e: _on_type_filter_change(app, e.control.value),
        border_radius=10, filled=True, bgcolor=WHITE,
    )
    add_button = ft.FilledButton(
        "Adicionar", icon=ft.Icons.ADD,
        style=ft.ButtonStyle(bgcolor=MEDIUM_GREEN, color=WHITE),
        on_click=lambda e: app.navigate("add"),
    )

    transactions = _get_filtered_transactions(app)
    table = _build_table(app, transactions)

    return ft.Column(
        [
            ft.Row(
                [header("Movimentações", "Todas as suas movimentações financeiras"),
                 ft.Row([search_field, type_dropdown, add_button], spacing=10)],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(height=12),
            ft.Container(
                bgcolor=WHITE, border_radius=16, padding=16, expand=True,
                content=ft.Column([table], expand=True, scroll=ft.ScrollMode.AUTO),
                shadow=ft.BoxShadow(blur_radius=14, color="#0000000F", offset=ft.Offset(0, 4)),
            ),
        ],
        expand=True,
    )


def _get_filtered_transactions(app) -> list:
    """Aplica o filtro de tipo (se houver) e depois a pesquisa por texto, sempre
    restrito ao utilizador atual."""
    if app.type_filter != "Todos":
        transactions = app.repo.filter_by_type(app.type_filter, user_id=app.current_user.id)
    else:
        transactions = app.repo.list_transactions(user_id=app.current_user.id)

    if app.search_text.strip():
        text = app.search_text.strip().lower()
        transactions = [t for t in transactions if text in t.descricao.lower()]

    return transactions


def _build_table(app, transactions: list) -> ft.DataTable:
    rows = []
    for t in transactions:
        color = MEDIUM_GREEN if t.tipo == INCOME_TYPE else YELLOW
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(t.id))),
                    ft.DataCell(ft.Text(t.descricao)),
                    ft.DataCell(ft.Container(
                        content=ft.Text(t.tipo, size=11, color=WHITE, weight=ft.FontWeight.W_600),
                        bgcolor=color, border_radius=8, padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                    )),
                    ft.DataCell(ft.Text(t.categoria)),
                    ft.DataCell(ft.Text(
                        f"{'+' if t.tipo == INCOME_TYPE else '-'}{format_kz(t.valor)}",
                        color=color, weight=ft.FontWeight.BOLD,
                    )),
                    ft.DataCell(ft.Text(t.data)),
                    ft.DataCell(ft.Row(
                        [
                            ft.IconButton(ft.Icons.EDIT_OUTLINED, icon_color=MEDIUM_GREEN, icon_size=18,
                                          tooltip="Editar", on_click=lambda e, tid=t.id: _edit(app, tid)),
                            ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=RED, icon_size=18,
                                          tooltip="Remover", on_click=lambda e, tid=t.id: _confirm_delete(app, tid)),
                        ],
                        spacing=0,
                    )),
                ]
            )
        )

    if not rows:
        rows = [ft.DataRow(cells=[ft.DataCell(ft.Text("")), ft.DataCell(ft.Text("Nenhuma movimentação encontrada.",
                color=GRAY_TEXT)), ft.DataCell(ft.Text("")), ft.DataCell(ft.Text("")), ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")), ft.DataCell(ft.Text(""))])]

    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")), ft.DataColumn(ft.Text("Descrição")), ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Categoria")), ft.DataColumn(ft.Text("Valor")), ft.DataColumn(ft.Text("Data")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=rows,
        heading_row_color=LIGHT_BG,
        column_spacing=24,
    )


def _on_search_change(app, value: str) -> None:
    app.search_text = value
    app.show_transactions()


def _on_type_filter_change(app, value: str) -> None:
    app.type_filter = value
    app.show_transactions()


def _edit(app, transaction_id: int) -> None:
    transaction = app.repo.get_transaction_by_id(transaction_id)
    if transaction is None:
        app.show_message("Movimentação não encontrada.", error=True)
        return
    app.navigate("add", transaction=transaction)


def _confirm_delete(app, transaction_id: int) -> None:
    def delete(e):
        try:
            app.repo.delete_transaction(transaction_id)
            app.show_message("Movimentação removida.")
        except ValueError as erro:
            app.show_message(str(erro), error=True)
        app.page.pop_dialog()
        app.show_transactions()

    def cancel(e):
        app.page.pop_dialog()

    app.page.show_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar remoção"),
            content=ft.Text("Tem a certeza de que deseja remover esta movimentação?"),
            actions=[ft.TextButton("Cancelar", on_click=cancel),
                     ft.FilledButton("Remover", style=ft.ButtonStyle(bgcolor=RED, color=WHITE), on_click=delete)],
        )
    )
