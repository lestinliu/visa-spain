import datetime
from selenium import webdriver
from random import randint
import time
from gmm import Email
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

TIMEOUT = 300

options = Options()
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(1)
driver.get("https://blsspain-belarus.com/book_appointment.php")

FIRST_NAME = "SEMCHANKA"
LAST_NAME = "VASILI"
PASSPORT_NUM = "MP4019821"
EMAIL = "alex23012019@gmail.com"
PHONE = "296903657"
DOB = "28/04/1977"
PASSPORT_ISSUE_DATE = "26/06/2017"
PASSPORT_EXPIRE_DATE = "26/06/2027"
NATIONALITY = "BELARUS"
DATE = "10"
TIME = "09:00 - 09:30"

# FIRST_NAME = "KAVALIUO"
# LAST_NAME = "ARTSIOM"
# PASSPORT_NUM = "HB3267358"
# EMAIL = "alex22012019@gmail.com"
# PHONE = "296903657"
# DOB = "4/9/1983"
# PASSPORT_ISSUE_DATE = "3/21/2019"
# PASSPORT_EXPIRE_DATE = "3/21/2029"
# NATIONALITY = "BELARUS"
# DATE = "2"
# TIME = "09:00 - 09:30"
#
# FIRST_NAME = "KAVALIOVA"
# LAST_NAME = "IRYNA"
# PASSPORT_NUM = "HB2922435"
# EMAIL = "alex22012019@gmail.com"
# PHONE = "﻿296903657"
# DOB = "10/17/1971"
# PASSPORT_ISSUE_DATE = "3/9/2016"
# PASSPORT_EXPIRE_DATE = "3/9/2026"
# NATIONALITY = "BELARUS"
# DATE = "2"
# TIME = "09:30 - 10:00"
#
# FIRST_NAME = "KAVALIOVA"
# LAST_NAME = "ALIAKSANDRA"
# PASSPORT_NUM = "HB2921250"
# EMAIL = "alex22012019@gmail.com"
# PHONE = "﻿296903657"
# DOB = "9/24/2009"
# PASSPORT_ISSUE_DATE = "3/2/2016"
# PASSPORT_EXPIRE_DATE = "3/2/2021"
# NATIONALITY = "BELARUS"
# DATE = "2"
# TIME = "10:00 - 10:30"
#
# FIRST_NAME = "KARYNCHUK"
# LAST_NAME = "SIARHEI"
# PASSPORT_NUM = "HB2424994"
# EMAIL = "alex22012019@gmail.com"
# PHONE = "﻿296903657"
# DOB = "5/20/1976"
# PASSPORT_ISSUE_DATE = "12/21/2011"
# PASSPORT_EXPIRE_DATE = "5/20/2021"
# NATIONALITY = "BELARUS"
# DATE = "2"
# TIME = "10:30 - 11:00"
#
# FIRST_NAME = "KRAUCHUK"
# LAST_NAME = "HALINA"
# PASSPORT_NUM = "HB2576777"
# EMAIL = "alex22012019@gmail.com"
# PHONE = "﻿296903657"
# DOB = "12/8/1979"
# PASSPORT_ISSUE_DATE = "3/21/2013"
# PASSPORT_EXPIRE_DATE = "3/21/2023"
# NATIONALITY = "BELARUS"
# DATE = "2"
# TIME = "11:00 - 11:30"
#
# FIRST_NAME = "KARYNCHUK"
# LAST_NAME = "ANDREI"
# PASSPORT_NUM = "HB30472499"
# EMAIL = "alex22012019@gmail.com"
# PHONE = "﻿296903657"
# DOB = "12/13/2008"
# PASSPORT_ISSUE_DATE = "5/5/2017"
# PASSPORT_EXPIRE_DATE = "5/5/2022"
# NATIONALITY = "BELARUS"
# DATE = "2"
# TIME = "11:30 - 12:00"
#
# FIRST_NAME = "LIAVITSKAYA"
# LAST_NAME = "TATSIANA"
# PASSPORT_NUM = "MC2521090"
# EMAIL = "alex22012019@gmail.com"
# PHONE = "﻿296903657"
# DOB = "7/6/1988"
# PASSPORT_ISSUE_DATE = "7/25/2013"
# PASSPORT_EXPIRE_DATE = "7/25/2023"
# NATIONALITY = "BELARUS"
# DATE = "2"
# TIME = "12:00 - 12:30"
#
# FIRST_NAME = "LEIKIN"
# LAST_NAME = "RAMAN"
# PASSPORT_NUM = "MP4264156"
# EMAIL = "alex22012019@gmail.com"
# PHONE = "﻿296903657"
# DOB = "4/10/2016"
# PASSPORT_ISSUE_DATE = "11/5/2018"
# PASSPORT_EXPIRE_DATE = "11/5/2023"
# NATIONALITY = "BELARUS"
# DATE = "2"
# TIME = "12:30 - 13:00"
#
# FIRST_NAME = "KHODOLEVA"
# LAST_NAME = "ELINA"
# PASSPORT_NUM = "BM2453912"
# EMAIL = "alex22012019@gmail.com"
# PHONE = "﻿296903657"
# DOB = "6/3/1992"
# PASSPORT_ISSUE_DATE = "6/9/2017"
# PASSPORT_EXPIRE_DATE = "6/9/2027"
# NATIONALITY = "BELARUS"
# DATE = "10"
# TIME = "9:00 - 9:30"
#
# FIRST_NAME = "STRUNEUSKI"
# LAST_NAME = "YAN"
# PASSPORT_NUM = "MP3995498"
# EMAIL = "alex22012019@gmail.com"
# PHONE = "﻿296903657"
# DOB = "5/7/1992"
# PASSPORT_ISSUE_DATE = "5/22/2017"
# PASSPORT_EXPIRE_DATE = "5/22/2027"
# NATIONALITY = "BELARUS"
# DATE = "10"
# TIME = "9:30 - 10:00"
#
# FIRST_NAME = "KARYNCHUK"
# LAST_NAME = "ANDREI"
# PASSPORT_NUM = "HB30472499"
# EMAIL = "alex22012019@gmail.com"
# PHONE = "﻿296903657"
# DOB = "12/13/2008"
# PASSPORT_ISSUE_DATE = "5/5/2017"
# PASSPORT_EXPIRE_DATE = "5/5/2022"
# NATIONALITY = "BELARUS"
# DATE = "10"
# TIME = "9:00 - 9:30"


