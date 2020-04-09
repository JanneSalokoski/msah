#!/usr/bin/env python3

# Import local configuration
from config import config

import re

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions

class ElementDoesNotContain(object):
    def __init__(self, locator, text):
        self.locator = locator
        self.text = text

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if self.text in element.text:
            return False
        else:
            return element


def get_capabilities():
    capabilities = DesiredCapabilities().FIREFOX
    capabilities['marionette'] = True

    return capabilities

def get_driver(capabilities):
    return webdriver.Firefox(capabilities=capabilities)

def load_page(driver, url):
    driver.get(url)

def get_element(driver, selector):
    return driver.find_element_by_css_selector(selector)

def switch_to_window(driver, window_index):
    driver.switch_to.window(driver.window_handles[window_index])

def wait_for_element(driver, selector):
    return WebDriverWait(driver, 10).until(
        ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, selector))
    )

def wait_until_element_does_not_contain(driver, selector, text):
    return WebDriverWait(driver, 10).until(
        ElementDoesNotContain((By.CSS_SELECTOR, selector), text)
    )

def close_browser(driver):
    driver.quit()

def switch_to_popup(driver):
    switch_to_window(driver, 1)

def switch_to_main(driver):
    switch_to_window(driver, 0)

def get_mopidy_auth_page(driver):
    load_page(driver, config['mopidy']['auth_endpoint'])
    assert "Mopidy-Spotify" in driver.title

def click_mopidy_auth_button(driver):
    get_element(driver, "a.auth-button").click()

def log_in_to_spotify(driver):
    username_input = wait_for_element(driver, "input#login-username")
    username_input.clear()
    username_input.send_keys(config['spotify']['username'])

    password_input = wait_for_element(driver, "input#login-password")
    password_input.clear()
    password_input.send_keys(config['spotify']['password'])
    password_input.send_keys(Keys.RETURN)

def accept_authorization(driver):
    wait_for_element(driver, "button#auth-accept").click()

def parse_mopidy_auth_codes(auth_config):
    client_id = re.findall(r'client_id = (.+?)\n', auth_config)[0]
    client_secret = re.findall(r'client_secret = (.+?)$', auth_config)[0]

    return {'id': client_id, 'secret': client_secret}

def get_mopidy_auth_codes(driver):
    return parse_mopidy_auth_codes(
        wait_until_element_does_not_contain(driver, "pre.copy.auth-config",
            "The config value will appear here."
        ).text
    )

def print_output_for_writing(auth_codes):
    print("--id {} --secret {}".format(auth_codes['id'], auth_codes['secret']))

def main():
    capabilities = get_capabilities()
    driver = get_driver(capabilities)

    get_mopidy_auth_page(driver)
    click_mopidy_auth_button(driver)

    switch_to_popup(driver)

    log_in_to_spotify(driver)
    accept_authorization(driver)

    switch_to_main(driver)

    auth_codes = get_mopidy_auth_codes(driver)

    close_browser(driver)
    
    print_output_for_writing(auth_codes)

main()

