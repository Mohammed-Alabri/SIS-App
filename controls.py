import flet as ft


class GradeTable(ft.UserControl):
    def __init__(self, data, page_width):
        super().__init__()
        self.semester = data[0]
        self.sem_GPA = data[1]
        self.cum_GPA = data[2]
        self.table = data[3]
        self.page_width = page_width

    def build(self):
        col = ft.Column()
        col.controls.append(ft.Row([ft.Text(self.semester)], alignment=ft.MainAxisAlignment.CENTER))
        col.controls.append(ft.Row([ft.Text(self.sem_GPA)], alignment=ft.MainAxisAlignment.CENTER))
        col.controls.append(ft.Row([ft.Text(self.cum_GPA)], alignment=ft.MainAxisAlignment.CENTER))
        col.controls.append(ft.Row([self.tabling()], scroll=ft.ScrollMode.HIDDEN))
        col.controls.append(ft.Divider())
        return col

    def tabling(self):
        cols = [ft.DataColumn(ft.Text(i)) for i in self.table[0]]
        rows = [ft.DataRow([ft.DataCell(ft.Text(cell, text_align=ft.TextAlign.CENTER)) for cell in row]) for row in
                self.table[1:]]
        return ft.Row([ft.DataTable(border=ft.border.all(2),
                                    width=self.page_width * 0.9,
                                    border_radius=10,
                                    column_spacing=5,
                                    vertical_lines=ft.border.BorderSide(1),
                                    horizontal_lines=ft.border.BorderSide(1),
                                    columns=cols,
                                    rows=rows)], alignment=ft.MainAxisAlignment.CENTER)

