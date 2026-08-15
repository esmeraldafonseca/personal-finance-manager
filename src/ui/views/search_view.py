import datetime as dt

import flet as ft

from models.transactions import INCOME_TYPE
from ui.views.theme import MEDIUM_GREEN, YELLOW, LIGHT_BG, WHITE, GRAY_TEXT, header, format_kz


def build(app) -> ft.Column:
    """Constrói a vista de Pesquisa dedicada (descrição, categoria e período),
    restrita às movimentações do utilizador atual."""

    results_column = ft.Column(spacing=10)
    existing_categories = app.repo.get_existing_categories(user_id=app.current_user.id)
    state = {"date_from": None, "date_until": None}

    def parse_data(texto: str):
        try:
            return dt.datetime.strptime(texto, "%d/%m/%Y")
        except (TypeError, ValueError):
            return None

    def search(e=None):
        text = (field.value or "").strip()
        category = category_dropdown.value
        results_column.controls.clear()

        sem_filtros = not text and category == "Todas" and not state["date_from"] and not state["date_until"]
        if sem_filtros:
            results_column.controls.append(
                ft.Text("Escreva um termo ou escolha um filtro para pesquisar.", color=GRAY_TEXT)
            )
            app.page.update()
            return

        found = (
            app.repo.search_transactions(text, user_id=app.current_user.id)
            if text else app.repo.list_transactions(user_id=app.current_user.id)
        )

        if category != "Todas":
            found = [t for t in found if t.categoria == category]

        if state["date_from"]:
            found = [t for t in found if (parse_data(t.data) or dt.datetime.min) >= state["date_from"]]
        if state["date_until"]:
            found = [t for t in found if (parse_data(t.data) or dt.datetime.max) <= state["date_until"]]

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

    category_dropdown = ft.Dropdown(
        label="Categoria", width=190, value="Todas",
        options=[ft.dropdown.Option("Todas")] + [ft.dropdown.Option(c) for c in existing_categories],
        border_radius=10, filled=True, bgcolor=WHITE,
        on_select=search,
    )

    def on_date_from_change(e):
        state["date_from"] = e.control.value
        date_from_field.value = e.control.value.strftime("%d/%m/%Y")
        app.page.update()
        search()

    def on_date_until_change(e):
        state["date_until"] = e.control.value
        date_until_field.value = e.control.value.strftime("%d/%m/%Y")
        app.page.update()
        search()

    date_from_picker = ft.DatePicker(
        first_date=dt.datetime(2000, 1, 1), last_date=dt.datetime.today(), on_change=on_date_from_change,
    )
    date_until_picker = ft.DatePicker(
        first_date=dt.datetime(2000, 1, 1), last_date=dt.datetime.today(), on_change=on_date_until_change,
    )

    if getattr(app, "_search_date_from_picker", None) in app.page.overlay:
        app.page.overlay.remove(app._search_date_from_picker)
    if getattr(app, "_search_date_until_picker", None) in app.page.overlay:
        app.page.overlay.remove(app._search_date_until_picker)
    app.page.overlay.append(date_from_picker)
    app.page.overlay.append(date_until_picker)
    app._search_date_from_picker = date_from_picker
    app._search_date_until_picker = date_until_picker

    date_from_field = ft.TextField(
        label="De", read_only=True, width=140, border_radius=10, filled=True, bgcolor=WHITE,
        suffix_icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: app.page.show_dialog(date_from_picker),
    )
    date_until_field = ft.TextField(
        label="Até", read_only=True, width=140, border_radius=10, filled=True, bgcolor=WHITE,
        suffix_icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: app.page.show_dialog(date_until_picker),
    )

    def clear_date_filters(e):
        state["date_from"] = None
        state["date_until"] = None
        date_from_field.value = ""
        date_until_field.value = ""
        search()

    clear_dates_button = ft.TextButton("Limpar datas", on_click=clear_date_filters)

    button = ft.FilledButton("Pesquisar", icon=ft.Icons.SEARCH,
                              style=ft.ButtonStyle(bgcolor=MEDIUM_GREEN, color=WHITE), on_click=search)

    return ft.Column(
        [
            header("Pesquisar Movimentações", "Encontre movimentações por descrição, categoria ou período"),
            ft.Container(height=12),
            ft.Container(
                bgcolor=WHITE, border_radius=16, padding=20,
                content=ft.Column(
                    [
                        ft.Row([field, button], spacing=10),
                        ft.Row([category_dropdown, date_from_field, date_until_field, clear_dates_button],
                               spacing=10),
                        ft.Divider(height=20),
                        results_column,
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                shadow=ft.BoxShadow(blur_radius=14, color="#0000000F", offset=ft.Offset(0, 4)),
                expand=True,
            ),
        ],
        expand=True,
    )
