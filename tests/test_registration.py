from pytest import mark
from selenium.webdriver.common.by import By
import config


# RT-12 / RT-13
def test_open_page_reg(browser):
    browser.find_element(By.ID, 'kc-register').click()
    assert browser.find_element(By.XPATH, '//h1[@class="card-container__title"]').text == 'Регистрация'


# RT-14 / RT-15
@mark.xfail(reason='Аккаунт уже существует')
@mark.parametrize('value', [config.MAIL, config.LOGIN])
def test_registration(value, browser):
    browser.find_element(By.ID, 'kc-register').click()
    inputs = browser.find_elements(By.XPATH, '//input[contains(@class, "rt-input__input")]')
    inputs[0].send_keys('Елена')
    inputs[1].send_keys('Рыбочкина')
    inputs[2].send_keys('Москва')
    inputs[3].send_keys(value)
    inputs[4].send_keys(config.PASSWORD)
    inputs[5].send_keys(config.PASSWORD)

    browser.find_element(By.NAME, 'register').click()

    assert browser.find_element(By.XPATH, '//h1[@class="card-container__title"]').text == 'Подтверждение email'


# RT-20 / RT-21 / RT-22 / RT-23 / RT-24 / RT-25
# @mark.xfail(reason='Captcha')
@mark.parametrize(
    ('first_name', 'last_name', 'region', 'login', 'password', 'password_2'),
    [
        ('FCG123', 'Рыбочкина', 'Москва', '78005553535', 'Qwerty12345!', 'Qwerty12345!'),
        ('Елена', 'FCG123', 'Москва', '78005553531', 'Qwerty12345!', 'Qwerty12345!'),
        ('Елена', 'Рыбочкина', 'Москва', '711', 'Qwerty12345!', 'Qwerty12345!'),
        ('Елена', 'Рыбочкина', 'Москва', 'fff@f.f', 'Qwerty12345!', 'Qwerty12345!'),
        ('Елена', 'Рыбочкина', 'Москва', '78005553532', 'Qwerty12345!', 'Qwerty12345!'),
        ('Елена', 'Рыбочкина', 'Москва', '78005553535', 'Qwerty12345!', 'cdg!'),
    ]
)
def test_registration_error(first_name, last_name, region, login, password, password_2, browser):
    browser.find_element(By.ID, 'kc-register').click()
    inputs = browser.find_elements(By.XPATH, '//input[contains(@class, "rt-input__input")]')
    inputs[0].send_keys(first_name)
    inputs[1].send_keys(last_name)
    inputs[2].send_keys(region)
    inputs[3].send_keys(login)
    inputs[4].send_keys(password)
    inputs[5].send_keys(password_2)

    browser.find_element(By.NAME, 'register').click()

    assert browser.find_element(By.XPATH, '//h1[@class="rt-input-container__meta--error"]').text != ''
