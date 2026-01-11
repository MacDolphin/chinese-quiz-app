# UI Styles handling
# UI 樣式處理

import os
import streamlit as st
from app.core import config

def load_custom_css() -> None:
    """
    載入自訂 CSS 樣式。
    Load custom CSS styles.
    """
    if os.path.exists(config.CSS_FILE):
        with open(config.CSS_FILE, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        # 後備樣式 (Fallback styles)
        st.markdown("""
        <style>
        div.stButton > button {
            font-size: 28px !important;
            height: 80px !important;
            border-radius: 15px !important;
        }
        </style>
        """, unsafe_allow_html=True)

def inject_memory_card_styles() -> None:
    """
    專門為記憶遊戲卡片注入的特殊樣式。
    Special styles for memory game cards.
    """
    st.markdown("""
    <style>
    /* 強制設定主區域所有按鈕的寬度 (針對記憶遊戲) */
    /* Force button width for memory game cards */
    section.main .stButton button {
        min-width: 540px !important;
        width: 100% !important;
        font-size: 48px !important;
        height: 100px !important;
    }
    </style>
    """, unsafe_allow_html=True)
