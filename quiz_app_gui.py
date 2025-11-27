import streamlit as st
import random
import csv
import os
from datetime import datetime

# ==========================================
# 設定區
# ==========================================
VOCAB_FILE = 'vocabulary.csv'      # 主要題庫
ERROR_LOG_FILE = 'review_list.csv' # 錯題紀錄
ENCODING_TYPE = 'utf-8-sig'        # 編碼設定

# 正向回饋語句庫 (擴充版) - 必須與 generate_audio_assets.py 一致
praises = [
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

# ==========================================
# 資料處理函式
# ==========================================

def load_vocabulary(filename):
    """
    通用讀取函式：可以讀取題庫，也可以讀取錯題本。
    回傳一個不重複的生字列表。
    """
    vocab_dict = {} # 使用字典來去除重複 (key=char)
    
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, mode='r', encoding=ENCODING_TYPE) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 去除前後空白
                clean_row = {k: v.strip() for k, v in row.items() if k and v}
                
                # 確保有 char 和 zhuyin 欄位
                if 'char' in clean_row and 'zhuyin' in clean_row:
                    # 使用 char 當作 key，這樣重複的字就會被覆蓋，達到去重效果
                    vocab_dict[clean_row['char']] = {
                        'char': clean_row['char'],
                        'zhuyin': clean_row['zhuyin'],
                        'book': clean_row.get('book', '未分類') # 預設為 '未分類'
                    }
        
        # 將字典轉回列表
        return list(vocab_dict.values())
        
    except Exception as e:
        st.error(f"❌ 讀取檔案 {filename} 時發生錯誤: {e}")
        return []

def log_mistake(word_data):
    """將答錯的題目寫入錯題本"""
    file_exists = os.path.isfile(ERROR_LOG_FILE)
    
    try:
        with open(ERROR_LOG_FILE, mode='a', newline='', encoding=ENCODING_TYPE) as f:
            fieldnames = ['char', 'zhuyin', 'timestamp']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'char': word_data['char'],
                'zhuyin': word_data['zhuyin'],
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
    except Exception as e:
        print(f"Error logging mistake: {e}")

def remove_mistake(target):
    """從錯題本中移除答對的字"""
    if not os.path.exists(ERROR_LOG_FILE):
        return

    try:
        # 讀取現有錯題
        rows = []
        with open(ERROR_LOG_FILE, mode='r', encoding=ENCODING_TYPE) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['char'] != target['char']:
                    rows.append(row)
        
        # 寫回檔案
        with open(ERROR_LOG_FILE, mode='w', encoding=ENCODING_TYPE, newline='') as csvfile:
            fieldnames = ['char', 'zhuyin']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            
    except Exception as e:
        print(f"Error removing mistake: {e}")

def get_question(db):
    """從題庫中隨機產生題目"""
    if not db:
        return None, None, None

    target = random.choice(db)
    options = [target]
    
    # 隨機選出錯誤選項 (干擾項)
    max_attempts = 100 
    attempts = 0
    while len(options) < 3 and attempts < max_attempts:
        distractor = random.choice(db)
        if distractor != target and distractor not in options:
            options.append(distractor)
        attempts += 1
    
    random.shuffle(options)
    
    # 決定模式: 1=看字選注音, 2=看注音選字
    mode = random.choice([1, 2]) 
    
    return target, options, mode

def get_audio_bytes_from_google_tts(text):
    """從 Google Translate TTS 下載音頻字節"""
    import requests
    from urllib.parse import quote
    
    try:
        encoded_text = quote(text)
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=zh-TW&client=tw-ob&q={encoded_text}"
        
        # 添加 User-Agent 避免被阻擋
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            return response.content
        else:
            return None
    except Exception as e:
        print(f"TTS Error: {e}")
        return None