# select centre
DOB_YEAR = DOB.year
DOB_MONTH = DOB.month
DOB_DAY = DOB.day

ISSUED_YEAR = PASSPORT_ISSUE_DATE.year
ISSUED_MONTH = PASSPORT_ISSUE_DATE.month
ISSUED_DAY = PASSPORT_ISSUE_DATE.day

EXPIRED_YEAR = PASSPORT_EXPIRE_DATE.year
EXPIRED_MONTH = PASSPORT_EXPIRE_DATE.month
EXPIRED_DAY = PASSPORT_EXPIRE_DATE.day


def click_el(element):
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()
    element.click()


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


# select centre
driver.execute_script("setCookie();")
click_el(driver.find_element_by_xpath("//select[@name='centre']"))
click_el(driver.find_element_by_xpath("//select[@name='centre']/option[text()='Minsk']"))
click_el(driver.find_element_by_xpath("//select[@name='category']"))
click_el(driver.find_element_by_xpath("//select[@name='category']/option[text()='Normal']"))

# enter phone
driver.find_element_by_id("phone").send_keys(PHONE)
driver.find_element_by_id("email").send_keys(EMAIL)

# enter wrong code
def enter_wrong_code():
    driver.find_element_by_id("otp").clear()
    driver.find_element_by_id("otp").send_keys(random_with_N_digits(4))
    click_el(driver.find_element_by_name("save"))
    driver.execute_script("sendOTP();")
    time.sleep(3)


# check mail
def get_code_from_email():
    mail = Email()
    code = mail.read_email(EMAIL, "Ab123456!")
    if code:
        return code
    else:
        print(datetime.datetime.now().time(), "no email")
        enter_wrong_code()
        time.sleep(TIMEOUT)
        get_code_from_email()

enter_wrong_code()

driver.find_element_by_id("otp").clear()
driver.find_element_by_id("otp").send_keys(get_code_from_email())
click_el(driver.find_element_by_name("save"))

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
click_el(driver.find_element_by_name("agree"))

# select slot

while True:
    click_el(driver.find_element_by_id("app_date"))
    dates = driver.find_elements_by_xpath(
        "//div[@class='datepicker-days']"
        "//td[not(@class='disabled')"
        " and not(@class='old disabled day disabled')"
        " and not(@class='old active day disabled fullcapspecial')"
        " and not(@class='old day disabled fullcapspecial')"
        " and not(@class='disabled day disabled')"
        " and not(@class='disabled day disabled')"
        " and not(@class='day disabled fullcapspecial')"
        " and not(@class='day disabled inactiveClass')"
        " and not(@class='new day disabled fullcapspecial')"
        " and not(@class='active day disabled fullcapspecial')"
        " and not(@class='disabled day disabled inactiveClass')"
        " and not(@class='active day disabled fullcap')"
        " and not(@class='day disabled fullcap')"
        " and not(@class='day disabled offday')"
        " and not(@class='new day disabled inactiveClass')"
        " and not(@class='new day disabled offday')"
        " and not(@class='new disabled day disabled')]")
    for i in dates:
        print(i.text, i.get_attribute("class"))
    # next month
    click_el(driver.find_element_by_xpath("//div[@class = 'datepicker-days']//th[@class = 'next']"))
    dates = driver.find_elements_by_xpath(
        "//div[@class='datepicker-days']"
        "//td[not(@class='disabled')"
        " and not(@class='old disabled day disabled')"
        " and not(@class='old active day disabled fullcapspecial')"
        " and not(@class='old day disabled fullcapspecial')"
        " and not(@class='disabled day disabled')"
        " and not(@class='disabled day disabled')"
        " and not(@class='day disabled fullcapspecial')"
        " and not(@class='day disabled inactiveClass')"
        " and not(@class='new day disabled fullcapspecial')"
        " and not(@class='active day disabled fullcapspecial')"
        " and not(@class='disabled day disabled inactiveClass')"
        " and not(@class='active day disabled fullcap')"
        " and not(@class='day disabled fullcap')"
        " and not(@class='day disabled offday')"
        " and not(@class='new day disabled inactiveClass')"
        " and not(@class='new day disabled offday')"
        " and not(@class='new disabled day disabled')]")
    for i in dates:
        print(i.text, i.get_attribute("class"))
    print(datetime.datetime.now().time())
    time.sleep(TIMEOUT)
    driver.refresh()

