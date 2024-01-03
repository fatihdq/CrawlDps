from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import time
import random

XPATH_NAME = '//*[@id="root"]/main/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div[3]/div[3]/div[1]/p[1]'
XPATH_TPS = '//*[@id="root"]/main/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div[3]/div[3]/div[1]/p[2]'
XPATH_KABUPATEN = '//*[@id="root"]/main/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div[3]/div[3]/div[3]/div[1]/p[1]'
XPATH_KECAMATAN = '//*[@id="root"]/main/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div[3]/div[3]/div[3]/div[1]/p[2]'
XPATH_KELURAHAN = '//*[@id="root"]/main/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div[3]/div[3]/div[3]/div[1]/p[3]'
XPATH_ALAMAT = '//*[@id="root"]/main/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div[3]/div[3]/div[3]/div[2]/p/span[2]'

XPATH_INVALID = '//*[@id="root"]/main/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/h2/b'

XPATH_BUTTON_SEARCH = '//*[@id="root"]/main/div[4]/div/div/div/div/div/div[2]/div/button'
XPATH_BUTTON_BACK = '//*[@id="root"]/main/div[4]/div/div/div/div/div/div[2]/button'

class DpsCrawler(object):
    def __init__(self,headless):
        self.url = 'https://cekdptonline.kpu.go.id/'
        self.headless = headless
        
        self.driver = webdriver.Chrome(options=self.settings(self.headless))
        if self.headless:
            stealth(self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        
    def settings(self,headless):
        chrome_options = Options()

        chrome_options.add_argument("--nogpu")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--enable-javascript")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-application-cache')
        chrome_options.add_argument("--disable-dev-shm-usage")

        if headless == False:
            ## Window Size
            chrome_options.add_argument("window-size={},{}".format(1080,720))
        else:
            ## Headless
            chrome_options.add_argument("start-maximized")
            chrome_options.add_argument('--headless')
            chrome_options.add_experimental_option(
                "prefs", {
                    # block image loading
                    "profile.managed_default_content_settings.images": 2,
                }
            )
            
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("prefs", {
            "safebrowsing.enabled": False
            })

        return chrome_options

    def start(self):
        try:
            self.driver.get(self.url)
        except Exception as e:
            print(e)
    
    def quit(self):
        self.driver.quit()
    
    def input(self,nik,idx,row):
        try:
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.TAG_NAME,'input')))
            self.driver.find_element(By.TAG_NAME,'input').clear()
            for ni in str(nik):
                self.driver.find_element(By.TAG_NAME,'input').send_keys(ni)
                time.sleep(random.uniform(0,0.5))
            return True
        except:
            self.driver.save_screenshot(f'./ss/error_input/not_registered_{row}_{nik}.png')
            print(f"{nik}: Handle Input NIK Error!")
            return False

    def clickSearch(self):
        try:
            self.driver.find_element(By.XPATH, XPATH_BUTTON_SEARCH).click()
        except:
            print("Handle Click Search Error!")

    def clickBack(self):
        try:
            self.driver.find_element(By.XPATH, XPATH_BUTTON_BACK).click()
        except:
            print("Handle Click Search Error!")

    def getData(self,data,idx,row,nik):
        itter = 1
        loading = True
        while itter <= 3 and loading==True:
            try:
                WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, XPATH_NAME)))
                data.loc[idx,'DPT'] = "Registered"
                data.loc[idx,'NAMA PEMILIH'] = str(self.driver.find_element(By.XPATH, XPATH_NAME).text.split('\n')[-1])
                data.loc[idx,'TPS'] = str(self.driver.find_element(By.XPATH, XPATH_TPS).text.split('\n')[-1])
                data.loc[idx,'KABUPATEN'] = str(self.driver.find_element(By.XPATH, XPATH_KABUPATEN).text.split('\n')[-1])
                data.loc[idx,'KECAMATAN'] = str(self.driver.find_element(By.XPATH, XPATH_KECAMATAN).text.split('\n')[-1])
                data.loc[idx,'KELURAHAN'] = str(self.driver.find_element(By.XPATH, XPATH_KELURAHAN).text.split('\n')[-1])
                data.loc[idx,'ALAMAT TPS'] = str(self.driver.find_element(By.XPATH, XPATH_ALAMAT).text)
                loading = False
                time.sleep(2)
            except:
                try:
                    self.driver.find_element(By.XPATH, XPATH_INVALID).text
                    data.loc[idx,'DPT'] = "Not Registered"
                    self.driver.save_screenshot(f'./ss/not_registered/not_registered_{row}_{nik}_{itter}.png')
                    loading= False
                except:
                    loading= True
                time.sleep(2)
            itter = itter + 1
        if loading == True:
            data.loc[idx,'DPT'] = "Invalid"
            self.driver.save_screenshot(f'./ss/invalid/invalid_{row}_{nik}_{itter}.png')
        return data
    
    def crawl(self,data,idx,row):
        if self.input(data.loc[idx,'NIK'],idx,row):
            self.clickSearch()
            data = self.getData(data,idx,row,data.loc[idx,'NIK'])
            self.clickBack()
        else:
            self.driver.refresh()
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, XPATH_NAME)))
        
        return data