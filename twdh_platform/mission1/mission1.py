import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriAver')

# https://yanwei-liu.medium.com/python爬蟲學習筆記-一-beautifulsoup-1ee011df8768
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import json
import base64
import requests
import csv

from os import listdir
from os.path import isfile, join

import pandas as pd
import os
from datetime import datetime
from google.colab import files

from IPython.display import clear_output 



# 只要爬一次目錄，有和目錄數量不同再爬CSV。
# 碰到星星的時候去抓csv


# # 國史館檔案史料文物查詢系統

# for f in [f for f in listdir("./") if isfile(join("./", f))]:
#   os.remove(f)

# wd = webdriver.Chrome('chromedriver', options =chrome_options)
# url = "https://ahonline.drnh.gov.tw/index.php?act=Archive"
# wd.get(url)
# df = pd.DataFrame(columns=["id", "up", "site", "data-set", "marker", "name", "number"])

# znames = wd.find_elements(by=By.CSS_SELECTOR, value='.zname')
# dataZnames = []
# for zname in znames:
#   dataZnames.append(zname.get_attribute("data-zname"))

# c = 1
# for dataZname in dataZnames:
#   datasets = []
#   print("=== " + dataZname + " ===")
#   url = "https://ahonline.drnh.gov.tw/index.php?act=Archive"
#   wd.get(url)
#   zname = wd.find_element(by=By.CSS_SELECTOR, value='.zname[data-zname="'+dataZname+'"]')
#   zname.click()
#   if len(wd.find_elements(by=By.CSS_SELECTOR, value='ul.level_group')):
#     level_group = wd.find_element(by=By.CSS_SELECTOR, value='ul.level_group')
#     for li in level_group.find_elements(by=By.CSS_SELECTOR, value='li'):
      
#       # text 必須是 display!=none 因此要改用 innerHTML，有些裡面又有tag包著，所以要用b4s包著
#       name = li.find_element(by=By.CSS_SELECTOR, value='span.name').text
#       number = li.find_element(by=By.CSS_SELECTOR, value='span.count').text
#       df = df.append({
#           "id": li.get_attribute("id"),
#           "up": li.get_attribute("up"),
#           "site": li.get_attribute("site"),
#           "data-set": li.get_attribute("data-set"),
#           "marker": "*" if len(li.find_elements(by=By.CSS_SELECTOR, value='i.fa-asterisk'))==1 else "-",
#           "name": name,
#           "number": number
#       }, ignore_index=True)
#       print(str(c) + " " + li.get_attribute("id") + " " + name + " " + number + " "+ li.get_attribute("switch") + " " + str(len(li.find_elements(by=By.CSS_SELECTOR, value='i.fa-asterisk'))))
#       c+=1
#       if li.get_attribute("switch")=="0" and len(li.find_elements(by=By.CSS_SELECTOR, value='i.fa-asterisk'))==0:
#         li.find_element(by=By.CSS_SELECTOR, value='.option').click() # 打開加號，要有顯示出來才能點，不然會跳element not interactable exception
#       if len(li.find_elements(by=By.CSS_SELECTOR, value='i.fa-asterisk'))==1:
#         datasets.append(li.get_attribute("data-set")); # 遇到*號 把data-set存下來
  
#   for dataset in datasets:
#     print(dataset)
#     wd.execute_script("var search = {'query':[{'field':'series','value':'"+dataset+"'}]}; location.href = 'index.php?act=Archive/search/'+encodeURIComponent(Base64M.encode(JSON.stringify(search)));");
#     # 這幾個網站的方法是會將搜尋結果存到資料庫 產生id 
#     if len(wd.find_elements(By.NAME, "user_select_target"))>0: # 李元簇副總統文物/視聽/[報導介紹]/[新增階層]=>壞了
#       export_type = wd.find_elements(By.NAME, "user_select_target")[1].get_attribute("value")
#       script = "window.open('index.php?act=Archive/export/result/'+encodeURIComponent(Base64.encode(\""+export_type+"\")));";
#       wd.execute_script(script)
#       time.sleep(1)
#   time.sleep(1)

