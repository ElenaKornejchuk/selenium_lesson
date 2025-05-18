from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage


class AdminLoginPage(BasePage):
    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
        self.path = "/administration"

    def open(self):
        super().open(self.path)

    def login(self, username, password):
        username_input = self.wait_for(By.ID, "input-username")
        username_input.clear()
        username_input.send_keys(username)

        password_input = self.wait_for(By.ID, "input-password")
        password_input.clear()
        password_input.send_keys(password)

        self.wait_for(By.CSS_SELECTOR, "button[type='submit']").click()

    def is_logged_in(self):
        self.wait_for(By.XPATH, "//h1[text()='Dashboard']")
        return True

    def logout(self):
        self.browser.find_element(By.CSS_SELECTOR, "a[href*='logout']").click()
