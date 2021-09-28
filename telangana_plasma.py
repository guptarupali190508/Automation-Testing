import csv
import datetime
import time

from selenium import webdriver



driver = webdriver.Chrome(executable_path='C:\\Users\goyal\Downloads\drivers\chromedriver_win32_1\chromedriver.exe')
driver.get("https://covidtelangana.com")
driver.maximize_window()
time.sleep(2)
plasma=driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div[3]/div/button[2]').click()
time.sleep(2)
Details=driver.find_elements_by_xpath('//*[@id="root"]/div/div/div[2]/div[2]/div/div/div')
l=len(Details)
print(l)
#UT=Updated Time
time_detail = {"time" : [], "T" : []}
def getUpdatedTimeStamp(UT):
    values = UT.split(" ")
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


outer_list = [['Hospital_List','phoneNumber_list','Description_List', 'updated_time_list', 'Plasma_count']]
time.sleep(2)
l=5
for i in range(l):
    Details_1=Details[i].text
    # print(Details_1)
    a = str.splitlines(Details_1)
    print(a)

    inner_list =[]
    #HN=hospital name
    HN=a[0]
    inner_list.append(HN)
    #PH=Phone number
    PH=a[1]
    inner_list.append(PH)
    #DS=Description(email & address)
    DS=a[2]+", "+a[3]
    inner_list.append(DS)
    #UT=updated time
    UT=a[5]
    getUpdatedTimeStamp(UT)
    lastTime = convertedTimeStamp()
    inner_list.append(lastTime)
    #PS=PlasmaCount
    if len(a)==10:
        PS=a[6]+" "+a[7]+","+a[8]+" "+a[9]
    else:
        PS=''
    inner_list.append(PS)
    outer_list.append(inner_list)
with open("D:\\Rupali_Stuff\\telaganaplasma.csv", 'w', newline='') as CSVfile:
    w = csv.writer(CSVfile, delimiter=',')
    for row in outer_list:
        w.writerow(row)
print(outer_list)











