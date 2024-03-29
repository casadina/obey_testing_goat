import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from .server_tools import reset_database
import time

MAX_WAIT = 5

reset_database_playbook_path = os.path.join(os.path.dirname(__file__), '../deploy_tools/reset_database.yml')
inventory_path = os.path.join(os.path.dirname(__file__), '../deploy_tools/hosts.ini')


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        self.test_email = os.environ.get("TEST_EMAIL")
        if self.staging_server:
            self.live_server_url = f'http://{self.staging_server}'
            reset_database(reset_database_playbook_path, inventory_path)

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                split_row = row_text.split(": ")[1]

                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    @staticmethod
    def wait_for(fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    def get_item_input_box(self):
        return self.browser.find_element(By.ID, "id_text")

    def add_list_item(self, item_text):
        num_rows = len(self.browser.find_elements(By.TAG_NAME, 'tr'))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f'{item_number}: {item_text}')
