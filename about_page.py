import flet as ft
from langauge import words


def about_page(page: ft.Page):
    view = ft.View()
    view.route = '/about'
    lang = page.client_storage.get("lang")
    view.controls.append(ft.AppBar(title=ft.Text(
        "About"), bgcolor=ft.colors.SURFACE_VARIANT))
    view.controls.append(
        ft.Row([ft.Text(words[lang]['about_txt'], text_align='center')], alignment='center'))
    view.controls.append(ft.Row([ft.OutlinedButton("Twitter: @3Mohammed21",
                                                   on_click=lambda _: page.launch_url(
                                                       "https://twitter.com/3Mohammed21"))],
                                alignment=ft.MainAxisAlignment.CENTER))
    view.controls.append(ft.Row([ft.OutlinedButton("Instagram: @thematrex_007",
                                                   on_click=lambda _: page.launch_url(
                                                       "https://www.instagram.com/thematrex_007/"))],
                                alignment=ft.MainAxisAlignment.CENTER))
    view.controls.append(ft.Row([ft.OutlinedButton("Github: SIS-App",
                                                   on_click=lambda _: page.launch_url(
                                                       "https://github.com/Mohammed-Alabri/SIS-App"))],
                                alignment=ft.MainAxisAlignment.CENTER))
    return view
