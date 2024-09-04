# 匯入相關套件
! pip install -U jieba
import jieba
import jieba.analyse
import numpy as np

# 匯入遊戲機本資訊以及評論關鍵字資料
escape_game = np.load("03_escape_game.npy", allow_pickle='TRUE').item()
game_critical_keyword = np.load("05_game_critical_keyword.npy", allow_pickle='TRUE').item()

# 定義內容關鍵字擷取函式，用來擷取遊戲基本資訊中的遊戲說明
def Content_keyword(critical):
  topK = 5
  tags = jieba.analyse.extract_tags(str(critical), topK=topK)
  return tags

# 創建一個副本以避免修改正在迭代的字典
modified_escape_game = escape_game.copy()
# 將評論關鍵字的資料丟入遊戲基本資訊中，並將遊戲說明的關鍵字納入整體遊戲關鍵字
for url, keyword in game_critical_keyword.items():
  for game, information in escape_game.items():
    if 'url' in information and information['url'] == url: # 確認評論關鍵字的網站是否與遊戲同一個
      modified_escape_game[game]['keyword'] = keyword # 是的話創建一個新key以及value值
      content_keyword = Critical_keyword(information['content']) # 將遊戲說明跑上式函式
      for word in content_keyword:
        modified_escape_game[game]['keyword'].append(word) # 將遊戲說明中的關鍵字也加入到整體遊戲關鍵字

np.save('Escape_Game_Data.npy',modified_escape_game)
print(modified_escape_game)
print(modified_escape_game['你'].keys()) # 呈現出各遊戲的字典裡有什麼樣的資訊