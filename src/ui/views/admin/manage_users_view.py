import datetime as dt

import flet as ft

from models.user import User
from ui.views.theme import (
    MEDIUM_GREEN, YELLOW, LIGHT_BG, WHITE, RED, header,
)


def build(app, editing_user: User = None) -> ft.Column:
    """Vista de Gestão de Utilizadores. Se 'editing_user' for passado, mostra o
    formulário de edição desse utilizador em vez da lista."""
    if editing_user is not None:
        return _build_edit_form(app, editing_user)
    return _build_list(app)


# Lista de utilizadores

def _build_list(app) -> ft.Column:
    users = app.user_repository.list_users()

    rows = []
    for u in users:
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(u.id))),
                    ft.DataCell(ft.Text(f"{u.primeiro_nome} {u.ultimo_nome}")),
                    ft.DataCell(ft.Text(u.username)),
                    ft.DataCell(ft.Text(u.telefone)),
                    ft.DataCell(ft.Text(u.data_nascimento)),
                    ft.DataCell(ft.Container(
                        content=ft.Text("Ativo" if u.ativo else "Inativo", size=11, color=WHITE,
                                         weight=ft.FontWeight.W_600),
                        bgcolor=MEDIUM_GREEN if u.ativo else RED, border_radius=8,
                        padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                    )),
                    ft.DataCell(ft.Row(
                        [
                            ft.IconButton(ft.Icons.EDIT_OUTLINED, icon_color=MEDIUM_GREEN, icon_size=18,
                                          tooltip="Editar",
                                          on_click=lambda e, usr=u: app.navigate("manage_users", user=usr)),
                            ft.IconButton(ft.Icons.LOCK_RESET, icon_color=YELLOW, icon_size=18,
                                          tooltip="Redefinir password",
                                          on_click=lambda e, usr=u: _abrir_reset_password(app, usr)),
                            ft.IconButton(
                                ft.Icons.BLOCK if u.ativo else ft.Icons.CHECK_CIRCLE_OUTLINE,
                                icon_color=RED if u.ativo else MEDIUM_GREEN, icon_size=18,
                                tooltip="Desativar" if u.ativo else "Ativar",
                                disabled=(u.id == 1),
                                on_click=lambda e, usr=u: _confirmar_alternar_estado(app, usr),
                            ),
                        ],
                        spacing=0,
                    )),
                ]
            )
        )

    if not rows:
        rows = [ft.DataRow(cells=[ft.DataCell(ft.Text("")) for _ in range(7)])]

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")), ft.DataColumn(ft.Text("Nome")), ft.DataColumn(ft.Text("Utilizador")),
            ft.DataColumn(ft.Text("Telefone")), ft.DataColumn(ft.Text("Nascimento")),
            ft.DataColumn(ft.Text("Estado")), ft.DataColumn(ft.Text("Ações")),
        ],
        rows=rows,
        heading_row_color=LIGHT_BG,
        column_spacing=20,
    )

    add_button = ft.FilledButton(
        "Cadastrar Utilizador", icon=ft.Icons.PERSON_ADD_OUTLINED,
        style=ft.ButtonStyle(bgcolor=MEDIUM_GREEN, color=WHITE),
        on_click=lambda e: _abrir_cadastro(app),
    )

    return ft.Column(
        [
            ft.Row(
                [header("Gerir Utilizadores", "Cadastre, edite, desative ou redefina passwords de utilizadores"),
                 add_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(height=12),
            ft.Container(
                bgcolor=WHITE, border_radius=16, padding=16, expand=True,
                content=ft.Column([table], expand=True, scroll=ft.ScrollMode.AUTO),
                shadow=ft.BoxShadow(blur_radius=14, color="#0000000F", offset=ft.Offset(0, 4)),
            ),
        ],
        expand=True,
    )


def _confirmar_alternar_estado(app, usuario: User) -> None:
    novo_estado = not usuario.ativo

    def confirmar(e):
        try:
            app.user_repository.set_active(usuario.id, novo_estado)
            app.show_message(f"Utilizador {'ativado' if novo_estado else 'desativado'} com sucesso.")
        except ValueError as erro:
            app.show_message(str(erro), error=True)
        app.page.pop_dialog()
        app.show_manage_users()

    def cancelar(e):
        app.page.pop_dialog()

    app.page.show_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar ação"),
            content=ft.Text(
                f"Deseja {'ativar' if novo_estado else 'desativar'} o utilizador "
                f"{usuario.primeiro_nome} {usuario.ultimo_nome}?"
            ),
            actions=[ft.TextButton("Cancelar", on_click=cancelar),
                     ft.FilledButton("Confirmar", style=ft.ButtonStyle(bgcolor=MEDIUM_GREEN, color=WHITE),
                                      on_click=confirmar)],
        )
    )


