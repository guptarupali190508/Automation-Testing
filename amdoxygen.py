from datetime import datetime
from json.decoder import NaN

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import json
import helpers as hp
import functions



time_detail = {"time" : [], "T" : []}


def getUpdatedTimeStamp(lastUpdated):
    values = lastUpdated.split(" ")
    for val in  values:
        if (val.isdigit()):
            time_detail['time']=val
        elif (val == 'minutes'):
            time_detail['T'] = 0
        elif (val == 'hours'):
            time_detail['T'] = 1
        elif (val == 'months'):
            time_detail['T'] = 2

def convertedTimeStamp():
  if (time_detail['T']==0):
      return time.time()*1000 - float(time_detail['time'])*60*1000
  elif (time_detail['T']==1):
      return time.time()*1000- float(time_detail['time']) *60*60*1000
  else:
      return time.time()*1000 - float(time_detail['time']) *2629743*100
      
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

#functions.displayoutput()
driver = webdriver.Chrome(executable_path="C:\\Users\goyal\Downloads\drivers\chromedriver_win32_1\chromedriver.exe")
driver.get("https://covidamd.com/oxygen")
driver.maximize_window()
time.sleep(1)
# srolling window
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

j='Load next 20'
while(j == 'Load next 20'):
    try:
        driver.find_element_by_xpath("//button[contains(text(),'Load next 20')]").click()
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        j = driver.find_element_by_xpath("//button[contains(text(),'Load next 20')]").text
    except:
        break
#functions.LoadNext("Load next 20","//button[contains(text(),'Load next 20')]",driver)
oxygen_data = driver.find_elements_by_xpath("/html/body/div/div/div/div[2]/div[2]/div/div/div/div")
l = len(oxygen_data)
print(l)
temp_list = []
for i in range(l-1):
    i=i+1
    data = oxygen_data[i].text
    a = str.splitlines(data)
    #print(a)
    c = []
    b = a[0] + a[5] + a[4]
    c.append('Gujarat')
    c.append("Oxygen")
    c.append(b)
    c.append(a[1])

    functions.getUpdatedTimeStamp(a[3])
    lastTime = functions.convertedTimeStamp()
    c.append(lastTime)
    temp_list.append(c)


df = pd.DataFrame(temp_list,columns=['State', 'Category','Description','Contact','Time'])

#print(df)

for x in df.index:
    test_string = df['Contact'][x]
    res = [int(i) for i in test_string.split() if i.isdigit()]
    df['Contact'][x] = str(res)
    #print(df['Contact'][x])

dictionary = df.to_dict(orient="index")

print(dictionary)

jsonString = json.dumps(dictionary, indent=4)
print(jsonString)
#response = hp.send(params)
#print(functions.df_to_json(df))

driver.close()