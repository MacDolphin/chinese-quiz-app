# Adventure Mode View
# 勇者闖關模式介面

import streamlit as st
import random
from app.core import config
from app.ui.views.quiz_view import handle_answer, prepare_next_question
from app.services import audio_service

def render_adventure_view():
    """渲染冒險闖關介面"""
    if st.session_state.player_hp <= 0:
        st.error("💀 你被打敗了... 勇者請重新來過！")
        if st.button("🏠 回主選單"):
            st.session_state.game_mode = None
            st.rerun()
        return

    if st.session_state.monster_hp <= 0:
        st.balloons()
        st.success("🏆 恭喜！你打敗了魔王！")
        if st.button("🏠 回主選單"):
            st.session_state.game_mode = None
            st.rerun()
        return

    # 狀態列 (Status Bars)
    col_p, col_m = st.columns(2)
    with col_p:
        st.write(f"❤️ 我的體力: {'❤️' * st.session_state.player_hp}")
    with col_m:
        st.write(f"👾 魔王體力: {st.session_state.monster_hp}%")
        st.progress(st.session_state.monster_hp / 100)

    # 顯示目前怪物 (Show Monster)
    if not st.session_state.current_monster:
        st.session_state.current_monster = random.choice(config.MONSTERS)
    
    st.markdown(f"<div style='text-align: center; font-size: 100px;'>{st.session_state.current_monster}</div>", unsafe_allow_html=True)

    # 借用 Quiz View 的邏輯 (Reuse quiz logic)
    from app.ui.views import quiz_view
    quiz_view.render_quiz_view()

    # 針對冒險模式的額外生命值扣減邏輯已在 handle_answer 中處理
