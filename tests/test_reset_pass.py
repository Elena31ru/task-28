from pytest import mark
from selenium.webdriver.common.by import By
import config


# RT-7
def test_open_page_reset(browser):
    auth = browser.find_element(By.CLASS_NAME, 'card-container__title')
    assert auth.text == 'Восстановление пароля'


# RT-8 / RT-9 / RT-10 / RT-11
@mark.xfail(reason='Captcha')
@mark.parametrize(
    ('value', 'tab'),
    [
        (config.MAIL, 't-btn-tab-mail'),
        (config.LOGIN, 't-btn-tab-login'),
        (config.PHONE, 't-btn-tab-phone'),
    ]
)
def test_reset_password_by_mail(value, tab, browser):
    browser.find_element(By.ID, 'forgot_password').click()
    browser.find_element(By.ID, tab).click()
    browser.find_element(By.ID, 'username').send_keys(config.MAIL)

    browser.find_element(By.ID, 'captcha').send_keys()
    browser.find_element(By.ID, 'reset')

    assert browser.find_element(By.XPATH, '//h1[@class="card-container__title"]').text == 'Восстановление пароля'


