import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

options = Options()
# options.add_argument('--incognito')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(20)

json = (
    "yalova.veronika@gmail.com",
    "geletei.renata@gmail.com",
    "komarova.gera@gmail.com",
    "ponomareva.taisiya@gmail.com",
    "rymar.inga@gmail.com",
    "galkina.sofya@gmail.com",
    "semochko.ekaterina@gmail.com",
    "gorbunova.ulyana@gmail.com",
    "vinogradova.zinaida@gmail.com",
    "andrukhovich.inessa@gmail.com",
    "yalova.florentina@gmail.com",
    "zimina.pelageya@gmail.com",
    "shumeiko.elena@gmail.com",
    "lanova.faina@gmail.com",
    "vishnyakova.zhanna@gmail.com",
    "borodai.evgeniya@gmail.com",
    "zykova.praskovya@gmail.com",
    "terenteva.yanita@gmail.com",
    "bondarenko.inna@gmail.com",
    "kiseleva.anzhelika@gmail.com",
    "prokhorova.veronika@gmail.com",
    "yalova.inga@gmail.com",
    "plaksii.gayane@gmail.com",
    "evseeva.klara@gmail.com",
    "selezneva.kristina@gmail.com",
    "shestakova.yana@gmail.com",
    "turova.regina@gmail.com",
    "khizhnyak.oktyabrina@gmail.com",
    "efremova.zhanna@gmail.com",
    "lebedeva.elvira@gmail.com",
    "knyazeva.zinaida@gmail.com",
    "tikhonova.erika@gmail.com",
    "korovyak.unona@gmail.com",
    "silina.raisa@gmail.com",
    "eliseeva.praskovya@gmail.com",
    "kulishenko.anzhelika@gmail.com",
    "mazailo.klara@gmail.com",
    "koroleva.alena@gmail.com",
    "chikolba.lidiya@gmail.com",
    "sokolova.unona@gmail.com",
    "serduk.dominika@gmail.com",
    "povalii.borislava@gmail.com",
    "filatova.marina@gmail.com",
    "shevchenko.sofiya@gmail.com",
    "temchenko.anastasiya@gmail.com",
    "stegailo.zlata@gmail.com",
    "evseeva.svetlana@gmail.com",
    "melnikova.zhanna@gmail.com",
    "agafonova.guzel@gmail.com",
    "dmitrieva.una@gmail.com",
    "trofimova.praskovya@gmail.com",
    "yalova.lusya@gmail.com",
    "bogdanova.zlata@gmail.com",
    "nikolaeva.nina@gmail.com",
    "savina.kharitina@gmail.com",
    "savina.polina@gmail.com",
    "kapustina.inna@gmail.com",
    "popova.emma@gmail.com",
    "maslova.zhanna@gmail.com",
    "trublaevska.raisa@gmail.com",
    "petrova.dominika@gmail.com",
    "kaskiv.sofiya@gmail.com",
    "mikhailova.dominika@gmail.com",
    "kolesnik.malvina@gmail.com",
    "pakhomova.ellada@gmail.com",
    "zimina.alena@gmail.com",
    "blokhina.klara@gmail.com",
    "kabanova.nina@gmail.com",
    "bespalova.uzefa@gmail.com",
    "strelkova.ludmila@gmail.com",
    "kulagina.lada@gmail.com",
    "sitnikova.khristina@gmail.com",
    "pakhomova.sofiya@gmail.com",
    "borodai.sofiya@gmail.com",
    "ryabkina.natalya@gmail.com",
    "medvedeva.inga@gmail.com",
    "krylova.zlata@gmail.com",
    "plaksii.zhanna@gmail.com",
    "borisenko.klara@gmail.com",
    "efremova.yaroslava@gmail.com",
    "kotova.tatyana@gmail.com",
    "fedunkiv.zoya@gmail.com",
    "andruseiko.kristina@gmail.com",
    "ryabova.zhanna@gmail.com",
    "shcherbak.izolda@gmail.com",
    "borodai.emiliya@gmail.com",
    "evseeva.yana@gmail.com",
    "afanaseva.khristina@gmail.com",
    "vlasova.dina@gmail.com",
    "avdeeva.praskovya@gmail.com",
    "bragina.nonna@gmail.com",
    "vorobeva.dominika@gmail.com",
    "yakusheva.margarita@gmail.com",
    "lobanova.florentina@gmail.com",
    "sorokina.khristina@gmail.com",
    "terenteva.ustinya@gmail.com",
    "miklashevska.svetlana@gmail.com",
    "yakusheva.kapitolina@gmail.com",
    "guseva.ustinya@gmail.com",
    "filippova.yadviga@gmail.com",
    "blokhin.nazar@gmail.com",
    "tkachenko.sergei@gmail.com",
    "petriv.zenon@gmail.com",
    "kalinin.bogdan@gmail.com",
    "zinovev.filipp@gmail.com",
    "karpenko-karyi.denis@gmail.com",
    "isakov.feliks@gmail.com",
    "bogdanov.nikolai@gmail.com",
    "polyakov.valeryan@gmail.com",
    "frolov.valeryan@gmail.com",
    "pilipeiko.vlad@gmail.com",
    "trublaevskii.dinar@gmail.com",
    "sazonov.tit@gmail.com",
    "kotov.maksim@gmail.com",
    "chumak.elisei@gmail.com",
    "karpov.fedor@gmail.com",
    "dyachkov.nikita@gmail.com",
    "teterin.efim@gmail.com",
    "romanov.ulyan@gmail.com",
    "korneichuk.arsenii@gmail.com",
    "larionov.timofei@gmail.com",
    "mnogogreshnyi.gerasim@gmail.com",
    "romanenko.milan@gmail.com",
    "maslovskii.matvei@gmail.com",
    "petukhov.filipp@gmail.com",
    "shubin.ustin@gmail.com",
    "shkraba.zhiger@gmail.com",
    "kulagin.trofim@gmail.com",
    "rymar.pavel@gmail.com",
    "kalashnikov.gordei@gmail.com",
    "gusev.trofim@gmail.com",
    "nesterov.platon@gmail.com",
    "belov.ludvig@gmail.com",
    "pasichnik.vikentii@gmail.com",
    "pestov.bogdan@gmail.com",
    "nikonov.gordei@gmail.com",
    "gorodetskii.ignatii@gmail.com",
    "shcherbak.zurab@gmail.com",
    "likhachev.yaromir@gmail.com",
    "pasichnik.miroslav@gmail.com",
    "pavlov.karim@gmail.com",
    "arkhipov.roman@gmail.com",
    "ivashchenko.georgii@gmail.com",
    "myasnikov.rostislav@gmail.com",
    "burov.petr@gmail.com",
    "likhachev.platon@gmail.com",
    "pogomii.timofei@gmail.com",
    "medvedev.rafail@gmail.com",
    "anisimov.arkadii@gmail.com",
    "gorobchuk.nazar@gmail.com",
    "makarov.erik@gmail.com",
    "lytkin.khariton@gmail.com",
    "shufrich.yakov@gmail.com",
    "andreiko.vsevolod@gmail.com",
    "isaev.andrei@gmail.com",
    "negoda.semen@gmail.com",
    "timofeev.ustin@gmail.com",
    "moiseev.bronislav@gmail.com",
    "kabanov.stanislav@gmail.com",
    "kozlov.svyatoslav@gmail.com",
    "shufrich.marat@gmail.com",
    "fadeev.savva@gmail.com",
    "zimin.marat@gmail.com",
    "navalnyi.ilya@gmail.com",
    "orekhov.bronislav@gmail.com",
    "komarov.ostin@gmail.com",
    "gorbachev.orlando@gmail.com",
    "sidorov.dmitrii@gmail.com",
    "gaichuk.rafail@gmail.com",
    "dzuba.lukillyan@gmail.com",
    "andreev.feliks@gmail.com",
    "dzuba.boris@gmail.com",
    "savelev.lenar@gmail.com",
    "vygovskii.maksim@gmail.com",
    "uvarov.khariton@gmail.com",
    "tyagai.leonid@gmail.com",
    "khokhlov.lev@gmail.com",
    "efremov.ostin@gmail.com",
    "popov.kuzma@gmail.com",
    "odintsov.leopold@gmail.com",
    "nekrasov.feliks@gmail.com",
    "gusev.kim@gmail.com",
    "fedotov.matvei@gmail.com",
    "frolov.eduard@gmail.com",
    "fedunkiv.filipp@gmail.com",
    "samsonov.tit@gmail.com",
    "tsvetkov.miroslav@gmail.com",
    "vasilev.dominik@gmail.com",
    "predybailo.ulii@gmail.com",
    "samoilov.bronislav@gmail.com",
    "bogdanov.filipp@gmail.com",
    "vygovskii.gennadii@gmail.com",
    "mikhailov.prokhor@gmail.com",
    "mishin.david@gmail.com",
    "lytkin.spartak@gmail.com",
    "filatov.mark@gmail.com",
    "gordeev.petr@gmail.com",
    "solovev.eduard@gmail.com",
    "kondratev.lubomir@gmail.com",
    "kondratiev.valery@gmail.com"
)


