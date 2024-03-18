import flet as ft
from langauge import words


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
        col.controls.append(
            ft.Row([ft.Text(self.semester)], alignment=ft.MainAxisAlignment.CENTER))
        col.controls.append(
            ft.Row([ft.Text(self.sem_GPA)], alignment=ft.MainAxisAlignment.CENTER))
        col.controls.append(
            ft.Row([ft.Text(self.cum_GPA)], alignment=ft.MainAxisAlignment.CENTER))
        col.controls.append(
            ft.Row([self.tabling()], scroll=ft.ScrollMode.HIDDEN))
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


class CourseGrade(ft.UserControl):
    def __init__(self, gpa, takencrdits, page: ft.Page):
        super().__init__()
        self.lang = page.client_storage.get("lang")
        self.page = page
        self.gpa = float(gpa)
        self.gpa_text = ft.Text(gpa, size=30)
        self.takencredits = float(takencrdits)
        self.grades = []
        cols = [ft.DataColumn(ft.Text(words[self.lang]["Course Code"])),
                ft.DataColumn(ft.Text(words[self.lang]["Credits"])),
                ft.DataColumn(ft.Text(words[self.lang]["Grade"]))]
        self.table = ft.DataTable(columns=reversed(cols) if self.lang == "ar" else cols,
                                  data_row_max_height=60
                                  )
        self.grades_list = {
            'A': 4,
            'A-': 3.7,
            'B+': 3.3,
            'B': 3,
            'B-': 2.7,
            'C+': 2.3,
            'C': 2,
            'C-': 1.7,
            'D+': 1.3,
            'D': 1,
            'F': 0
        }

    def build(self):
        col = ft.Column()
        col.controls.append(ft.Row([self.gpa_text], alignment='center'))
        col.controls.append(self.table)
        return col

    def calc_grade(self, e):
        total_credits = self.takencredits
        summ = self.takencredits * self.gpa
        gr: ft.Dropdown
        for cr, gr in self.grades:
            total_credits += cr
            summ += self.grades_list[gr.value] * cr
        self.gpa_text.value = round(summ / total_credits, 2)
        if len(self.page.views) == 2:
            self.update()

    def add_row(self, crscd: str, credit: int):
        dropdown = ft.Dropdown(options=[ft.dropdown.Option(gr)
                                        for gr in self.grades_list], on_change=self.calc_grade)
        dropdown.value = 'A'
        self.grades.append([float(credit), dropdown])
        row = [ft.DataCell(ft.Text(crscd)),
               ft.DataCell(ft.Text(str(credit))),
               ft.DataCell(dropdown)]
        self.table.rows.append(ft.DataRow(reversed(row) if self.lang == "ar" else row))
