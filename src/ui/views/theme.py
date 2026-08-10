import flet as ft

# Paleta de cores e tipografia da identidade visual "PersonalFinanceManager"
DARK_BG = "#0D2B2E"
MEDIUM_GREEN = "#1F6F63"
LIGHT_GREEN = "#4CAF87"
PALE_GREEN = "#BFE3D1"
YELLOW = "#F4B400"
LIGHT_BG = "#F2F4F7"
WHITE = "#FFFFFF"
DARK_TEXT = "#0D2B2E"
GRAY_TEXT = "#5F6B6A"
RED = "#D9534F"

TITLE_FONT = "Poppins"
TEXT_FONT = "Inter"

MONTHS = [
    ("01", "Janeiro"), ("02", "Fevereiro"), ("03", "Março"), ("04", "Abril"),
    ("05", "Maio"), ("06", "Junho"), ("07", "Julho"), ("08", "Agosto"),
    ("09", "Setembro"), ("10", "Outubro"), ("11", "Novembro"), ("12", "Dezembro"),
]


def format_kz(valor: float) -> str:
    """Formata um valor float como texto de moeda em Kwanzas (ex: 1.234,56 Kz)."""
    return f"{valor:,.2f} Kz".replace(",", "X").replace(".", ",").replace("X", ".")


def header(titulo: str, subtitulo: str) -> ft.Column:
    """Cabeçalho reutilizável (título + subtítulo) para o topo de cada vista."""
    return ft.Column(
        [
            ft.Text(titulo, size=24, weight=ft.FontWeight.BOLD, color=DARK_TEXT, font_family=TITLE_FONT),
            ft.Text(subtitulo, size=13, color=GRAY_TEXT, font_family=TEXT_FONT),
        ],
        spacing=2,
    )


def summary_card(titulo: str, valor: str, icone: str, cor: str) -> ft.Container:
    """Cartão de resumo reutilizável (usado no dashboard)."""
    return ft.Container(
        bgcolor=WHITE,
        border_radius=16,
        padding=18,
        expand=True,
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(icone, color=cor, size=22),
                    width=44, height=44, bgcolor=f"{cor}22", border_radius=12,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Column(
                    [ft.Text(titulo, size=12, color=GRAY_TEXT, font_family=TEXT_FONT),
                     ft.Text(valor, size=19, weight=ft.FontWeight.BOLD, color=DARK_TEXT, font_family=TITLE_FONT)],
                    spacing=2,
                ),
            ],
            spacing=14,
        ),
        shadow=ft.BoxShadow(blur_radius=14, color="#0000000F", offset=ft.Offset(0, 4)),
    )


def card_container(content) -> ft.Container:
    """Container branco com sombra, usado como 'moldura' das vistas."""
    return ft.Container(
        bgcolor=WHITE, border_radius=16, padding=20, expand=True,
        content=content,
        shadow=ft.BoxShadow(blur_radius=14, color="#0000000F", offset=ft.Offset(0, 4)),
    )