# df.to_csv('國史館檔案史料文物查詢系統.csv',encoding='utf-8-sig')
# files.download("國史館檔案史料文物查詢系統.csv")
# df.head()

# wd = webdriver.Chrome('chromedriver', options =chrome_options)

# df = pd.read_csv("國史館檔案史料文物查詢系統 04261124.csv")
# datasets = df[df["marker"]=="*"]["data-set"].tolist()
# url = "https://ahonline.drnh.gov.tw/index.php?act=Archive"
# wd.get(url)
# count = 1
# for dataset in datasets:
#   if count > 0  :
#     try: 
#       search_field = wd.find_element(By.ID, "search_field")
#       Select(search_field).select_by_value("series")

#       search_input = wd.find_element(By.ID, "search_input")
#       search_input.clear()
#       search_input.send_keys(dataset)
#       search_input.send_keys(Keys.ENTER)
#       time.sleep(0.5)   

#       數量 = wd.find_element(By.CLASS_NAME, "record_summary").find_element(By.TAG_NAME, "span").text
#       數量 = int("".join([c for c in 數量 if c.isdigit()]))
#       print(str(count) + " " + datetime.now().strftime("%Y/%m/%d/ %H:%M:%S") + " " + dataset + " " +  str(數量))
#       export_type = wd.find_elements(By.NAME, "user_select_target")[1].get_attribute("value")
#       script = "window.open('index.php?act=Archive/export/result/'+encodeURIComponent(Base64.encode(\""+export_type+"\")));";
#       wd.execute_script(script)
#       time.sleep(0.5)
#     except:
#       print(str(count) + " " + dataset + " " +  "錯誤")
#   count += 1

# # 臺灣省議會史料總庫

# wd = webdriver.Chrome('chromedriver', options =chrome_options)
# url = "https://drtpa.th.gov.tw/index.php?act=Archive/index"
# wd.get(url)
# level_group = wd.find_element(by=By.CSS_SELECTOR, value='.level_group')

# # level_group.find_elements_by_css_selector('li[switch="1"]') #1是開啟 0是關閉
# # <i class="fa fa-minus open" aria-hidden="true"></i> 已經打開 
# # <i class="fa fa-plus hide" aria-hidden="true"></i> 可以打開
# # <i class="fa fa-asterisk" aria-hidden="true"></i> 最後

# df = pd.DataFrame(columns=["id", "up", "site", "data-set", "marker", "name", "number"])

# def 轉(標記, li):
#   if 標記 == "-":
#     print(li.get_attribute("id") + " - " + li.find_elements(by=By.TAG_NAME, value='span')[1].text + " " + li.find_element(by=By.CSS_SELECTOR, value='span.count').text )
#   return {
#     "id": li.get_attribute("id"),
#     "up": li.get_attribute("up"),
#     "site": li.get_attribute("site"),
#     "data-set": li.get_attribute("data-set"),
#     "marker": 標記,
#     "name": li.find_elements(by=By.TAG_NAME, value='span')[1].text, # li.find_element(by=By.CSS_SELECTOR, value='span.name').text,
#     "number": int(li.find_element(by=By.CSS_SELECTOR, value='span.count').text.replace("冊", "").replace("件", "")) # li.find_element(by=By.CSS_SELECTOR, value='span.count').text
#   }

# def 點(id):
#   global df
#   time.sleep(0.2) # 被按了之後會去API抓下方的tree
#   if len(level_group.find_elements(by=By.CSS_SELECTOR, value='li[up="'+id+'"]'))>0:
#     for li in level_group.find_elements(by=By.CSS_SELECTOR, value='li[up="'+id+'"]'):
#       if len(li.find_elements(by=By.CSS_SELECTOR, value='i.fa-asterisk'))==0:
#         df = df.append(轉("-", li), ignore_index=True)
#         li.find_element(by=By.CSS_SELECTOR, value='span.option').click()
#         點(li.get_attribute("id"))
#       else:
#         df = df.append(轉("*", li), ignore_index=True)
#         # print(li.get_attribute("id") + " * " + li.find_element(by=By.CSS_SELECTOR, value='span.name').text + " " + li.find_element(by=By.CSS_SELECTOR, value='span.count').text )
#   else:
#     點(id) # 代表沒有出來重等一次

