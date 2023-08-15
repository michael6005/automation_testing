from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver


class Login:
    def __init__(self, driver: webdriver):
        self.driver = driver

    def btn_transition_otp(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_negative")

    def tab_enter_with_password(self):
        return self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "התחברות באמצעות סיסמה")

    def entering_member_id(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/textInputEditText")

    def entering_password(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/textInputEditTextPassword")

    def btn_enter(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/enterButton")

    def approve_push_notification(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btnAction2")

    # Approving phone number on the pop-up of approving phone number
    def approve_phone_num(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btnConfirm")

    # Pick on the parent family member
    def pick_parent(self):
        list_of_members = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/familyMemberPicker")
        members = []
        for member in list_of_members.find_elements(AppiumBy.CLASS_NAME, "android.widget.LinearLayout"):
            members.append(member)
        return members[0]
