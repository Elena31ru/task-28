from pytest import mark
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config


# RT-1
def test_open_page_auth(browser):
    auth = browser.find_element(By.CLASS_NAME, 'card-container__title')
    assert auth.text == 'Авторизация'


# RT-2
@mark.parametrize(
    ('value', 'label'),
    [
        (config.MAIL, 'Почта'),
        (config.LOGIN, 'Логин'),
    ]
)
def test_change_tab_on_mail(value, label, browser):
    browser.find_element(By.ID, 'username').send_keys(value)
    browser.find_element(By.ID, 'password').click()
    assert browser.find_element(By.XPATH, '//div[contains(@class, "rt-tab--active")]').text == label


# RT-3 / RT-4 / RT-5 / RT-6
@mark.parametrize('value', [config.MAIL, config.LOGIN, config.PHONE])
def test_auth_mail(value, browser):
    browser.find_element(By.ID, 'username').send_keys(value)
    browser.find_element(By.ID, 'password').send_keys(config.PASSWORD)
    browser.find_element(By.ID, 'kc-login').click()
    assert '/account_b2c/page' in browser.current_url


# RT-16 / RT-17 / RT-18 / RT-19
@mark.xfail(reason='Captcha')
@mark.parametrize(
    ('login', 'password'),
    [
        ('71231112312', 'Qwer---1234215'),
        (config.MAIL, 'Qwer---1234215'),
        ('', 'Qwerty12345'),
        ('11111111111', 'Qwerty12345'),
    ]
)
def test_auth_error(login, password, browser):
    inputs = browser.find_elements(By.XPATH, '//input[contains(@class, "rt-input__input")]')
    inputs[0].send_keys(login)
    inputs[1].send_keys(password)
    browser.find_element(By.ID, 'kc-login').click()
    err = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'form-error-message')))
    assert err.text == 'Неверный логин или пароль'
