from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page_objects.base_page import BasePage

class RegisterPage(BasePage):
    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
        self.path = "/index.php?route=account/register"

    def open(self):
        super().open(self.path)

    def register(self, firstname, lastname, email, password):
        self.wait_for(By.NAME, "firstname").send_keys(firstname)
        self.browser.find_element(By.NAME, "lastname").send_keys(lastname)
        self.browser.find_element(By.NAME, "email").send_keys(email)
        self.browser.find_element(By.NAME, "password").send_keys(password)

        agree_checkbox = self.browser.find_element(By.NAME, "agree")
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", agree_checkbox)

        try:
            WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.NAME, "agree"))).click()
        except Exception as e:
            print(f"Ошибка при клике на чекбокс: {str(e)}")
            self.browser.execute_script("arguments[0].click();", agree_checkbox)

        try:
            continue_button = self.browser.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
            WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(continue_button)).click()
        except Exception as e:
            self.browser.execute_script("arguments[0].click();", continue_button)

    def is_registration_successful(self):
        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "body"), "Your Account Has Been Created!"
            )
        )
        return True
