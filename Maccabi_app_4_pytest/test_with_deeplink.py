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
from Maccabi_app.login_2 import Login
from Maccabi_app.bubbles_2 import Bubbles
from Maccabi_app.commitment_screen_2 import Commitment_screen
from Maccabi_app.timeline_commitment_2 import Timeline_commitment
from appium.webdriver.common.mobileby import MobileBy as AppiumBy
from appium.webdriver.common.touch_action import TouchAction
import logging
from selenium.webdriver.common.action_chains import ActionChains
from appium import webdriver
import unittest

class Tests(unittest.TestCase):
    appium_service = None
    driver = None
    # A decorator classmethod is a function of a decorator and binds a method to a class, not to a specific instance of that class
    @classmethod
    def setUpClass(cls):
        # We use cls instead self this will allow us to refer to the class rather than an instance of the class
        #logging.basicConfig(level=logging.DEBUG)
        # Start Appium server
        cls.appium_service = AppiumService()
        cls.appium_service.start(args=['--address', "127.0.0.1", '--port', "4723", "--base-path", '/wd/hub'])
        # Set up Webdriver options
        options = UiAutomator2Options().load_capabilities({
            'deviceName': 'R38N3014ZMX',
            'platformName': 'Android',
            'platformVersion': '11',
            'app': 'C:/applications/maccabi.apk',
            #'noReset': True,
            'autoGrantPermissions': True,
            'unlockType': 'pin',
            'unlockKey': '1111'
        })
        cls.driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
        cls.driver.implicitly_wait(40)
        cls.login = Login(cls.driver)
        cls.bubbles = Bubbles(cls.driver)
        cls.timeline_commitment = Timeline_commitment(cls.driver)
        cls.commitment_screen = Commitment_screen(cls.driver)
        current_process = psutil.Process()
        for child in current_process.children(recursive=True):
            child.kill()

    @classmethod
    def tearDownClass(cls):
        cls.driver.remove_app('com.ideomobile.maccabi')
        cls.driver.quit()
        cls.appium_service.stop()


    def test_1(self):
        """ A test that passes authorization, creates a new one commitment and checks that the new commitment was created correctly """
        # The LogIn process
        self.wait = WebDriverWait(self.driver, 60)
        pop_up_blabla = self.wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/dynamicActionButton")))
        # Running deeplink of commitments
        self.driver.get("https://mc.maccabi4u.co.il/transfer/?module=TLRequests")
        # Continuation of logIn
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
        this_my_gadget = self.wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/btnAction2")))
        this_my_gadget.click()
        # Approving phone number
        this_my_number = self.wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/btnConfirm")))
        this_my_number.click()
        # Continuing of creating new commitment
        self.timeline_commitment.btn_fab().click()
        self.timeline_commitment.new_commitment().click()
        # Pick on the parent family member
        list_of_members = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/familyMemberPicker")
        members = []
        for member in list_of_members.find_elements(AppiumBy.CLASS_NAME, "android.widget.LinearLayout"):
            members.append(member)
        members[0].click()
        self.commitment_screen.choice_reference().click()
        self.commitment_screen.i_have_no_reference().click()
        # Scrolling down
        self.wait.until(EC.element_to_be_clickable(self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/ivIcon")))
        element = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/ivIcon")
        x = element.location['x']
        y = element.location['y']
        # Creating object  TouchAction
        action = TouchAction(self.driver)
        # Scrolling down
        action.long_press(x=x, y=y).move_to(x=x, y=y - 250).release().perform()
        # Entering of medical field
        self.commitment_screen.medical_field().click()
        self.commitment_screen.entering_medical_field().click()
        self.commitment_screen.entering_medical_field().send_keys("עיניים")
        self.driver.back()
        self.commitment_screen.eyes_medical_field().click()
        self.commitment_screen.btn_continue().click()
        # Transition to second screen of commitment
        self.commitment_screen.btn_not_appointment().click()
        self.commitment_screen.btn_approve().click()
        # Transition to third screen of commitment
        # Attaching files
        self.commitment_screen.add_file().click()
        self.commitment_screen.icon_my_files().click()
        # Permissions
        self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btnAction1").click()
        self.commitment_screen.my_file().click()
        confirm_file = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/camera_confirm_ic")
        confirm_file.click()
        cancel_btn = self.wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "ביטול")))
        confirm_file.click()
        ibDelete = self.wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/ibDelete")))
        self.commitment_screen.send_request().click()
        # PopUp your request was sent successfully
        pop_up_success = self.driver.find_element(AppiumBy.ID, "android:id/content")
        # Test that check the PopUp of success was displayed
        self.assertTrue(pop_up_success.is_displayed())
        # OK button
        ok_btn = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_negative")
        ok_btn.click()
        # Checking that new commitment was created
        # Find all the TextView elements in a commitment that was created within the view group using a loop
        text_views = []
        for element in self.timeline_commitment.first_created_commitment().find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
            text_views.append(element)
        # Print the text of each TextView element
        text_views_texts = []
        for text_view in text_views:
            text_views_texts.append(text_view.text)
        print(text_views_texts)
        # Get the current date
        today = datetime.date.today()
        # Format the date in format of application
        formatted_date = today.strftime("%d/%m/%y")
        # The test that check that the date who appeared in new commitment is correct
        self.assertTrue(text_views_texts[0] == formatted_date)
        # The test that check that new commitment was created for correcting family member
        self.assertTrue(text_views_texts[1] == "תם")
        # The test that check that the status of created commitment is correct
        self.assertTrue(text_views_texts[2] == "חדש")
        # The test that check the name of created commitment is correct
        self.assertTrue(text_views_texts[3] == "בקשות להתחייבות")


    def test_2(self):
        """ Test that check validation of mobile phone number in module update personal details """
        self.driver.get("https://mc.maccabi4u.co.il/transfer/?module=updatePersonalDetails")
        field_phone_number = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, value="תיבת טקסט עבור: נייד , ניתן להקליד עד : 11 תווים")
        field_phone_number.click()
        field_phone_number.send_keys("032428442")
        self.driver.back()
        self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_continue").click()
        self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_continue").click()
        self.assertTrue(self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/tv_errorMessage").text =="מספר הטלפון אינו תקין", "The text have not found")


    def test_3(self):
        """Test that check updating personal english name in module update personal details (Test case 156353)"""
        self.driver.get("https://mc.maccabi4u.co.il/transfer/")
        self.bubbles.menu_hamburger().click()
        # Scrolling down
        element = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "לחצן למעבר למכבי פארם")
        x = element.location['x']
        y = element.location['y']
        # Creating object  TouchAction
        action = TouchAction(self.driver)
        # Scrolling down
        action.long_press(x=x, y=y).move_to(x=x, y=y - 250).release().perform()
        element = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "לחצן למעבר לעדכון פרטים אישיים")
        element.click()
        # Pick on the parent family member
        list_of_members = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/familyMemberPicker")
        members = []
        for member in list_of_members.find_elements(AppiumBy.CLASS_NAME, "android.widget.LinearLayout"):
            members.append(member)
        members[0].click()
        #A test that checks the correct entry into the module
        self.assertTrue(self.driver.find_element(AppiumBy.ID,"com.ideomobile.maccabi:id/tv_toolbarMainTitle").text == "עדכון פרטים אישיים - תם" )
        name_english = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="תיבת טקסט עבור: שם פרטי , ניתן להקליד עד : 15 תווים")
        name_english.clear()
        name_english.click()
        # Generate a random letter from the English alphabet
        letter = random.choice(string.ascii_lowercase)
        if letter == name_english.text:
            letter = random.choice(string.ascii_lowercase)
            name_english.send_keys(letter)
        else:
            name_english.send_keys(letter)
        self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_continue").click()
        #Test that checks correcting of updating personal english name
        self.assertTrue(self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/tvEnglishName").text[0] == letter)



if __name__ == '__main__':
    unittest.main()



