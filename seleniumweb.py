from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

class Infow():
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def get_info(self, query):
        self.query = query
        try:
            self.driver.get("https://www.wikipedia.org")
            search = self.driver.find_element(By.XPATH, '//input[@id="searchInput"]')
            search.click()
            search.send_keys(query)
            enter = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
            enter.click()
        except Exception as e:
            print(f"An error occurred: {e}")
        return self



time.sleep(30)
