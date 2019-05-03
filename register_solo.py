import datetime
from selenium import webdriver
from random import randint
import time
from gmm import Email
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

TIMEOUT = 300
EMAIL = "alex23012019@gmail.com"
PHONE = "296903657"

people = {1: [
    {"LAST_NAME": "LIAVITSKAYA",
     "FIRST_NAME": "TATSIANA",
     "PASSPORT_NUM": "MC2521090",
     "DOB": "7/6/1988",
     "PASSPORT_ISSUE_DATE": "7/25/2013",
     "PASSPORT_EXPIRE_DATE": "7/25/2023",
     "NATIONALITY": "BELARUS",
     "TRAVEL_DATE": "5/15/2019",
     "DATE_FROM": "25/4/2019",
     "DATE_TO": "30/5/2019"},
    {"LAST_NAME": "LEIKIN",
     "FIRST_NAME": "RAMAN",
     "PASSPORT_NUM": "MP4264156",
     "DOB": "4/10/2016",
     "PASSPORT_ISSUE_DATE": "11/5/2018",
     "PASSPORT_EXPIRE_DATE": "11/5/2023",
     "NATIONALITY": "BELARUS",
     "TRAVEL_DATE": "5/15/2019",
     "DATE_FROM": "25/4/2019",
     "DATE_TO": "30/4/2019"}]
}

person = people[1][0]

FIRST_NAME = person["FIRST_NAME"]
LAST_NAME = person["LAST_NAME"]
PASSPORT_NUM = person["PASSPORT_NUM"]
DOB = person["DOB"]
PASSPORT_ISSUE_DATE = person["PASSPORT_ISSUE_DATE"]
PASSPORT_EXPIRE_DATE = person["PASSPORT_EXPIRE_DATE"]
NATIONALITY = person["NATIONALITY"]
TRAVEL_DATE = person["TRAVEL_DATE"]
DATE_FROM = person["DATE_FROM"]
DATE_TO = person["DATE_TO"]

# select centre
DOB_YEAR = int(DOB.split("/")[0])
DOB_MONTH = int(DOB.split("/")[1])
DOB_DAY = int(DOB.split("/")[2])

ISSUED_YEAR = int(PASSPORT_ISSUE_DATE.split("/")[0])
ISSUED_MONTH = int(PASSPORT_ISSUE_DATE.split("/")[1])
ISSUED_DAY = int(PASSPORT_ISSUE_DATE.split("/")[2])

EXPIRED_YEAR = int(PASSPORT_EXPIRE_DATE.split("/")[0])
EXPIRED_MONTH = int(PASSPORT_EXPIRE_DATE.split("/")[1])
EXPIRED_DAY = int(PASSPORT_EXPIRE_DATE.split("/")[2])

TRAVEL_YEAR = int(TRAVEL_DATE.split("/")[0])
TRAVEL_MONTH = int(TRAVEL_DATE.split("/")[1])
TRAVEL_DAY = int(TRAVEL_DATE.split("/")[2])

DATE_FROM_YEAR = int(DATE_FROM.split("/")[0])
DATE_FROM_MONTH = int(DATE_FROM.split("/")[1])
DATE_FROM_DAY = int(DATE_FROM.split("/")[2])

DATE_TO_YEAR = int(DATE_TO.split("/")[0])
DATE_TO_MONTH = int(DATE_TO.split("/")[1])
DATE_TO_DAY = int(DATE_TO.split("/")[2])

options = Options()
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(1)


def click_el(element):
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()
    element.click()


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def open_page(page):
    driver.get(page)


def select_centre(city, category):
    driver.execute_script("setCookie();")
    click_el(driver.find_element_by_xpath("//select[@name='centre']"))
    click_el(driver.find_element_by_xpath("//select[@name='centre']/option[text()='{}']".format(city)))
    click_el(driver.find_element_by_xpath("//select[@name='category']"))
    click_el(driver.find_element_by_xpath("//select[@name='category']/option[text()='{}']".format(category)))


def enter_phone_and_email(phone, email):
    # enter phone
    driver.find_element_by_id("phone").send_keys(phone)
    driver.find_element_by_id("email").send_keys(email)


