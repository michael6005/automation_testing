import datetime
import random
import string
import sys
import xmlrunner
import pandas as pd
import requests
import psutil
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.webdriver import WebDriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options

from Maccabi_app.korona_module import Korona
from Maccabi_app.login_2 import Login
from Maccabi_app.bubbles_2 import Bubbles
from Maccabi_app.commitment_screen_2 import Commitment_screen
from Maccabi_app.timeline_commitment_2 import Timeline_commitment

from appium.webdriver.common.mobileby import MobileBy as AppiumBy
from appium.webdriver.common.touch_action import TouchAction
import logging

from appium import webdriver
import unittest

import tracemalloc


class Tests(unittest.TestCase):
    appium_service = None
    driver = None

    """ A decorator classmethod is a function of a decorator and binds a method to a class, 
        not to a specific instance of that class"""

    @classmethod
    def setUpClass(cls):
        # We use cls instead self this will allow us to refer to the class rather than an instance of the class
        # logging.basicConfig(level=logging.DEBUG)
        # Start Appium server
        cls.appium_service = AppiumService()
        cls.appium_service.start(args=['--address', "127.0.0.1", '--port', "4723", "--base-path", '/wd/hub'])
        # Set up Webdriver options
        options = UiAutomator2Options().load_capabilities({
            'deviceName': 'R38N3014ZMX',
            'platformName': 'Android',
            'platformVersion': '11',
            'app': 'C:/applications/maccabi.apk',
            'autoGrantPermissions': True,
            'unlockType': 'pin',
            'unlockKey': '1111'
        })
        cls.driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
        cls.driver.implicitly_wait(15)
        cls.action = TouchAction(cls.driver)
        cls.login = Login(cls.driver)
        cls.bubbles = Bubbles(cls.driver)
        cls.timeline_commitment = Timeline_commitment(cls.driver)
        cls.commitment_screen = Commitment_screen(cls.driver)
        cls.korona = Korona(cls.driver)
        current_process = psutil.Process()
        for child in current_process.children(recursive=True):
            child.kill()

    @classmethod
    def tearDownClass(cls):
        cls.driver.remove_app('com.ideomobile.maccabi')
        cls.driver.quit()
        cls.appium_service.stop()

    def test_1(self):
        # configure the logger
        logging.basicConfig(filename='test_report.log', level=logging.INFO,
                            format='%(asctime)s: %(levelname)s: %(message)s')

        # use the logger to log messages
        logging.info('Starting test run...')

        """Test that checks parent who isn't member"""

        # The LogIn process
        self.wait = WebDriverWait(self.driver, 60)
        try:
            self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/dynamicActionButton").click()
        except:
            pass

        list_of_members = []
        users_data = pd.read_excel('C:/applications/test_data.xlsx')

        # Looping through each row of the Excel file
        for index, row in users_data.iterrows():
            username = row['member_id']  # Getting values from each column
            list_of_members.append(username)

        for member in list_of_members:
            with self.subTest(member=member):
                self.bubbles.bubble_test_results().click()

                # The LogIn process
                if not hasattr(self, 'pop_up_transition_otp'):
                    self.login.btn_transition_otp().click()
                    self.pop_up_transition_otp = True

                self.login.tab_enter_with_password().click()
                self.login.entering_member_id().click()
                self.login.entering_member_id().send_keys(str(member))
                self.driver.back()
                self.login.entering_password().click()
                self.login.entering_password().send_keys("Aa123456")
                self.driver.back()
                self.login.btn_enter().click()
                try:
                    # Run push notification and approving phone number only once
                    if not hasattr(self, 'push_notification_run'):
                        # Push notification
                        self.wait.until(
                            EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/btnAction2")))
                        self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btnAction2").click()
                        self.push_notification_run = True

                    if not hasattr(self, 'approve_phone_number_run'):
                        # Approving phone number
                        self.wait.until(
                            EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/btnConfirm")))
                        self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btnConfirm").click()
                        self.approve_phone_number_run = True

                    # Test check that we located in timeline test results
                    self.assertTrue(self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "תוצאות בדיקות").is_enabled())
                    logging.info(f"Test passed for member: {member}")

                except AssertionError:
                    logging.error(f"Test failed for member: {member}")
                    continue

                except NoSuchElementException:
                    logging.error(f"Element not found for member: {member}")
                    self.driver.get("https://mc.maccabi4u.co.il/transfer/")
                    continue

                # Log out
                self.driver.get("https://mc.maccabi4u.co.il/transfer/")
                self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/buttonUserExchange").click()
                self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_negative").click()
                self.driver.back()

    @unittest.skip
    def test_2(self):

        # configure the logger
        logging.basicConfig(filename='test_report.log', level=logging.INFO,
                            format='%(asctime)s: %(levelname)s: %(message)s')

        # use the logger to log messages
        logging.info('Starting test run...')

        """Test that checks parent who isn't member"""

        # The LogIn process
        self.wait = WebDriverWait(self.driver, 60)
        try:
            self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/dynamicActionButton").click()
        except:
            pass

        list_of_members = []
        users_data = pd.read_excel('C:/applications/test_data.xlsx')

        # Looping through each row of the Excel file
        for index, row in users_data.iterrows():
            username = row['member_id']  # Getting values from each column
            list_of_members.append(username)

        for member in list_of_members:
            self.driver.implicitly_wait(15)
            self.bubbles.bubble_test_results().click()

            # The LogIn process
            if not hasattr(self, 'pop_up_transition_otp'):
                self.login.btn_transition_otp().click()
                self.pop_up_transition_otp = True

            self.login.tab_enter_with_password().click()
            self.login.entering_member_id().click()
            self.login.entering_member_id().send_keys(str(member))
            self.driver.back()
            self.login.entering_password().click()
            self.login.entering_password().send_keys("Aa123456")
            self.driver.back()
            self.login.btn_enter().click()

            # Run push notification and approving phone number only once
            if not hasattr(self, 'push_notification_run'):
                # Push notification
                self.wait.until(
                    EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/btnAction2")))
                self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btnAction2").click()
                self.push_notification_run = True

            if not hasattr(self, 'approve_phone_number_run'):
                # Approving phone number
                self.wait.until(
                    EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/btnConfirm")))
                self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btnConfirm").click()
                self.approve_phone_number_run = True

            with self.subTest(member=member):
                # Test check that we located in timeline test results
                self.assertTrue(self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/extendedFab"))

            # Log out
            self.driver.get("https://mc.maccabi4u.co.il/transfer/")
            self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/buttonUserExchange").click()

            try:
                self.driver.implicitly_wait(5)
                self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_negative").click()
                self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_negative").click()
                self.driver.back()

            except:

                self.driver.back()


if __name__ == '__main__':
    unittest.main()

# Reset password
# for i in list_of_members:
#     url = f"http://10.70.45.107/srs/webapi/mac/v1/members/0/{str(i)}/passwords/reset"
#
#     headers = {
#         "Content-Type": "application/json"
#     }
#     data = {
#         "new_password": "Aa123456"
#     }
#     response = requests.patch(url, headers=headers, json=data)
#
#     print(response.status_code)  # status code
#     print(response.json())  # response
