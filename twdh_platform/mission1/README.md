# 任務一
任務需求

* 由四個系統全匯出資料
* CSV 對映、清洗、儲存至「資料整合層」
* 依據metadata的規範。


## 三大步驟
1. 下載分類及檔案 mission1.py
2. 剖析並存入資料庫 cron.php
3. 簡易查詢 index.php



## 一、下載分類及檔案
由於牽涉相當多使用者互動，因此需使用 selenium 模擬瀏覽器。
因為每個脈絡系統都有下載筆數限制，因此最好的作法就是，搜尋下載最小分類。
基本原則：
1. 不斷展開分類(+號)，以取得所有分類。
2. 找出所有最底層的分類，前方會是*號(i.fa-asterisk)。
3. 在搜尋欄中打上分類，點選取得所有項目，點擊下載。

四個網站有三種不同爬蟲方式，下方簡單提點重要步驟。

#### (一) 國史館檔案史料文物查詢系統
https://ahonline.drnh.gov.tw/index.php?act=Archive

一一點選全宗  > 抓取左方階層選單
```
znames = wd.find_elements(by=By.CSS_SELECTOR, value='.zname')
dataZnames = []
for zname in znames:
  dataZnames.append(zname.get_attribute("data-zname"))
  
wd.find_element(by=By.CSS_SELECTOR, value='.zname[data-zname="'+dataZname+'"]').click()
level_group = wd.find_element(by=By.CSS_SELECTOR, value='ul.level_group')
for li in level_group.find_elements(by=By.CSS_SELECTOR, value='li'):
```

#### (二) 臺灣省議會史料總庫 & 國史館臺灣文獻館文獻檔案查詢系統
https://drtpa.th.gov.tw/index.php?act=Archive/index
https://onlinearchives.th.gov.tw/index.php?act=Archive

每點一次加號就會重新透過API跟資料庫要下一層的資料，因此必須使用遞迴的方式由上而下點過一次。
直到點到星號。

```python=
def 點(id):
    for li in level_group.find_elements(by=By.CSS_SELECTOR, value='li[up="'+id+'"]')
        if len(li.find_elements(by=By.CSS_SELECTOR, value='i.fa-asterisk'))==0:
            li.find_element(by=By.CSS_SELECTOR, value='span.option').click()
            點(li.get_attribute("id"))
```


#### (三) 地方議會議事錄
https://journal.th.gov.tw/query.php


需要先使用訪客登入
```python
wd.execute_script("UserLoginSubmit('Guestlogin');")
```
點選所有縣市 > 一階一階由上而下點開。

```
for h2 in  wd.find_elements(by=By.CSS_SELECTOR, value='h2'): 
    h2.click()
    
for i in range(1, 4):
    LevelTerms = wd.find_elements(by=By.CSS_SELECTOR, value='li.LevelTerm')
    for LevelTerm in LevelTerms:
```
#### 下載
四個脈絡系統的下載方式大致相同
1. 在下拉選單選擇"搜尋系列"
2. 輸入分類名稱
3. 點選下載

```python
search_field = wd.find_element(By.ID, "search_field")
Select(search_field).select_by_value("series")
search_input = wd.find_element(By.ID, "search_input")
search_input.clear()
search_input.send_keys(dataset)
search_input.send_keys(Keys.ENTER)
```

四個網站都必需點"所有結果"，再下載。

國史館檔案史料文物查詢系統、臺灣省議會史料總庫、國史館臺灣文獻館文獻檔案查詢系統
這三個網站的方法是會將搜尋結果存到資料庫 產生一組隨機id
再利用這組id下載
```python
export_type = wd.find_elements(By.NAME, "user_select_target")[1].get_attribute("value")
script = "window.open('index.php?act=Archive/export/result/'+encodeURIComponent(Base64.encode(\""+export_type+"\")));";
wd.execute_script(script)
```


地方議會議事錄需要先點加入資料夾，再去點下載鈕。
```python
wd.find_element(By.ID, "result_selected_all").click();
wd.find_elements(By.NAME, "user_select_target")[1].click();
wd.find_element(By.CLASS_NAME, "save_button").click();
time.sleep(3)
script = "window.open('"+wd.find_element(By.CLASS_NAME, "sel_export").get_attribute("href")+"');";
wd.execute_script(script)
```