def enter_wrong_code():
    driver.find_element_by_id("otp").clear()
    driver.find_element_by_id("otp").send_keys(random_with_N_digits(4))
    click_el(driver.find_element_by_name("save"))
    driver.execute_script("sendOTP();")
    time.sleep(3)


# check mail
def get_code_from_email():
    time.sleep(3)
    mail = Email()
    code = mail.read_email(EMAIL, "Ab123456!")
    if code:
        return code
    else:
        print(datetime.datetime.now().time(), "no email")
        enter_wrong_code()
        time.sleep(TIMEOUT)
        get_code_from_email()


def enter_code_from_email():
    driver.find_element_by_id("otp").clear()
    driver.find_element_by_id("otp").send_keys(get_code_from_email())
    click_el(driver.find_element_by_name("save"))

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    click_el(driver.find_element_by_name("agree"))


def get_available_days(month):
    result_dates = {}
    map = ["January 2019", "February 2019", "March 2019", "April 2019", "May 2019", "June 2019",
           "July 2019", "August 2019", "September 2019", "October 2019", "November 2019", "December 2019"]
    month_el = driver.find_element_by_xpath("//div[@class='datepicker-days']//th[@class='datepicker-switch']")
    click_times = map.index(month) - map.index(month_el.text)
    print("click_times: ", click_times)
    if click_times > 0:
        for _ in range(click_times):
            click_el(driver.find_element_by_xpath("//div[@class = 'datepicker-days']//th[@class = 'next']"))

    dates = driver.find_elements_by_xpath("//div[@class='datepicker-days']//td[contains(@class, ' activeClass')]")
    if len(dates):
        print("month_el: ", month_el.text)
        for date in dates:
            result_dates[date.text] = {}
    return [map.index(month_el.text) + 1, result_dates]


def get_available_time(day):
    click_el(driver.find_element_by_id("app_date"))
    time.sleep(2)
    click_el(driver.find_element_by_xpath(
        "//div[@class='datepicker-days']//td[contains(@class, ' activeClass') and text() = '{}']".format(day)))
    times = driver.find_elements_by_xpath("//select[@id='app_time']/option")
    available_time = []
    for i in times:
        available_time.append(i.text)
    available_time.pop(0)
    return available_time


def check_available_dates(*args):
    click_el(driver.find_element_by_id("app_date"))
    dates = {}
    for mon in args:
        days = get_available_days(mon)
        if days[1]:
            dates[str(days[0])] = days[1]
    if bool(dates):
        return dates
    else:
        time.sleep(10)
        driver.refresh()
        check_available_dates(*args)



def check_available_times(available_dates):
    available_times = available_dates
    for month in available_dates.keys():
        print("month: ", month)
        for day in available_dates[month]:
            print("day:", day)
            print("get_available_time:", get_available_time(day))
            print("available_times: ", available_times)
            print("available_times[month]", available_times[month])
            print("available_times[month]", available_times[month])
            available_times[month][day] = get_available_time(day)
    print("available_times", available_times)
    return available_times


def select_date_for_person(available_times):
    for month in available_times.keys():
        if DATE_FROM_MONTH <= month <= DATE_TO_MONTH:
            for day in available_times[month]:
                if DATE_FROM_DAY <= day <= DATE_TO_DAY:
                    select_appointment_date_and_time(month, day)
                    break


def select_appointment_date_and_time(month, day):
    click_el(driver.find_element_by_id("app_date"))
    map = ["January 2019", "February 2019", "March 2019", "April 2019", "May 2019", "June 2019",
           "July 2019", "August 2019", "September 2019", "October 2019", "November 2019", "December 2019"]
    get_available_days(map[month - 1])
    click_el(driver.find_element_by_xpath(
        "//div[@class='datepicker-days']//td[contains(@class, ' activeClass') and text() = '{}']".format(day)))
    click_el(driver.find_element_by_xpath("(//select[@id='app_time']/option)[2]"))


def fill_travel_date(day, month, year):
    click_el(driver.find_element_by_id("travelDate"))
    select_date(day, month, year)


