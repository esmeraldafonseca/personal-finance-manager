import flet as ft

from ui.views.theme import MEDIUM_GREEN, YELLOW, LIGHT_BG, WHITE, GRAY_TEXT, RED, header, format_kz


def build(app) -> ft.Column:
    """Vista 'Movimentações' do administrador: tabela de utilizadores com os seus
    totais de receitas e despesas (o admin não regista movimentações próprias)."""

    users = app.user_repository.list_users()
    totals = {row[0]: (row[1], row[2]) for row in app.repo.totals_by_user()}

    rows = []
    for u in users:
        receita, despesa = totals.get(u.id, (0.0, 0.0))
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(u.id))),
                    ft.DataCell(ft.Text(f"{u.primeiro_nome} {u.ultimo_nome}")),
                    ft.DataCell(ft.Text(u.username)),
                    ft.DataCell(ft.Text(format_kz(receita), color=MEDIUM_GREEN, weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(format_kz(despesa), color=YELLOW, weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Container(
                        content=ft.Text("Ativo" if u.ativo else "Inativo", size=11, color=WHITE,
                                         weight=ft.FontWeight.W_600),
                        bgcolor=MEDIUM_GREEN if u.ativo else RED, border_radius=8,
                        padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                    )),
                ]
            )
        )

    if not rows:
        rows = [ft.DataRow(cells=[ft.DataCell(ft.Text("")), ft.DataCell(ft.Text("Nenhum utilizador cadastrado.",
                color=GRAY_TEXT)), ft.DataCell(ft.Text("")), ft.DataCell(ft.Text("")), ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text(""))])]

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")), ft.DataColumn(ft.Text("Nome")), ft.DataColumn(ft.Text("Utilizador")),
            ft.DataColumn(ft.Text("Receitas")), ft.DataColumn(ft.Text("Despesas")), ft.DataColumn(ft.Text("Estado")),
        ],
        rows=rows,
        heading_row_color=LIGHT_BG,
        column_spacing=24,
    )

    return ft.Column(
        [
            header("Movimentações dos Utilizadores", "Totais de receitas e despesas por utilizador"),
            ft.Container(height=12),
            ft.Container(
                bgcolor=WHITE, border_radius=16, padding=16, expand=True,
                content=ft.Column([table], expand=True, scroll=ft.ScrollMode.AUTO),
                shadow=ft.BoxShadow(blur_radius=14, color="#0000000F", offset=ft.Offset(0, 4)),
            ),
        ],
        expand=True,
    )
