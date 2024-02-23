import flet as ft
from controls import GradeTable


def grades_page(page: ft.Page):
    view = ft.View()
    view.route = '/grades'
    view.scroll = ft.ScrollMode.AUTO
    view.controls.append(ft.AppBar(title=ft.Text("Grades"), bgcolor=ft.colors.SURFACE_VARIANT))
    grades = page.session.get("ses").get_grades()

    for table in grades:
        view.controls.append((GradeTable(table, page.width)))
    return view
