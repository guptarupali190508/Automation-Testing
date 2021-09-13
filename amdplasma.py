from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import json

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
      return time.time()*1000 - float(time_detail['time']) *2629743*1000


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
driver = webdriver.Chrome(executable_path="C:\\Users\goyal\Downloads\drivers\chromedriver_win32_1\chromedriver.exe")
driver.get("https://covidamd.com")
time.sleep(2)
driver.find_element_by_xpath("//button[contains(text(),'Plasma')]").click()
driver.maximize_window()
time.sleep(3)
plasma_data = driver.find_elements_by_xpath("/html/body/div/div/div/div[2]/div[2]/div/div/div")
l=len(plasma_data)
#print(l)
temp_list = []
for i in range(l):
    data = plasma_data[i].text
    i=i+1
    a = str.splitlines(data)
    print(a)
    c=[]

    b=a[0]+a[2]+a[3]
    c.append("Gujarat")
    c.append("Plasma")
    c.append(b)
    c.append(a[1])
    getUpdatedTimeStamp(a[5])
    lastTime = convertedTimeStamp()
    c.append(lastTime)
    temp_list.append(c)
    #print(c)
df= pd.DataFrame(temp_list,columns=['State','Category', 'Description','Phone number','Linux_Time'])
#print(df)
for x in df.index:
    test_string = df['Phone number'][x]
    res = [int(i) for i in test_string.split() if i.isdigit()]
    df['Phone number'][x] = str(res)
    #print(df['Phone number'][x])

dictionary = df.to_dict(orient="index")
jsonString = json.dumps(dictionary, indent=4)
print(jsonString)
driver.close()