# for li in level_group.find_elements(by=By.CSS_SELECTOR, value='li'):
#   if li.get_attribute("switch")=="0":
#     if len(li.find_elements(by=By.CSS_SELECTOR, value='i.fa-asterisk'))==0:
#       df = df.append(轉("-", li), ignore_index=True)
#       li.find_element(by=By.CSS_SELECTOR, value='span.option').click()
#       點(li.get_attribute("id"))
#     else:
#       df = df.append(轉("*", li), ignore_index=True)
#   else:
#     df = df.append(轉("-", li), ignore_index=True)

# df.to_csv('臺灣省議會史料總庫.csv',encoding='utf-8-sig')
# files.download("臺灣省議會史料總庫.csv")
# df.head()

# wd = webdriver.Chrome('chromedriver', options =chrome_options)

# df = pd.read_csv("臺灣省議會史料總庫 04261026.csv")
# datasets = df[df["marker"]=="*"]["data-set"].tolist()
# url = "https://drtpa.th.gov.tw/index.php?act=Archive/index"
# wd.get(url)
# count = 1
# for dataset in datasets:
#   if count > 0 :
#     try: 
#       search_input = wd.find_element(By.ID, "search_input")
#       search_input.clear()
#       search_input.send_keys(dataset)
#       search_input.send_keys(Keys.ENTER)
#       time.sleep(1)

#       數量 = wd.find_element(By.CLASS_NAME, "record_summary").find_element(By.TAG_NAME, "span").text
#       數量 = int("".join([c for c in 數量 if c.isdigit()]))
#       print(str(count) + " " + dataset + " " +  str(數量))
#       export_type = wd.find_elements(By.NAME, "user_select_target")[1].get_attribute("value")
#       script = "window.open('index.php?act=Archive/export/result/'+encodeURIComponent(Base64.encode(\""+export_type+"\")));";
#       wd.execute_script(script)
#     except:
#       print(str(count) + " " + dataset + " " +  "錯誤")
#   count += 1

# # 國史館臺灣文獻館文獻檔案查詢系統

# wd = webdriver.Chrome('chromedriver', options =chrome_options)
# url = "https://onlinearchives.th.gov.tw/index.php?act=Archive"
# wd.get(url)
# level_group = wd.find_element(by=By.CSS_SELECTOR, value='.level_group')

# # level_group.find_elements_by_css_selector('li[switch="1"]') #1是開啟 0是關閉
# # <i class="fa fa-minus open" aria-hidden="true"></i> 已經打開 
# # <i class="fa fa-plus hide" aria-hidden="true"></i> 可以打開
# # <i class="fa fa-asterisk" aria-hidden="true"></i> 最後

# df = pd.DataFrame(columns=["id", "up", "site", "data-set", "marker", "name", "number"])

# def 轉(標記, li):
#   if 標記 == "-":
#     print(li.get_attribute("id") + " - " + li.find_elements(by=By.TAG_NAME, value='span')[1].text + " " + li.find_element(by=By.CSS_SELECTOR, value='span.count').text )
#   return {
#     "id": li.get_attribute("id"),
#     "up": li.get_attribute("up"),
#     "site": li.get_attribute("site"),
#     "data-set": li.get_attribute("data-set"),
#     "marker": 標記,
#     "name": li.find_elements(by=By.TAG_NAME, value='span')[1].text, # li.find_element(by=By.CSS_SELECTOR, value='span.name').text,
#     "number": int(li.find_element(by=By.CSS_SELECTOR, value='span.count').text.replace("冊", "").replace("件", "")) # li.find_element(by=By.CSS_SELECTOR, value='span.count').text
#   }

