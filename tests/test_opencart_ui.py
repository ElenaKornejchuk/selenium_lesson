import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page_objects.admin_catalog_page import AdminCatalogPage
from page_objects.main_page import MainPage
from page_objects.admin_login_page import AdminLoginPage
from page_objects.register_page import RegisterPage
from page_objects.product_page import ProductPage
# from faker import Faker



class TestsOpencart:

    def test_opencart_main(self, browser, base_url):
        page = MainPage(browser, base_url)
        page.open()
        assert "Your Store" in page.get_title()

    def test_opencart_admin(self, browser, base_url):
        admin_page = AdminLoginPage(browser, base_url)
        admin_page.open()
        assert "Administration" in browser.title

    @pytest.mark.parametrize("by, value", [
        (By.ID, "logo"),
        (By.NAME, "search"),
        (By.CLASS_NAME, "image"),
        (By.LINK_TEXT, "Desktops"),
        (By.LINK_TEXT, "My Account"),
    ])
    def test_main_page_elements(self, browser, base_url, by, value):
        page = MainPage(browser, base_url)
        page.open()
        page.wait_for(by, value)

    @pytest.mark.parametrize("by, value", [
        (By.CLASS_NAME, "product-thumb"),
        (By.ID, "content"),
        (By.ID, "input-sort"),
        (By.CLASS_NAME, "list-group"),
        (By.CLASS_NAME, "pagination"),
    ])
    def test_category_page_elements(self, browser, base_url, by, value):
        page = MainPage(browser, base_url)
        page.open("/index.php?route=product/category&path=20")
        page.wait_for(by, value)

    @pytest.mark.parametrize("by, value", [
        (By.CLASS_NAME, "col-sm"),
        (By.ID, "input-quantity"),
        (By.ID, "button-cart"),
        (By.CLASS_NAME, "rating"),
        (By.ID, "tab-description"),
    ])
    def test_product_page_elements(self, browser, base_url, by, value):
        page = ProductPage(browser, base_url, product_id=42)
        page.open()
        page.wait_for(by, value)

    @pytest.mark.parametrize("by, value", [
        (By.ID, "input-username"),
        (By.ID, "input-password"),
        (By.CLASS_NAME, "btn-primary"),
        (By.TAG_NAME, "form"),
        (By.CLASS_NAME, "card-header"),
    ])
    def test_admin_login_page_elements(self, browser, base_url, by, value):
        page = AdminLoginPage(browser, base_url)
        page.open()
        page.wait_for(by, value)

    @pytest.mark.parametrize("by, value", [
        (By.ID, "input-firstname"),
        (By.ID, "input-lastname"),
        (By.ID, "input-email"),
        (By.ID, "input-password"),
        (By.NAME, "agree"),
    ])
    def test_registration_page_elements(self, browser, base_url, by, value):
        page = RegisterPage(browser, base_url)
        page.open()
        page.wait_for(by, value)

    def test_currency_switch_main_page(self, browser, base_url):
        page = MainPage(browser, base_url)
        page.open()

        prices_before = page.get_prices()
        page.switch_currency("£ Pound Sterling")
        prices_after = page.get_prices()

        assert prices_before != prices_after, "Currency switch did not affect prices"

    def test_currency_switch_category_page(self, browser, base_url):
        page = MainPage(browser, base_url)
        page.open("/index.php?route=product/category&path=20")

        prices_before = page.get_prices()

        page.switch_currency("€ Euro")
        page.wait_for(By.CLASS_NAME, "price")

        prices_after = page.get_prices()
        assert prices_before != prices_after, "Prices did not change in category after currency switch"

    def test_admin_login_logout(self, browser, base_url):
        admin_page = AdminLoginPage(browser, base_url)
        admin_page.open()
        admin_page.login("user", "bitnami")

        assert admin_page.is_logged_in()

        admin_page.logout()

        assert "login" in browser.current_url.lower()

    def test_add_new_product(self, browser, base_url):
        login_page = AdminLoginPage(browser, base_url)
        login_page.open()
        login_page.login("user", "bitnami")

        assert login_page.is_logged_in(), "Не удалось войти в админку"

        admin_catalog_page = AdminCatalogPage(browser, base_url)
        admin_catalog_page.open_products()
        admin_catalog_page.add_new_product("Test Product", "Test Meta Title", "12345", "test123")

        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "input-name")))

        assert admin_catalog_page.is_product_added("Test Product"), "Продукт не был добавлен"

    def test_delete_product(self, browser, base_url):
        login_page = AdminLoginPage(browser, base_url)
        login_page.open()
        login_page.login("user", "bitnami")

        assert login_page.is_logged_in(), "Не удалось войти в админку"

        admin_catalog_page = AdminCatalogPage(browser, base_url)
        admin_catalog_page.open_products()    #
        admin_catalog_page.delete_product("Product to Delete")

        assert admin_catalog_page.is_product_deleted("Product to Delete"), "Продукт не был удален"

    def test_register_new_user(self, browser, base_url):
        fake = Faker()
        register_page = RegisterPage(browser, base_url)
        register_page.open()

        firstname = fake.first_name()
        lastname = fake.last_name()
        email = fake.unique.email()
        password = "Test1234!"

        register_page.register(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password
        )

        assert register_page.is_registration_successful(), "Регистрация не удалась"

    @pytest.mark.parametrize("currency_name, expected_symbol", [
        ("€ Euro", "€"),
        ("£ Pound Sterling", "£"),
        ("$ US Dollar", "$")
    ])
    def test_currency_switch_main_page(self, browser, base_url, currency_name, expected_symbol):
        page = MainPage(browser, base_url)
        page.open()

        page.switch_currency(currency_name)
        prices_after = page.get_prices()

        assert any(expected_symbol in price for price in prices_after), (
            f"Prices after switching to {currency_name} do not contain symbol '{expected_symbol}'"
        )