## 二、剖析並存入資料庫

程式會根據檔名開始，判斷要使用哪一個方式剖析。

要注意【類目階層】、【相關人員】、【相關地點】、【相關組織】，都不能使用"/"、","，要使用";"分開

由於內容可能會有 \n, \r, \, 等特殊字元導致無法正常匯入sql 因此需要加上
```php
$conn->real_escape_string($題名)
```

欄位轉換方式如下

| 欄位          |臺灣省議會史料總庫    |  國史館檔案史料文物查詢系統  |國史館臺灣文獻館文獻檔案查詢系統    |地方議會議事錄    |
| ------| :---- |:---- |:---- |:---- |
| 開始行數        |5                  |4                       |4                         | 5                   |
| 原始欄位數量     |6                  |8                      |7                          |27                  |
|id              |自動遞增            |自動遞增                 |自動遞增                      |自動遞增    |
|來源系統          |臺灣省議會史料總庫   |國史館檔案史料文物查詢系統   |國史館臺灣文獻館文獻檔案查詢系統 |地方議會議事錄    |
|來源系統縮寫       |NDAP              |AHCMS                    | AHTWH                    |tlcda    |
|題名              |5 內容摘要(，前)    |2 卷名                   |3 title(，前)              |4 書目名稱   |
|摘要              |5 內容摘要         |4 題名摘要                |3 title                   |15 內容摘要   |
|類目階層          |3 瀏覽階層          |3 檔案系列                |4 檔案系列                 |7 內容類別   |
|原始時間記錄       |4 日期描述         |5+6 卷件開始日期+卷件結束日期 |5+6 date_from+date_stop  |13+14 日期起   |
|西元年            |4 日期描述(前四字)  |5 卷件開始日期(前四字)       |5 date_from(前四字)      |13  日期起(前四字)  |
|起始時間          |4 日期描述(~前)    |5 卷件開始日期               |5 date_from              |13 日期起   |
|結束時間          |4 日期描述(~後)    |6 卷件結束日期               |6 date_stop              |14 日期迄   |
|典藏號            |2 典藏號          |7 數位典藏號                |2 數位典藏號               |5 典藏序號   |
|相關人員           |無            |無            |無            |16,17,18,19 會議主席;提案議員;相關議員;請願人|
|相關地點           |無            |無            |無            |無                                     |
|相關組織           |無            |無            |無            |20,21,22 機關;相關機關;請願機關           |
|文件原系統頁面URL   |無            |無            |無            |26 資料連結                              |
|有沒有被匯入詳細資料 |無            |無            |無            |無                               |


## 三、簡易查詢

因為mysql只有對空格拆字，因此要加一個全文檢索欄位，將要檢索的詞，要一個個用空格拆開。
```
臺灣省參議會第一屆第一次定期大會
臺 灣 省 參 議 會 第 一 屆 第 一 次 定 期 大 會
```
並將欄位設為 FULLTEXT
```sql
\xampp\mysql\bin\my.ini
[mysqld]
ft_min_word_len = 1 
```


```sql
ALTER TABLE   metadata2 ADD FULLTEXT(`全文檢索`)
```



使用Highcahrt繪製長條圖

有用全文檢索
搜尋花了: 0.040657997131348 毫秒
```sql
SELECT 來源系統, COUNT(id) AS 數量 FROM `metadata2` WHERE MATCH(全文檢索) AGAINST('"烏 腳 病"') GROUP BY `來源系統`;
```
沒用全文檢索
搜尋花了: 3.681116104126 毫秒

```sql
SELECT 來源系統, COUNT(id) AS 數量 FROM `metadata2` WHERE MATCH(全文檢索) AGAINST('"烏 腳 病"') GROUP BY `來源系統`;
```


其他加速方法，改變my.ini設定。
```
## of RAM but beware of setting memory usage too high
innodb_buffer_pool_size=16G
## Set .._log_file_size to 25 % of buffer pool size
innodb_log_file_size=100M
innodb_log_buffer_size=4G

```