click_el(driver.find_element_by_id("app_date"))
click_el(driver.find_element_by_xpath("//td[contains(@class,'fullcapspecial')]"))
click_el(driver.find_element_by_id("premiumService"))

click_el(driver.find_element_by_id("app_date"))
click_el(driver.find_element_by_xpath("//td[contains(@class, 'day activeClass') and text() = '{}']".format(DATE)))

click_el(driver.find_element_by_xpath("//select[@name='app_time']"))
click_el(driver.find_element_by_xpath("//select[@name='app_time']/option[text()='{}']".format(TIME)))

# Дата поездки
click_el(driver.find_element_by_id("travelDate"))
click_el(driver.find_element_by_xpath(
    "//div[@class='datepicker-days']//td[(@class='day' or @class='active day') and text()='24']"))

click_el(driver.find_element_by_xpath("//select[@id='VisaTypeId']"))
click_el(driver.find_element_by_xpath("//select[@id='VisaTypeId']/option[text()='Tourism']"))

driver.find_element_by_id("first_name").send_keys(FIRST_NAME)
driver.find_element_by_id("last_name").send_keys(LAST_NAME)

years_back = (2019 - int(DOB_YEAR)) // 10
while years_back:
    years_back -= 1
    click_el(driver.find_element_by_xpath("//div[@class = 'datepicker-years']//th[@class = 'prev']"))
click_el(driver.find_element_by_id("dateOfBirth"))

click_el(driver.find_element_by_xpath(
    "//div[@class='datepicker-years']//span[not(contains(@class, 'disabled')) and text()='{}']".format(DOB_YEAR)))
click_el(driver.find_element_by_xpath(
    "//div[@class='datepicker-months']//span[text()='{}']".format(DOB_MONTH)))
click_el(driver.find_element_by_xpath(
    "//div[@class='datepicker-days']//td[not(@class='new day') and not(@class='old day') and text()='{}']".format(
        DOB_DAY)))

click_el(driver.find_element_by_xpath("//select[@id='passportType']"))
click_el(driver.find_element_by_xpath("//select[@id='passportType']/option[@value='01']"))

driver.find_element_by_id("passport_no").send_keys(PASSPORT_NUM)

click_el(driver.find_element_by_id("pptIssueDate"))
click_el(driver.find_element_by_xpath(
    "//div[@class='datepicker-years']//span[not(contains(@class, 'disabled')) and text()='{}']".format(ISSUED_YEAR)))
click_el(driver.find_element_by_xpath(
    "//div[@class='datepicker-months']//span[text()='{}']".format(ISSUED_MONTH)))
click_el(driver.find_element_by_xpath(
    "//div[@class='datepicker-days']//td[not(@class='new day') and not(@class='old day') and text()='{}']".format(
        ISSUED_DAY)))

click_el(driver.find_element_by_id("pptExpiryDate"))
click_el(driver.find_element_by_xpath(
    "//div[@class='datepicker-years']//span[not(contains(@class, 'disabled')) and text()='{}']".format(EXPIRED_YEAR)))
click_el(driver.find_element_by_xpath(
    "//div[@class='datepicker-months']//span[text()='{}']".format(EXPIRED_MONTH)))
click_el(driver.find_element_by_xpath(
    "//div[@class='datepicker-days']//td[not(@class='new day') and not(@class='old day') and text()='{}']".format(
        EXPIRED_DAY)))

driver.find_element_by_id("pptIssuePalace").send_keys(NATIONALITY)
# click_el(driver.find_element_by_id("courierId"))  # courier
# click_el(driver.find_element_by_id("vasId12"))  # sms
# click_el(driver.find_element_by_id("vasId6"))  # form filling
# click_el(driver.find_element_by_id("vasId5"))  # photo
# click_el(driver.find_element_by_id("vasId2"))  # prime time
time.sleep(10)
driver.find_element_by_id("captcha").send_keys("12345")  # prime time

# click_el(driver.find_element_by_xpath("//input[@name='save']"))
#
# alert = driver.switch_to.alert
# alert.accept()
#
# reg_no = driver.find_element_by_xpath("//td[contains(text(), 'Регистрационный номер')]").text
# print(reg_no)
# info = driver.find_element_by_xpath("//img[@class = 'barcode']/../..").text
# print(info)
#
# click_el(driver.find_element_by_xpath("//div[text()='EMAIL']"))
#
# alert = driver.switch_to.alert
# alert.accept()
