from selenium import webdriver
import pytest
from config import BASE_URL


@pytest.fixture()
def browser():
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    browser.get(BASE_URL)
    yield browser

    browser.quit()
