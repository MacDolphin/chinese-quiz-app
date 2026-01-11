# Main entry point for the Streamlit app
# 程式進入點

import streamlit as st
import random
from app.core import config
from app.ui import styles
from app.ui.views import main_menu, quiz_view, adventure_view, memory_view
from app.services import game_service
from app.repositories import vocab_repository

def init_session_state():
    """
    初始化所有 session state 變數。
    Initialize all session state variables.
    """
    defaults = {
        'current_question': None,
        'score': 0,
        'total_answered': 0,
        'feedback': None,
        'game_mode': None,  # 'general', 'review', 'adventure', 'memory'
        'db': [],
        'full_db': [],
        'char_to_speak': None,
        'auto_play_audio': False,
        'selected_books': [],
        
        # Adventure
        'monster_hp': config.INITIAL_MONSTER_HP,
        'player_hp': config.INITIAL_PLAYER_HP,
        'current_monster': None,
        
        # Memory
        'memory_cards': [],
        'flipped_indices': [],
        'memory_solved': False,
    }
    
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def start_game(mode_name, full_db):
    """
    點擊模式按鈕後的啟動邏輯。
    Game startup logic after clicking a mode button.
    """
    if not st.session_state.selected_books:
        st.warning("⚠️ 請至少選擇一冊！")
        return

    # 過濾題庫 (Filter DB by selected books)
    filtered_db = [item for item in full_db if item['book'] in st.session_state.selected_books]
    
    # 錯題複習特殊處理 (Special handling for Review mode)
    if mode_name == 'review':
        mistakes_cache = vocab_repository.load_vocabulary(config.ERROR_LOG_FILE)
        char_to_book = {item['char']: item['book'] for item in full_db}
        filtered_db = []
        for item in mistakes_cache:
            book = char_to_book.get(item['char'], '未分類')
            if book in st.session_state.selected_books:
                item['book'] = book
                filtered_db.append(item)

    if len(filtered_db) < config.MIN_WORDS_FOR_QUIZ and mode_name != 'memory':
        st.warning(f"⚠️ 生字數量不足 ({len(filtered_db)})，請重新選擇範圍")
        return

    st.session_state.db = filtered_db
    st.session_state.game_mode = mode_name
    
    # 重置遊戲狀態 (Reset states)
    st.session_state.score = 0
    st.session_state.total_answered = 0
    st.session_state.feedback = None
    st.session_state.monster_hp = config.INITIAL_MONSTER_HP
    st.session_state.player_hp = config.INITIAL_PLAYER_HP
    st.session_state.current_monster = random.choice(config.MONSTERS)

    if mode_name == 'memory':
        st.session_state.memory_cards = game_service.init_memory_game_cards(filtered_db)
        st.session_state.flipped_indices = []
        st.session_state.memory_solved = False
    else:
        # 產生第一題 (Generate first question)
        target, options, mode = game_service.get_question(filtered_db, full_db)
        st.session_state.current_question = {'target': target, 'options': options, 'mode': mode}
    
    st.rerun()

def main():
    """主程式循環"""
    st.set_page_config(page_title="美洲華語生字小幫手", page_icon="📝", layout="wide")
    styles.load_custom_css()
    init_session_state()

    # 側邊欄 (Sidebar)
    with st.sidebar:
        st.title("📝 華語學習助手")
        if st.button("🏠 回主選單", use_container_width=True):
            st.session_state.game_mode = None
            st.rerun()
        st.divider()
        st.caption("Designed for Tablet Interface")

    # 視圖切換 (View Routing)
    mode = st.session_state.game_mode
    if mode is None:
        main_menu.render_main_menu(on_start_game=start_game)
    elif mode in ['general', 'review']:
        quiz_view.render_quiz_view()
    elif mode == 'adventure':
        adventure_view.render_adventure_view()
    elif mode == 'memory':
        memory_view.render_memory_view()

if __name__ == "__main__":
    main()
