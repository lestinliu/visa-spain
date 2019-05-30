import json
from datetime import datetime

from model.person import Person
from utils import captcha
from utils.gmm import Email
from selenium.webdriver import ActionChains
from io import BytesIO
from PIL import Image
import time
from utils.basic import Basic
from utils.google_sheet import GoogleSheets


class Visa(Basic):

    def __init__(self, driver):
        self.driver = driver
        self.gs = GoogleSheets()
        self.gs_visa_tab = self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "visa")
        self.gs_account_tab = self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "accounts")
        self.gs_dates_tab = self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "dates")

    def click_el(self, xpath):
        element = self.driver.find_element_by_xpath(xpath)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()
        element.click()

    def open_page(self, page):
        self.driver.get(page)

    def select_centre(self, city, category):
        self.driver.execute_script("setCookie();")
        self.click_el("//select[@name='centre']")
        self.click_el("//select[@name='centre']/option[text()='{}']".format(city))
        self.click_el("//select[@name='category']")
        self.click_el("//select[@name='category']/option[text()='{}']".format(category))

    def enter_phone_and_email(self, phone, email):
        # enter phone
        self.driver.find_element_by_id("phone").send_keys(phone)
        self.driver.find_element_by_id("email").send_keys(email)

    def enter_wrong_code(self):
        self.driver.find_element_by_id("otp").clear()
        self.driver.find_element_by_id("otp").send_keys(self.random_with_n_digits(4))
        self.click_el("//input[@name = 'save']")
        self.driver.execute_script("sendOTP();")
        time.sleep(3)

    # check mail
    def get_code_from_email(self, email):
        time.sleep(3)  # get code from email
        mail = Email()
        code = mail.read_email(email, "Ab123456!")
        if code:
            return code
        else:
            print(datetime.now().time(), "no email")
            self.enter_wrong_code()
            self.get_code_from_email(email)

    def enter_code_from_email(self, email):
        self.driver.find_element_by_id("otp").clear()
        self.driver.find_element_by_id("otp").send_keys(self.get_code_from_email(email))
        self.click_el("//input[@name = 'save']")
        time.sleep(1)  # wait for window loaded
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        view = self.driver.find_element_by_xpath("//div[@class = 'row whiteBG paddingInBox black']")
        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', view)
        self.click_el("//button[@name = 'agree']")

    def get_available_dates(self):
        self.click_el("//input[@id = 'app_date']")
        next_button_xpath = "//div[@class = 'datepicker-days']" \
                            "//th[@class = 'next' and not(@style = 'visibility: hidden;')]"
        available_dates = []
        while True:
            nd = self.get_normal_dates()
            if nd:
                available_dates.extend(nd)
            if len(self.driver.find_elements_by_xpath(next_button_xpath)):
                self.click_el(next_button_xpath)
            else:
                break

        print("{}: available: {}".format(datetime.now(), available_dates))
        return available_dates

    def fill_appintment_date(self, date):
        self.click_el("//input[@id = 'app_date']")
        # print("date", date)
        month_el = datetime.strptime(
            self.driver.find_element_by_xpath("//div[@class='datepicker-days']//th[@class='datepicker-switch']").text,
            '%B %Y')
        for i in range(self.diff_month(date, month_el)):
            self.click_el("//div[@class = 'datepicker-days']//th[@class = 'next']")
        self.click_el(
            "//div[@class='datepicker-days']//td[@class = 'day activeClass' and text() = '{}']".format(date.day))
        self.click_el("(//select[@id='app_time']/option)[2]")

    def get_normal_dates(self):
        normal_dates_xpath = "//div[@class='datepicker-days']//td[@class = 'day activeClass']"
        result_dates = []
        if len(self.driver.find_elements_by_xpath(normal_dates_xpath)):
            found_month = self.driver.find_element_by_xpath(
                "//div[@class='datepicker-days']//th[@class='datepicker-switch']")
            for date in self.driver.find_elements_by_xpath(normal_dates_xpath):
                found_date_str = date.text + " " + found_month.text
                found_date = datetime.strptime(found_date_str, '%d %B %Y').date()
                result_dates.append(found_date)

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
        self.click_el("//input[@id = 'app_date']")
        time.sleep(2)
        self.click_el(
            "//div[@class='datepicker-days']//td[contains(@class, ' activeClass') and text() = '{}']".format(day))
        times = self.driver.find_elements_by_xpath("//select[@id='app_time']/option")
        available_time = []
        for i in times:
            available_time.append(i.text)
        available_time.pop(0)
        return available_time

    def check_available_times(self, available_dates):
        available_times = available_dates
        for month in available_dates.keys():
            print("month: ", month)
            for day in available_dates[month]:
                print("day:", day)
                print("get_available_time:", self.get_available_time(day))
                print("available_times: ", available_times)
                print("available_times[month]", available_times[month])
                print("available_times[month]", available_times[month])
                available_times[month][day] = self.get_available_time(day)
        print("available_times", available_times)
        return available_times

    # format (02 8 2019)
    def fill_travel_date(self, date):
        self.click_el("//input[@id = 'travelDate']")
        # print("date", date)
        month_el = datetime.strptime(
            self.driver.find_element_by_xpath("//div[@class='datepicker-days']//th[@class='datepicker-switch']").text,
            '%B %Y')
        for i in range(self.diff_month(date, month_el)):
            self.click_el("//div[@class = 'datepicker-days']//th[@class = 'next']")
        days_el = self.driver.find_elements_by_xpath(
            "//td[@class = 'active day' or @class = 'day']")
        for day_el in days_el:
            print("day", date.day, day_el.text)
            if date.day == int(day_el.text):
                print("//td[@class = 'active day' or @class = 'day' and text()='{}']".format(date.day))
                self.click_el(
                    "//td[@class = 'active day' or @class = 'day' and text()='{}']".format(date.day))
                break
        else:
            raise RuntimeError("no dates for this month")

    # fix - assert if not clickable
    def select_date(self, day, month, year):
        years_back = (int(datetime.now().year) - int(year)) // 10
        while years_back:
            years_back -= 1
            self.click_el("//div[@class = 'datepicker-years']//th[@class = 'prev']")
        self.click_el(
            "//div[@class='datepicker-years']//span[not(contains(@class, 'disabled')) and text()='{}']".format(year))
        self.click_el(
            "//div[@class='datepicker-months']//span[text()='{}']".format(month))
        self.click_el(
            "//div[@class='datepicker-days']//td[not(@class='new day') and not(@class='old day') and text()='{}']"
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
        self.driver.find_element_by_id("captcha").send_keys(captcha.get_code("visa_captcha.png").lower())

    def submit_form(self):
        self.click_el("//input[@name = 'save']")
        alert = self.driver.switch_to.alert
        alert.accept()
        time.sleep(1)

    def fill_other_fields(self, person):
        self.fill_travel_date(person.travel_date)
        # visa type
        self.click_el("//select[@id='VisaTypeId']")
        self.click_el("//select[@id='VisaTypeId']/option[text()='Tourism']")

        # first and last name
        self.driver.find_element_by_id("first_name").send_keys(person.first_name)
        self.driver.find_element_by_id("last_name").send_keys(person.last_name)

        # dob
        self.click_el("//input[@id = 'dateOfBirth']")
        years_back = (datetime.now().year - person.birth_date.year) // 10

        while years_back:
            years_back -= 1
            self.click_el("//div[@class = 'datepicker-years']//th[@class = 'prev']")

        self.click_el("//input[@id = 'dateOfBirth']")
        self.click_el(
            "//div[@class='datepicker-years']//span[not(contains(@class, 'disabled')) and text()='{}']".format(
                person.birth_date.year))
        self.click_el(
            "//div[@class='datepicker-months']//span[text()='{}']".format(person.birth_date.strftime("%b")))
        self.click_el(
            "//div[@class='datepicker-days']//td[not(@class='new day') and not(@class='old day') and text()='{}']"
                .format(person.birth_date.day))

        # passport and number
        self.click_el("//select[@id='passportType']")
        self.click_el("//select[@id='passportType']/option[@value='01']")
        self.driver.find_element_by_id("passport_no").send_keys(person.passport)

        # issued
        self.click_el("//input[@id = 'pptIssueDate']")
        self.click_el(
            "//div[@class='datepicker-years']//span[not(contains(@class, 'disabled')) and text()='{}']".format(
                person.pasport_issued.year))
        self.click_el(
            "//div[@class='datepicker-months']//span[text()='{}']".format(
                person.pasport_issued.strftime("%b")))
        self.click_el(
            "//div[@class='datepicker-days']//td[not(@class='new day') and not(@class='old day') and text()='{}']".format(
                person.pasport_issued.day))

        # expired
        self.click_el("//input[@id = 'pptExpiryDate']")
        first_year = int(self.driver.find_element_by_xpath("//span[@class = 'year disabled']").text)
        years_back = (person.passport_expired.year - int(first_year)) // 10
        while years_back:
            years_back -= 1
            self.click_el("//div[@class = 'datepicker-years']//th[@class = 'next']")
        self.click_el(
            "//div[@class='datepicker-years']//span[not(contains(@class, 'disabled')) and text()='{}']".format(
                person.passport_expired.year))
        self.click_el(
            "//div[@class='datepicker-months']//span[text()='{}']".format(person.passport_expired.strftime("%b")))
        self.click_el(
            "//div[@class='datepicker-days']//td[not(@class='new day') and not(@class='old day') and text()='{}']".format(
                person.passport_expired.day))
        # nationality
        self.driver.find_element_by_id("pptIssuePalace").send_keys(person.nationality)

    def save_available_dates(self, available_dates):
        self.gs_dates_tab.update_acell("B1", "{}".format(available_dates))

    def register_people_for_dates(self, dates):
        for date in dates:
            filtered = self.gs.filter_visa_with_appropriate_date(json.dumps(self.gs_visa_tab.get_all_records()), date)
            if filtered:
                for p in filtered:
                    self.open_page("https://blsspain-belarus.com/book_appointment.php")
                    self.select_centre("Minsk", "Normal")
                    self.enter_phone_and_email(p["phone"], p["email"])
                    self.enter_wrong_code()
                    self.enter_code_from_email(p["email"])  # Иногда приходит письмо с security alert и не читается код
                    self.register_person_for_date(p, date)
                    reg_number = self.driver.find_element_by_xpath("//tbody/tr[4]/td[2]").text.split(" - ")[1]
                    print(reg_number)
                    self.gs.update_visa_item_by_id(self.gs_visa_tab, p["id"], "status", datetime.now())
                    self.gs.update_visa_item_by_id(self.gs_visa_tab, p["id"], "script_comment", reg_number)
            print("filtered for {} is {}".format(date, filtered))

    def register_person_for_date(self, p, date):
        person = Person(
            p["id"], p["type"], p["last_name"], p["first_name"], p["passport"], p["birth_date"],
            p["passport_issued"], p["passport_expired"], p["issued_by"], p["phone"], p["nationality"],
            p["travel_date"], p["start_date"], p["end_date"], p["family"], p["status"], p["script_comment"], p["email"])
        print("selected day:", date.day)
        self.fill_appintment_date(date)
        self.fill_other_fields(person)
        self.fill_captcha()
        self.submit_form()

    def open_new_tab(self, param):
        self.driver.execute_script("window.open('https://www.google.com/search?q={}');".format(param))
        print(self.driver.title)
