import csv

import driver as driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import pandas as pd

from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import StaleElementReferenceException

keyword = input('Enter Keyword : ')
#CROSS BROWSER TESTING
browserName = "chrome"
if browserName == "chrome":
    #options = webdriver.ChromeOptions()
    #options.headless = True
    driver= webdriver.Chrome(ChromeDriverManager().install())
elif browserName =="firefox":
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver= webdriver.Firefox(GeckoDriverManager().install(),options=options)
elif browserName == "safari":
    options = webdriver.SafariOptions()
    options.headless = True
    driver = webdriver.Safari(options=options)
else:
    print('pass correct browser name:'   +browserName)

driver.implicitly_wait(10)
wait=WebDriverWait(driver,10)
driver.get("https://www.glassdoor.com/Job/index.htm")
driver.maximize_window()

#deleting cookies
cookies= driver.get_cookies()
#print(len(cookies))
driver.delete_all_cookies()
cookies= driver.get_cookies()
#print(len(cookies))
driver.find_element_by_xpath(" //input[@id='KeywordSearch']").send_keys(keyword)
where_input = driver.find_element_by_xpath("//input[@id='LocationSearch']")
where_input.send_keys(Keys.CONTROL,"a")
where_input.send_keys(Keys.DELETE)
driver.find_element_by_id("HeroSearchButton").click()

#pagination
# Extracting text of string "Page 1 of 30"
Element = driver.find_element_by_xpath('//*[@id="MainCol"]/div[2]/div[1]').text
print(Element)
# finding index of "of" from string "Page 1 of 30"
a = Element.index('of')
print(a)
# using substring method finding number "30" which is total pages count
s = Element[a+3:]
print(s)
# convert string 30 into data type integer
total_pages = int(s)
for p in range (total_pages):
    driver.find_element_by_xpath("//ul//li//a[@data-test='pagination-next']").click()
    time.sleep(5)

