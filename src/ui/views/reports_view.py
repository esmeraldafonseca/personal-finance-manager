import datetime as dt
import os

import flet as ft
from fpdf import FPDF

from ui.views.theme import MEDIUM_GREEN, WHITE, DARK_TEXT, GRAY_TEXT, TITLE_FONT, MONTHS, header, format_kz


def build(app) -> ft.Column:
    """Constrói a vista de Relatório Mensal, restrita às movimentações do utilizador atual."""

    existing_years = app.repo.get_existing_years(user_id=app.current_user.id) or [str(dt.date.today().year)]
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
        report = app.report_service.generate_monthly_report(
            app.report_month, app.report_year, user_id=app.current_user.id
        )

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

    def export_pdf(e):
        """Gera um PDF simples com o histórico completo do utilizador (sem filtro de mês/ano)."""
        transactions = app.repo.list_transactions(user_id=app.current_user.id)
        if not transactions:
            app.show_message("Não há movimentações para gerar o relatório.", error=True)
            return

        incomes = [t.valor for t in transactions if t.tipo == "Receita"]
        expenses = [t.valor for t in transactions if t.tipo == "Despesa"]
        total_income = sum(incomes)
        total_expenses = sum(expenses)
        balance = total_income - total_expenses

        expenses_by_category = {}
        for t in transactions:
            if t.tipo == "Despesa":
                expenses_by_category[t.categoria] = expenses_by_category.get(t.categoria, 0.0) + t.valor
        top_category = max(expenses_by_category, key=expenses_by_category.get) if expenses_by_category else "-"

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 12, "Relatorio Financeiro - Historico Completo", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 8, f"Utilizador: {app.current_user.primeiro_nome} {app.current_user.ultimo_nome}", ln=True)
        pdf.cell(0, 8, f"Gerado em {dt.datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
        pdf.ln(6)

        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Resumo", ln=True)
        pdf.set_font("Helvetica", "", 11)
        resumo = [
            ("Total de Receitas", format_kz(total_income)),
            ("Total de Despesas", format_kz(total_expenses)),
            ("Saldo", format_kz(balance)),
            ("Total de Movimentacoes", str(len(transactions))),
            ("Categoria com Maior Despesa", top_category),
            ("Maior Receita", format_kz(max(incomes) if incomes else 0.0)),
            ("Maior Despesa", format_kz(max(expenses) if expenses else 0.0)),
        ]
        for label, valor in resumo:
            pdf.cell(0, 7, f"{label}: {valor}", ln=True)

        pdf.ln(6)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Movimentacoes", ln=True)

        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(31, 111, 99)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(26, 7, "Data", border=1, fill=True)
        pdf.cell(24, 7, "Tipo", border=1, fill=True)
        pdf.cell(38, 7, "Categoria", border=1, fill=True)
        pdf.cell(72, 7, "Descricao", border=1, fill=True)
        pdf.cell(24, 7, "Valor", border=1, fill=True, ln=True)

        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(0, 0, 0)
        for t in transactions:
            pdf.cell(26, 6, t.data, border=1)
            pdf.cell(24, 6, t.tipo, border=1)
            pdf.cell(38, 6, (t.categoria or "")[:22], border=1)
            pdf.cell(72, 6, (t.descricao or "")[:44], border=1)
            pdf.cell(24, 6, format_kz(t.valor), border=1, ln=True)

        os.makedirs("relatorios_exportados", exist_ok=True)
        nome_ficheiro = f"relatorios_exportados/relatorio_completo_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(nome_ficheiro)
        app.show_message(f"Relatório PDF gerado em: {nome_ficheiro}")

    export_button = ft.OutlinedButton(
        "Exportar Histórico Completo (PDF)", icon=ft.Icons.PICTURE_AS_PDF_OUTLINED,
        style=ft.ButtonStyle(color=MEDIUM_GREEN),
        on_click=export_pdf,
    )

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
                        ft.Divider(height=20),
                        ft.Text("Exportação em PDF", size=13, weight=ft.FontWeight.BOLD, color=DARK_TEXT),
                        ft.Text("Gera um relatório em PDF com todo o seu histórico de movimentações, sem filtro de mês.",
                                size=12, color=GRAY_TEXT),
                        ft.Container(height=6),
                        export_button,
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                shadow=ft.BoxShadow(blur_radius=14, color="#0000000F", offset=ft.Offset(0, 4)),
                expand=True,
            ),
        ],
        expand=True,
    )
