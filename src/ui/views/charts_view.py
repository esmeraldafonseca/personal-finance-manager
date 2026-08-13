import flet as ft

from charts.charts import income_vs_expenses_chart, expenses_by_category_chart, NoChartDataError
from ui.views.theme import MEDIUM_GREEN, LIGHT_BG, WHITE, DARK_TEXT, GRAY_TEXT, TITLE_FONT, MONTHS, header, format_kz


def build(app) -> ft.Column:
    """Constrói a vista de Gráficos Estatísticos (por categoria / receitas vs despesas)."""

    existing_years = app.repo.get_existing_years()
    month_dropdown = ft.Dropdown(width=150, value=app.chart_month,
                                  options=[ft.dropdown.Option("Meses")] + [ft.dropdown.Option(m, label) for m, label in MONTHS],
                                  border_radius=10, filled=True, bgcolor=WHITE,
                                  on_select=lambda e: _update_period(app, e.control.value, app.chart_year))
    year_dropdown = ft.Dropdown(width=110, value=app.chart_year,
                                 options=[ft.dropdown.Option("Anos")] + [ft.dropdown.Option(a) for a in existing_years],
                                 border_radius=10, filled=True, bgcolor=WHITE,
                                 on_select=lambda e: _update_period(app, app.chart_month, e.control.value))

    def tab(label, key):
        selected = app.chart_tab == key
        return ft.Container(
            content=ft.Text(label, color=WHITE if selected else DARK_TEXT, weight=ft.FontWeight.W_600),
            bgcolor=MEDIUM_GREEN if selected else LIGHT_BG,
            padding=ft.Padding.symmetric(horizontal=16, vertical=8), border_radius=10,
            on_click=lambda e: _change_tab(app, key), ink=True,
        )

    tabs_row = ft.Row([tab("Por Categoria", "category"), tab("Receitas vs Despesas", "comparison")], spacing=10)

    if app.chart_tab == "category":
        chart_area = _build_category_chart(app)
    else:
        chart_area = _build_comparison_chart(app)

    return ft.Column(
        [
            header("Gráficos Estatísticos", "Visualize as suas finanças de forma gráfica"),
            ft.Container(height=12),
            ft.Container(
                bgcolor=WHITE, border_radius=16, padding=20, expand=True,
                content=ft.Column(
                    [tabs_row, ft.Divider(height=20), chart_area, ft.Row([month_dropdown, year_dropdown], spacing=10)],
                    expand=True, scroll=ft.ScrollMode.AUTO,
                ),
                shadow=ft.BoxShadow(blur_radius=14, color="#0000000F", offset=ft.Offset(0, 4)),
            ),
        ],
        expand=True,
    )


def _build_category_chart(app):
    data = app.repo.totals_by_category("Despesa")
    total = sum(v for _, v in data) or 1
    try:
        image = expenses_by_category_chart(data)
        legend = ft.Column(
            [ft.Row(
                [ft.Container(width=10, height=10, bgcolor=MEDIUM_GREEN, border_radius=5),
                 ft.Text(cat, expand=True, size=12),
                 ft.Text(format_kz(val), size=12, weight=ft.FontWeight.W_600),
                 ft.Text(f"{(val / total) * 100:.1f}%", size=11, color=GRAY_TEXT)],
                spacing=8,
            ) for cat, val in data],
            spacing=10,
        )
        return ft.Row(
            [ft.Image(src=image, width=340, height=300, fit=ft.BoxFit.CONTAIN), ft.Container(legend, expand=True)],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    except NoChartDataError as erro:
        return ft.Container(ft.Text(str(erro), color=GRAY_TEXT), alignment=ft.Alignment.CENTER, height=280)


def _build_comparison_chart(app):
    transactions = app.repo.list_transactions()
    total_income = sum(t.valor for t in transactions if t.tipo == "Receita")
    total_expenses = sum(t.valor for t in transactions if t.tipo == "Despesa")
    try:
        image = income_vs_expenses_chart(total_income, total_expenses)
        return ft.Row([ft.Image(src=image, width=420, height=320, fit=ft.BoxFit.CONTAIN)],
                       alignment=ft.MainAxisAlignment.CENTER)
    except NoChartDataError as erro:
        return ft.Container(ft.Text(str(erro), color=GRAY_TEXT), alignment=ft.Alignment.CENTER, height=280)


def _change_tab(app, key: str) -> None:
    app.chart_tab = key
    app.show_charts()


def _update_period(app, month, year) -> None:
    app.chart_month, app.chart_year = month, year
    app.show_charts()
