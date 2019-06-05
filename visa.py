import json
import pickle
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
        self.driver.execute_script("sendOTP();")
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
        next_button_xpath = "//div[@class = 'datepicker-days']" \
                            "//th[@class = 'next' and not(@style = 'visibility: hidden;')]"
        available_dates = []
        while True:
            nd = self.get_normal_dates()
            if nd:
                available_dates.extend(nd)
            if len(self.driver.find_elements_by_xpath(next_button_xpath)):
                self.click_el(xpath=next_button_xpath)
            else:
                break
        return available_dates

    def fill_appintment_date(self, date):
        self.click_el(id="app_date")
        month_el = datetime.strptime(
            self.driver.find_element_by_xpath("//div[@class='datepicker-days']//th[@class='datepicker-switch']").text,
            '%B %Y')
        for i in range(self.diff_month(date, month_el)):
            self.click_el(xpath="//div[@class = 'datepicker-days']//th[@class = 'next']")
        self.click_el(
            xpath="//div[@class='datepicker-days']//td[@class = 'day activeClass' and text() = '{}']".format(date.day))
        self.click_el(xpath="(//select[@id='app_time']/option)[2]")

    def get_normal_dates(self):
        normal_dates_xpath = "//div[@class='datepicker-days']//td[@class = 'day activeClass']"
        result_dates = []
        if len(self.driver.find_elements_by_xpath(normal_dates_xpath)):
            found_month = self.driver.find_element_by_xpath(
                "//div[@class='datepicker-days']//th[@class='datepicker-switch']")
            for date in self.driver.find_elements_by_xpath(normal_dates_xpath):
                found_date = datetime.strptime(date.text + " " + found_month.text, '%d %B %Y')
                result_dates.append(found_date.strftime("%d/%m/%Y"))
        return result_dates

    def wait_for_available_dates(self):
        available_dates = self.get_available_dates()
        if not available_dates:
            time.sleep(3)
            self.driver.refresh()
            self.wait_for_available_dates()
        else:
            return available_dates

    def get_available_time(self, day):
        self.click_el(id="app_date")
        time.sleep(2)
        self.click_el(
            xpath="//div[@class='datepicker-days']//td[contains(@class, ' activeClass') and text() = '{}']".format(day))
        times = self.driver.find_elements_by_xpath("//select[@id='app_time']/option")
        available_time = []
        for i in times:
            available_time.append(i.text)
        available_time.pop(0)
        return available_time

    def check_available_times(self, available_dates):
        available_times = available_dates
        for month in available_dates.keys():
            for day in available_dates[month]:
                available_times[month][day] = self.get_available_time(day)
        return available_times

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

    def write_available_dates(self, available_dates):
        with open("resources/date.txt", 'wb') as f:
            pickle.dump(available_dates, f)

    def read_available_dates(self):
        with open("resources/date.txt", 'rb') as f:
            my_list = pickle.load(f)
        dates = []
        for str_date in my_list:
            dates.append(datetime.strptime(str_date, "%d/%m/%Y"))
        return dates

    def fill_emails(self):
        accounts = self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "accounts")
        visa = self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "visa")
        for person in visa.get_all_records():
            if not person["email"] and not person["status"]:
                for account in accounts.get_all_records():
                    if account["used"] < config.MAX_EMAILS:
                        visa.update_acell("R{}".format(person["id"] + 1), account["email"])
                        break

    def go_to_select_date_page(self, phone, email):
        self.fill_emails()
        self.open_page("https://blsspain-belarus.com/book_appointment.php")
        self.select_centre("Minsk", "Normal")
        self.enter_phone_and_email(phone, email)
        self.enter_wrong_code(email, config.PASSWORD)
        self.enter_code_from_email(email)

    def register_people_for_dates(self, dates):
        for date in dates:
            print("date:", date.strftime("%d/%m/%Y"))
            filtered = self.gs.filter_visa_with_appropriate_date(json.dumps(
                self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "visa").get_all_records()), date)
            if filtered:
                for p in filtered:
                    self.go_to_select_date_page(p["phone"], p["email"])
                    self.register_person_for_date(self.driver, p, date)
                    reg_number = self.driver.find_element_by_xpath("//tbody/tr[4]/td[2]").text.split(" - ")[1]
                    self.gs.update_visa_item_by_id(self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "visa"),
                                                   p["id"], "script_comment", reg_number)
                    self.gs.update_visa_item_by_id(self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "visa"),
                                                   p["id"], "status", date.strftime("%d/%m/%Y"))
                    self.driver.execute_script("document.title = '{}'".format(reg_number))
                    self.driver.execute_script('window.print();')

    def register_person_for_date(self, driver, p, date):
        person = Person(driver, p["id"], p["type"], p["last_name"], p["first_name"], p["passport"], p["birth_date"],
                        p["passport_issued"], p["passport_expired"], p["issued_by"], p["phone"], p["nationality"],
                        p["travel_date"], p["start_date"], p["end_date"], p["family"], p["status"], p["script_comment"],
                        p["email"])
        self.fill_appintment_date(date)
        self.fill_other_fields(person)
        self.fill_captcha()
        self.submit_form()
