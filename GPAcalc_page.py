import flet as ft
from controls import CourseGrade
from SISSession import SISSession
from langauge import words


def GPAcalc_page(page: ft.Page):
    view = ft.View()
    view.route = '/GPAcalc'
    view.controls.append(ft.AppBar(title=ft.Text("GPA calc"), bgcolor=ft.colors.SURFACE_VARIANT))
    ses = page.session.get("ses")
    data = ses.get_points()
    table = CourseGrade(data['GPA'], data['credit'], page)
    ses: SISSession
    courses: list
    courses = ses.get_registered()
    for course in courses[1:]:
        table.add_row(course[0], course[3])
    view.controls.append(table)
    table.calc_grade(1)
    page.update()
    return view
