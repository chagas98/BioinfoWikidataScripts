import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep, ctime

link = "https://www.linkedin.com/search/results/people/?geoUrn=%5B%22106057199%22%5D&keywords=bioinformatician&origin=FACETED_SEARCH&sid=gHz" #SEARCH: BIOINFORMATICIAN BRAZIL
driverpath = r"/home/biowitcher/WebScrapping/chromedriver_linux64/chromedriver"
save_output = r"/home/biowitcher/BioinfoWikidatascripts/Data_Bioinfo_Linkedin.csv"


class LinkedinGet():
    def __init__(self):
        
        self.final_data = []
        
        #Headless browser
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)
        self.login()
        
        sleep(2)
        
        self.driver.get(link)
        
        sleep(2)

        self.ClickNextButton()
        
            
        print(self.final_data)
        pd.DataFrame(self.final_data).to_csv(save_output)
        

    
    def check_exists_by_id(self,selector):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[aria-label='Next']")))
        except NoSuchElementException:
            return True
        return False  

    def login(self):
    
        self.driver.get('https://www.linkedin.com')
        username = self.driver.find_element("name", 'session_key')
        username.send_keys("EMAIL_USERNAME")
        password = self.driver.find_element("name", 'session_password')
        password.send_keys("PASSWORD")
        log_in_button = self.driver.find_element(By.XPATH, "//button[@ type='submit']")
        log_in_button.click()
          
     
    def GetData(self):

        item_search = list(map(lambda x:x.text, self.driver.find_elements(By.CLASS_NAME,"mb1")))
        sleep(2)
        for i in range(len(item_search)):
            
            if re.search("degree connection", item_search[i]) and "LinkedIn" not in item_search[i]:
                
                item = item_search[i].split("\n")

                if re.search("degree connection", item_search[i+1]) or "LinkedIn" in item_search[i+1]: 
                
                    self.final_data.append({
                        "Name": item[0],
                        "Field": item[4],
                        "Location": item[5],
                        "More": ""
                    })
                  
                else:
                    self.final_data.append({
                        "Name": item[0],
                        "Field": item[4],
                        "Location": item[5],
                        "More": item_search[i+1]
                    })
        
    def ClickNextButton(self):

        limit_clicks = True
        #https://medium.com/@kurumert/web-scraping-linkedin-job-page-with-selenium-python-e0b6183a5954
        while limit_clicks:
                
            sleep(3)
            #next_pages = self.driver.find_elements(By.CLASS_NAME,"artdeco-pagination__indicator artdeco-pagination__indicator--number ember-view")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
             
            #next_page =WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[aria-label='Next']"))) 
            try:
                self.GetData()
                sleep(3)
                next_page = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[aria-label='Next']")))
        
            except TimeoutException:
                return limit_clicks == False
            #return limit_clicks == True 
            #next_page = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next']")
            next_page.click()
            #limit_clicks = False

        

if __name__ == "__main__":
   
    bot = LinkedinGet()
    bot.run()