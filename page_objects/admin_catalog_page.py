import time

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page_objects.base_page import BasePage
from tests.conftest import logger


class AdminCatalogPage(BasePage):

    @allure.step("Открытие каталога продуктов")
    def open_products(self):
        logger.info("Открытие каталога продуктов")
        self.wait_for(By.ID, "menu-catalog").click()
        self.wait_for(By.LINK_TEXT, "Products").click()

    @allure.step("Добавление нового продукта")
    def add_new_product(self, name, meta_title, model, seo):
        logger.info(
            f"Добавление нового продукта: name='{name}', meta_title='{meta_title}', model='{model}', seo='{seo}'")

        add_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-primary[aria-label='Add New']"))
        )
        self.browser.execute_script("arguments[0].scrollIntoView(true);", add_button)
        time.sleep(1)
        self.browser.execute_script("arguments[0].click();", add_button)

        WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.ID, "input-name-1"))
        )

        self.browser.find_element(By.ID, "input-name-1").send_keys(name)
        self.browser.find_element(By.ID, "input-meta-title-1").send_keys(meta_title)

        logger.debug("Заполнение вкладки Data")
        self.browser.find_element(By.LINK_TEXT, "Data").click()
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.ID, "input-model"))
        )
        self.browser.find_element(By.ID, "input-model").send_keys(model)

        logger.debug("Заполнение вкладки SEO")
        self.browser.find_element(By.LINK_TEXT, "SEO").click()
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.ID, "input-keyword-0-1"))
        )
        self.browser.find_element(By.ID, "input-keyword-0-1").send_keys(seo)

        logger.info("Сохранение продукта")
        save_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-original-title='Save']"))
        )
        self.browser.execute_script("arguments[0].click();", save_button)

        WebDriverWait(self.browser, 10).until(
            EC.url_contains("route=catalog/product")
        )
        logger.info("Продукт успешно добавлен")

    @allure.step("Проверка наличия продукта")
    def is_product_added(self, name):
        logger.debug(f"Проверка наличия продукта '{name}'")
        return name in self.browser.page_source

    @allure.step("Удаление продукта по имени")
    def delete_product(self, name):
        logger.info(f"Удаление продукта с именем: {name}")
        search_input = self.wait_for(By.ID, "input-name")
        search_input.clear()
        search_input.send_keys(name)
        self.wait_for(By.ID, "button-filter").click()

        try:
            checkboxes = WebDriverWait(self.browser, 10).until(
                EC.presence_of_all_elements_located((By.NAME, "selected[]"))
            )

            for checkbox in checkboxes:
                if checkbox.is_displayed() and checkbox.is_enabled():
                    checkbox.click()
                    break

            logger.debug("Нажатие на кнопку Delete")
            delete_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-original-title='Delete']"))
            )
            delete_button.click()

            logger.debug("Подтверждение удаления")
            self.browser.switch_to.alert.accept()
            logger.info("Удаление завершено")
        except Exception as e:
            logger.error(f"Ошибка при удалении продукта: {e}")

    @allure.step("Проверка, что продукт '{name}' удалён")
    def is_product_deleted(self, name):
        logger.debug(f"Проверка, что продукт '{name}' удалён")
        search_input = self.wait_for(By.ID, "input-name")
        search_input.clear()
        search_input.send_keys(name)
        self.wait_for(By.ID, "button-filter").click()
        return "No results!" in self.browser.page_source