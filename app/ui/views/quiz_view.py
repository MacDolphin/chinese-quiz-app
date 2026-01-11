# Quiz View for General and Review modes
# 一般練習與錯題複習介面

import streamlit as st
import random
from app.core import config
from app.services import audio_service, game_service
from app.repositories import vocab_repository

def render_quiz_view():
    """渲染測驗介面 (一般/複習)"""
    q = st.session_state.current_question
    target = q.get('target') if q else None
    options = q.get('options') if q else None
    mode = q.get('mode') if q else None

    if not target:
        st.balloons()
        st.success("🎉 太棒了！你已經完成了所有練習！")
        if st.button("🏠 回主選單", use_container_width=True):
            st.session_state.game_mode = None
            st.rerun()
        return

    # 顯示問題 (Question Display)
    st.markdown(f"<div style='text-align: center; font-size: 80px; padding: 20px;'>", unsafe_allow_html=True)
    if mode == 1: # 看字選注音
        st.write(f"### {target['char']}")
        st.write("這是什麼注音？")
    else: # 看注音選字
        st.write(f"### {target['zhuyin']}")
        st.write("這是哪一個字？")
    st.markdown("</div>", unsafe_allow_html=True)

    # 選項按鈕 (Option Buttons)
    cols = st.columns(len(options))
    for i, opt in enumerate(options):
        label = opt['zhuyin'] if mode == 1 else opt['char']
        if cols[i].button(label, key=f"opt_{i}", use_container_width=True):
            handle_answer(opt)

    # 反饋區 (Feedback Area)
    if st.session_state.feedback:
        fb = st.session_state.feedback
        if fb['type'] == 'success':
            st.success(fb['msg'])
        else:
            st.error(fb['msg'])
        
        if st.button("下一題 ➡️", type="primary", use_container_width=True):
            prepare_next_question()
            st.rerun()

    # 自動播放音訊 (Auto Play Audio)
    if st.session_state.char_to_speak and st.session_state.auto_play_audio:
        audio_service.generate_audio_html(st.session_state.char_to_speak)
        st.session_state.auto_play_audio = False

def handle_answer(selected_option):
    """處理答案點擊事件"""
    target = st.session_state.current_question['target']
    st.session_state.total_answered += 1
    
    if selected_option['char'] == target['char']:
        st.session_state.score += 1
        praise = random.choice(config.PRAISES)
        msg = f"✅ {praise['text']}{praise['emoji']}"
        
        # 冒險模式：扣減魔王體力
        # Adventure Mode: Decrease monster HP
        if st.session_state.game_mode == 'adventure':
            st.session_state.monster_hp -= config.DAMAGE_PER_CORRECT
            if st.session_state.monster_hp < 0:
                st.session_state.monster_hp = 0

        if st.session_state.game_mode == 'review':
            try:
                vocab_repository.remove_mistake_from_file(target)
                msg += " (已從錯題本移除)"
            except Exception:
                msg += " (⚠️ 紀錄更新失敗)"
            
            # 從當前題庫移除，避免重複抽到
            st.session_state.db = [item for item in st.session_state.db if item['char'] != target['char']]

        st.session_state.feedback = {'type': 'success', 'msg': msg}
    else:
        st.session_state.feedback = {
            'type': 'error', 
            'msg': f"❌ 哎呀，正確答案是： {target['char']} {target['zhuyin']}"
        }
        vocab_repository.log_mistake(target)
        # 冒險模式：扣減玩家體力
        # Adventure Mode: Decrease player HP
        if st.session_state.game_mode == 'adventure':
            st.session_state.player_hp -= 1

    st.session_state.char_to_speak = target['char']
    st.session_state.auto_play_audio = True

def prepare_next_question():
    """準備下一題數據"""
    target, options, mode = game_service.get_question(st.session_state.db, st.session_state.full_db)
    st.session_state.current_question = {'target': target, 'options': options, 'mode': mode}
    st.session_state.feedback = None
    st.session_state.char_to_speak = None
