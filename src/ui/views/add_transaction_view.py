import datetime as dt

import flet as ft

from models.transactions import Transaction, INCOME_TYPE, EXPENSE_TYPE, INCOME_CATEGORIES, EXPENSE_CATEGORIES
from ui.views.theme import MEDIUM_GREEN, WHITE, header


def build(app, transaction: Transaction = None) -> ft.Column:
    """Constrói o formulário de adicionar/editar movimentação.
    Se 'transaction' for passado, o formulário abre em modo de edição."""

    editing = transaction is not None
    app.selected_transaction_id = transaction.id if editing else None

    description_field = ft.TextField(
        label="Descrição *", hint_text="Ex.: Compra de material escolar",
        value=transaction.descricao if editing else "",
        border_radius=10, filled=True, bgcolor=WHITE, expand=True,
    )
    type_dropdown = ft.Dropdown(
        label="Tipo *",
        options=[ft.dropdown.Option(INCOME_TYPE), ft.dropdown.Option(EXPENSE_TYPE)],
        value=transaction.tipo if editing else EXPENSE_TYPE,
        border_radius=10, filled=True, bgcolor=WHITE, expand=True,
    )
    initial_categories = INCOME_CATEGORIES if type_dropdown.value == INCOME_TYPE else EXPENSE_CATEGORIES
    category_dropdown = ft.Dropdown(
        label="Categoria *", hint_text="Selecione uma categoria",
        options=[ft.dropdown.Option(c) for c in initial_categories],
        value=transaction.categoria if editing else None,
        border_radius=10, filled=True, bgcolor=WHITE, expand=True,
    )

    def on_type_change(e):
        categories = INCOME_CATEGORIES if type_dropdown.value == INCOME_TYPE else EXPENSE_CATEGORIES
        category_dropdown.options = [ft.dropdown.Option(c) for c in categories]
        category_dropdown.value = None
        app.page.update()

    type_dropdown.on_select = on_type_change

    value_field = ft.TextField(
        label="Valor (Kz) *", hint_text="Ex.: 250,00",
        value=f"{transaction.valor:.2f}".replace(".", ",") if editing else "",
        border_radius=10, filled=True, bgcolor=WHITE, expand=True,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    date_field = ft.TextField(
        label="Data *", hint_text="DD/MM/AAAA",
        value=transaction.data if editing else dt.date.today().strftime("%d/%m/%Y"),
        border_radius=10, filled=True, bgcolor=WHITE, expand=True,
    )
    note_field = ft.TextField(
        label="Observação", value=transaction.observacao if editing else "",
        multiline=True, min_lines=3, max_lines=4, border_radius=10, filled=True, bgcolor=WHITE,
    )

    def save(e):
        try:
            value_text = (value_field.value or "").replace(".", "").replace(",", ".")
            new_transaction = Transaction(
                id=app.selected_transaction_id,
                descricao=(description_field.value or "").strip(),
                tipo=type_dropdown.value,
                categoria=category_dropdown.value or "",
                valor=float(value_text) if value_text else 0,
                data=(date_field.value or "").strip(),
                observacao=(note_field.value or "").strip(),
            )
            if app.selected_transaction_id:
                app.repo.update_transaction(new_transaction)
                app.show_message("Movimentação atualizada.")
            else:
                app.repo.add_transaction(new_transaction)
                app.show_message("Movimentação registada com sucesso.")
            app.navigate("transactions")
        except ValueError as erro:
            app.show_message(str(erro), error=True)
        except RuntimeError as erro:
            app.show_message(f"Erro ao ligar à base de dados: {erro}", error=True)

    save_button = ft.FilledButton(
        "Atualizar" if editing else "Salvar", icon=ft.Icons.SAVE_OUTLINED,
        style=ft.ButtonStyle(bgcolor=MEDIUM_GREEN, color=WHITE),
        on_click=save,
    )

    return ft.Column(
        [
            header(
                "Editar Movimentação" if editing else "Adicionar Movimentação",
                "Atualize os dados da movimentação selecionada" if editing else "Registe uma nova receita ou despesa",
            ),
            ft.Container(height=12),
            ft.Container(
                bgcolor=WHITE, border_radius=16, padding=26,
                content=ft.Column(
                    [
                        ft.Row([description_field, type_dropdown], spacing=16),
                        ft.Row([category_dropdown, value_field], spacing=16),
                        date_field,
                        note_field,
                        ft.Container(height=8),
                        save_button,
                    ],
                    spacing=18,
                ),
                shadow=ft.BoxShadow(blur_radius=14, color="#0000000F", offset=ft.Offset(0, 4)),
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )
