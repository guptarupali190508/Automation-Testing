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

driver.find_element_by_xpath(" //header/div[1]/div[1]/div[1]/div[2]/span[2]/*[1]").click()
time.sleep(2)
driver.find_element_by_xpath("//header/div[@id='PrimaryDropdown']/ul[1]/li[2]/span[1]").click()
time.sleep(2)
outer_list=[['Job Title','Company Name','Job Location','Job Description','Job Posted Time','Current Timestamp','Job Link']]
#pagination
# Extracting text of string "Page 1 of 30"
Element = driver.find_element_by_xpath('//*[@id="MainCol"]/div[2]/div[1]').text
print(Element)
# finding index of "of" from string "Page 1 of 30"
a = Element.index('of')
# using substring method finding number "30" which is total pages count
s = Element[a+3:]
print(s)
# convert string 30 into data type integer
total_pages = int(s)
for p in range(total_pages):

    data = driver.find_elements_by_xpath("//body/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/section[1]/article[1]/div[1]/ul[1]/li")
    l = len(data)
    #l = 2
    for d in range(l):
        inner_list = []
        try:
            data[d].click()
        except StaleElementReferenceException:
            data = driver.find_elements_by_xpath("//body/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/section[1]/article[1]/div[1]/ul[1]/li")
            data[d].click()
        try:
            pop_up_elem = driver.find_element_by_xpath('//*[@id="JAModal"]/div/div[2]/span')
            pop_up_elem.click()
            #print("pop 1")
        except:
            print("No pop")
        #jt = job title
        jt = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[2]').text
        inner_list.append(jt)
        time.sleep(2)
        #cn = company name
        cn1 = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]').text
        cn = cn1.split("\n")[0]
        inner_list.append(cn)
        #jl = job location
        jl = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div/div[1]/div[3]').text
        inner_list.append(jl)
        driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
        time.sleep(2)
        # xpath for showmore
        driver.find_element_by_xpath('//*[@id="JobDescriptionContainer"]/div[2]').click()
        time.sleep(2)
        #jd = job description
        jd = driver.find_element_by_id('JobDescriptionContainer').text
        inner_list.append(jd)
        #jtp = job time posted
        #wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="MainCol"]/div[1]/ul/li[2]/div[2]/div[2]/div/div[2]')))
        #jtp  = driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li[2]/div[2]/div[2]/div/div[2]').text
        jtp = '24hr'
        inner_list.append(jtp)
        #ct = current timestamp
        ct = datetime.datetime.now()
        inner_list.append(ct)
        #jl= job link
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[2]/div/div[1]/div[1]/a')))
            j = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[2]/div/div[1]/div[1]/a')
            jl = j.get_attribute('href')
        except:
            jl = ''
        inner_list.append(jl)
        outer_list.append(inner_list)
    driver.find_element_by_xpath("//ul//li//a[@data-test='pagination-next']").click()
    time.sleep(3)
with open("C:\\Users\\goyal\\Downloads\\glassdoorhackathon\\" + keyword + ".csv", 'w', encoding='utf-8',newline='') as CSVfile:
    w = csv.writer(CSVfile, delimiter=',')
    for row in outer_list:
        w.writerow(row)



''''
    #next page
    try:
        np_sign = driver.find_element_by_xpath('//*[@id="FooterPageNav"]/div/ul/li[7]/a').is_enabled()
    except:
        np_sign = False
    if np_sign == True:
        driver.find_element_by_xpath('//*[@id="FooterPageNav"]/div/ul/li[7]/a').click()
    i=i+1

#df = pd.DataFrame(outer_list)
print(df)
#df.to_csv("C:\\Users\\goyal\\Downloads\\glassdoorhackathon\\"+keyword+"_df.csv")

driver.close()
'''