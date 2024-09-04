import gradio as gr
import numpy as np
import jieba
import jieba.analyse

class EscapeGameRecommender:
    def __init__(self, data_path="Escape_Game_Data.npy"):
        # 將建立好的遊戲資料庫匯入
        self.escape_game_data = np.load(data_path, allow_pickle='TRUE').item()

    def extract_keywords(self, input_text, topK=3):
        """用 jieba 整理輸入文字中的關鍵字。"""
        tags = jieba.analyse.extract_tags(str(input_text), topK=topK)
        return tags

    def find_games(self, tags):
        """根據關鍵字查找符合的遊戲。"""
        game_matches = []
        for tag in tags:
            for game_name, info in self.escape_game_data.items():
                if tag in info.get('keyword', []):
                    game_matches.append(game_name)
        return game_matches

    def format_game_info(self, game_names):
        """格式化遊戲資訊以便顯示。"""
        formatted_games = []
        for name in game_names:
            game_info = []
            for key, value in self.escape_game_data[name].items():
                if key == 'topic':
                    game_info.append(f'主題：{value}')
                elif key == 'money':
                    game_info.append(f'價錢：{value}')
                elif key == 'content':
                    game_info.append(f'遊戲說明：{value}')
                elif key == 'keyword':
                    game_info.append("遊戲類型：" + " ".join("#" + x.rstrip(',') for x in value))
                elif key == 'url':
                    game_info.append(f'網站連結：{value}')
            formatted_games.append("\n".join(game_info))
        return "\n---------------------------------------------\n".join(formatted_games)

    def recommend_games(self, input_text):
        """主函數：根據輸入文字推薦遊戲。"""
        tags = self.extract_keywords(input_text)
        matched_games = self.find_games(tags)
        if not matched_games:
            return "沒有找到符合的遊戲。"
        return self.format_game_info(matched_games)

def launch_gradio_interface():
    recommender = EscapeGameRecommender()

    def escape_recommend(input_text):
        return recommender.recommend_games(input_text)

    # 建造此系統之網頁
    demo = gr.Interface(fn=escape_recommend, inputs="text", outputs="text")
    demo.launch()

if __name__ == "__main__":
    launch_gradio_interface()
