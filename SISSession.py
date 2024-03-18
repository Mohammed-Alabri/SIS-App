import requests as rq
import time
from bs4 import BeautifulSoup


class SISSession:
    def __init__(self, username, password):
        self.session_sis = rq.Session()
        self.session_portal = rq.session()
        self.username = username
        self.password = password

    def login_sis(self):
        global r
        r = ""
        attempts = 0
        data = {
            'username': self.username,
            'password': self.password
        }
        while attempts < 5:
            try:
                url = "https://sis.squ.edu.om/sis/webreg/3s/login.jsp"
                time.sleep(0.5)
                r = self.session_sis.post(url, data=data)
                break
            except Exception as e:
                print(f"ERROR: {e}")
                attempts += 1
        if "Authentication failed; invalid user name or password" in str(r.content):
            return False
        self.get("https://sis.squ.edu.om/sis/webreg/reg.jsp")
        self.login_portal()
        return True

    def login_portal(self):
        global t
        attempts = 0
        data = {
            'IDToken1': self.username,
            'IDToken2': self.password
        }
        while attempts < 5:
            try:
                url = "https://sso1.squ.edu.om/opensso/UI/Login"
                time.sleep(0.5)
                t = self.session_portal.post(url, data=data)
                break
            except Exception as e:
                print(f"ERROR: {e}")
                attempts += 1

    def get(self, url):
        req = self.session_sis.get(url)
        if "Either an abnormal error has occurred or your session has" in req.text:
            self.login_sis()
            req = self.session_sis.get(url)
        return req

    def change_language(self, lang):
        # table_page = self.session_portal.get("https://portal.squ.edu.om")
        # doc = BeautifulSoup(table_page.text, 'html.parser')
        # set_lang = doc.find("a", {'class': 'taglib-language-list-text'}).text
        if lang == "ar":
            self.session_portal.get(
                "https://portal.squ.edu.om/web/guest/home?p_p_id=82&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_82_struts_action=%2Flanguage%2Fview&_82_redirect=%2Fweb%2Fguest%2Fhome&_82_languageId=ar_SA")
        elif lang == "en":
            self.session_portal.get(
                "https://portal.squ.edu.om/web/guest/home?p_p_id=82&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_82_struts_action=%2Flanguage%2Fview&_82_redirect=%2Fweb%2Fguest%2Fhome&_82_languageId=en_US")

    def get_name(self):
        reg_page = self.get("https://sis.squ.edu.om/sis/webreg/reg.jsp")
        doc = BeautifulSoup(reg_page.text, 'html.parser')
        name = doc.find("tr").find_all("td")[1].text
        return name

    def get_data_en(self):
        table_page = self.get(
            "https://sis.squ.edu.om/sis/webreg/timetable.jsp?type=N")
        doc = BeautifulSoup(table_page.text, 'html.parser')
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
        return dic

    def get_data(self):
        table_page = self.session_portal.get(
            "https://portal.squ.edu.om/transcripts")
        doc = BeautifulSoup(table_page.text, 'html.parser')

        name = doc.find("div", {'class': 'col-sm-5'}).text

        major, adivor = [x.text for x in doc.find_all(
            "div", {'class': 'col-sm-6'})[-2:]]
        result = {
            'Name': name,
            'Advisor': adivor,
            'Major': major
        }
        return result

    def get_timetable(self):
        my_table = []
        table_page = self.get(
            "https://sis.squ.edu.om/sis/webreg/timetable.jsp?type=N")
        doc = BeautifulSoup(table_page.text, 'html.parser')
        table = doc.find_all("table")[2]
        days = []
        for day in table.find("tr").find_all("td"):
            days.append(day.text.replace("\xa0", ''))
        my_table.append(days)
        rows = table.find_all("tr")[1:]
        for row in rows:
            my_table.append([cell.text.replace("\xa0", '') if not "/" in cell.text else cell.text[
                :-cell.text[::-1].find(
                    '/') - 4] + "\n" + cell.text[
                -cell.text[
                    ::-1].find(
                    '/') - 4:]
                for cell in row.find_all("td")])
        return my_table

    def get_grades(self):
        req2 = self.session_portal.get("https://portal.squ.edu.om/grades")
        doc = BeautifulSoup(req2.text, 'html.parser')

        find2 = doc.find("div", {'id': 'accordion'})
        semesters = [i.text.strip() for i in find2.find_all(
            "div", {'class': 'span3 text-left'})]
        sem_GPAs = [i.text.strip()
                    for i in find2.find_all("div", {'class': 'span4'})]
        cum_GPAs = [i.text.strip() for i in find2.find_all(
            "div", {'class': 'span5 text-right'})]
        tables = []
        for table in find2.find_all("table"):
            tables.append([[cell.text.strip() for cell in row.find_all("td")] if row.find_all("td") != [] else [
                cell.text.strip() for cell in row.find_all("th")] for row in table.find_all("tr")])
        llast = [[semesters[i], sem_GPAs[i], cum_GPAs[i], tables[i]]
                 for i in range(len(semesters))]
        return llast

    def get_registered(self):
        req2 = self.session_portal.get(
            "https://portal.squ.edu.om/student-registered-courses")
        doc = BeautifulSoup(req2.text, 'html.parser')
        table = [[cell.text.strip() for cell in row.find_all("td")] if row.find_all("td") != [] else [
            cell.text.strip() for cell in row.find_all("th")] for row in
            doc.find("table", id='stdCrsListTable').find_all("tr")]

        return table

    def get_points(self):
        table_page = self.session_portal.get(
            "https://portal.squ.edu.om/gpa-calculation")
        doc = BeautifulSoup(table_page.text, 'html.parser')
        gpa = doc.find('input', {'name': 'AGPA'})['value']
        earned_credit = doc.find('input', {'name': 'creditsEarn'})['value']
        points = doc.find('input', {'name': 'points'})['value']

        return {'GPA': gpa,
                'credit': earned_credit,
                'points': points}
