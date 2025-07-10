from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class DriverManager:
    def __init__(self):
        self.driver = None

    def start_driver(self):
        if self.driver is None:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            #options.add_argument('--log-level=1')  # info 이하 로그 숨김
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def get_driver(self):
        return self.driver
        
