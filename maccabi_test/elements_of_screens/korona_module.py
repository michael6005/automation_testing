from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
class Korona:

    def __init__(self, driver: webdriver):
        self.driver = driver

    def vac_performed_btn(self):
        return self.driver.find_element(AppiumBy.ID, "com.ideomobile.maccabi:id/vaccinationsPerformedButton")

    



