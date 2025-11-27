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

# 正向回饋語句庫
praises = ["太棒了！🎉", "完全正確！🌟", "你真厲害！💪", "水啦！答對了！✨", "Excellent!", "你是漢字小天才！🎓"]

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
                        'zhuyin': clean_row['zhuyin']
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
            # st.toast(f"📝 [{word_data['char']}] 已加入複習清單！") # Optional: show toast
            
    except Exception as e:
        st.error(f"⚠️ 無法寫入錯題紀錄: {e}")

def get_question(db):
    """產生題目與選項"""
    if len(db) < 3:
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

def reset_game():
    st.session_state.current_question = None
    st.session_state.score = 0
    st.session_state.total_answered = 0
    st.session_state.feedback = None

def next_question():
    target, options, mode = get_question(st.session_state.db)
    st.session_state.current_question = {
        'target': target,
        'options': options,
        'mode': mode
    }
    st.session_state.feedback = None

def check_answer(selected_option):
    target = st.session_state.current_question['target']
    
    st.session_state.total_answered += 1
    
    if selected_option == target:
        st.session_state.score += 1
        st.session_state.feedback = {
            'type': 'success',
            'msg': f"✅ {random.choice(praises)}"
        }
    else:
        st.session_state.feedback = {
            'type': 'error',
            'msg': f"❌ 哎呀，正確答案是： {target['char']} {target['zhuyin']}"
        }
        log_mistake(target)
    
    # Delay slightly or show a 'Next' button? 
    # For simplicity in Streamlit, we usually update state and force rerun.
    # We will show the feedback and a "Next Question" button.

def main():
    st.set_page_config(page_title="美洲華語生字小幫手", page_icon="📝")
    init_session_state()

    st.title("📝 美洲華語生字小幫手")

    # Sidebar for navigation
    if st.button("🏠 回主選單"):
        st.session_state.game_mode = None
        reset_game()
        st.rerun()

    # Main Menu
    if st.session_state.game_mode is None:
        st.header("請選擇模式")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📖 一般練習模式", use_container_width=True):
                db = load_vocabulary(VOCAB_FILE)
                if not db:
                    st.error("⚠️ 找不到題庫檔案，請確認 vocabulary.csv 存在。")
                elif len(db) < 3:
                    st.warning("⚠️ 題庫生字少於 3 個，無法開始遊戲。")
                else:
                    st.session_state.db = db
                    st.session_state.game_mode = 'general'
                    reset_game()
                    next_question()
                    st.rerun()

        with col2:
            if st.button("🔧 錯題複習模式", use_container_width=True):
                if not os.path.exists(ERROR_LOG_FILE):
                    st.warning("⚠️ 目前還沒有錯題紀錄喔！")
                else:
                    db = load_vocabulary(ERROR_LOG_FILE)
                    if not db:
                        st.warning("⚠️ 錯題檔案讀取失敗或內容為空。")
                    elif len(db) < 3:
                        st.warning("⚠️ 錯題生字少於 3 個，請先多練習累積錯題！")
                    else:
                        st.session_state.db = db
                        st.session_state.game_mode = 'review'
                        reset_game()
                        next_question()
                        st.rerun()

    # Game Interface
    elif st.session_state.game_mode in ['general', 'review']:
        
        # Display Score
        st.caption(f"目前模式: {'一般練習' if st.session_state.game_mode == 'general' else '錯題複習'}")
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
            st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{q['target']['char']}</h1>", unsafe_allow_html=True)
            question_text = "請選擇正確的**注音**："
        else:
            # Zhuyin -> Char
            st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{q['target']['zhuyin']}</h1>", unsafe_allow_html=True)
            question_text = "請選擇正確的**國字**："
            
        st.markdown(f"<h3 style='text-align: center;'>{question_text}</h3>", unsafe_allow_html=True)
        st.divider()

        # Display Options or Feedback
        if st.session_state.feedback:
            # Show feedback
            if st.session_state.feedback['type'] == 'success':
                st.success(st.session_state.feedback['msg'])
            else:
                st.error(st.session_state.feedback['msg'])
            
            if st.button("下一題 ➡️", type="primary", use_container_width=True):
                next_question()
                st.rerun()
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