def play_audio_with_javascript(text):
    """使用 JavaScript 直接播放音頻（iOS 相容）"""
    import streamlit.components.v1 as components
    import base64
    
    # 獲取音頻字節
    audio_bytes = get_audio_bytes_from_google_tts(text)
    
    if not audio_bytes:
        st.warning("⚠️ 語音載入失敗")
        return
    
    # 轉換為 base64
    audio_base64 = base64.b64encode(audio_bytes).decode()
    
    # 使用 HTML5 Audio API 播放
    html_code = f"""
    <div style="text-align: center; padding: 10px;">
        <audio id="audioPlayer" controls autoplay style="width: 100%; max-width: 500px;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            您的瀏覽器不支援音頻播放
        </audio>
    </div>
    <script>
        // 確保音頻能在 iOS 上播放
        const audio = document.getElementById('audioPlayer');
        audio.play().catch(e => console.log('Autoplay prevented:', e));
    </script>
    """
    
    components.html(html_code, height=80)

# ==========================================
# Streamlit 介面邏輯
# ==========================================

# ==========================================
# Streamlit 介面邏輯
# ==========================================

def init_session_state():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_answered' not in st.session_state:
        st.session_state.total_answered = 0
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None
    if 'game_mode' not in st.session_state:
        st.session_state.game_mode = None # 'general' or 'review' or None (Main Menu)
    if 'db' not in st.session_state:
        st.session_state.db = []
    if 'char_to_speak' not in st.session_state:
        st.session_state.char_to_speak = None
    if 'show_audio_player' not in st.session_state:
        st.session_state.show_audio_player = False

def reset_game():
    st.session_state.current_question = None
    st.session_state.score = 0
    st.session_state.total_answered = 0
    st.session_state.feedback = None
    st.session_state.char_to_speak = None
    st.session_state.show_audio_player = False

def next_question():
    target, options, mode = get_question(st.session_state.db)
    st.session_state.current_question = {
        'target': target,
        'options': options,
        'mode': mode
    }
    st.session_state.feedback = None
    st.session_state.char_to_speak = None
    st.session_state.show_audio_player = False

def check_answer(selected_option):
    target = st.session_state.current_question['target']
    
    st.session_state.total_answered += 1
    
    if selected_option == target:
        st.session_state.score += 1
        praise = random.choice(praises)
        
        msg = f"✅ {praise['text']}{praise['emoji']}"
        
        # 如果是在錯題複習模式下答對，將該字從錯題本移除
        if st.session_state.game_mode == 'review':
            remove_mistake(target)
            msg += " (已從錯題本移除)"
            
            # 更新當前的 db，避免下一題又抽到剛剛移除的字 (雖然機率低，但為了體驗)
            st.session_state.db = [item for item in st.session_state.db if item['char'] != target['char']]
            
            # 如果錯題都練完了
            if len(st.session_state.db) < 3 and len(st.session_state.db) > 0:
                 # 剩下的字太少，無法繼續出題 (因為選項需要3個干擾項? 其實選項是從 full_db 抓的嗎？)
                 # get_question 的選項是從傳入的 db 抓的。
                 # 如果 db 變少，選項可能會不夠。
                 # 這裡簡單處理：如果剩餘錯題太少，就提示完成
                 pass

        st.session_state.feedback = {
            'type': 'success',
            'msg': msg
        }
    else:
        st.session_state.feedback = {
            'type': 'error',
            'msg': f"❌ 哎呀，正確答案是： {target['char']} {target['zhuyin']}"
        }
        log_mistake(target)
    
    # 無論答對或答錯，都朗讀正確答案（該字的讀音）
    st.session_state.char_to_speak = target['char']

