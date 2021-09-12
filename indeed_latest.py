import csv
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

# keyword = input('Enter Keyword : ')
keyword = 'postman'
driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
wait = WebDriverWait(driver, 10)
driver.get('https://www.indeed.com/jobs?q=' + keyword)
time.sleep(50)

date_posted = driver.find_element_by_id('filter-dateposted')
date_posted.click()
last_24hours_data = driver.find_element_by_link_text('Last 24 hours')
last_24hours_data.click()

time.sleep(5)

jobs = driver.find_elements_by_xpath("//a[contains(@class,'tapItem')]")
scraped_descriptions = []
jobDetails_list = [['job_title', 'job_category', 'company_name', 'job_location', 'job_description', 'job_link',
                    'date_of_posting', 'current_timestamp']]
job_title: str = ''
job_category: str = ''
company_name: str = ''
job_location: str = ''
job_description: str = ''
job_link: str = ''
date_of_posting: str = ''
current_timestamp: str = ''

page_count = driver.find_elements_by_xpath('//span[@class="pn"]')

for count in range(len(page_count)):
    for job in jobs:

        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'tapItem')))
        try:  # click on the job card and add its description to descriptions list
            job.click()
            wait.until(EC.presence_of_element_located((By.ID, 'vjs-container')))
            iframe = driver.find_element_by_xpath("//iframe[@id='vjs-container-iframe']")
            driver.switch_to.frame(iframe)

            # Job Titles
            jobTitles = driver.find_elements_by_xpath("//div[@class='jobsearch-JobInfoHeader-title-container ']/h1")
            for title in jobTitles:
                job_title = str.replace(title.text, '\n- job post', '')
                # print('##############' + str.replace(title.text, '\n', '') + '################')

            # 'job_category'
            jCat = driver.find_elements_by_xpath("//span[@class='jobsearch-JobMetadataHeader-item  icl-u-xs-mt--xs']")
            for jc in jCat:
                job_category = str.replace(jc.text, '-', '')

            # company name
            c_name = driver.find_elements_by_xpath("//div[contains(@class,'jobsearch-JobInfoHeader-subtitle')]/div/div/a")
            for cn in c_name:
                company_name = cn.text

            # Company Location
            job_loc = driver.find_elements_by_xpath("//div[contains(@class,'jobsearch-JobInfoHeader-subtitle')]/div[not(@class)]")
            for jl in job_loc:
                job_location = jl.text

            # Job Descriptions
            jds = driver.find_elements_by_xpath("//div[@id='jobDescriptionText']")
            for jd in jds:
                job_description = jd.text

            # 'job_link'
            jLink = driver.find_elements_by_xpath("//div[@class='jobsearch-IndeedApplyButton']/span")
            for jlnk in jLink:
                job_link = jlnk.get_attribute('data-indeed-apply-joburl')

            # 'date_of_posting', # 'current_timestamp'
            jTime = driver.find_elements_by_xpath("//div[@class ='jobsearch-JobMetadataFooter']/div[not(@class)]")
            for jt in jTime:
                date_of_posting = jt.text
                now = datetime.now()
                current_timestamp = now.strftime("%H:%M:%S")

            # Save current row and move to Next Row
            driver.switch_to.default_content()
            jobDetails_list.append([job_title, job_category, company_name, job_location, job_description, job_link,
                                    date_of_posting, current_timestamp])


        except ElementClickInterceptedException:
            print(str(ElementClickInterceptedException))
next_page = driver.find_elements_by_xpath('//span[@class="np"]')

     if (len(next_page) == 1):
        next_page[0].click()
     else:
        next_page[1].click()

with open("D:\scrapeIndeed.csv", 'w', newline='') as CSVfile:
    w = csv.writer(CSVfile, delimiter=',')
    for row in jobDetails_list:
        w.writerow(row)

# print(jobDetails_list)
driver.close()
driver.quit()