def _abrir_reset_password(app, usuario: User) -> None:
    nova_senha_field = ft.TextField(label="Nova password", password=True, can_reveal_password=True, width=280)
    erro_texto = ft.Text("", color=RED, size=12)

    def confirmar(e):
        try:
            app.user_repository.reset_password(usuario.id, nova_senha_field.value)
        except ValueError as erro:
            erro_texto.value = str(erro)
            app.page.update()
            return
        app.show_message("Password redefinida com sucesso.")
        app.page.pop_dialog()

    def cancelar(e):
        app.page.pop_dialog()

    app.page.show_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Redefinir password — {usuario.primeiro_nome} {usuario.ultimo_nome}"),
            content=ft.Column([nova_senha_field, erro_texto], tight=True, spacing=8),
            actions=[ft.TextButton("Cancelar", on_click=cancelar),
                     ft.FilledButton("Redefinir", style=ft.ButtonStyle(bgcolor=MEDIUM_GREEN, color=WHITE),
                                      on_click=confirmar)],
        )
    )


def _abrir_cadastro(app) -> None:
    primeiro_nome_field = ft.TextField(label="Primeiro nome *", width=270)
    ultimo_nome_field = ft.TextField(label="Último nome *", width=270)

    data_padrao = dt.datetime.today().replace(year=dt.datetime.today().year - 18)
    data_estado = {"valor": data_padrao}
    data_field = ft.TextField(
        label="Data de nascimento *", value=data_padrao.strftime("%d/%m/%Y"), read_only=True,
        width=270, suffix_icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: app.page.show_dialog(date_picker),
    )

    def on_date_change(e):
        data_estado["valor"] = e.control.value
        data_field.value = e.control.value.strftime("%d/%m/%Y")
        app.page.update()

    date_picker = ft.DatePicker(
        first_date=dt.datetime(1930, 1, 1), last_date=dt.datetime.today(), on_change=on_date_change,
    )
    if getattr(app, "_cadastro_date_picker", None) in app.page.overlay:
        app.page.overlay.remove(app._cadastro_date_picker)
    app.page.overlay.append(date_picker)
    app._cadastro_date_picker = date_picker

    telefone_field = ft.TextField(label="Telefone", width=270,
                                   keyboard_type=ft.KeyboardType.NUMBER)
    senha_field = ft.TextField(label="Password inicial *", password=True, can_reveal_password=True, width=270)
    erro_texto = ft.Text("", color=RED, size=12)

    def confirmar(e):
        try:
            novo_user = User(
                primeiro_nome=(primeiro_nome_field.value or "").strip(),
                ultimo_nome=(ultimo_nome_field.value or "").strip(),
                data_nascimento=data_estado["valor"].strftime("%d/%m/%Y"),
                telefone=(telefone_field.value or "").strip(),
            )
            if not senha_field.value or len(senha_field.value) < 6:
                raise ValueError("A password inicial deve ter no mínimo 6 caracteres.")
            app.user_repository.add_user(novo_user, senha_field.value)
        except ValueError as erro:
            erro_texto.value = str(erro)
            app.page.update()
            return
        app.show_message("Utilizador cadastrado com sucesso.")
        app.page.pop_dialog()
        app.show_manage_users()

    def cancelar(e):
        app.page.pop_dialog()

    app.page.show_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("Cadastrar Utilizador"),
            content=ft.Column(
                [primeiro_nome_field, ultimo_nome_field, data_field, telefone_field, senha_field, erro_texto],
                tight=True, spacing=10, scroll=ft.ScrollMode.AUTO, height=380,
            ),
            actions=[ft.TextButton("Cancelar", on_click=cancelar),
                     ft.FilledButton("Cadastrar", style=ft.ButtonStyle(bgcolor=MEDIUM_GREEN, color=WHITE),
                                      on_click=confirmar)],
        )
    )


