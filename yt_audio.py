from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

class Music:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def play(self, query):
        self.query = query
        self.driver.get("https://www.youtube.com/results?search_query=" + query)
        time.sleep(3)  # Give some time for the page to load
        videos = self.driver.find_element(By.XPATH, '//*[@id="dismissible"]/div')
        videos.click()

#assist = Music()
#assist.play('pain belevier')

time.sleep(30)  # This will keep the browser open for 30 seconds
