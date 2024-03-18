import flet as ft


def registeredCourses_page(page: ft.Page):
    view = ft.View()
    view.route = '/registered-courses'
    view.controls.append(ft.AppBar(title=ft.Text(
        "Registed Courses"), bgcolor=ft.colors.SURFACE_VARIANT))
    table: list
    table = page.session.get("ses").get_registered()
    cols = [ft.DataColumn(ft.Text(i)) for i in table[0]]
    rows = [ft.DataRow([ft.DataCell(ft.Text(cell, text_align=ft.TextAlign.CENTER)) for cell in row]) for row in
            table[1:]]
    view.controls.append(ft.Row([ft.DataTable(border=ft.border.all(2),
                                              border_radius=10,
                                              column_spacing=5,
                                              vertical_lines=ft.border.BorderSide(
                                                  1),
                                              horizontal_lines=ft.border.BorderSide(
                                                  1),
                                              columns=cols,
                                              rows=rows)], alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO))
    return view
