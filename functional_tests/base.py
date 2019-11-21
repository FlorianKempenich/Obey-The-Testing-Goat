from functools import wraps
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from .server_tools import reset_database
import time
import os

MAX_WAIT = 10


def wait(assertion_fn):
    @wraps(assertion_fn)
    def decorated(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return assertion_fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time >= MAX_WAIT:
                    raise e
                time.sleep(0.1)

    return decorated


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self):
        self.browser.quit()

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    @wait
    def wait_for(self, assertion_fn):
        return assertion_fn()

    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    @wait
    def wait_for_404_page(self):
        self.assertEqual(
            self.browser.find_element_by_css_selector('.jumbotron h1').text,
            'Page not found'
        )

    @wait
    def wait_for_link(self, link_text):
        self.browser.find_element_by_link_text(link_text)

    def add_list_item(self, item_text):
        num_rows = len(
            self.browser.find_elements_by_css_selector('#id_list_table tr')
        )
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f'{item_number}: {item_text}')

    def get_path(self, path):
        return self.browser.get(self.live_server_url + path)
