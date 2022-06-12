from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd

# 啟動瀏覽器工具的選項
options = webdriver.ChromeOptions()
options.add_argument("--headless")              #不開啟實體瀏覽器背景執行
options.add_argument("--start-maximized")         #最大化視窗
options.add_argument("--incognito")               #開啟無痕模式
#options.add_argument("--disable-popup-blocking ") #禁用彈出攔截

# 使用 Chrome 的 WebDriver
PATH='D:/資料20220523備份/數據分析相關/Python/crawler_pratice/webdriver/version102/chromedriver.exe'
driver = webdriver.Chrome(PATH,options = options)
#headers = {'user-agent': '你的user-agent'}

url='https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001007%2C2004001010%2C2016001007%2C2007002002%2C2003002008&keyword=%E6%95%B8%E6%93%9A%E5%88%86%E6%9E%90&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=15&asc=0&sr=99&page=1&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1'
driver.get(url)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[3]/div/div[3]/div[4]/article[1]/div[1]')))

job_title=[]
company=[]
jobtype=[]
region=[]
working_Exp=[]
edu_level=[]
salary=[]

page=1
for i in range(1,639):
    print('第',page,'頁')
    job=driver.find_element(By.XPATH,'//*[@id="js-job-content"]/article[{}]/div[1]'.format(i))
    t = BeautifulSoup(job.get_attribute('outerHTML'), "html.parser")
    job_title.append(t.find('a', class_='js-job-link').text)
    company.append(t.find_all('a')[1].string)
    jobtype.append(t.find_all('li')[2].string)
    region.append(t.find_all('li')[3].string)
    working_Exp.append(t.find_all('li')[4].string)
    edu_level.append(t.find_all('li')[5].string)
    salary.append(t.find('span',class_='b-tag--default').string)
    
    print(i)
    if (i)%20==0:
        page+=1

    if page <15:
        if i%15==0:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="js-job-content"]/article[{}]/div[1]'.format(i+20))))

    elif page <32:
        if (i)%20==0:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(),'手動載入')]")))
            driver.find_elements(By.XPATH,"//*[contains(text(),'手動載入')]")[page-15].click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="js-job-content"]/article[{}]/div[1]'.format(i+20))))
            time.sleep(1)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

time.sleep(3)
driver.quit()

data=pd.DataFrame({'job_title': job_title, 'company': company,'jobtype':jobtype,'region':region,'working_Exp':working_Exp,'edu_level':edu_level,'salary':salary})
print(data.head(10))

print(data.tail(10))

data.to_csv('D:/資料20220523備份/數據分析相關/Python/crawler_pratice/104/data_analysis_0607.csv',index=False)