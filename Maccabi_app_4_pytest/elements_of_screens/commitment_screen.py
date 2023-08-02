from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver

class Commitment_screen:
    def __init__(self, driver: webdriver):
        self.driver = driver

# Elements of first screen commitment
    def choice_reference(self):
        referral_selection = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/cmpReferralSelection")
        return referral_selection.find_element(AppiumBy.CLASS_NAME, "android.widget.TextView")

    def i_have_no_reference(self):
        rv_list = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/rvList")
        rv = []
        for i in rv_list.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
            rv.append(i)
        return rv[1]

    def medical_field(self):
        return self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "בחירת תחום רפואי או מחלקה")

    def entering_medical_field(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/etSearch")

    def btn_close(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/ibClose")

    def btn_continue(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btnContinue")

    def eyes_medical_field(self):
        rv_code_list = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/rvCodeList")
        rv_codes = []
        for rv in rv_code_list.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup"):
            rv_codes.append(rv)
        return rv_codes[1]

# Elements of second screen commitments
    def btn_not_appointment(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/buttonDidntSetAppointment")

    def btn_approve(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_approve")

# Elements of third screen commitments

    def add_file(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/linearLayoutAddFile")


    def my_file(self):
        file_list = self.driver.find_element(AppiumBy.ID, "com.google.android.documentsui:id/dir_list")
        my_files = []
        for file in file_list.find_elements(AppiumBy.CLASS_NAME, "android.widget.FrameLayout"):
            my_files.append(file)
        return my_files[0]

    def icon_my_files(self):
        iv_items_list = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/lv_items")
        iv_items = []
        for iv in iv_items_list.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup"):
            iv_items.append(iv)
        return iv_items[0]

    def icon_camera(self):
        iv_items_list = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/lv_items")
        iv_items = []
        for iv in iv_items_list.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup"):
            iv_items.append(iv)
        return iv_items[2]

    def send_request(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_sendRequest")



