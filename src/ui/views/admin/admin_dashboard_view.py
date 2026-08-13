import flet as ft

from ui.views.theme import (
    header, summary_card, format_kz,
    MEDIUM_GREEN, LIGHT_GREEN, YELLOW, WHITE,
    DARK_TEXT, GRAY_TEXT, RED, TITLE_FONT,
)


def build(app) -> ft.Column:
    """Dashboard do administrador: visão geral dos utilizadores e das suas movimentações
    (quantos utilizadores existem, quanto gastam/recebem no total, quando foram adicionados)."""

    users = app.user_repository.list_users()
    totals = {row[0]: (row[1], row[2]) for row in app.repo.totals_by_user()}

    total_users = len(users)
    ativos = sum(1 for u in users if u.ativo)
    total_despesas = sum(despesa for _, despesa in totals.values())
    total_receitas = sum(receita for receita, _ in totals.values())

    cards = ft.Row(
        [
            summary_card("Total de Utilizadores", str(total_users), ft.Icons.GROUP_OUTLINED, MEDIUM_GREEN),
            summary_card("Utilizadores Ativos", str(ativos), ft.Icons.CHECK_CIRCLE_OUTLINE, LIGHT_GREEN),
            summary_card("Despesas de Todos", format_kz(total_despesas), ft.Icons.TRENDING_DOWN, YELLOW),
            summary_card("Receitas de Todos", format_kz(total_receitas), ft.Icons.TRENDING_UP, MEDIUM_GREEN),
        ],
        spacing=16,
    )

    recentes = sorted(users, key=lambda u: u.criado_em, reverse=True)[:5]
    linhas = []
    for u in recentes:
        linhas.append(
            ft.Row(
                [
                    ft.Icon(ft.Icons.PERSON_OUTLINE, color=MEDIUM_GREEN, size=16),
                    ft.Column(
                        [ft.Text(f"{u.primeiro_nome} {u.ultimo_nome}", size=12, weight=ft.FontWeight.W_600,
                                 color=DARK_TEXT),
                         ft.Text(u.username, size=10, color=GRAY_TEXT)],
                        spacing=0, expand=True,
                    ),
                    ft.Text(u.criado_em, size=11, color=GRAY_TEXT),
                    ft.Container(
                        content=ft.Text("Ativo" if u.ativo else "Inativo", size=10, color=WHITE,
                                         weight=ft.FontWeight.W_600),
                        bgcolor=MEDIUM_GREEN if u.ativo else RED, border_radius=8,
                        padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                    ),
                ],
                spacing=10,
            )
        )
    if not linhas:
        linhas = [ft.Text("Ainda não existem utilizadores cadastrados.", color=GRAY_TEXT, size=12)]

    recentes_card = ft.Container(
        bgcolor=WHITE, border_radius=16, padding=20, expand=True,
        content=ft.Column(
            [
                ft.Row(
                    [ft.Text("Utilizadores Recentes", size=15, weight=ft.FontWeight.BOLD, color=DARK_TEXT,
                             font_family=TITLE_FONT),
                     ft.TextButton("Gerir utilizadores", on_click=lambda e: app.navigate("manage_users"))],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Column(linhas, spacing=14),
            ],
            spacing=10,
        ),
        shadow=ft.BoxShadow(blur_radius=14, color="#0000000F", offset=ft.Offset(0, 4)),
    )

    return ft.Column(
        [
            header("Dashboard do Administrador", "Visão geral dos utilizadores do sistema"),
            ft.Container(height=8),
            cards,
            ft.Container(height=16),
            recentes_card,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
