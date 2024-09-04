import jieba
import jieba.analyse
import numpy as np

class GameDataIntegrator:
    def __init__(self, escape_game, game_critical_keyword):
        self.escape_game = escape_game
        self.game_critical_keyword = game_critical_keyword
        self.modified_escape_game = self.escape_game.copy()

    def extract_content_keywords(self, critical, topK=5):
        """擷取遊戲說明中的關鍵字。"""
        tags = jieba.analyse.extract_tags(str(critical), topK=topK)
        return tags

    def integrate_data(self):
        """將評論關鍵字整合到遊戲基本資訊中。"""
        for url, keywords in self.game_critical_keyword.items():
            for game, info in self.escape_game.items():
                if 'url' in info and info['url'] == url:
                    self.modified_escape_game[game]['keyword'] = keywords
                    content_keywords = self.extract_content_keywords(info['content'])
                    self.modified_escape_game[game]['keyword'].extend(content_keywords)
        np.save('06_Escape_Game_Data.npy', self.modified_escape_game)

def main():
    # 加載先前腳本生成的數據
    escape_game = np.load("03_escape_game.npy", allow_pickle=True).item()
    game_critical_keyword = np.load("05_game_critical_keyword.npy", allow_pickle=True).item()
    integrator = GameDataIntegrator(escape_game, game_critical_keyword)
    integrator.integrate_data()
    print(integrator.modified_escape_game)

if __name__ == "__main__":
    main()