# def 點(id):
#   global df
#   time.sleep(0.2) # 被按了之後會去API抓下方的tree
#   if len(level_group.find_elements(by=By.CSS_SELECTOR, value='li[up="'+id+'"]'))>0:
#     for li in level_group.find_elements(by=By.CSS_SELECTOR, value='li[up="'+id+'"]'):
#       if len(li.find_elements(by=By.CSS_SELECTOR, value='i.fa-asterisk'))==0:
#         df = df.append(轉("-", li), ignore_index=True)
#         li.find_element(by=By.CSS_SELECTOR, value='span.option').click()
#         點(li.get_attribute("id"))
#       else:
#         df = df.append(轉("*", li), ignore_index=True)
#         # print(li.get_attribute("id") + " * " + li.find_element(by=By.CSS_SELECTOR, value='span.name').text + " " + li.find_element(by=By.CSS_SELECTOR, value='span.count').text )
#   else:
#     點(id) # 代表沒有出來重等一次

# for li in level_group.find_elements(by=By.CSS_SELECTOR, value='li'):
#   if li.get_attribute("switch")=="0":
#     if len(li.find_elements(by=By.CSS_SELECTOR, value='i.fa-asterisk'))==0:
#       df = df.append(轉("-", li), ignore_index=True)
#       li.find_element(by=By.CSS_SELECTOR, value='span.option').click()
#       點(li.get_attribute("id"))
#     else:
#       df = df.append(轉("*", li), ignore_index=True)
#   else:
#     df = df.append(轉("-", li), ignore_index=True)

# df.to_csv('國史館臺灣文獻館文獻檔案查詢系統.csv',encoding='utf-8-sig')
# files.download("國史館臺灣文獻館文獻檔案查詢系統.csv")
# df.head()

# wd = webdriver.Chrome('chromedriver', options =chrome_options)

# df = pd.read_csv("國史館臺灣文獻館文獻檔案查詢系統 0427 0530.csv")
# datasets = df[df["marker"]=="*"]["data-set"].tolist()
# url = "https://onlinearchives.th.gov.tw/index.php?act=Archive"
# wd.get(url)
# count = 1
# for dataset in datasets:
#   if count > 0 :
#     try: 
#       search_input = wd.find_element(By.ID, "search_input")
#       search_input.clear()
#       search_input.send_keys(dataset)
#       search_input.send_keys(Keys.ENTER)
#       time.sleep(0.5)

#       數量 = wd.find_element(By.CLASS_NAME, "record_summary").find_element(By.TAG_NAME, "span").text
#       數量 = int("".join([c for c in 數量 if c.isdigit()]))
#       print(str(count) + " " + datetime.now().strftime("%Y/%m/%d/ %H:%M:%S") + " " + dataset + " " +  str(數量))
#       export_type = wd.find_elements(By.NAME, "user_select_target")[1].get_attribute("value")
#       script = "window.open('index.php?act=Archive/export/result/'+encodeURIComponent(Base64.encode(\""+export_type+"\")));";
#       wd.execute_script(script)
#       time.sleep(0.5)
#     except:
#       print(str(count) + " " + dataset + " " +  "錯誤")
#   count += 1

# # 地方議會議事錄

# wd = webdriver.Chrome('chromedriver', options=chrome_options)
# url = "https://journal.th.gov.tw/query.php"
# wd.get(url)
# wd.execute_script("UserLoginSubmit('Guestlogin');") # 需要先登入
# df = pd.DataFrame(columns=["id", "up", "site", "data-set", "marker", "name", "number"])

# h2s = wd.find_elements(by=By.CSS_SELECTOR, value='h2')
# for h2 in h2s: # 需要先點各縣市 全部展開
#   h2.click()

# categories = []
# exists = []

