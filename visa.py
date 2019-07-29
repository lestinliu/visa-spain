import json
from subprocess import Popen, PIPE
from datetime import datetime

from person import Person
from utils import captcha
from utils.gmm import Email
from utils import config
from io import BytesIO
from PIL import Image
import time
from utils.basic import Basic
from utils.google_sheet import GoogleSheets


class Visa(Basic):

    def __init__(self, driver):
        super().__init__(driver)
        self.gs = GoogleSheets()

    def open_page(self, page):
        self.driver.get(page)

    def select_centre(self, city, category):
        self.driver.execute_script("setCookie();")
        self.click_el(name="centre")
        self.click_el(xpath="//select[@name='centre']/option[text()='{}']".format(city))
        self.wait_for_loading()
        self.click_el(name="category")
        self.click_el(xpath="//select[@name='category']/option[text()='{}']".format(category))

    def enter_phone_and_email(self, phone, email):
        # enter phone
        self.enter_message(phone, id="phone")
        self.enter_message(email, id="email")

    def enter_wrong_code(self, username, password):
        self.enter_message(self.random_with_n_digits(4), id="otp")
        self.click_el(name="save")
        email = Email()
        email.make_seen(username, password)
        self.click_el(id="verification_code")
        time.sleep(3)

    # check mail
    def get_code_from_email(self, email):
        time.sleep(3)  # get code from email
        mail = Email()
        code = mail.read_email(email, config.PASSWORD)
        if code:
            return code
        else:
            print(datetime.now().time(), "no email")
            time.sleep(config.TIMEOUT)
            self.enter_wrong_code(email, config.PASSWORD)
            self.get_code_from_email(email)

    def enter_code_from_email(self, email):
        self.enter_message(self.get_code_from_email(email), id="otp")
        self.click_el(name="save")
        time.sleep(1)  # wait for window loaded
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        view = self.driver.find_element_by_xpath("//div[@class = 'row whiteBG paddingInBox black']")
        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', view)
        self.click_el(name="agree")

    def get_available_dates(self):
        self.click_el(id="app_date")
        next_button_xpath = "//div[@class = 'datepicker-days']//th[@class = 'next' and @style = 'visibility: visible;']"
        available_dates = {}
        while True:
            nd = self.get_normal_dates()
            if nd:
                available_dates.update(nd)
            if self.driver.find_elements_by_xpath(next_button_xpath):
                self.click_el(xpath=next_button_xpath)
            else:
                break
        return available_dates

    def get_available_people(self):
        visa = self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "visa")
        available_people = {}
        for person in visa.get_all_records():
            if not person["script_comment"] and not person["status"]:
                family = "0" if not person["family"] else str(person["family"])
                if family not in available_people:
                    available_people[family] = []
                available_people[family].append(person)
        return available_people

    def fill_appointment_date(self, date):
        self.click_el(id="app_date")
        month_el = datetime.strptime(
            self.driver.find_element_by_xpath("//div[@class='datepicker-days']//th[@class='datepicker-switch']").text,
            '%B %Y')
        print("")
        for i in range(self.diff_month(date, month_el)):
            self.click_el(xpath="//div[@class = 'datepicker-days']//th[@class = 'next']")
        self.click_el(
            xpath="//div[@class='datepicker-days']//td[@class = 'day activeClass' and text() = '{}']".format(date.day))
        self.click_el(xpath="(//select[@id='app_time']/option)[2]")

    def get_normal_dates(self):
        normal_dates_xpath = "//div[@class='datepicker-days']//td[@class = 'day activeClass']"
        result_dates = {}
        dates = []
        if len(self.driver.find_elements_by_xpath(normal_dates_xpath)):
            found_month = self.driver.find_element_by_xpath(
                "//div[@class='datepicker-days']//th[@class='datepicker-switch']").text
            for day in self.driver.find_elements_by_xpath(normal_dates_xpath):  # need refactor fix
                dates.append(day.text)
            for day in dates:
                found_date = datetime.strptime(day + " " + found_month, '%d %B %Y')
                result_dates[found_date.strftime("%d/%m/%Y")] = []
        return result_dates

    def get_available_time(self, date):
        self.driver.refresh()
        self.click_el(id="app_date")
        month_el = datetime.strptime(self.driver.find_element_by_xpath(
            "//div[@class='datepicker-days']//th[@class='datepicker-switch']").text, '%B %Y')
        for i in range(self.diff_month(date, month_el)):
            self.click_el(xpath="//div[@class = 'datepicker-days']//th[@class = 'next']")
        self.click_el(
            xpath="//div[@class='datepicker-days']//td[contains(@class, ' activeClass') and text() = '{}']"
                .format(date.day))
        times = self.driver.find_elements_by_xpath("//select[@id='app_time']/option")
        available_time = []
        for i in times:
            available_time.append(i.text)
        available_time.pop(0)
        return available_time

    # format (02 8 2019)
    def fill_travel_date(self, date):
        self.click_el(id="travelDate")
        month_el = datetime.strptime(
            self.driver.find_element_by_xpath("//div[@class='datepicker-days']//th[@class='datepicker-switch']").text,
            '%B %Y')
        for i in range(self.diff_month(date, month_el)):
            self.click_el(xpath="//div[@class = 'datepicker-days']//th[@class = 'next']")
        days_el = self.driver.find_elements_by_xpath(
            "//td[@class = 'active day' or @class = 'day']")
        for day_el in days_el:
            if date.day == int(day_el.text):
                self.click_el(
                    xpath="//td[@class = 'active day' or @class = 'day' and text()='{}']".format(date.day))
                break
        else:
            raise RuntimeError("no dates for this month")

    # fix - assert if not clickable
    def select_date(self, day, month, year):
        years_back = (int(datetime.now().year) - int(year)) // 10
        while years_back:
            years_back -= 1
            self.click_el(xpath="//div[@class = 'datepicker-years']//th[@class = 'prev']")
        self.click_el(
            xpath="//div[@class='datepicker-years']//span[not(contains(@class, 'disabled')) and text()='{}']"
                .format(year))
        self.click_el(
            xpath="//div[@class='datepicker-months']//span[text()='{}']"
                .format(month))
        self.click_el(
            xpath="//div[@class='datepicker-days']//td[not(@class='new day') and not(@class='old day') and text()='{}']"
                .format(day))

    def get_captcha_image(self, file_name):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        page_height = self.driver.execute_script("return document.body.scrollHeight")
        win_height = self.driver.get_window_size()["height"]
        hidden_height = page_height - win_height + 123  # correction 123

        element = self.driver.find_element_by_id('captcha-img')
        location = element.location
        size = element.size
        left = location['x']
        top = location['y'] - hidden_height
        right = left + size['width']
        bottom = top + size['height']

        im = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
        im = im.crop((left, top, right, bottom))  # defines crop points
        im.save(file_name)  # saves new cropped image

    def fill_captcha(self):
        self.get_captcha_image("visa_captcha.png")
        self.enter_message(captcha.get_code("visa_captcha.png").lower(), id="captcha")

    def submit_form(self):
        self.click_el(name="save")
        alert = self.driver.switch_to.alert
        alert.accept()
        time.sleep(1)

    def fill_other_fields(self, person):
        self.fill_travel_date(person.travel_date)
        # visa type
        self.click_el(id="VisaTypeId")
        self.click_el(xpath="//select[@id='VisaTypeId']/option[text()='Tourism']")

        # first and last name
        self.enter_message(person.first_name, id="first_name")
        self.enter_message(person.last_name, id="last_name")

        # dob
        self.click_el(id="dateOfBirth")
        years_back = (datetime.now().year - person.birth_date.year) // 10

        while years_back:
            years_back -= 1
            self.click_el(xpath="//div[@class = 'datepicker-years']//th[@class = 'prev']")

        self.click_el(id="dateOfBirth")
        self.click_el(
            xpath="//div[@class='datepicker-years']//span[not(contains(@class, 'disabled')) and text()='{}']"
                .format(person.birth_date.year))
        self.click_el(
            xpath="//div[@class='datepicker-months']//span[text()='{}']".format(person.birth_date.strftime("%b")))
        self.click_el(
            xpath="//div[@class='datepicker-days']//td[not(@class='new day') and not(@class='old day') and text()='{}']"
                .format(person.birth_date.day))

        # passport and number
        self.click_el(id="passportType")
        self.click_el("//select[@id='passportType']/option[@value='01']")
        self.enter_message(person.passport, id="passport_no")

        # issued
        self.click_el(id="pptIssueDate")
        self.click_el(
            xpath="//div[@class='datepicker-years']//span[not(contains(@class, 'disabled')) and text()='{}']".format(
                person.pasport_issued.year))
        self.click_el(
            xpath="//div[@class='datepicker-months']//span[text()='{}']".format(
                person.pasport_issued.strftime("%b")))
        self.click_el(
            xpath="//div[@class='datepicker-days']//td[not(@class='new day') and not(@class='old day') and text()='{}']".format(
                person.pasport_issued.day))

        # expired
        self.click_el(id="pptExpiryDate")
        first_year = int(self.driver.find_element_by_xpath("//span[@class = 'year disabled']").text)
        years_back = (person.passport_expired.year - int(first_year)) // 10
        while years_back:
            years_back -= 1
            self.click_el(xpath="//div[@class = 'datepicker-years']//th[@class = 'next']")
        self.click_el(
            xpath="//div[@class='datepicker-years']//span[not(contains(@class, 'disabled')) and text()='{}']".format(
                person.passport_expired.year))
        self.click_el(
            xpath="//div[@class='datepicker-months']//span[text()='{}']".format(person.passport_expired.strftime("%b")))
        self.click_el(
            xpath="//div[@class='datepicker-days']//td[not(@class='new day') and not(@class='old day') and text()='{}']"
                .format(person.passport_expired.day))
        # nationality
        self.driver.find_element_by_xpath(
            "//select[@name='nationalityId']/option[contains(text(),'{}')]".format(person.nationality)).click()

        self.enter_message(person.issued_by, id="pptIssuePalace")

    def read_available_dates(self):
        with open('resources/dates.json', 'r') as f:
            dates_dict = json.load(f)
        return dates_dict

    def read_available_people(self):
        with open('resources/people.json', 'r') as f:
            people_dict = json.load(f)
        return people_dict

    def go_to_select_date_page(self, phone, email):
        self.open_page("https://blsspain-belarus.com/book_appointment.php")
        self.select_centre("Minsk", "Normal")
        self.enter_phone_and_email(phone, email)
        self.enter_wrong_code(email, config.PASSWORD)
        self.enter_code_from_email(email)

    def collect_people_for_dates(self, dates, people):
        available_dates = {}
        # people: {'0': [{'id': 8, ...}, {'id': 9, ...}], '6': [{'id': 13, ...}, {'id': 14, ...}]
        # dates: {'26/06/2019': [], '01/07/2019': [], ...}
        if people and dates:
            for family in people:
                if family == "0":
                    for person in people[family]:
                        start_date = datetime.strptime(person["start_date"], "%d/%m/%Y")
                        end_date = datetime.strptime(person["end_date"], "%d/%m/%Y")
                        for date in dates:
                            current_date = datetime.strptime(date, "%d/%m/%Y")
                            if start_date <= current_date <= end_date:
                                if not dates[date]:
                                    dates[date] = self.get_available_time(current_date)
                                if not available_dates.get(date):
                                    available_dates[date] = []
                                available_dates[date].append(person)
                                print("collected_date: ", date)

                                if len(dates[date]) > 1:
                                    del dates[date][0]
                                else:
                                    del dates[date]
                                break
                else:
                    start_date = datetime.strptime(people[family][0]["start_date"], "%d/%m/%Y")
                    end_date = datetime.strptime(people[family][0]["end_date"], "%d/%m/%Y")
                    for date in dates:  # date = '17/06/2019'
                        current_date = datetime.strptime(date, "%d/%m/%Y")
                        if start_date <= current_date <= end_date:
                            if not dates[date]:
                                dates[date] = self.get_available_time(current_date)
                            if len(dates[date]) >= len(people[family]):  # if has enough time slots for family
                                if not available_dates.get(date):
                                    available_dates[date] = []
                                for person in people[family]:
                                    available_dates[date].append(person)
                                    if len(dates[date]) > 1:
                                        del dates[date][0]
                                    else:
                                        del dates[date]
                                break
        return available_dates

    def register_person_for_date(self, p, date):
        person = Person(self.driver, p["id"], p["type"], p["last_name"], p["first_name"], p["passport"],
                        p["birth_date"],
                        p["passport_issued"], p["passport_expired"], p["issued_by"], p["phone"], p["nationality"],
                        p["travel_date"], p["start_date"], p["end_date"], p["family"], p["status"], p["script_comment"],
                        p["email"], p["date_registered"], p["vpn_location"])
        self.fill_appointment_date(date)
        self.fill_other_fields(person)
        self.fill_captcha()
        self.enable_vpn(person.vpn_location)
        self.submit_form()
        reg_element = self.driver.find_elements_by_xpath("//tbody/tr[4]/td[2]")
        if len(self.driver.find_elements_by_xpath("//div[contains(@style, 'color:#F00')]")):
            if "Please enter the correct image characters." in self.driver.find_element_by_xpath(
                    "//div[contains(@style, 'color:#F00')]").text:
                self.fill_captcha()
                self.enable_vpn(person.vpn_location)
                self.submit_form()
        if len(reg_element):
            reg_number = self.driver.find_element_by_xpath("//tbody/tr[4]/td[2]").text.split(" - ")[1]
            self.driver.execute_script("document.title = '{}'".format(reg_number))
            self.driver.execute_script('window.print();')
            self.disable_vpn()
            self.gs.update_visa_item_by_id(self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "visa"),
                                           p["id"], "script_comment", reg_number)
            self.gs.update_visa_item_by_id(self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "visa"),
                                           p["id"], "status", date.strftime("%d/%m/%Y"))
            self.gs.update_visa_item_by_id(self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "visa"),
                                           p["id"], "date_registered", datetime.now().strftime("%d/%m/%Y"))
            return "\n🤑 id: {} is successfully registered. reg num: {}".format(p["id"], reg_number)
        else:
            if len(self.driver.find_elements_by_xpath("//div[contains(@style, 'color:#F00')]")):
                error = self.driver.find_element_by_xpath("//div[contains(@style, 'color:#F00')]").text
            else:
                error = "unknown error"
            self.gs.update_visa_item_by_id(self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "visa"),
                                           p["id"], "status", error)
            return "\n❌ id: {} is failed. Error message: {}".format(p["id"], error)

    def send_monitoring_message(self, bot, message):
        if config.CURRENT_MONITORING_MESSAGE != message:
            try:
                bot.send_message(config.CHAT_ID, message)
                config.CURRENT_MONITORING_MESSAGE = message
            except:
                pass

    def send_register_message(self, bot, message):
        if config.CURRENT_REGISTER_REGISTER != message:
            try:
                bot.send_message(config.CHAT_ID, message)
                config.CURRENT_REGISTER_REGISTER = message
            except:
                pass

    def enable_vpn(self, location):
        self.disable_vpn()
        curr_location = "expressvpn connect {}".format(location)
        cmd = Popen(curr_location, stdout=PIPE, shell=True)
        cmd.communicate()

    def disable_vpn(self):
        cmd = Popen("expressvpn disconnect", stdout=PIPE, shell=True)
        cmd.communicate()

    def update_emails(self):
        spain = self.gs.open_sheet(self.gs.authorize(), "spain", "visa")
        visa = self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "visa")
        locations = self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "vpn_locations")
        for person in spain.get_all_records():
            if not person["reg_date"] and not person["reg_number"]:
                if not visa.cell(person["id"] + 1, 1).value:
                    if person["id"] and person["type"] and person["last_name"] and person["first_name"] \
                            and person["passport"] and person["issued_by"] and person["phone"] \
                            and datetime.strptime(person["birth_date"], "%d/%m/%Y") < datetime.now() \
                            and datetime.strptime(person["passport_issued"], "%d/%m/%Y") < datetime.now() \
                            and person["nationality"] in ("Belarus", "Russian Federation") \
                            and datetime.strptime(person["passport_expired"], "%d/%m/%Y") > datetime.now() \
                            and datetime.strptime(person["travel_date"], "%d/%m/%Y") > datetime.now() \
                            and datetime.strptime(person["start_date"], "%d/%m/%Y") > datetime.now() \
                            and datetime.strptime(person["end_date"], "%d/%m/%Y") > datetime.now():
                        visa.insert_row(list(person.values()), person["id"] + 1)
        for person in visa.get_all_records():
            if person["email"] != "done" and "MHP" in person["script_comment"]:
                time_between = datetime.now() - datetime.strptime(person["date_registered"], "%d/%m/%Y")
                if time_between.days > config.MAX_EMAILS:
                    visa.update_acell("R{}".format(person["id"] + 1), "done")
        for location in locations.get_all_records():
            if location["date_used"] and location["times"] >= config.MAX_EMAILS:
                time_between = datetime.now() - datetime.strptime(location["date_used"], "%d/%m/%Y")
                if time_between.days > config.MAX_VPN_DAYS:
                    locations.update_acell("D{}".format(location["id"] + 1), "0")
                    locations.update_acell("C{}".format(location["id"] + 1), datetime.now().strftime("%d/%m/%Y"))

    def fill_emails(self):
        accounts = self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "accounts")
        visa = self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "visa")
        locations = self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "vpn_locations")
        for person in visa.get_all_records():
            if not person["email"] and not person["status"]:
                for account in accounts.get_all_records():
                    if account["used"] < config.MAX_EMAILS:
                        visa.update_acell("R{}".format(person["id"] + 1), account["email"])
                        break
                for location in locations.get_all_records():
                    if location["times"] < config.MAX_EMAILS:
                        visa.update_acell("T{}".format(person["id"] + 1), location["location"])
                        break
