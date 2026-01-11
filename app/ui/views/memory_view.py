# Memory Game View
# 記憶翻牌配對介面

import streamlit as st
from app.core import config
from app.ui import styles
from app.services import audio_service

def render_memory_view():
    """渲染記憶配對介面"""
    st.subheader("🧩 翻牌配對")
    
    # 說明：針對卡片進行樣式優化，避免在大寬度下導致版面崩潰
    # Description: Optimize card styles to prevent layout collapse on narrow screens
    st.markdown("""
    <style>
    section.main .stButton button {
        width: 100% !important;
        height: 120px !important;
        font-size: 32px !important;
        margin-bottom: 10px !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.session_state.memory_solved:
        st.balloons()
        st.success("🎉 恭喜！你完成了配對！")
        if st.button("🔄 再玩一次", type="primary"):
            from app.services import game_service
            st.session_state.memory_cards = game_service.init_memory_game_cards(st.session_state.db)
            st.session_state.flipped_indices = []
            st.session_state.memory_solved = False
            st.rerun()
        return

    # 檢查是否有兩張不匹配的卡片，顯示「重試」按鈕
    # Check for mismatch and provide a way to flip them back
    if len(st.session_state.flipped_indices) == 2:
        from app.services import game_service
        if not game_service.check_memory_match(st.session_state.memory_cards, st.session_state.flipped_indices):
            if st.button("❌ 不匹配，點此重試 / Try Again", type="primary", use_container_width=True):
                st.session_state.flipped_indices = []
                st.rerun()

    # 繪製格線 (Draw card grid)
    cols = st.columns(config.MEMORY_GAME_COLUMNS)
    
    for i, card in enumerate(st.session_state.memory_cards):
        col = cols[i % config.MEMORY_GAME_COLUMNS]
        
        if card['is_matched']:
            col.button("✅", key=f"card_{i}", disabled=True)
        elif i in st.session_state.flipped_indices:
            # 翻開的卡片
            col.button(card['content'], key=f"card_{i}", disabled=True, type="primary")
        else:
            # 未翻開的卡片
            if col.button("🎴", key=f"card_{i}"):
                handle_flip(i)

    # 自動播放音訊 (Audio trigger for char cards)
    if st.session_state.char_to_speak and st.session_state.auto_play_audio:
        audio_service.generate_audio_html(st.session_state.char_to_speak)
        st.session_state.auto_play_audio = False

def handle_flip(index: int):
    """處理卡片翻轉邏輯"""
    # 如果已經翻了兩張且不匹配，點擊第三張時自動重置
    if len(st.session_state.flipped_indices) >= 2:
        st.session_state.flipped_indices = []

    st.session_state.flipped_indices.append(index)
    card = st.session_state.memory_cards[index]
    
    # 如果是字卡就朗讀
    if card['type'] == 'char':
        st.session_state.char_to_speak = card['content']
        st.session_state.auto_play_audio = True

    # 立即檢查配對 (如果是第二張)
    if len(st.session_state.flipped_indices) == 2:
        from app.services import game_service
        if game_service.check_memory_match(st.session_state.memory_cards, st.session_state.flipped_indices):
            idx1, idx2 = st.session_state.flipped_indices
            st.session_state.memory_cards[idx1]['is_matched'] = True
            st.session_state.memory_cards[idx2]['is_matched'] = True
            st.toast("✨ 配對成功！", icon="🎉")
            st.session_state.flipped_indices = []
            
            if all(c['is_matched'] for c in st.session_state.memory_cards):
                st.session_state.memory_solved = True
        else:
            st.toast("❌ 配對失敗", icon="⚠️")
    
    st.rerun()
