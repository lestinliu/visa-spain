import time
from datetime import datetime
from random import randint

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Basic:
    def __init__(self, driver):
        self.driver = driver

    def gdfs(self, str_date):  # get date from string
        return datetime.strptime(str_date, '%d/%m/%Y').date()

    def random_with_n_digits(self, n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

    def diff_month(self, d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month

    def click_el(self, xpath=None, id=None, name=None, text=None):
        locator = None
        if xpath:
            locator = (By.XPATH, xpath)
        elif id:
            locator = (By.ID, id)
        elif name:
            locator = (By.NAME, name)
        else:
            locator = (By.XPATH, "//*[contains(text(), '{}')]".format(text))
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(locator), message="No element").click()

    def wait_for_loading(self):
        WebDriverWait(self.driver, 10).until(ec.invisibility_of_element_located((By.ID, "overlay")))

    def enter_message(self, message, xpath=None, id=None, name=None, text=None):
        if xpath:
            locator = (By.XPATH, xpath)
        elif id:
            locator = (By.ID, id)
        elif name:
            locator = (By.NAME, name)
        else:
            locator = (By.XPATH, "//*[contains(text(), '{}')]".format(text))
        element = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(locator),
                                                       message="No element {}".format(locator))
        element.clear()
        element.send_keys(message)