def select_date(day, month, year):
    years_back = (2019 - int(year)) // 10
    while years_back:
        years_back -= 1
        click_el(driver.find_element_by_xpath("//div[@class = 'datepicker-years']//th[@class = 'prev']"))
    click_el(driver.find_element_by_id("dateOfBirth"))

    click_el(driver.find_element_by_xpath(
        "//div[@class='datepicker-years']//span[not(contains(@class, 'disabled')) and text()='{}']".format(year)))
    click_el(driver.find_element_by_xpath(
        "//div[@class='datepicker-months']//span[text()='{}']".format(month)))
    click_el(driver.find_element_by_xpath(
        "//div[@class='datepicker-days']//td[not(@class='new day') and not(@class='old day') and text()='{}']".format(
            day)))


def fill_other_fields():
    # visa type
    click_el(driver.find_element_by_xpath("//select[@id='VisaTypeId']"))
    click_el(driver.find_element_by_xpath("//select[@id='VisaTypeId']/option[text()='Tourism']"))

    # first and last name
    driver.find_element_by_id("first_name").send_keys(FIRST_NAME)
    driver.find_element_by_id("last_name").send_keys(LAST_NAME)

    # dob
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

    # passport and number
    click_el(driver.find_element_by_xpath("//select[@id='passportType']"))
    click_el(driver.find_element_by_xpath("//select[@id='passportType']/option[@value='01']"))
    driver.find_element_by_id("passport_no").send_keys(PASSPORT_NUM)

    # issued
    click_el(driver.find_element_by_id("pptIssueDate"))
    click_el(driver.find_element_by_xpath(
        "//div[@class='datepicker-years']//span[not(contains(@class, 'disabled')) and text()='{}']".format(
            ISSUED_YEAR)))
    click_el(driver.find_element_by_xpath(
        "//div[@class='datepicker-months']//span[text()='{}']".format(ISSUED_MONTH)))
    click_el(driver.find_element_by_xpath(
        "//div[@class='datepicker-days']//td[not(@class='new day') and not(@class='old day') and text()='{}']".format(
            ISSUED_DAY)))

    # expired
    click_el(driver.find_element_by_id("pptExpiryDate"))
    click_el(driver.find_element_by_xpath(
        "//div[@class='datepicker-years']//span[not(contains(@class, 'disabled')) and text()='{}']".format(
            EXPIRED_YEAR)))
    click_el(driver.find_element_by_xpath(
        "//div[@class='datepicker-months']//span[text()='{}']".format(EXPIRED_MONTH)))
    click_el(driver.find_element_by_xpath(
        "//div[@class='datepicker-days']//td[not(@class='new day') and not(@class='old day') and text()='{}']".format(
            EXPIRED_DAY)))

    # nationality
    driver.find_element_by_id("pptIssuePalace").send_keys(NATIONALITY)


# Given open page
open_page("https://blsspain-belarus.com/book_appointment.php")

# When select centre "Minsk"
# And select category "Normal"
select_centre("Minsk", "Normal")

# And enter phone number "256062209"
# And enter email "sash.kardash@gmail.com"
enter_phone_and_email(PHONE, EMAIL)

# And enter random code
# And click "request code" button
enter_wrong_code()

# And enter code from email
# And click "continue" button
# And click "accept" button
enter_code_from_email()

# And click on date field
# And get available dates and times
# And select date and time for person
# And select travel date "22/11/2019"

# select_date_for_person(check_available_times(check_available_dates("May 2019")))
click_el(driver.find_element_by_id("app_date"))
click_el(driver.find_element_by_xpath("//td[contains(@class,'fullcapspecial')]"))
click_el(driver.find_element_by_id("premiumService"))
time.sleep(2)

select_date_for_person({5:{23:"09:00 - 09:30"}})


fill_travel_date(TRAVEL_DAY, TRAVEL_MONTH, TRAVEL_YEAR)
# And select visa type "Tourism"
# And enter first name "Alexandr"
# And enter last name "Kardash"
# And select birthday "22/11/2019"
# And enter pasport number "AB123456"
# And select issued date "22/11/2019"
# And select expired date "22/11/2019"
# And enter issued city "Ивацевичи"
fill_other_fields()

# And enter captcha
# And click "submit" button
