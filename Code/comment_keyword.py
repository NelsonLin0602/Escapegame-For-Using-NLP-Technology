import numpy as np
import requests
from bs4 import BeautifulSoup
from collections import Counter
from jieba.analyse import extract_tags

class KeywordExtractor:
    def extract_keywords(self, text_list, topK=5):
        """從文字列表中提取關鍵字。"""
        keywords = []
        for text in text_list:
            tags = extract_tags(text, topK=topK)
            keywords.extend(tags)
        return keywords

class CommentKeywordProcessor:
    def __init__(self, game_reviews):
        self.game_reviews = game_reviews

    def fetch_review_content(self, url):
        """從遊戲評論頁面獲取所有評論內容。"""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        reviews = soup.find_all('p', class_='chakra-text css-q9z15z')
        return [review.getText() for review in reviews]

    def process_reviews(self):
        """處理每個遊戲的評論關鍵字。"""
        keyword_extractor = KeywordExtractor()
        for url, reviews in self.game_reviews.items():
            keypoint = [keyword_extractor.extract_keywords([review]) for review in reviews]
            keypoint_flat = [item for sublist in keypoint for item in sublist]
            element_counts = Counter(keypoint_flat)
            most_common_values = element_counts.most_common(5)
            key_keywords = [value for value, _ in most_common_values]
            self.game_reviews[url] = key_keywords

    def save_keywords(self, filename='05_game_critical_keyword.npy'):
        """儲存處理後的關鍵字。"""
        np.save(filename, self.game_reviews)

def main():
    # 確保此程式能夠連接到其他腳本生成的資料
    game_reviews = np.load("02_game_url.npy", allow_pickle=True).item()
    processor = CommentKeywordProcessor(game_reviews)
    processor.process_reviews()
    processor.save_keywords()

if __name__ == "__main__":
    main()
