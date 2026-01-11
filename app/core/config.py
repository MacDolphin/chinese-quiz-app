# Config module for application constants
# 應用程式常數設定模組

import os

# ==========================================
# File Paths (檔案路徑)
# ==========================================
VOCAB_FILE = 'vocabulary.csv'      # 主要題庫
ERROR_LOG_FILE = 'review_list.csv' # 錯題紀錄
CSS_FILE = 'styles.css'            # CSS 樣式表
ENCODING_TYPE = 'utf-8-sig'        # CSV 編碼設定

# ==========================================
# Game Settings (遊戲設定)
# ==========================================
MIN_WORDS_FOR_QUIZ = 3             # 最少需要的生字數量
NUM_OPTIONS = 3                    # 選項數量
MAX_DISTRACTOR_ATTEMPTS = 100      # 尋找干擾項的最大嘗試次數

# ==========================================
# Memory Game (記憶遊戲)
# ==========================================
MEMORY_GAME_PAIRS = 15             # 記憶遊戲的配對數量（15 組 = 30 張卡牌）
MEMORY_GAME_COLUMNS = 6            # 記憶遊戲的欄位數（6 欄 × 5 列）

# ==========================================
# Adventure Mode (冒險模式)
# ==========================================
INITIAL_MONSTER_HP = 100
INITIAL_PLAYER_HP = 3
DAMAGE_PER_CORRECT = 20
MONSTERS = ["🦖", "👾", "🐉", "🧟", "🧛", "🦈", "🦍", "🕷️"]

# ==========================================
# Praises (正向回饋語句)
# ==========================================
PRAISES = [
    {"text": "太棒了！", "emoji": "🎉", "filename": "praise_01"},
    {"text": "完全正確！", "emoji": "🌟", "filename": "praise_02"},
    {"text": "你真厲害！", "emoji": "💪", "filename": "praise_03"},
    {"text": "水啦！答對了！", "emoji": "✨", "filename": "praise_04"},
    {"text": "Excellent!", "emoji": "", "filename": "praise_05"},
    {"text": "你是漢字小天才！", "emoji": "🎓", "filename": "praise_06"},
    {"text": "好聰明喔！", "emoji": "🧠", "filename": "praise_07"},
    {"text": "答得好！繼續保持！", "emoji": "🚀", "filename": "praise_08"},
    {"text": "沒錯！就是這個！", "emoji": "🎯", "filename": "praise_09"},
    {"text": "你的中文越來越好了！", "emoji": "📈", "filename": "praise_10"},
    {"text": "太神了！", "emoji": "💯", "filename": "praise_11"},
    {"text": "給你一個大拇指！", "emoji": "👍", "filename": "praise_12"}
]
