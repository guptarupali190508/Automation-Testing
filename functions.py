import time
from selenium import webdriver
import json
import pandas as pd

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

def LoadNext(button_name,button_xpath,driver):
    j = button_name
    while (j == button_name):
        try:
            driver.find_element_by_xpath(button_xpath).click()
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            j = driver.find_element_by_xpath(button_xpath).text
        except:
            break

def df_to_json(df):
    dict_out = df.to_dict(orient="index")
    json_out = json.dumps(dict_out, indent=4)
    return json_out

def displayoutput():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)