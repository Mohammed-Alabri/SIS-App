import requests as rq
import time
from bs4 import BeautifulSoup


def login(user_pass, session: rq.Session):
    global t
    attempts = 0
    while attempts < 5:
        try:
            url = "https://sis.squ.edu.om/sis/webreg/3s/login.jsp"
            time.sleep(0.5)
            t = session.post(url, data=user_pass)
            break
        except Exception as e:
            print(f"ERROR: {e}")
            attempts += 1
    if "Authentication failed; invalid user name or password" in str(t.content):
        return False
    return True


def get_name(session: rq.Session):
    reg_page = session.get("https://sis.squ.edu.om/sis/webreg/reg.jsp")
    doc = BeautifulSoup(reg_page.text, 'lxml')

    name = doc.find("tr").find_all("td")[1].text
    return name


def get_timetable(session: rq.Session):
    my_table = []
    session.get("https://sis.squ.edu.om/sis/webreg/reg.jsp")
    table_page = session.get("https://sis.squ.edu.om/sis/webreg/timetable.jsp?type=N")
    doc = BeautifulSoup(table_page.text, 'lxml')
    table = doc.find("table", id='table2')
    dic = {}
    for row in table.find_all("tr"):
        last = ""
        for cell in row.find_all("td"):
            data = cell.text.replace("\n", '').split(":")
            if len(data) == 2:
                dic[data[0].strip()] = data[1].strip()
                last = data[0]
            if last == 'College' or last == 'Major':
                dic[last] = data[0]
    table = doc.find_all("table")[2]
    days = []
    for day in table.find("tr").find_all("td"):
        days.append(day.text.replace("\xa0", ''))
    my_table.append(days)
    rows = table.find_all("tr")[1:]
    for row in rows:
        my_table.append([cell.text.replace("\xa0", '') if not "/" in cell.text else cell.text[:-cell.text[::-1].find('/')-4] + "\n" + cell.text[-cell.text[::-1].find('/')-4:] for cell in row.find_all("td")])
    return my_table