def main():
    st.set_page_config(page_title="美洲華語生字小幫手", page_icon="📝")
    
    # ==========================================
    # 自定義 CSS 樣式
    # ==========================================
    st.markdown("""
    <style>
    /* 全局按鈕樣式調整 */
    div.stButton > button {
        font-size: 28px !important;  /* 放大按鈕文字 */
        height: 80px !important;     /* 增加按鈕高度 */
        border-radius: 15px !important; /* 圓角 */
        border: 2px solid #e0e0e0;
        background-color: #ffffff;
        color: #333333;
        transition: all 0.3s ease;
    }
    
    /* 滑鼠懸停效果 */
    div.stButton > button:hover {
        border-color: #4CAF50 !important;
        color: #4CAF50 !important;
        background-color: #f9fff9 !important;
        transform: scale(1.02);
    }

    /* 針對主要選項按鈕的容器微調 */
    .option-btn-container {
        margin-top: 20px;
    }
    
    /* 題目文字樣式 */
    .question-text {
        font-size: 32px;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 20px;
        background-color: #e8f6f3;
        padding: 15px;
        border-radius: 10px;
    }
    
    /* 大字卡樣式 */
    .big-char {
        font-size: 100px;
        font-weight: bold;
        color: #e74c3c; /* 紅色字體更顯眼 */
        text-align: center;
        padding: 20px;
        background-color: #fff5f5;
        border-radius: 20px;
        border: 3px dashed #ffcccb;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    init_session_state()

    st.title("📝 美洲華語生字小幫手")

    # Sidebar for navigation
    with st.sidebar:
        st.header("功能選單")
        if st.button("🏠 回主選單", use_container_width=True):
            st.session_state.game_mode = None
            reset_game()
            st.rerun()
        st.markdown("---")
        st.caption("Designed for Tablet")

    # Main Menu
    if st.session_state.game_mode is None:
        st.header("請選擇模式")
        
        # 預先讀取題庫以獲取冊別資訊
        full_db = load_vocabulary(VOCAB_FILE)
        
        # 自定義排序函式 (讓第一冊、第二冊...依序排列)
        def book_sort_key(book_name):
            cn_map = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
            try:
                if book_name.startswith("第") and book_name.endswith("冊"):
                    num_str = book_name[1:-1]
                    if num_str in cn_map:
                        return cn_map[num_str]
            except:
                pass
            return 100 # 其他放在最後

        # 取得所有不重複的冊別並排序
        all_books = sorted(list(set(item['book'] for item in full_db)), key=book_sort_key)
        
        # 初始化選擇狀態
        if 'selected_books' not in st.session_state:
            st.session_state.selected_books = []

        # 如果有分類（不只是'未分類'），顯示按鈕篩選器
        if len(all_books) > 1 or (len(all_books) == 1 and all_books[0] != '未分類'):
             st.subheader("📚 選擇範圍")
             st.caption("請點擊按鈕選擇要練習的冊別（可多選）：")
             
             # 使用 columns 排列按鈕
             cols = st.columns(3) # 一行3個
             for i, book in enumerate(all_books):
                 col = cols[i % 3]
                 is_selected = book in st.session_state.selected_books
                 
                 if is_selected:
                     # 已選中：顯示為 Primary 顏色，點擊後取消
                     if col.button(f"✅ {book}", key=f"btn_{book}", type="primary", use_container_width=True):
                         st.session_state.selected_books.remove(book)
                         st.rerun()
                 else:
                     # 未選中：顯示為一般顏色，點擊後加入
                     if col.button(f"{book}", key=f"btn_{book}", use_container_width=True):
                         st.session_state.selected_books.append(book)
                         st.rerun()
        else:
            # 如果沒有分類，預設全選
            st.session_state.selected_books = all_books
        
        st.divider()

        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📖 一般練習", use_container_width=True):
                if not full_db:
                    st.error("⚠️ 找不到題庫檔案，請確認 vocabulary.csv 存在。")
                elif not st.session_state.selected_books:
                    st.warning("⚠️ 請至少選擇一冊來進行練習！")
                else:
                    # 根據選擇的冊別過濾
                    filtered_db = [item for item in full_db if item['book'] in st.session_state.selected_books]
                    
                    if len(filtered_db) < 3:
                        st.warning(f"⚠️ 選擇範圍內的生字少於 3 個 (共 {len(filtered_db)} 個)，無法開始遊戲。")
                    else:
                        st.session_state.db = filtered_db
                        st.session_state.game_mode = 'general'
                        reset_game()
                        next_question()
                        st.rerun()

        with col2:
            if st.button("🔧 錯題複習", use_container_width=True):
                if not os.path.exists(ERROR_LOG_FILE):
                    st.warning("⚠️ 目前還沒有錯題紀錄喔！")
                elif not st.session_state.selected_books:
                    st.warning("⚠️ 請至少選擇一冊來進行複習！")
                else:
                    # 讀取錯題
                    mistakes_db = load_vocabulary(ERROR_LOG_FILE)
                    
                    if not mistakes_db:
                        st.warning("⚠️ 錯題檔案讀取失敗或內容為空。")
                    else:
                        # 建立生字對應冊別的查表 (從完整題庫中)
                        char_to_book = {item['char']: item['book'] for item in full_db}
                        
                        # 過濾錯題：只保留在「已選冊別」中的字
                        # 注意：如果錯題本裡的字在主題庫找不到（例如被刪除了），預設歸類為 '未分類'
                        filtered_mistakes = []
                        for item in mistakes_db:
                            book = char_to_book.get(item['char'], '未分類')
                            if book in st.session_state.selected_books:
                                # 把冊別資訊補進去 (雖然遊戲中可能用不到，但保持資料完整)
                                item['book'] = book
                                filtered_mistakes.append(item)
                        
                        if len(filtered_mistakes) < 3:
                            st.warning(f"⚠️ 選擇範圍內的錯題少於 3 個 (共 {len(filtered_mistakes)} 個)，請先多練習累積錯題！")
                        else:
                            st.session_state.db = filtered_mistakes
                            st.session_state.game_mode = 'review'
                            reset_game()
                            next_question()
                            st.rerun()

    # Game Interface
    elif st.session_state.game_mode in ['general', 'review']:
        
        # Display Score
        col_score1, col_score2 = st.columns([3, 1])
        with col_score1:
            st.caption(f"目前模式: {'一般練習' if st.session_state.game_mode == 'general' else '錯題複習'}")
        with col_score2:
            st.metric("得分", f"{st.session_state.score} / {st.session_state.total_answered}")
        
        # Check if we have a question
        if st.session_state.current_question is None:
            next_question()
            st.rerun()
            
        q = st.session_state.current_question
        
        # Display Question
        st.divider()
        if q['mode'] == 1:
            # Char -> Zhuyin
            st.markdown(f"<div class='big-char'>{q['target']['char']}</div>", unsafe_allow_html=True)
            question_text = "請選擇正確的 <b>注音</b>"
        else:
            # Zhuyin -> Char
            st.markdown(f"<div class='big-char'>{q['target']['zhuyin']}</div>", unsafe_allow_html=True)
            question_text = "請選擇正確的 <b>國字</b>"
            
        st.markdown(f"<div class='question-text'>{question_text}</div>", unsafe_allow_html=True)
        # st.divider()

        # Display Options or Feedback
        if st.session_state.feedback:
            # Show feedback
            if st.session_state.feedback['type'] == 'success':
                st.success(st.session_state.feedback['msg'], icon="✅")
            else:
                st.error(st.session_state.feedback['msg'], icon="❌")
            
            # 顯示「聽讀音」按鈕
            col_audio, col_next = st.columns([1, 2])
            
            with col_audio:
                if st.session_state.char_to_speak:
                    if st.button("🔊 聽讀音", use_container_width=True, type="secondary"):
                        st.session_state.show_audio_player = True
                        st.rerun()
            
            with col_next:
                if st.button("下一題 ➡️", type="primary", use_container_width=True):
                    next_question()
                    st.rerun()
            
            # 如果用戶點擊了「聽讀音」，使用 JavaScript 直接播放
            if st.session_state.show_audio_player and st.session_state.char_to_speak:
                with st.spinner('載入語音中...'):
                    play_audio_with_javascript(st.session_state.char_to_speak)
        else:
            # Show Options
            cols = st.columns(3)
            for i, opt in enumerate(q['options']):
                with cols[i]:
                    # Determine button label based on mode
                    label = opt['zhuyin'] if q['mode'] == 1 else opt['char']
                    if st.button(label, key=f"opt_{i}", use_container_width=True):
                        check_answer(opt)
                        st.rerun()

if __name__ == "__main__":
    main()
