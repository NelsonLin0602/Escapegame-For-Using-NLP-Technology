# 爬取遊戲評論
# 定義動態網頁爬蟲，爬取遊戲近幾筆評論
def Critical_catch(url):
  try:
    options = Options()
    options.add_argument("--disable-notifications")  # 取消所有的alert彈出視窗
    browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options) # 利用ChromeDriver爬取
    browser.get(str(url)) # 輸入欲爬取網址
    time.sleep(15) # 強制等待15秒，因為網頁會有幾秒的廣告時間
    area = browser.find_element_by_id("tabs-:r6:--tab-1") # 找到「玩家評論」的按鈕
    area.click() # 點選「玩家評論」的按鈕
    soup = BeautifulSoup(browser.page_source, "html.parser") # 將點選完的網站HTML記錄下來，方便找到下一行的class名稱
    nextpage = browser.find_element(By.CLASS_NAME,'chakra-button.css-wubf5g') # 找到「其他評論」的按鈕
    # 持續點擊「其他評論」的按鈕，以利跑出更多評論(最多30下)
    for i in range(30):
      try:
        nextpage.click()
      except:
        pass
    time.sleep(3) # 強制等待3秒
    soup2 = BeautifulSoup(browser.page_source, "html.parser") # 將點選完的網站HTML記錄下來，方便找到下一行的class名稱
    elements = soup2.find_all("p", class_="text-gray-800 text-sm whitespace-pre-line") # 找到玩家評論的每條內容
    critical = [el.getText() for el in elements] # 將每條評論內容依序讀到串列裡面
  except:
    critical = 'NaN'  # 若以上有問題的話則先輸入NaN註記
  return critical # 回傳該遊戲抓取的玩家評論串列

# 匯入之前抓好的所有遊戲網址
game_url = np.load("game_url.npy", allow_pickle='TRUE')

# 建立一個空字典，用來存放每個遊戲抓到的每個評論
game_url_critical = {}
# 利用for迴圈將每個遊戲網址輸入到動態爬蟲函式，將玩家評論爬下來
for url in game_url:
    critical_list = Critical_catch(str(url))
    game_url_critical[url] = critical_list # 將爬好的玩家評論，整理成串列當成該遊戲url的value值存入字典中
np.save('game_url_critical.npy',game_url_critical) # 儲存遊戲玩家評論字典


# 整理評論成關鍵字
# 匯入jieba套件
# ! pip install -U jieba
import jieba
import jieba.analyse

# 定義關鍵字擷取函式
def Critical_keyword(critical):
  topK = 10
  tags = jieba.analyse.extract_tags(str(critical), topK=topK)
  return tags

# 匯入資料處理相關套件
import numpy as np
from collections import Counter

# 匯入遊戲評論資料
game_url_critical = np.load("game_url_critical.npy", allow_pickle='TRUE').item()

# 將遊戲評論丟入關鍵字擷取函式，並產生出每個遊戲的評論關鍵字
for url in game_url_critical.keys():
  keypoint = [Critical_keyword(critical) for critical in game_url_critical[url]] # 以遊戲為單位將所有評論依序產生關鍵字，將產生後的關鍵字整理成一個串列
  keypoint_new = [item for bot in keypoint for item in bot] # 將關鍵字串列降維
  element_counts = Counter(keypoint_new) # 計算每個值出現的次數
  most_common_values = element_counts.most_common(5) # 找到10個重複最多的值以及次數
  key_keyword = [] # 建立一個空串列來放最終的評論關鍵字
  for value, count in most_common_values: # 利用for迴圈將找到10個重複最多的關鍵字放入到串列中
    key_keyword.append(value)
  game_url_critical[url] = key_keyword # 將原本該遊戲的評論替換成最終評論關鍵字

# 儲存最新的評論關鍵字
game_critical_keyword = game_url_critical
np.save('game_critical_keyword.npy',game_critical_keyword)