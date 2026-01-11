# Main Menu View
# 主選單介面

import streamlit as st
from typing import List
from app.core import config
from app.repositories import vocab_repository

def get_book_sort_key(book_name: str) -> int:
    """自定義排序函式 (讓第一冊、第二冊...依序排列)"""
    cn_map = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
    try:
        if book_name.startswith("第") and book_name.endswith("冊"):
            num_str = book_name[1:-1]
            if num_str in cn_map:
                return cn_map[num_str]
    except:
        pass
    return 100

def render_main_menu(on_start_game):
    """
    渲染主選單。
    Render the main menu.
    """
    st.header("請選擇模式")
    
    # 載入題庫
    full_db = vocab_repository.load_vocabulary(config.VOCAB_FILE)
    st.session_state.full_db = full_db
    
    # 取得排序後的冊別
    all_books = sorted(list(set(item['book'] for item in full_db)), key=get_book_sort_key)
    
    # 冊別選擇區
    if len(all_books) > 1 or (len(all_books) == 1 and all_books[0] != '未分類'):
        st.subheader("📚 選擇範圍")
        st.caption("請點擊按鈕選擇要練習的冊別（可多選）：")
        
        cols = st.columns(3)
        for i, book in enumerate(all_books):
            col = cols[i % 3]
            is_selected = book in st.session_state.selected_books
            
            if is_selected:
                if col.button(f"✅ {book}", key=f"btn_{book}", type="primary", use_container_width=True):
                    st.session_state.selected_books.remove(book)
                    st.rerun()
            else:
                if col.button(f"{book}", key=f"btn_{book}", use_container_width=True):
                    st.session_state.selected_books.append(book)
                    st.rerun()
    else:
        st.session_state.selected_books = all_books
    
    st.divider()

    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📖 一般練習", use_container_width=True):
            on_start_game('general', full_db)

    with col2:
        if st.button("⚔️ 勇者闖關", use_container_width=True):
            on_start_game('adventure', full_db)

    with col3:
        if st.button("🔧 錯題複習", use_container_width=True):
            on_start_game('review', full_db)

    st.divider()
    col4, col5 = st.columns(2)
    with col4:
        if st.button("🧩 翻牌配對", use_container_width=True):
            on_start_game('memory', full_db)
