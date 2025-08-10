import allure
import logging

import allure
import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

logger = logging.getLogger("test_logger")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def pytest_addoption(parser):
    parser.addoption("--browser", help="Browser to run tests", default="chrome")
    parser.addoption("--headless", action="store_true", help="Activate headless mode")
    parser.addoption(
        "--drivers", help="Drivers storage", default="/home/mikhail/Downloads/drivers"
    )
    parser.addoption(
        "--base_url", help="Base application url", default="192.168.144.128:8081"
    )


@pytest.fixture(scope="session")
def base_url(request):
    raw_url = request.config.getoption("--base_url")
    return raw_url if raw_url.startswith("http") else "http://" + raw_url


@pytest.fixture()
def browser(request):
    driver = None
    browser_name = request.config.getoption("--browser")
    browser_name = browser_name.lower() if browser_name else "chrome"

    drivers_storage = request.config.getoption("--drivers")
    headless = request.config.getoption("--headless")

    if browser_name in ["ch", "chrome"]:
        options = ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if headless:
            options.add_argument("headless=new")
        driver = webdriver.Chrome(options=options)

    elif browser_name in ["ff", "firefox"]:
        options = FFOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)

    elif browser_name in ["ya", "yandex"]:
        options = ChromiumOptions()
        options.binary_location = "/usr/bin/yandex-browser"
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if headless:
            options.add_argument("headless=new")
        driver = webdriver.Chrome(
            options=options,
            service=ChromiumService(executable_path=f"{drivers_storage}/yandexdriver"),
        )
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    yield driver

    if driver:
        driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        browser = item.funcargs.get("browser")
        if browser:
            screenshot = browser.get_screenshot_as_png()
            allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)