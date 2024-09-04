# 匯入gradio套件
# !pip install gradio
import gradio as gr
import numpy as np

# 匯入jieba套件
# ! pip install -U jieba
import jieba
import jieba.analyse

# 將建立好的遊戲資料庫匯入
Escape_Game_Data = np.load("Escape_Game_Data.npy", allow_pickle='TRUE').item()
print(Escape_Game_Data)


# 建立Gradio system
# 將輸入文字找尋關鍵字，並依照關鍵字去查找符合的遊戲
def Escape_recommend(input):
  # 用jieba整理輸入的關鍵字
  topK = 3
  tags = jieba.analyse.extract_tags(str(input), topK=topK)
  # 建立一個空串列用來放查找到擁有對應關鍵字的遊戲名稱
  game = []
  for item in tags:
    for game1,information in Escape_Game_Data.items():
      if item in information.get('keyword',[]): # 判斷關鍵是是否有在keyword的value裡
        game.append(game1)
  # 建立一個空串列，用來放推薦的遊戲資訊
  g=[]
  for word in game:
    p = []
    # 整理遊戲輸出的資訊
    for key, value in Escape_Game_Data[word].items():
      if key == 'topic':
        p.append(f'主題：{value}')
      elif key == 'information':
        p.append(f'價錢：{value}')
      elif key == 'content':
        p.append(f'遊戲說明：{value}')
      elif key == 'type':
        p.append("遊戲類型：" + " ".join("#" + x.rstrip(',') for x in value))
      elif key == 'url':
        p.append(f'網站連結：{value}')
    g.append(p)
  # 建立一個空字串，用來放要輸出的所有遊戲資訊
  result = ""
  for sublist in g:
    for item in sublist:
      result += item.rstrip(',') + "\n" # 各遊戲中的資訊用換行隔開
    result += "---------------------------------------------\n"  # 遊戲與遊戲之間隔開
  return result # 輸出字串

# 建造此系統之網頁
demo = gr.Interface(fn=Escape_recommend, inputs="text", outputs="text")
demo.launch()