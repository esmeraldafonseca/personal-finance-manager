import flet as ft

from charts import charts
from ui.views.theme import MEDIUM_GREEN, WHITE, GRAY_TEXT, header


def build(app) -> ft.Column:
    """Vista de Gráficos do administrador: estatísticas visuais sobre os utilizadores
    (ativos vs inativos, despesas por utilizador)."""

    users = app.user_repository.list_users()
    totals = {row[0]: (row[1], row[2]) for row in app.repo.totals_by_user()}

    ativos = sum(1 for u in users if u.ativo)
    inativos = len(users) - ativos

    despesas_por_user = [
        (f"{u.primeiro_nome} {u.ultimo_nome}", totals.get(u.id, (0.0, 0.0))[1])
        for u in users
    ]

    image_controls = []
    try:
        image_controls.append(_chart_container(
            "Utilizadores Ativos vs Inativos", charts.users_status_chart(ativos, inativos)
        ))
    except charts.NoChartDataError as erro:
        image_controls.append(ft.Text(str(erro), color=GRAY_TEXT))

    try:
        image_controls.append(_chart_container(
            "Despesas por Utilizador", charts.expenses_by_user_chart(despesas_por_user)
        ))
    except charts.NoChartDataError as erro:
        image_controls.append(ft.Text(str(erro), color=GRAY_TEXT))

    return ft.Column(
        [
            header("Gráficos", "Estatísticas visuais sobre os utilizadores do sistema"),
            ft.Container(height=12),
            ft.Column(image_controls, spacing=16, scroll=ft.ScrollMode.AUTO, expand=True),
        ],
        expand=True,
    )


def _chart_container(titulo: str, image_bytes: bytes) -> ft.Container:
    return ft.Container(
        bgcolor=WHITE, border_radius=16, padding=16,
        content=ft.Column(
            [ft.Text(titulo, size=14, weight=ft.FontWeight.BOLD, color=MEDIUM_GREEN),
             ft.Image(src=image_bytes, fit=ft.BoxFit.CONTAIN)],
            spacing=8,
        ),
        shadow=ft.BoxShadow(blur_radius=14, color="#0000000F", offset=ft.Offset(0, 4)),
    )