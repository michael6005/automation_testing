import logging
import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from Maccabi_app_2.base_test import *
from appium.webdriver.common.mobileby import MobileBy as AppiumBy, MobileBy


class TestServiceGuideWeakLogin(BaseTest):
    @pytest.mark.skip
    def test_1(self):
        """Summoning an appointment to a family doctor with weak identification"""

        # A pop-up pops up when an application is loaded
        # self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.ideomobile.maccabi:id/dynamicActionButton")))
        # self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/dynamicActionButton").click()

        # Opening a hamburger menu
        self.bubbles.menu_hamburger().click()

        # Opening the service guide
        el1 = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "לחצן למעבר לאיתור שירותמצב סגור, לחץ פעמיים לפתיחה")
        el1.click()
        el2 = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "לחצן למעבר לרופאים/ות")
        el2.click()
        sleep(3)
        self.wait.until(EC.visibility_of_all_elements_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))
        els2 = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        els2[0].click()
        sleep(3)
        els2[0].send_keys("סבטלנה אייזנשטט")
        self.driver.hide_keyboard()

        # Click on free place on screen to show search button
        self.wait.until(EC.text_to_be_present_in_element((AppiumBy.CLASS_NAME, "android.view.View"), 'איזה רופא/ה ברצונך למצוא?'))
        free_plc = self.driver.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")
        free_plc[0].click()

        # Swipe up and down for a search button to be clickable
        x = free_plc[0].location['x']
        y = free_plc[0].location['y']
        self.action.long_press(x=x, y=y).move_to(x=x, y=y + 2500).release().perform()  # Swipe up
        self.action.long_press(x=x, y=y).move_to(x=x, y=y - 2500).release().perform()  # Swipe down

        # Click on search button
        list_of_buttons = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
        self.wait.until(lambda driver: len(list_of_buttons) >= 5)
        search_btn = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
        search_btn[4].click()

        # Click in appointment reservation
        self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.view.View["
                                                                    "@content-desc=\"פרטי השכלה "
                                                                    "ומומחיות\"]/android.widget.TextView[2]")))
        appoint_reserve = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.view.View")
        appoint_reserve[15].click()

        # Weak identification
        self.login.btn_transition_otp().click()
        el2 = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "התחברות ללא סיסמה")
        el2.click()
        self.login.entering_member_id().click()
        self.login.entering_member_id().send_keys("328929997")
        self.driver.hide_keyboard()

        # Click on birthday date
        el1 = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/textInputEditTextDate")
        el1.click()

        # Swipe of birthday year
        els6 = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        while els6[2].text != "2000":
            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(318, 1343)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(324, 1204)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        # Swipe birthday month
        while els6[1].text != "אוק׳":
            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(551, 1343)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(554, 1204)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        # Swipe birthday day
        while els6[0].text != "31":
            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(774, 1340)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(777, 1201)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        # Click on OK
        ok_btn = self.driver.find_element(AppiumBy.ID, "android:id/button1")
        ok_btn.click()
        self.login.btn_enter().click()

        # Choosing a visit type
        self.wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/tvVisitType")))
        els12 = self.driver.find_elements(AppiumBy.CLASS_NAME, "androidx.appcompat.widget.LinearLayoutCompat")
        els12[0].click()

        # Choosing a first available visit date
        self.wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/tvText")))
        list_of_dates = self.driver.find_element(AppiumBy.ID, 'com.ideomobile.maccabi:id/hourPicker')
        list_of_dates.find_element(AppiumBy.CLASS_NAME, "android.view.ViewGroup").click()

        # Approving appointment
        approval_btn = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/buttonApproval")
        approval_btn.click()

        # Test that summoning an appointment was succeeded
        self.assertTrue(self.driver.find_element(AppiumBy.ID,
                                                 "com.ideomobile.maccabi:id/textViewSuccessHeader").text == "התור זומן בהצלחה")

        # Finishing of appointment
        self.wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.ideomobile.maccabi:id/textViewSuccessHeader")))
        finish_btn = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/buttonApproval")
        finish_btn.click()
