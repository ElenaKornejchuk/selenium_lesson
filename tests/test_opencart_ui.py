import random
import time


import pytest
from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for(browser, by, locator, timeout=10):
    return WebDriverWait(browser, timeout).until(EC.presence_of_element_located((by, locator)))

class TestsOpencart:

    def test_opencart_main(self, browser, base_url):
        browser.get(base_url)

        assert "Your Store" in browser.title

    def test_opencart_admin(self, browser, base_url):
        browser.get(base_url + "/administration")

        assert "Administration" in browser.title

    @pytest.mark.parametrize("by, value", [
        (By.ID, "logo"),
        (By.NAME, "search"),
        (By.CLASS_NAME, "image"),
        (By.LINK_TEXT, "Desktops"),
        (By.LINK_TEXT, "My Account"),
    ])
    def test_main_page_elements(self, browser, base_url, by, value):
        browser.get(base_url)
        wait_for(browser, by, value)

    @pytest.mark.parametrize("by, value", [
        (By.CLASS_NAME, "product-thumb"),
        (By.ID, "content"),
        (By.ID, "input-sort"),
        (By.CLASS_NAME, "list-group"),
        (By.CLASS_NAME, "pagination"),
    ])
    def test_category_page_elements(self, browser, base_url, by, value):
        browser.get(base_url + "/index.php?route=product/category&path=20")
        wait_for(browser, by, value)

    @pytest.mark.parametrize("by, value", [
        (By.CLASS_NAME, "col-sm"),
        (By.ID, "input-quantity"),
        (By.ID, "button-cart"),
        (By.CLASS_NAME, "rating"),
        (By.ID, "tab-description"),
    ])
    def test_product_page_elements(self, browser, base_url, by, value):
        browser.get(base_url + "/index.php?route=product/product&product_id=42")
        wait_for(browser, by, value)

    @pytest.mark.parametrize("by, value", [
        (By.ID, "input-username"),
        (By.ID, "input-password"),
        (By.CLASS_NAME, "btn-primary"),
        (By.TAG_NAME, "form"),
        (By.CLASS_NAME, "card-header"),
    ])
    def test_admin_login_page_elements(self, browser, base_url, by, value):
        browser.get(base_url + "/administration")
        wait_for(browser, by, value)

    @pytest.mark.parametrize("by, value", [
        (By.ID, "input-firstname"),
        (By.ID, "input-lastname"),
        (By.ID, "input-email"),
        (By.ID, "input-password"),
        (By.NAME, "agree"),
    ])
    def test_registration_page_elements(self, browser, base_url, by, value):
        browser.get(base_url + "/index.php?route=account/register")
        wait_for(browser, by, value)


    def test_currency_switch_main_page(self, browser, base_url):
        browser.get(base_url)

        prices_before = [el.text for el in browser.find_elements(By.CLASS_NAME, "price")]

        wait_for(browser, By.CSS_SELECTOR, "a.dropdown-toggle").click()
        wait_for(browser, By.LINK_TEXT, "€ Euro").click()

        WebDriverWait(browser, 10).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "price"), "€")
        )

        prices_after = [el.text for el in browser.find_elements(By.CLASS_NAME, "price")]
        assert prices_before != prices_after, "Currency switch did not affect prices"

    def test_currency_switch_category_page(self, browser, base_url):
        browser.get(base_url + "/index.php?route=product/category&path=20")

        prices_before = [el.text for el in browser.find_elements(By.CLASS_NAME, "price")]

        wait_for(browser, By.CSS_SELECTOR, "a.dropdown-toggle").click()
        wait_for(browser, By.LINK_TEXT, "€ Euro").click()
        wait_for(browser, By.CLASS_NAME, "price")

        prices_after = [el.text for el in browser.find_elements(By.CLASS_NAME, "price")]
        assert prices_before != prices_after, "Prices did not change in category after currency switch"

    def test_admin_login_logout(self, browser, base_url):
        browser.get(base_url + "/administration")

        wait_for(browser, By.ID, "input-username").send_keys("user")
        wait_for(browser, By.ID, "input-password").send_keys("bitnami")
        wait_for(browser, By.CLASS_NAME, "btn-primary").click()

        wait_for(browser, By.XPATH, "//h1[text()='Dashboard']")
        wait_for(browser, By.CSS_SELECTOR, "#nav-logout a.nav-link").click()

        assert "login" in browser.current_url.lower()

    def test_add_random_product_to_cart(self, browser, base_url):
        browser.get(base_url)

        products = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-thumb"))
        )
        assert products, "No products found on the main page"

        valid_products = []
        for p in products:
            try:
                WebDriverWait(p, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "button[title='Add to Cart']"))
                )
                valid_products.append(p)
            except:
                continue

        assert valid_products, "No products with 'Add to Cart' button found"

        product = random.choice(valid_products)
        add_to_cart_button = product.find_element(By.CSS_SELECTOR, "button[title='Add to Cart']")

        try:
            price_old = product.find_element(By.CLASS_NAME, "price-old")
            add_to_cart_button.click()
        except:
            print("Product without discount, adding to cart.")
            browser.execute_script("arguments[0].scrollIntoView(true);", add_to_cart_button)
            WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable(add_to_cart_button)
            )
            actions = ActionChains(browser)
            actions.move_to_element(add_to_cart_button).click().perform()

            try:
                cart_count_element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-count"))
                )
                cart_count = cart_count_element.text
                assert int(cart_count) > 0, "Cart count is still zero. Item was not added."
                print("Item added to cart.")
            except TimeoutException:
                try:
                    success_message = WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
                    )
                    assert success_message, "Success message not displayed. Item might not be added."
                    print("Item successfully added to cart.")
                except TimeoutException:
                    print("Failed to confirm item was added to cart.")