import flet as ft
from SISSession import SISSession
from langauge import words


def login_page(page: ft.Page):
    view = ft.View()
    page.route = '/login'
    lang = page.client_storage.get("lang")
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    view.horizontal_alignment = ft.MainAxisAlignment.CENTER
    view.controls.append(ft.AppBar(title=ft.Text(
        "SIS APP"), bgcolor=ft.colors.SURFACE_VARIANT))
    username_box = ft.TextField(label=words[lang]['uname'])
    password_box = ft.TextField(
        label=words[lang]['pass'], password=True, can_reveal_password=True)
    if page.client_storage.contains_key("uspass"):
        uspass = page.client_storage.get("uspass")
        username_box.value = uspass[0]
        password_box.value = uspass[1]

    def dlg_close(e):
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(modal=True, actions=[
        ft.TextButton("Ok", on_click=dlg_close)],
        actions_alignment=ft.MainAxisAlignment.END)

    def dlg_open(title, message):
        page.dialog = dlg
        dlg.title = ft.Text(title)
        dlg.content = ft.Text(message)
        dlg.open = True
        page.update()

    def dlg_wait_close():
        dlg_wait.open = False
        page.update()

    dlg_wait = ft.AlertDialog(modal=True)

    def dlg_wait_open():
        page.dialog = dlg_wait
        dlg_wait.content = ft.Row(
            controls=[ft.ProgressRing(), ft.Text("Please wait...")])
        dlg_wait.open = True
        page.update()

    def passing(e):
        pass

    def clicked():
        dlg_wait_open()
        username = username_box.value
        password = password_box.value
        if username == '' or password == '':
            dlg_open("ERROR", "Please fill all entries")
            return False
        s = SISSession(username, password)
        if not s.login_sis():
            dlg_open("ERROR", "Username or password is incorrect.")
            return False
        lang = page.client_storage.get("lang")
        page.session.set("ses", s)
        page.client_storage.set("uspass", [username, password])
        s.change_language(lang)
        page.session.set("data", s.get_data())
        dlg_wait_close()
        page.go('/')
        return True

    def clicked_fuse(e):
        try:
            return clicked()
        except Exception as e:
            dlg_open("error", f"Something went wrong, please try again.")
        return False

    login_btn = ft.ElevatedButton(words[lang]['login'], on_click=clicked_fuse)
    view.controls += [username_box, password_box,
                      ft.Row(controls=[login_btn], alignment=ft.MainAxisAlignment.CENTER)]

    view.controls.append(ft.Row([ft.OutlinedButton("Github: Mohammed-Alabri",
                                                   on_click=lambda _: page.launch_url(
                                                       "https://github.com/Mohammed-Alabri"))],
                                alignment=ft.MainAxisAlignment.CENTER))
    view.vertical_alignment = 'center'
    return view
