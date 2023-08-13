from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy


class Bubbles:
    def __init__(self, driver: webdriver):
        self.driver = driver

    def menu_hamburger(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/btn_toggleDrawer")

    def ivExpand(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/ivExpand")

    def bubble_commitment(self):
        rv_bottom_sheet_list = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/rvBottomSheet")
        bubbles_list = []
        for bubble in rv_bottom_sheet_list.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup"):
            bubbles_list.append(bubble)
        return bubbles_list[6]

    def bubble_test_results(self):
        rv_bottom_sheet_list = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/rvBottomSheet")
        bubbles_list = []
        for bubble in rv_bottom_sheet_list.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup"):
            bubbles_list.append(bubble)
        return bubbles_list[1]

    def bubble_queue_reservation(self):
        rv_bottom_sheet_list = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/rvBottomSheet")
        bubbles_list = []
        for bubble in rv_bottom_sheet_list.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup"):
            bubbles_list.append(bubble)
        return bubbles_list[0]

    def korona(self):
        return self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "לחצן למעבר לקורונה - פעולות ומידע")
