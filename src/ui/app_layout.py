import datetime as dt

import flet as ft

from repositories.transaction_repository import TransactionRepository
from services.reports import FinancialReport
from ui.views import (
    dashboard_view, transactions_view, add_transaction_view,
    search_view, reports_view, charts_view, categories_view, 
)
from ui.views.theme import DARK_BG, MEDIUM_GREEN, PALE_GREEN, LIGHT_BG, WHITE, RED, TITLE_FONT, TEXT_FONT


class AppLayout:
    """Classe principal: monta a sidebar, gere a navegação e guarda o
    estado partilhado entre vistas (mês/ano selecionados, filtros, etc.)."""

    def __init__(self, page: ft.Page, repository: TransactionRepository, report_service: FinancialReport):
        self.page = page
        self.repo = repository
        self.report_service = report_service

        # Estado partilhado entre as vistas
        self.current_view = "dashboard"
        self.selected_transaction_id = None
        self.search_text = ""
        self.type_filter = "Todos"

        today = dt.date.today()
        self.dashboard_month = f"{today.month:02d}"
        self.dashboard_year = str(today.year)
        self.report_month = f"{today.month:02d}"
        self.report_year = str(today.year)
        self.chart_month = "Todos"
        self.chart_year = "Todos"
        self.chart_tab = "category"

        self._configure_page()
        self.content_area = ft.Container(expand=True, bgcolor=LIGHT_BG, padding=30)
        self._build_sidebar()
        self.show_dashboard()

    # Configuração geral da janela

    def _configure_page(self) -> None:
        self.page.title = "PersonalFinanceManager"
        self.page.theme = ft.Theme(font_family=TEXT_FONT)
        self.page.bgcolor = LIGHT_BG
        self.page.padding = 0
        self.page.window.width = 1360
        self.page.window.height = 860

    def show_message(self, text: str, error: bool = False) -> None:
        """Mostra uma mensagem breve ao utilizador através de um SnackBar."""
        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(text, color=WHITE),
                bgcolor=RED if error else MEDIUM_GREEN,
                duration=3200,
            )
        )

    # Sidebar e navegação

    def _build_sidebar(self) -> None:
        self.nav_items = [
            ("dashboard", ft.Icons.SPACE_DASHBOARD_OUTLINED, "Dashboard"),
            ("transactions", ft.Icons.SWAP_VERT, "Movimentações"),
            ("add", ft.Icons.ADD_CIRCLE_OUTLINE, "Adicionar"),
            ("reports", ft.Icons.DESCRIPTION_OUTLINED, "Relatórios"),
            ("charts", ft.Icons.PIE_CHART_OUTLINE, "Gráficos"),
            ("categories", ft.Icons.CATEGORY_OUTLINED, "Categorias"),
            ("search", ft.Icons.SEARCH, "Pesquisar"),
        ]
        self.nav_buttons = {}
        nav_column = []
        for key, icon, label in self.nav_items:
            button = self._nav_button(key, icon, label)
            self.nav_buttons[key] = button
            nav_column.append(button)

        logo = ft.Column(
            [
                ft.Container(
                    content=ft.Text("PFM", size=20, weight=ft.FontWeight.BOLD, color=WHITE, font_family=TITLE_FONT),
                    width=56, height=56, bgcolor=MEDIUM_GREEN, border_radius=14, alignment=ft.Alignment.CENTER,
                ),
                ft.Text("PersonalFinance", size=15, weight=ft.FontWeight.BOLD, color=WHITE, font_family=TITLE_FONT),
                ft.Text("M A N A G E R", size=10, color=PALE_GREEN),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4,
        )

        sidebar = ft.Container(
            width=230, bgcolor=DARK_BG, padding=ft.Padding.symmetric(vertical=24, horizontal=14),
            content=ft.Column(
                [logo, ft.Divider(color=MEDIUM_GREEN, height=28),
                 ft.Column(nav_column, spacing=4, expand=True, scroll=ft.ScrollMode.AUTO)],
                expand=True,
            ),
        )
        self.page.add(ft.Row([sidebar, self.content_area], expand=True, spacing=0))

    def _nav_button(self, key: str, icon: str, label: str) -> ft.Container:
        selected = key == self.current_view
        return ft.Container(
            content=ft.Row(
                [ft.Icon(icon, color=WHITE if selected else PALE_GREEN, size=19),
                 ft.Text(label, color=WHITE if selected else PALE_GREEN, size=13)],
                spacing=12,
            ),
            padding=ft.Padding.symmetric(vertical=11, horizontal=12),
            border_radius=10,
            bgcolor=MEDIUM_GREEN if selected else None,
            on_click=lambda e, k=key: self.navigate(k),
            ink=True,
        )

    def navigate(self, destination: str, transaction=None) -> None:
        """Muda a vista atual e volta a desenhar a sidebar + conteúdo."""
        self.current_view = destination
        for key, button in self.nav_buttons.items():
            selected = key == destination
            button.bgcolor = MEDIUM_GREEN if selected else None
            row = button.content
            row.controls[0].color = WHITE if selected else PALE_GREEN
            row.controls[1].color = WHITE if selected else PALE_GREEN

        dispatch = {
            "dashboard": self.show_dashboard,
            "transactions": self.show_transactions,
            "add": lambda: self.show_add_transaction(transaction),
            "reports": self.show_reports,
            "charts": self.show_charts,
            "categories": self.show_categories,
            "search": self.show_search,
        }
        dispatch.get(destination, self.show_dashboard)()



    def show_dashboard(self) -> None:
        self.content_area.content = dashboard_view.build(self)
        self.page.update()

    def show_transactions(self) -> None:
        self.content_area.content = transactions_view.build(self)
        self.page.update()

    def show_add_transaction(self, transaction=None) -> None:
        self.content_area.content = add_transaction_view.build(self, transaction)
        self.page.update()

    def show_search(self) -> None:
        self.content_area.content = search_view.build(self)
        self.page.update()

    def show_reports(self) -> None:
        self.content_area.content = reports_view.build(self)
        self.page.update()

    def show_charts(self) -> None:
        self.content_area.content = charts_view.build(self)
        self.page.update()

    def show_categories(self) -> None:
        self.content_area.content = categories_view.build(self)
        self.page.update()