def click_el(xpath=None, id=None, name=None, text=None):
    locator = None
    if xpath:
        locator = (By.XPATH, xpath)
    elif id:
        locator = (By.ID, id)
    elif name:
        locator = (By.NAME, name)
    else:
        locator = (By.XPATH, "//*[contains(text(), '{}')]".format(text))
    WebDriverWait(driver, 10).until(ec.element_to_be_clickable(locator), message="No element").click()
    time.sleep(1)


def enter_message(message, xpath=None, id=None, name=None, text=None):
    if xpath:
        locator = (By.XPATH, xpath)
    elif id:
        locator = (By.ID, id)
    elif name:
        locator = (By.NAME, name)
    else:
        locator = (By.XPATH, "//*[contains(text(), '{}')]".format(text))
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator), message="No element {}".format(locator)).send_keys(message)
    time.sleep(1)


driver.get("https://www.google.com/gmail/")
time.sleep(3)
click_el(xpath="//span[text() = 'Create account']")
click_el(xpath="//content[@aria-label = 'For myself']")
enter_message("Alex", name="firstName")
enter_message("Kardash", name="lastName")
enter_message("Alex.Kardash", id="username")
click_el(id="passwd")
enter_message("Ab123456!", name="Passwd")
click_el(id="confirm-passwd")
enter_message("Ab123456!", name="ConfirmPasswd")
click_el(text="Next")
click_el(xpath="(//ul[@id='usernameList']//button)[1]")
click_el(text="Next")
