import requests
from bs4 import BeautifulSoup
import numpy as np
# !pip install webdriver-manager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


# 整理工作室的網站連結
# 將所有工作室網站url的後位數字謄寫下來
workshop_url_last_number = ['2612','2656','2627','8119','2659','2626','2629','12541','2637','10586','2635','2617','2624','2630','4082','2667','2652','18812','2640','11445','10282','2633','4906','15315','11224','4936','20075','2662','2632','20496']
# 建立一個空串列用來放完整的所有工作室網站連結
workshop_url = []
# 利用for迴圈把藤寫下來的數字轉換成實際連結
for number in range(len(workshop_url_last_number)):
    workshop_url.append('https://escape.bar/firm/'+workshop_url_last_number[number])
np.save('workshop_url.npy',workshop_url) # 儲存整理好的工作室連結字典
print(workshop_url)

# 整理所有遊戲的網站連結
# 定義從工作室網站中抓取遊戲連結的函式
def Game_url(url):
    response = requests.get(str(url)) # 抓取「工作室網址」
    soup = BeautifulSoup(response.text, "html.parser") # 將網址的HTML寫進程式
    # 將網址中所有該工作室遊戲連結抓下來
    total_url = soup.find_all('div',class_='chakra-card__header css-4pyn5f')
    total_html=['https://escape.bar'+str(i.select_one('a').get('href')) for i in total_url]
    return total_html # 回傳該工作室的所有遊戲連結

# 建立一個空串列用來存放完整遊戲的網站連結
game_url = []
# 利用for迴圈把所有工作室網站連結下去跑函式，產生出各工作室中的遊戲連結
for workshop in range(len(workshop_url)):
    game_url.append(Game_url(workshop_url[workshop])) # 將各工作室中的遊戲連結加入到串列裡
game_url = [j for i in game_url for j in i] # 將串列降成一維
np.save('game_url.npy',game_url) # 儲存整理好的遊戲連結字典
print(game_url)


# 整理所有遊戲的資訊
# 定義從遊戲網站中抓取遊戲資訊的函式
def Game_information(url):
    response = requests.get(str(url)) # 抓取「遊戲網址」
    soup = BeautifulSoup(response.text, "html.parser") # 將網址的HTML寫進程式
    title = soup.find("h1", class_="text-2xl lg:text-3xl font-black") # 將「遊戲名稱」抓下來
    money = soup.find('p',class_='mb-2 pl-4 leading-normal text-sm lg:text-base whitespace-pre-wrap') # 將「遊戲價錢」抓下來
    content = soup.find('article',class_='ContentBlock_contentStyle__jR1s5')  # 將「遊戲說明」抓下來
    Type = soup.find_all('b',class_='chakra-text css-0',limit=3) # 將「遊戲的關鍵字」抓下來，最多三個關鍵字

    # 將抓下來的所有資訊，整理成一個字典，即為該遊戲的資訊
    game_dict = {'topic':title.getText(),
      'information':money.getText(),
      'content':content.getText(),
      'type':[t.getText() for t in Type],
      'url':url}
    return game_dict  # 回傳該遊戲資訊(字典型態)

# 建立一個空字典，用來存放所有遊戲的資訊
escape_game = {}
# 利用for迴圈將爬出來的所有遊戲資訊打包成字典
for num in range(len(game_url)):
    escape = Game_information(game_url[num]) # 將每個遊戲的網站連結丟入Game_information函式
    escape_game[escape['topic']] = escape # 利用該遊戲的名稱當成key值;所有內容當成value值
np.save('escape_game.npy',escape_game) # 儲存整理好的遊戲字典

Escape_games = np.load("escape_game.npy", allow_pickle='TRUE')
print(Escape_games)
print(type(Escape_games))