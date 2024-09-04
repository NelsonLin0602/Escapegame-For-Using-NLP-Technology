# Escapegame For Using NLP Technology

## Project motivation
There are many types of escape games, which are distinguished according to factors such as atory style, puzzle presentation, length of time, comment status, etc., and the same escape room may be covered with many keywords, such as "mechanism type" and "Chinese style" , "massive puzzle type", "horror theme"... 

Under normal situation when we search for the escape games we want to play, we have to input the keywords we want to play and search one by one to find one or two escape games.

 Therefore, I want to design a system where users can input **the requirements** for the escape games they want to play based on their own conditions, and the system will judge the user's input and output recommended escape games that meet expectations.

## Expected Results

This system allows users to enter the type, name, and even content they want to play, and then recommends escape games that match the user's needs, allowing users to make choices based on their own needs.

For example, if I want to play a game related to the universe, space, or time, I only need to enter "universe, space, time" so that the system can help me find games with similar content.

example1 : 
* input area : 我想要具有酒吧風格或是可以喝酒的遊戲。
* output area : 符合input area條件的遊戲資訊（遊戲名稱、遊戲價錢、遊戲說明、遊戲類型、遊戲連結...）

example2 :
* input area : 實驗室、科學家、宇宙、時空
* output area : 符合input area條件的遊戲資訊（遊戲名稱、遊戲價錢、遊戲說明、遊戲類型、遊戲連結...）

## Used Technology

* Web Crawler Technology : Include **BeautifulSoup** and **Selenium**.
* NLP Technology : **jieba keyword retrieval**.
* Interface Paclage : **Gradio**.