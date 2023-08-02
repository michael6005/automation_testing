import time
import allure
import webbrowser
import pytest
import subprocess
from appium.webdriver.appium_service import AppiumService
from appium.options.android import UiAutomator2Options
from appium import webdriver


@pytest.fixture(scope='class')
def driver():
    appium_service = AppiumService()
    appium_service.start(args=['--address', "127.0.0.1", '--port', "4723", "--base-path", '/wd/hub'])
    # Set up Webdriver options
    options = UiAutomator2Options().load_capabilities({
        'deviceName': 'R58N80FGCCB',
        'platformName': 'Android',
        'platformVersion': '12',
        'app': 'C:/applications/maccabi.apk',
        'autoGrantPermissions': True,
        'unlockType': 'pin',
        'unlockKey': '1111'
    })
    driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
    driver.implicitly_wait(50)
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


if __name__ == '__main__':
    pytest.main()
