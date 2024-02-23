import flet as ft
from home_page import home_page
from login_page import login_page
from timetable_page import timetable_page
from grades_page import grades_page
from registredCourses_page import registeredCourses_page
from about_page import about_page


def main(page: ft.Page):
    page.design = 'adaptive'
    if not page.client_storage.contains_key("lang"):
        page.client_storage.set("lang", "ar")
    page.theme_mode = page.client_storage.get(
        "theme") if page.client_storage.contains_key("theme") else ()

    def route_change(route):
        page.views.clear()
        if page.route == '/login':
            page.views.append(login_page(page))
        else:
            page.views.append(home_page(page))
            if page.route == "/timetable":
                page.views.append(timetable_page(page))
            if page.route == '/grades':
                page.views.append(grades_page(page))
            if page.route == '/registered-courses':
                page.views.append(registeredCourses_page(page))
            if page.route == '/about':
                page.views.append(about_page(page))
        page.update()

    def view_pop(view):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go('/login')


ft.app(target=main)
