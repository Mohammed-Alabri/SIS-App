import flet as ft


def timetable_page(page: ft.Page):
    view = ft.View()
    view.route = '/timetable'
    timetable_type = page.client_storage.get("timetable_type") if page.client_storage.contains_key(
        "timetable_type") else "N"

    def change_time_table(e):
        if timetable_type == "N":
            page.client_storage.set("timetable_type", "R")
        else:
            page.client_storage.set("timetable_type", "N")
        page.go(f'/timetable{timetable_type}')

    view.controls.append(ft.AppBar(title=ft.Text("Timetable"), bgcolor=ft.colors.SURFACE_VARIANT, actions=[ft.IconButton(ft.icons.NIGHTLIGHT_ROUND_SHARP if timetable_type == "N" else ft.icons.SUNNY, on_click=change_time_table)]))
    coll = ft.Column()
    view.controls.append(ft.Row(controls=[coll], alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.HIDDEN))
    table: list
    table = page.session.get("ses").get_timetable(timetable_type)
    cols = []
    for i in table[0]:
        cols.append(ft.DataColumn(ft.Text(i, text_align=ft.TextAlign.CENTER)))
    rows = []
    for row in table[1:]:
        rows.append(ft.DataRow([ft.DataCell(ft.Text(cell, text_align=ft.TextAlign.CENTER)) for cell in row]))
    coll.controls.append(ft.DataTable(border=ft.border.all(2),
                                      border_radius=10,
                                      column_spacing=5,
                                      vertical_lines=ft.border.BorderSide(1),
                                      horizontal_lines=ft.border.BorderSide(1),
                                      data_row_color={"hovered": "0x30FF0000"},
                                      columns=cols,
                                      rows=rows))
    return view
