import os
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

seleniumOptions = Options()
seleniumOptions.headless = True
seleniumOptions.add_argument('start-maximized')
seleniumOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
seleniumOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
seleniumOptions.add_experimental_option('useAutomationExtension', False)
seleniumOptions.add_argument('--disable-blink-features=AutomationControlled')

driver = Chrome(os.getenv('CHROMEDRIVER_PATH'), options=seleniumOptions)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})
