import flet as ft
from SISSession import SISSession
from langauge import words


def home_page(page: ft.Page):
    view = ft.View()
    view.route = '/'
    lang = page.client_storage.get("lang")
    view.controls.append(ft.AppBar(title=ft.Text(
        "Home"), bgcolor=ft.colors.SURFACE_VARIANT))
    user_data = page.session.get("data")
    view.controls.append(ft.Row([ft.Text("welcome " + user_data['Name'], text_align=ft.TextAlign.CENTER)],
                                alignment=ft.MainAxisAlignment.CENTER))
    view.controls.append(ft.Row([ft.Text("Advisor: " + user_data['Advisor'], text_align=ft.TextAlign.CENTER)],
                                alignment=ft.MainAxisAlignment.CENTER))
    view.controls.append(ft.Row([ft.Text("Major: " + user_data['Major'], text_align=ft.TextAlign.CENTER)],
                                alignment=ft.MainAxisAlignment.CENTER))

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

    def clicked_fuse(e):
        try:
            page.go(e)
        except Exception as e:
            dlg_open("Error", "Something went wrong, Please try again.")

    view.controls.append(
        ft.Row(controls=[ft.ElevatedButton(text=words[lang]['tb'], on_click=lambda _: clicked_fuse('/timetable'))],
               alignment=ft.MainAxisAlignment.CENTER))
    view.controls.append(
        ft.Row(
            controls=[
                ft.ElevatedButton(text=words[lang]['regcor'], on_click=lambda _: clicked_fuse('/registered-courses'))],
            alignment=ft.MainAxisAlignment.CENTER))
    view.controls.append(
        ft.Row(controls=[ft.ElevatedButton(text=words[lang]['gr'], on_click=lambda _: clicked_fuse('/grades'))],
               alignment=ft.MainAxisAlignment.CENTER))
    view.controls.append(
        ft.Row(controls=[ft.ElevatedButton(text=words[lang]['LogOut'], on_click=lambda _: clicked_fuse('/login'))],
               alignment=ft.MainAxisAlignment.CENTER))

    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT or page.theme_mode == "light":
            page.theme_mode = "dark"
        else:
            page.theme_mode = "light"
        page.update()
        page.client_storage.set("theme", page.theme_mode)

    def change_lang(e):
        if lang == 'ar':
            page.client_storage.set('lang', 'en')
        else:
            page.client_storage.set('lang', 'ar')
        page.go(f"/{page.client_storage.get('lang')}")
    view.controls.append(ft.Divider())
    view.controls.append(
        ft.Row(controls=[ft.ElevatedButton(text=words[lang]['changeTheme'], on_click=change_theme)],
               alignment=ft.MainAxisAlignment.CENTER))

    view.controls.append(
        ft.Row(controls=[ft.ElevatedButton(text=words[lang]['chanlang'], on_click=change_lang)],
               alignment=ft.MainAxisAlignment.CENTER))

    view.controls.append(
        ft.Row(controls=[ft.ElevatedButton(text=words[lang]['about'], on_click=lambda _: page.go('/about'))],
               alignment=ft.MainAxisAlignment.CENTER))

    return view
