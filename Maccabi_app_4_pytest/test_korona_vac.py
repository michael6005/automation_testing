import datetime
import random
import string
import psutil
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.webdriver import WebDriver
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

    #A decorator classmethod is a function of a decorator and binds a method to a class, not to a specific instance of that class
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
        cls.driver.implicitly_wait(10)
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
        """A test that checks module korona vaccinations of parent (opening of files,visibility of text hebrew and english)"""
        # The LogIn process
        self.wait = WebDriverWait(self.driver, 60)
        try:
            self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/dynamicActionButton").click()
        except:
            pass
        self.bubbles.menu_hamburger().click()
        self.bubbles.korona().click()
        # Entering to module korona vaccinations
        self.korona.vac_performed_btn().click()
        # The LogIn process
        self.login.btn_transition_otp().click()
        self.login.tab_enter_with_password().click()
        self.login.entering_member_id().click()
        self.login.entering_member_id().send_keys("125")
        self.driver.back()
        self.login.entering_password().click()
        self.login.entering_password().send_keys("Aa123456")
        self.driver.back()
        self.login.btn_enter().click()
        # Push notification
        wait = WebDriverWait(self.driver, 60)
        this_my_gadget = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/btnAction2")))
        this_my_gadget.click()
        # Approving phone number
        this_my_number = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/btnConfirm")))
        this_my_number.click()
        # Pick on the parent family member
        list_of_members = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/familyMemberPicker")
        members = []
        for member in list_of_members.find_elements(AppiumBy.CLASS_NAME, "android.widget.LinearLayout"):
            members.append(member)
        members[0].click()
        # Test that check correcting entry to module vaccinations korona
        self.assertTrue(self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "החיסונים של תם").get_attribute(
            "content-desc") == "החיסונים של תם")

        # Selection of first vaccination of user
        list_user_vac = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/content_container")
        all_user_vac = []
        for vac in list_user_vac.find_elements(AppiumBy.CLASS_NAME, "android.widget.ImageView"):
            all_user_vac.append(vac)
        first_user_vac = all_user_vac[0]

        # Entry to first vaccination
        first_user_vac.click()

        # Test that entry to first vaccination was correctly
        self.assertTrue(self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "צפייה קובץ חיסוני קורונה").is_displayed())
        self.assertTrue(self.driver.find_element(AppiumBy.ACCESSIBILITY_ID,
                                                 "חיסון קורונה חברת פייזר Pfizer Covid 19").get_attribute(
            "content-desc") == "חיסון קורונה חברת פייזר Pfizer Covid 19")

        # Test the opening of vaccination certificate
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "צפייה קובץ חיסוני קורונה").click()

        # Tools for opening file
        tools_list = self.driver.find_element(AppiumBy.ID, "android:id/resolver_list")
        tools = []
        for tool in tools_list.find_elements(AppiumBy.CLASS_NAME, "android.widget.LinearLayout"):
            tools.append(tool)
        drive_pdf = tools[6]
        drive_pdf.click()
        # Test checks that file pdf was opened properly
        self.assertTrue(
            self.driver.find_element(AppiumBy.ID, "com.google.android.apps.docs:id/projector_toolbar").is_displayed())
        # Test checks that file pdf is appearing
        self.assertTrue(
            self.driver.find_element(AppiumBy.ID, "com.google.android.apps.docs:id/pdf_view").is_displayed())

    def test_2(self):
        " A test that checks the correctness of the vaccination module for a user who does not have vaccinations (Child 125 with name ליאו )"
        self.driver.get("https://mc.maccabi4u.co.il/transfer/")
        self.bubbles.menu_hamburger().click()
        self.bubbles.korona().click()
        # Entering to module korona vaccinations
        self.korona.vac_performed_btn().click()
        # Pick on the parent family member
        list_of_members = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/familyMemberPicker")
        members = []
        for member in list_of_members.find_elements(AppiumBy.CLASS_NAME, "android.widget.LinearLayout"):
            members.append(member)
        members[5].click()
        # Test that check correctness entry to user that doesn't have vaccination
        self.assertTrue(self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "החיסונים של ליאו").is_displayed())
        self.assertTrue(self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "לא נמצאו חיסונים להצגה").is_displayed())
        self.assertTrue(self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.ImageView").is_displayed())

    def test_3(self):
        " A test that checks the correctness of the vaccination module for a child in age 0 who does not have vaccinations (Child 125 with name אפס )"
        self.driver.get("https://mc.maccabi4u.co.il/transfer/")
        self.bubbles.menu_hamburger().click()
        self.bubbles.korona().click()
        # Entering to module korona vaccinations
        self.korona.vac_performed_btn().click()
        # Pick on the parent family member
        list_of_members = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/familyMemberPicker")
        members = []
        for member in list_of_members.find_elements(AppiumBy.CLASS_NAME, "android.widget.LinearLayout"):
            members.append(member)
        x = members[5].location['x']
        y = members[5].location['y']
        self.action.long_press(x=x, y=y).move_to(x=x + 6000, y=y).release().perform()
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "תיבת סימון עבור,אפס, לא מסומן").click()

        # Test that check correctly entry to user in age 0 that doesn't have vaccination
        self.assertTrue(self.driver.find_element(AppiumBy.XPATH,
                                                 "//android.view.View[@content-desc='החיסונים של אפס']").is_displayed())
        self.assertTrue(self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "לא נמצאו חיסונים להצגה").is_displayed())
        self.assertTrue(self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.ImageView").is_displayed())

if __name__ == '__main__':
    unittest.main()
