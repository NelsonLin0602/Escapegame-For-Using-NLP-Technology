import requests
from bs4 import BeautifulSoup
import numpy as np

class EscapeGameScraper:
    def __init__(self, workshop_ids):
        self.workshop_ids = workshop_ids
        self.workshop_urls = self._generate_workshop_urls()
        self.game_urls = []

    def _generate_workshop_urls(self):
        """根據工作室ID生成工作室網址。"""
        workshop_urls = [f'https://escape.bar/firm/{id}' for id in self.workshop_ids]
        np.save('01_workshop_url.npy', workshop_urls)
        return workshop_urls

    def fetch_game_urls(self):
        """從工作室網址中獲取所有遊戲網址。"""
        for workshop_url in self.workshop_urls:
            self.game_urls.extend(self._scrape_game_urls_from_workshop(workshop_url))
        np.save('02_game_url.npy', self.game_urls)
        return self.game_urls

    def _scrape_game_urls_from_workshop(self, url):
        """從單個工作室頁面爬取遊戲網址。"""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        total_url = soup.find_all('div', class_='chakra-card__header css-4pyn5f')
        return ['https://escape.bar' + i.select_one('a').get('href') for i in total_url]

    def fetch_game_information(self):
        """從遊戲網址中獲取所有遊戲資訊。"""
        escape_game = {}
        for game_url in self.game_urls:
            game_info = self._scrape_game_information(game_url)
            escape_game[game_info['topic']] = game_info
        np.save('03_escape_game.npy', escape_game)
        return escape_game

    def _scrape_game_information(self, url):
        """從單個遊戲頁面爬取遊戲資訊。"""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("h1", class_="text-2xl lg:text-3xl font-black").getText()
        money = soup.find('p', class_='mb-2 pl-4 leading-normal text-sm lg:text-base whitespace-pre-wrap').getText()
        content = soup.find('article', class_='ContentBlock_contentStyle__jR1s5').getText()
        topic = soup.find('div', class_='mt-3').getText().strip()
        game_info = {
            'title': title,
            'money': money,
            'content': content,
            'topic': topic,
            'url': url
        }
        return game_info

def main():
    # Example usage of the EscapeGameScraper class
    scraper = EscapeGameScraper(workshop_ids=[1, 2, 3])  # 輸入工作室 ID 列表
    scraper.fetch_game_urls()
    scraper.fetch_game_information()

if __name__ == "__main__":
    main()
