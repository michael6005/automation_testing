import time

import pytest
import allure
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from Maccabi_app_4_pytest.conftest import driver
from Maccabi_app_4_pytest.elements_of_screens.bubbles import Bubbles
from Maccabi_app_4_pytest.elements_of_screens.korona_module import Korona
from Maccabi_app_4_pytest.elements_of_screens.login import Login
from Maccabi_app_4_pytest.elements_of_screens.timeline_commitment import Timeline_commitment
from appium.webdriver.common.mobileby import MobileBy as AppiumBy


@pytest.mark.parametrize('deviceName, platformName, platformVersion', [('R38N3014ZMX', 'Android', '11')])
class TestServiceGuideStrongLogin:
    @allure.description("Summoning an appointment to a family doctor maccabi with strong identification (Test Case "
                        "24829)")
    def test_1(self, driver, deviceName, platformName, platformVersion):
        bubbles = Bubbles(driver)
        login = Login(driver)
        korona = Korona(driver)
        timeline_commitment = Timeline_commitment(driver)
        wait = WebDriverWait(driver, 60)
        # A pop-up pops up when an application is loaded
        # wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.ideomobile.maccabi:id/dynamicActionButton")))
        # driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/dynamicActionButton").click()

        # Click on bubble queue reservation
        bubbles.bubble_queue_reservation().click()

        # The LogIn process
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
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.ideomobile.maccabi:id/btnAction2")))
        login.approve_push_notification().click()

        # Approving phone number
        wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/btnConfirm")))
        login.approve_phone_num().click()

        # Calling a doctor's appointment from a FAB button in timeline
        timeline_commitment.btn_fab().click()
        timeline_commitment.new_commitment().click()

        # Choice doctor in the screen "Which service do you want to make an appointment with?"
        time.sleep(8)
        services = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/recyclerView")
        services_list = []
        for e in services.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button"):
            services_list.append(e)
        services_list[2].click()

        # Pick on the parent family member
        login.pick_parent().click()

        # Filling in the input field doctor's name
        time.sleep(8)
        wait.until(EC.visibility_of_all_elements_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))
        els2 = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        els2[0].send_keys("סבטלנה אייזנשטט")
        driver.hide_keyboard()

        # Click on free place on screen to show search button
        free_plc = driver.find_elements(AppiumBy.CLASS_NAME, "android.view.View")
        free_plc[0].click()

        # Swipe up and down for a search button to be clickable
        action = TouchAction(driver)
        x = free_plc[0].location['x']
        y = free_plc[0].location['y']
        action.long_press(x=x, y=y).move_to(x=x, y=y + 2500).release().perform()  # Swipe up
        action.long_press(x=x, y=y).move_to(x=x, y=y - 2500).release().perform()  # Swipe down

        # Click on search button
        time.sleep(8)
        wait.until(EC.visibility_of_all_elements_located((AppiumBy.CLASS_NAME, "android.widget.Button")))
        search_btn = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
        search_btn[4].click()

        # Click in appointment reservation
        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.view.View["
                                                               "@content-desc=\"פרטי השכלה "
                                                               "ומומחיות\"]/android.widget.TextView[2]")))

        appoint_reserve = driver.find_elements(AppiumBy.CLASS_NAME, "android.view.View")
        appoint_reserve[15].click()

        # Test that check that we are located on first screen of dialog with doctor
        ##wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.ideomobile.maccabi:id/visit_instructions_title")))
        time.sleep(8)
        # list_text_views = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        # list_of_visit_types = [list_text_views[5].text, list_text_views[6].text]
        # with allure.step('Take a screenshot'):
        #     allure.attach(
        #         driver.get_screenshot_as_png(),
        #         name='screenshot',
        #         attachment_type=allure.attachment_type.PNG
        #     )
        # #assert (list_of_visit_types[1] == "ביקור רגיל")

        # Choosing a visit type
        wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/tvVisitType")))
        els12 = driver.find_elements(AppiumBy.CLASS_NAME, "androidx.appcompat.widget.LinearLayoutCompat")
        els12[0].click()

        # Choosing a first available visit date
        wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/tvText")))
        list_of_dates = driver.find_element(AppiumBy.ID, 'com.ideomobile.maccabi:id/hourPicker')
        list_of_dates.find_element(AppiumBy.CLASS_NAME, "android.view.ViewGroup").click()

        # Approving appointment
        approval_btn = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/buttonApproval")
        approval_btn.click()

        # Finishing of appointment
        wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/textViewSuccessHeader")))
        finish_btn = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/buttonApproval")
        finish_btn.click()

        # Cancellation process of a future appointment
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.ideomobile.maccabi:id/extendedFab")))
        queue_list = driver.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup")
        first_queue = queue_list[4]
        first_queue.click()

        wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.ideomobile.maccabi:id/btn_cancel")))
        btn_cancel = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_cancel")
        btn_cancel.click()

        wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.ideomobile.maccabi:id/btn_negative")))
        btn_negative = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_negative")
        btn_negative.click()

    @allure.description("Summoning an appointment for a strong identification flu vaccine (Test Case 419222)")
    def test_2(self, driver, deviceName, platformName, platformVersion):
        wait = WebDriverWait(driver, 60)

        # Deeplink for services directory transition with a nurse's clinic
        driver.get("https://mc.maccabi4u.co.il/transfer/?module=bookNurse")

        # Pick on the parent family member
        list_of_members = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/familyMemberPicker")
        members = []
        for member in list_of_members.find_elements(AppiumBy.CLASS_NAME, "android.widget.LinearLayout"):
            members.append(member)
        members[0].click()

        # Enter the name of a clinic
        list_of_buttons = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
        wait.until(lambda x: len(list_of_buttons) == 5)
        els8 = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        els8[0].send_keys("בורוכוב נטלי")

        # Click on free place on screen to show search button
        free_plc = driver.find_elements(AppiumBy.CLASS_NAME, "android.view.View")
        free_plc[0].click()
        # Click on search button
        wait.until(EC.visibility_of_all_elements_located((AppiumBy.CLASS_NAME, "android.widget.Button")))
        search_btn = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
        search_btn[4].click()

        # Click on appointment reserve
        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.view.View["
                                                               "@content-desc=\"טיפולים\"]/android.widget"
                                                               ".TextView[2]")))

        appoint_reserve = driver.find_elements(AppiumBy.CLASS_NAME, "android.view.View")
        appoint_reserve[13].click()

        # Click on the flu vaccine button in visit type screen
        list_visit_types = driver.find_elements(AppiumBy.CLASS_NAME,
                                                "androidx.appcompat.widget.LinearLayoutCompat")
        list_visit_types[4].click()

        # Choosing a first available visit date
        wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/tvText")))
        list_of_dates = driver.find_element(AppiumBy.ID, 'com.ideomobile.maccabi:id/hourPicker')
        list_of_dates.find_element(AppiumBy.CLASS_NAME, "android.view.ViewGroup").click()

        # Approving appointment
        approval_btn = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/buttonApproval")
        approval_btn.click()

        # Finishing of appointment
        wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/textViewSuccessHeader")))
        finish_btn = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/buttonApproval")
        finish_btn.click()

        # Cancellation process of a future appointment
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.ideomobile.maccabi:id/extendedFab")))
        queue_list = driver.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup")
        first_queue = queue_list[4]
        first_queue.click()

        wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.ideomobile.maccabi:id/btn_cancel")))
        btn_cancel = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_cancel")
        btn_cancel.click()

        wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.ideomobile.maccabi:id/btn_negative")))
        btn_negative = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_negative")
        btn_negative.click()

    @pytest.mark.skip
    @allure.description("Summoning an appointment for a strong identification to office (Test Case 419377)")
    def test_3(self, driver, deviceName, platformName, platformVersion):
        bubbles = Bubbles(driver)
        login = Login(driver)
        korona = Korona(driver)
        timeline_commitment = Timeline_commitment(driver)
        wait = WebDriverWait(driver, 60)

        # Deeplink beyond a bubble screen
        driver.get("https://mc.maccabi4u.co.il/transfer/")

        # Opening a hamburger menu
        bubbles.menu_hamburger().click()

        # Opening the service guide
        el1 = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "לחצן למעבר לאיתור שירותמצב סגור, לחץ פעמיים לפתיחה")
        el1.click()
        el2 = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "לחצן למעבר למשרד")
        el2.click()

        # Pick on the parent family member
        list_of_members = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/familyMemberPicker")
        members = []
        for member in list_of_members.find_elements(AppiumBy.CLASS_NAME, "android.widget.LinearLayout"):
            members.append(member)
        members[0].click()

        # Enter the name of office
        list_of_buttons = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
        wait.until(lambda driver: len(list_of_buttons) == 3)
        els8 = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        els8[0].send_keys("יקנעם עילית")
        driver.hide_keyboard()
        els4 = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.ListView")
        els4[0].click()

        # Click on free place on screen to show search button
        free_plc = driver.find_elements(AppiumBy.CLASS_NAME, "android.view.View")
        free_plc[0].click()

        # Click on search button
        wait.until(EC.visibility_of_all_elements_located((AppiumBy.CLASS_NAME, "android.widget.Button")))
        search_btn = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
        search_btn[1].click()

        # Click on appointment reserve
        wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, "//android.view.View[@content-desc=\"מרכז רפואי יקנעם-משרד\"]/android.widget.TextView")))

        appoint_reserve = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        appoint_reserve[10].click()

        # Choosing a visit
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.ideomobile.maccabi:id/visit_instructions_title")))
        wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/tvVisitType")))
        btn_visit_type = driver.find_elements(AppiumBy.CLASS_NAME, "androidx.appcompat.widget.LinearLayoutCompat")
        btn_visit_type[0].click()

        # Choosing a first available visit date
        wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/tvText")))
        list_of_dates = driver.find_element(AppiumBy.ID, 'com.ideomobile.maccabi:id/hourPicker')
        list_of_dates.find_element(AppiumBy.CLASS_NAME, "android.view.ViewGroup").click()

        # Approving appointment
        approval_btn = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/buttonApproval")
        approval_btn.click()

        # Finishing of appointment
        wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/textViewSuccessHeader")))
        finish_btn = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/buttonApproval")
        finish_btn.click()

        # Cancellation process of a future appointment
        driver.wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.ideomobile.maccabi:id/extendedFab")))
        queue_list = driver.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup")
        first_queue = queue_list[4]
        first_queue.click()

        driver.wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.ideomobile.maccabi:id/btn_cancel")))
        btn_cancel = driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_cancel")
        btn_cancel.click()

        driver.wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.ideomobile.maccabi:id/btn_negative")))
        btn_negative = driver.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_negative")
        btn_negative.click()


if __name__ == '__main__':
    pytest.main()
