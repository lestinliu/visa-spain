import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from utils.basic import Basic
from utils.google_sheet import GoogleSheets

options = Options()
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(20)

class Activate(Basic):
    gs = GoogleSheets()

    def login_to_gmail(self):
        visa = self.gs.open_sheet(self.gs.authorize(), "Visa Spain", "accounts").get_all_records()
        for user in visa:
            self.driver.get("https://gmail.com")
            self.enter_message(user["email"], id="identifierId")
            self.click_el(xpath="//span[text() = 'Next']")
            self.enter_message(user["password"], name="password")
            self.click_el(xpath="//span[text() = 'Next']")
            self.click_el(xpath="//span[text() = 'Done']")
            self.click_el(name="welcome_dialog_next")
            self.click_el(name="ok")
            self.click_el(xpath="//div[@aria-label = 'Settings']")
            self.click_el(xpath="//div[text() = 'Settings']")


    def activate_settings(self):
        self.driver.get("https://myaccount.google.com/")

    def activate_account(self):
        self.driver.get("https://myaccount.google.com/")

gmail = Activate(driver)
gmail.login_to_gmail()
