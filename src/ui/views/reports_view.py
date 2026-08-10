import datetime as dt

import flet as ft

from ui.views.theme import MEDIUM_GREEN, WHITE, DARK_TEXT, GRAY_TEXT, TITLE_FONT, MONTHS, header, format_kz


def build(app) -> ft.Column:
    """Constrói a vista de Relatório Mensal."""

    existing_years = app.repo.get_existing_years() or [str(dt.date.today().year)]
    if app.report_year not in existing_years:
        existing_years = sorted(set(existing_years + [app.report_year]), reverse=True)

    month_dropdown = ft.Dropdown(width=160, value=app.report_month,
                                  options=[ft.dropdown.Option(m, label) for m, label in MONTHS],
                                  border_radius=10, filled=True, bgcolor=WHITE)
    year_dropdown = ft.Dropdown(width=110, value=app.report_year,
                                 options=[ft.dropdown.Option(a) for a in existing_years],
                                 border_radius=10, filled=True, bgcolor=WHITE)
    results_area = ft.Column(spacing=10)

    def line(label, value):
        return ft.Row(
            [ft.Text(label, color=GRAY_TEXT), ft.Text(value, weight=ft.FontWeight.BOLD, color=DARK_TEXT)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def generate(e=None):
        app.report_month, app.report_year = month_dropdown.value, year_dropdown.value
        month_name = dict(MONTHS).get(app.report_month, app.report_month)
        report = app.report_service.generate_monthly_report(app.report_month, app.report_year)

        results_area.controls = [
            ft.Text(f"Resumo de {month_name} / {report.year}", size=15, weight=ft.FontWeight.BOLD,
                    color=DARK_TEXT, font_family=TITLE_FONT),
            ft.Divider(),
            line("Total de Receitas", format_kz(report.total_income)),
            line("Total de Despesas", format_kz(report.total_expenses)),
            line("Saldo do Mês", format_kz(report.balance)),
            line("Total de Movimentações", str(report.transaction_count)),
            line("Categoria com Maior Despesa", report.top_expense_category),
            line("Maior Receita Registada", format_kz(report.highest_income)),
            line("Maior Despesa Registada", format_kz(report.highest_expense)),
        ]
        app.page.update()

    month_dropdown.on_select = generate
    year_dropdown.on_select = generate
    generate_button = ft.FilledButton("Gerar Relatório", icon=ft.Icons.INSERT_CHART_OUTLINED,
                                       style=ft.ButtonStyle(bgcolor=MEDIUM_GREEN, color=WHITE), on_click=generate)

    generate()

    return ft.Column(
        [
            header("Relatório Mensal", "Consulte o resumo financeiro de um mês específico"),
            ft.Container(height=12),
            ft.Container(
                bgcolor=WHITE, border_radius=16, padding=20,
                content=ft.Column(
                    [
                        ft.Row([month_dropdown, year_dropdown, generate_button], spacing=10),
                        ft.Divider(height=20),
                        results_area,
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                shadow=ft.BoxShadow(blur_radius=14, color="#0000000F", offset=ft.Offset(0, 4)),
                expand=True,
            ),
        ],
        expand=True,
    )