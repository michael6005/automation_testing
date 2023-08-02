from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver

class Timeline_commitment:
    def __init__(self, driver: webdriver):
        self.driver = driver

    def btn_fab(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/extendedFab")

    def new_commitment(self):
        timeline_fab_list = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/timeline_fab")
        buttons_fab = []
        for button in timeline_fab_list.find_elements(AppiumBy.CLASS_NAME, "android.widget.ImageButton"):
            buttons_fab.append(button)
        return buttons_fab[0]

    def parent_4242(self):
        return self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "תיבת סימון עבור,53 טסט, לא מסומן")

    def first_created_commitment(self):
        timeline_items_list = self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/timeline_items_list")
        return timeline_items_list.find_element(AppiumBy.CLASS_NAME, "android.view.ViewGroup")