# for i in range(1, 4):
#   LevelTerms = wd.find_elements(by=By.CSS_SELECTOR, value='li.LevelTerm')
#   for LevelTerm in LevelTerms:
#     id = LevelTerm.get_attribute('id')
#     if id not in exists:
#       name = LevelTerm.find_element(by=By.CSS_SELECTOR, value='.level_name').find_element(by=By.TAG_NAME, value='a').get_attribute('innerHTML')
#       number = int(LevelTerm.find_element(by=By.CSS_SELECTOR, value='.level_num').get_attribute('innerHTML').replace("(", "").replace(")", ""))
#       href = LevelTerm.find_element(by=By.CSS_SELECTOR, value='.level_name').find_element(by=By.TAG_NAME, value='a').get_attribute('href')
#       a = LevelTerm.find_element(by=By.CSS_SELECTOR, value='span.level_option').find_element(by=By.CSS_SELECTOR, value='a')
#       marker = LevelTerm.find_element(by=By.CSS_SELECTOR, value='span.level_option').find_element(by=By.CSS_SELECTOR, value='a').get_attribute('innerHTML').replace(" ", "")
#       if marker == "+":
#         wd.execute_script("Open_Level('" + id.replace("#meeting#", "-") + "','" + id + "');")
#       print(marker + " " + id + " " + name + " " + str(number))
#       categories.append({
#         "id": LevelTerm.get_attribute('id'),
#         "href": href
#       })
#       df = df.append({
#         "id": id,
#         "up": "", # li.get_attribute("up"),
#         "site": i, 
#         "data-set": "", # li.get_attribute("data-set"),
#         "marker": marker,
#         "name": name,
#         "number": number
#       }, ignore_index=True)
#       exists.append(id)
# print("抓完分類了")
# print(exists)

# df.to_csv('地方議會議事錄.csv',encoding='utf-8-sig')
# files.download("地方議會議事錄.csv")
# df.head()

df = pd.read_csv("地方議會議事錄.csv")
ids = df[(df["site"]==2) & (df["number"]<10000)]["id"].tolist()
print(ids)

# ids = []
# for second in df[(df["site"]==2) & (df["number"]>=10000)]["id"].tolist():
#   ids = ids + df[(df["site"]==3) & (df["number"]<10000) & (df["id"].str.startswith(second))]["id"].tolist()
print(ids)

# 010-M207 這個本身有問題 SyntaxError: Unexpected token < in JSON at position 0
# 超過10000的下載也都有問題

print(len(ids))

for id in ids:
  try:
    # 每次都要重新登入，把myFolder清空
    flag = False
    while flag==False:
      try:
        # !cp /usr/lib/chromium-browser/chromedriver /usr/bin
        # !rm /usr/bin
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # agent = UserAgent().random
        # print(agent)
        # chrome_options.add_argument(f'user-agent={UserAgent().random}')
        wd = webdriver.Chrome('chromedriver', options=chrome_options)
        wd.get("https://journal.th.gov.tw/query.php")
        wd.execute_script("UserLoginSubmit('Guestlogin');")
        time.sleep(5)
        flag = True
      except Exception as e:
        # print(wd.page_source)
        # print(str(e))
        flag = False
        wd.quit()
      # print(wd.find_element_by_xpath('//*').get_attribute('innerHTML'))
    print("https://journal.th.gov.tw/query.php?act=level&Query_String=" + id.replace("#meeting#", "-"))
    wd.get("https://journal.th.gov.tw/query.php?act=level&Query_String=" + id.replace("#meeting#", "-"))
    # 全選 > 所有結果 > Add > Myfolder匯出
    wd.find_element(By.ID, "result_selected_all").click();
    wd.find_elements(By.NAME, "user_select_target")[1].click();
    wd.find_element(By.CLASS_NAME, "save_button").click();
    while len(wd.find_elements(By.CLASS_NAME, "system_loading_area"))==0:
      time.sleep(0.1) # 按鈕產製中
    while wd.find_element(By.CLASS_NAME, "system_loading_area").value_of_css_property("display") != "block":   
      print(wd.find_element(By.CLASS_NAME, "system_loading_area").value_of_css_property("display"))
      time.sleep(0.1) # 系統處理中   
    while len(wd.find_elements(By.CLASS_NAME, "sel_export"))==0:
      time.sleep(0.1) # 按鈕產製中
    script = "window.open('"+wd.find_element(By.CLASS_NAME, "sel_export").get_attribute("href")+"');";
    wd.execute_script(script)
    # file_name = "tlcda_meta_"+datetime.now().strftime("%Y-%m-%d")+".csv"
    file_name = "tlcda_meta_2022-06-01.csv"
    while not os.path.isfile(file_name):
      time.sleep(0.1) # 下載中
    os.rename(file_name, "tlcda_meta_"+id+".csv")    
    print(id + "下載完成")  
    wd.quit()
  except:
    print(id + "錯誤")
