import time

import allure
import pytest
from appium.webdriver.appium_service import AppiumService
from appium.options.android import UiAutomator2Options
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import datetime
from elements_of_screens.bubbles import Bubbles
from elements_of_screens.korona_module import Korona
from elements_of_screens.commitment_screen import Commitment_screen
from elements_of_screens.login import Login
from elements_of_screens.timeline_commitment import Timeline_commitment
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import random
import string


@pytest.fixture(scope='class')
def driver():
    appium_service = AppiumService()
    appium_service.start(args=['--address', "127.0.0.1", '--port', "4723", "--base-path", '/wd/hub'])
    # Extracting of adb id device
    get_connected_devices = lambda: [line.split('\t')[0] for line in subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=True).stdout.strip().split('\n')[1:] if line.endswith('\tdevice')]
    serial_number = get_connected_devices()
    # Set up Webdriver options
    options = UiAutomator2Options().load_capabilities({
        'deviceName': serial_number[0],
        # 'platformName': 'Android',
        # 'platformVersion': '11',
        # 'app': 'C:/applications/maccabi.apk',
        'appPackage': 'com.ideomobile.maccabi',
        'appActivity': '.ui.splash.SplashActivity',
        'autoGrantPermissions': True,
        'unlockType': 'pin',
        'unlockKey': '1111'
    })
    driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
    driver.implicitly_wait(30)
    yield driver
    driver.quit()
    appium_service.stop()


@pytest.fixture(scope='function', autouse=True)
def take_screenshot(driver):
    yield
    with allure.step('Take a screenshot'):
        allure.attach(
            driver.get_screenshot_as_png(),
            name='screenshot',
            attachment_type=allure.attachment_type.PNG
        )


@pytest.mark.usefixtures('driver')
class TestExample:
    @allure.description("Test checks for pop-up on startup ")
    @pytest.mark.skip
    def test_login(self, driver):
        driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/dynamicActionButton")
        assert driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/dynamicActionButton").is_displayed()

    def test_commitment(self, driver):
        """ A test that passes authorization, creates a new one commitment and checks that the new commitment was
        created correctly """
        bubbles = Bubbles(driver)
        login = Login(driver)
        timeline_commitment = Timeline_commitment(driver)
        commitment_screen = Commitment_screen(driver)
        # The LogIn process
        bubbles.ivExpand().click()
        bubbles.bubble_commitment().click()
        login.btn_transition_otp().click()
        login.tab_enter_with_password().click()
        login.entering_member_id().click()
        login.entering_member_id().send_keys("125")
        driver.back()
        login.entering_password().click()
        login.entering_password().send_keys("Bb12345C")
        driver.back()
        login.btn_enter().click()
        # Push notification
        wait = WebDriverWait(driver, 60)
        this_my_gadget = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/btnAction2")))
        this_my_gadget.click()
        # Approving phone number
        this_my_number = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/btnConfirm")))
        this_my_number.click()
        # Continuing of creating new commitment
        timeline_commitment.btn_fab().click()
        timeline_commitment.new_commitment().click()
        # Pick on the parent family member
        list_of_members = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/familyMemberPicker")
        members = []
        for member in list_of_members.find_elements(AppiumBy.CLASS_NAME, "android.widget.LinearLayout"):
            members.append(member)
        members[0].click()
        time.sleep(2)
        commitment_screen.choice_reference().click()
        commitment_screen.i_have_no_reference().click()
        # Scrolling down
        element = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/ivIcon")
        x = element.location['x']
        y = element.location['y']
        # Creating object  TouchAction
        action = TouchAction(driver)
        # Scrolling down
        action.long_press(x=x, y=y).move_to(x=x, y=y - 250).release().perform()
        # Entering of medical field
        commitment_screen.medical_field().click()
        commitment_screen.entering_medical_field().click()
        commitment_screen.entering_medical_field().send_keys("עיניים")
        driver.back()
        commitment_screen.eyes_medical_field().click()
        commitment_screen.btn_continue().click()
        # Transition to second screen of commitment
        commitment_screen.btn_not_appointment().click()
        commitment_screen.btn_approve().click()

        # Transition to third screen of commitment
        commitment_screen.send_request().click()

        # Pop up successful
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.ideomobile.maccabi:id/btn_negative")))
        pop_up_success = driver.find_element(AppiumBy.ID, "android:id/content")

        # Test that checks the PopUp of success was displayed
        assert pop_up_success.is_displayed()

    def test_korona_vac(self, driver):
        """A test that checks module korona vaccinations of parent (opening of files,visibility of text hebrew and
        english)"""
        bubbles = Bubbles(driver)
        korona = Korona(driver)
        # The LogIn process
        driver.get("https://mc.maccabi4u.co.il/transfer/")
        bubbles.menu_hamburger().click()
        bubbles.korona().click()

        # Entering to module korona vaccinations
        korona.vac_performed_btn().click()

        # Pick on the parent family member
        list_of_members = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/familyMemberPicker")
        members = []
        for member in list_of_members.find_elements(AppiumBy.CLASS_NAME, "android.widget.LinearLayout"):
            members.append(member)
        members[0].click()

        # Test that check correcting entry to module vaccinations korona
        assert (driver.find_element(AppiumBy.ACCESSIBILITY_ID, "החיסונים של תםם").get_attribute(
            "content-desc") == "החיסונים של תםם")

        # Selection of first vaccination of user
        list_user_vac = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/content_container")
        all_user_vac = []
        for vac in list_user_vac.find_elements(AppiumBy.CLASS_NAME, "android.widget.ImageView"):
            all_user_vac.append(vac)
        first_user_vac = all_user_vac[1]

        # Entry to first vaccination
        first_user_vac.click()

        # Test that entry to first vaccination was correctly
        assert (driver.find_element(AppiumBy.ACCESSIBILITY_ID, "צפייה קובץ חיסוני קורונה").is_displayed())
        assert (driver.find_element(AppiumBy.ACCESSIBILITY_ID,
                                    "חיסון קורונה חברת פייזר Pfizer Covid 19").get_attribute(
            "content-desc") == "חיסון קורונה חברת פייזר Pfizer Covid 19")

        # Test the opening of vaccination certificate
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "צפייה קובץ חיסוני קורונה").click()
        # Tools for opening file
        tools_list = driver.find_element(AppiumBy.ID, "android:id/resolver_list")
        tools = []
        for tool in tools_list.find_elements(AppiumBy.CLASS_NAME, "android.widget.LinearLayout"):
            tools.append(tool)
        drive_pdf = tools[8]
        drive_pdf.click()

        # Test checks that file pdf was opened properly
        assert (driver.find_element(AppiumBy.ID, "com.google.android.apps.docs:id/projector_toolbar").is_displayed())

        # Test checks that file pdf is appearing
        assert (driver.find_element(AppiumBy.ID, "com.google.android.apps.docs:id/pdf_view").is_displayed())


if __name__ == '__main__':
    pytest.main()
