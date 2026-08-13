import flet as ft

from ui.views.theme import DARK_BG, MEDIUM_GREEN, LIGHT_GREEN, PALE_GREEN, LIGHT_BG, WHITE, DARK_TEXT, GRAY_TEXT, RED, TITLE_FONT, TEXT_FONT


class LoginView:
    """Ecrã de login em duas metades: identidade visual à esquerda, formulário à
    direita. Em caso de sucesso, substitui o conteúdo da página pelo AppLayout."""

    def __init__(self, page: ft.Page, auth_service, transaction_repository, user_repository, report_service):
        self.page = page
        self.auth_service = auth_service
        self.transaction_repository = transaction_repository
        self.user_repository = user_repository
        self.report_service = report_service
        self._build()

    def _build(self) -> None:
        self.page.title = "PersonalFinanceManager — Login"
        self.page.theme = ft.Theme(font_family=TEXT_FONT)
        self.page.bgcolor = LIGHT_BG
        self.page.padding = 0
        self.page.window.width = 900
        self.page.window.height = 560
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.controls.clear()

        left_panel = self._build_left_panel()
        right_panel = self._build_right_panel()

        card = ft.Container(
            width=820, height=480,
            border_radius=28,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Row(
                [left_panel, right_panel],
                spacing=0, expand=True,
            ),
            shadow=ft.BoxShadow(blur_radius=30, color="#00000022", offset=ft.Offset(0, 10)),
        )

        self.page.add(ft.Container(content=card, alignment=ft.Alignment.CENTER, expand=True))
        self.page.update()

    def _build_left_panel(self) -> ft.Container:
        logo_box = ft.Container(
            content=ft.Text("PFM", size=26, weight=ft.FontWeight.BOLD, color=WHITE, font_family=TITLE_FONT),
            width=72, height=72, bgcolor=MEDIUM_GREEN, border_radius=18, alignment=ft.Alignment.CENTER,
        )

        return ft.Container(
            expand=1,
            bgcolor=DARK_BG,
            padding=44,
            content=ft.Column(
                [
                    logo_box,
                    ft.Container(height=22),
                    ft.Text("PersonalFinance", size=24, weight=ft.FontWeight.BOLD, color=WHITE,
                            font_family=TITLE_FONT),
                    ft.Text("M A N A G E R", size=12, color=PALE_GREEN),
                    ft.Container(height=18),
                    ft.Text(
                        "Organize as suas receitas e despesas, acompanhe relatórios e mantenha as "
                        "suas finanças sob controlo.",
                        size=12, color=PALE_GREEN, font_family=TEXT_FONT,
                    ),
                    ft.Container(expand=True),

                ],
                alignment=ft.MainAxisAlignment.START,
            ),
        )

    def _build_right_panel(self) -> ft.Container:
        self.username_field = ft.TextField(
            label="Utilizador", prefix_icon=ft.Icons.PERSON_OUTLINE,
            border_radius=10, filled=True, bgcolor=LIGHT_BG, border_color="transparent",
            on_submit=self._login,
        )
        self.password_field = ft.TextField(
            label="Password", prefix_icon=ft.Icons.LOCK_OUTLINE, password=True, can_reveal_password=True,
            border_radius=10, filled=True, bgcolor=LIGHT_BG, border_color="transparent",
            on_submit=self._login,
        )
        self.error_text = ft.Text("", color=RED, size=12)

        login_button = ft.FilledButton(
            "Entrar", icon=ft.Icons.LOGIN, width=320, height=46,
            style=ft.ButtonStyle(bgcolor=MEDIUM_GREEN, color=WHITE, shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=self._login,
        )

        return ft.Container(
            expand=1,
            bgcolor=WHITE,
            padding=44,
            content=ft.Column(
                [
                    ft.Container(expand=True),
                    ft.Text("Bem-vindo de volta", size=22, weight=ft.FontWeight.BOLD, color=DARK_TEXT,
                            font_family=TITLE_FONT),
                    ft.Text("Inicie sessão para aceder à sua conta", size=12, color=GRAY_TEXT),
                    ft.Container(height=22),
                    self.username_field,
                    self.password_field,
                    self.error_text,
                    ft.Container(height=4),
                    login_button,
                    ft.Container(expand=True),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

    def _login(self, e) -> None:
        try:
            user = self.auth_service.autenticar(self.username_field.value, self.password_field.value)
        except ValueError as erro:
            self.error_text.value = str(erro)
            self.page.update()
            return

        self.error_text.value = ""
        self._abrir_app(user)

    def _abrir_app(self, user) -> None:
        from ui.app_layout import AppLayout  

        self.page.controls.clear()
        self.page.overlay.clear()
        self.page.vertical_alignment = None
        self.page.horizontal_alignment = None
        AppLayout(
            self.page, self.transaction_repository, self.report_service,
            current_user=user, user_repository=self.user_repository,
            auth_service=self.auth_service,
        )