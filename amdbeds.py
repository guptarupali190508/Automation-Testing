from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import json

import functions

functions.displayoutput()
driver = webdriver.Chrome(executable_path="C:\\Users\goyal\Downloads\drivers\chromedriver_win32_1\chromedriver.exe")
driver.get("https://covidamd.com")
time.sleep(1)

driver.find_element_by_xpath("//button[contains(text(),'Beds')]").click()
driver.maximize_window()
time.sleep(1)

driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
i='Load next 20'
while(i == 'Load next 20'):
    try:
        driver.find_element_by_xpath("//button[contains(text(),'Load next 20')]").click()
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        i = driver.find_element_by_xpath("//button[contains(text(),'Load next 20')]").text
    except:
        break

time.sleep(1)
plus_button = driver.find_elements_by_tag_name("strong")
l = len(plus_button)
#print(l)
for a in range(l):
    plus_button[a].click()
Beds_data = driver.find_elements_by_class_name("card-body")
data = Beds_data[0].text
a = str.splitlines(data)
#print(a)
b = a[6:]
print(b)

o_lst = []
k=0
for j in range(l):
    i_lst = []
    i_lst.append('Gujarat')
    i_lst.append(b[k+1])
    c=b[k]+" ; "+b[k+5][9:]
    i_lst.append(c)
    i_lst.append(b[k + 3][7:])
    m,n,o,p = b[k + 2].split(' / ? ')
    i_lst.append(n)
    o_lst.append(i_lst)
    k=k+7
print(o_lst)

df = pd.DataFrame(o_lst,columns=['State', 'District','Description','Contact','Beds With Oxgen'])
dictionary = df.to_dict(orient="index")

print(dictionary)

jsonString = json.dumps(dictionary, indent=4)
print(jsonString)


driver.close()