# Formulário de edição
def _build_edit_form(app, usuario: User) -> ft.Column:
    primeiro_nome_field = ft.TextField(label="Primeiro nome *", value=usuario.primeiro_nome, width=300)
    ultimo_nome_field = ft.TextField(label="Último nome *", value=usuario.ultimo_nome, width=300)

    data_inicial = dt.datetime.strptime(usuario.data_nascimento, "%d/%m/%Y")
    data_estado = {"valor": data_inicial}
    data_field = ft.TextField(
        label="Data de nascimento *", value=data_inicial.strftime("%d/%m/%Y"), read_only=True,
        width=300, suffix_icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: app.page.show_dialog(date_picker),
    )

    def on_date_change(e):
        data_estado["valor"] = e.control.value
        data_field.value = e.control.value.strftime("%d/%m/%Y")
        app.page.update()

    date_picker = ft.DatePicker(
        first_date=dt.datetime(1930, 1, 1), last_date=dt.datetime.today(), value=data_inicial,
        on_change=on_date_change,
    )
    if getattr(app, "_edit_user_date_picker", None) in app.page.overlay:
        app.page.overlay.remove(app._edit_user_date_picker)
    app.page.overlay.append(date_picker)
    app._edit_user_date_picker = date_picker

    telefone_field = ft.TextField(label="Telefone *", value=usuario.telefone, width=300,
                                   keyboard_type=ft.KeyboardType.NUMBER)
    username_field = ft.TextField(label="Utilizador (não editável)", value=usuario.username, width=300,
                                   read_only=True, disabled=True)

    def salvar(e):
        try:
            usuario.primeiro_nome = (primeiro_nome_field.value or "").strip()
            usuario.ultimo_nome = (ultimo_nome_field.value or "").strip()
            usuario.data_nascimento = data_estado["valor"].strftime("%d/%m/%Y")
            usuario.telefone = (telefone_field.value or "").strip()
            app.user_repository.update_user_data(usuario)
            app.show_message("Dados do utilizador atualizados.")
            app.navigate("manage_users")
        except ValueError as erro:
            app.show_message(str(erro), error=True)

    def cancelar(e):
        app.navigate("manage_users")

    salvar_button = ft.FilledButton("Guardar", icon=ft.Icons.SAVE_OUTLINED,
                                     style=ft.ButtonStyle(bgcolor=MEDIUM_GREEN, color=WHITE), on_click=salvar)
    cancelar_button = ft.OutlinedButton("Cancelar", style=ft.ButtonStyle(color=MEDIUM_GREEN), on_click=cancelar)

    return ft.Column(
        [
            header("Editar Utilizador", f"A editar os dados de {usuario.primeiro_nome} {usuario.ultimo_nome}"),
            ft.Container(height=12),
            ft.Container(
                bgcolor=WHITE, border_radius=16, padding=26,
                content=ft.Column(
                    [
                        username_field,
                        ft.Row([primeiro_nome_field, ultimo_nome_field], spacing=16),
                        ft.Row([data_field, telefone_field], spacing=16),
                        ft.Container(height=8),
                        ft.Row([salvar_button, cancelar_button], spacing=12),
                    ],
                    spacing=18,
                ),
                shadow=ft.BoxShadow(blur_radius=14, color="#0000000F", offset=ft.Offset(0, 4)),
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )
