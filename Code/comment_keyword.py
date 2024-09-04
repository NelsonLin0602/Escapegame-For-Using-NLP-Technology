import time
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import jieba
import jieba.analyse
from collections import Counter

class GameReviewScraper:
    def __init__(self):
        self.driver = None  # 初始化WebDriver為None

    def start_browser(self):
        """啟動瀏覽器並設置選項。"""
        options = Options()
        options.add_argument("--disable-notifications")  # 取消所有的通知彈窗
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def stop_browser(self):
        """關閉瀏覽器。"""
        if self.driver:
            self.driver.quit()

    def fetch_reviews(self, url):
        """爬取指定URL的遊戲評論。"""
        try:
            self.driver.get(url)  # 打開指定的網址
            time.sleep(15)  # 等待網頁加載完成，包括廣告時間
            area = self.driver.find_element(By.ID, "tabs-:r6:--tab-1")  # 找到「玩家評論」按鈕
            area.click()  # 點擊「玩家評論」按鈕
            nextpage = self.driver.find_element(By.CLASS_NAME, 'chakra-button.css-wubf5g')  # 找到「其他評論」按鈕
            
            # 持續點擊「其他評論」按鈕，最多點擊30次
            for _ in range(30):
                try:
                    nextpage.click()
                except:
                    pass
            
            time.sleep(3)  # 等待頁面更新
            soup2 = BeautifulSoup(self.driver.page_source, "html.parser")  # 解析更新後的HTML
            elements = soup2.find_all("p", class_="text-gray-800 text-sm whitespace-pre-line")  # 找到所有評論元素
            reviews = [el.get_text() for el in elements]  # 提取每條評論的文本
        except:
            reviews = ['NaN']  # 如果出現錯誤，返回'NaN'
        return reviews

class KeywordExtractor:
    @staticmethod
    def extract_keywords(reviews, topK=10):
        """從評論中提取關鍵字。"""
        all_reviews = ' '.join(reviews)  # 將所有評論合併成一個字符串
        return jieba.analyse.extract_tags(all_reviews, topK=topK)  # 提取前topK個關鍵字

def main():
    """主函式，控制爬取和關鍵字提取的流程。"""
    scraper = GameReviewScraper()
    scraper.start_browser()  # 啟動瀏覽器

    # 匯入遊戲網址並爬取評論
    game_urls = np.load("game_url.npy", allow_pickle=True)
    game_reviews = {}

    for url in game_urls:
        reviews = scraper.fetch_reviews(str(url))  # 爬取評論
        game_reviews[url] = reviews  # 將評論存入字典中

    scraper.stop_browser()  # 關閉瀏覽器
    np.save('04_game_url_critical.npy', game_reviews)  # 儲存爬取的評論

    keyword_extractor = KeywordExtractor()
    game_reviews = np.load("game_url_critical.npy", allow_pickle=True).item()

    # 提取每個遊戲的評論關鍵字
    for url in game_reviews.keys():
        keypoint = [keyword_extractor.extract_keywords([review]) for review in game_reviews[url]]
        keypoint_flat = [item for sublist in keypoint for item in sublist]  # 扁平化關鍵字列表
        element_counts = Counter(keypoint_flat)  # 計算每個關鍵字的出現次數
        most_common_values = element_counts.most_common(5)  # 找到出現最多的前5個關鍵字
        key_keywords = [value for value, _ in most_common_values]  # 提取前5個關鍵字
        game_reviews[url] = key_keywords  # 更新遊戲的評論關鍵字

    np.save('05_game_critical_keyword.npy', game_reviews)  # 儲存最終的關鍵字

if __name__ == "__main__":
    main()
