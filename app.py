import streamlit as st
import time
import os
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 8: O cengel", page_icon="🎨", layout="centered")

# CSS 優化
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        font-size: 24px;
        background-color: #FFD700;
        color: #333;
        border: none;
        padding: 10px;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background-color: #FFC107;
        transform: scale(1.02);
    }
    .big-font {
        font-size: 36px !important;
        font-weight: bold;
        color: #2E86C1;
        text-align: center;
        margin-bottom: 5px;
    }
    .med-font {
        font-size: 22px !important;
        color: #555;
        text-align: center;
        margin-bottom: 10px;
    }
    .card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    /* 顏色球樣式 */
    .color-circle {
        height: 60px;
        width: 60px;
        border-radius: 50%;
        display: inline-block;
        margin-bottom: 10px;
        border: 2px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 數據資料庫 (Unit 8 專屬) ---

# 單字：顏色 (全部小寫)
# 備註：langdaway 有時指青色/藍色/綠色，kangdaway 專指綠色，這裡做教學區分
VOCABULARY = {
    "kahengangay": {"zh": "紅色", "color": "#FF0000", "file": "u8_kahengangay"},
    "kohecalay":   {"zh": "白色", "color": "#FFFFFF", "file": "u8_kohecalay"},
    "kohetingay":  {"zh": "黑色", "color": "#000000", "file": "u8_kohetingay"},
    "kalawlaway":  {"zh": "黃色", "color": "#FFD700", "file": "u8_kalawlaway"},
    "langdaway":   {"zh": "藍色", "color": "#1E90FF", "file": "u8_langdaway"},
    "kangdaway":   {"zh": "綠色", "color": "#32CD32", "file": "u8_kangdaway"}
}

# 句型：描述顏色
SENTENCES = [
    {"amis": "O maan ko cengel?", "zh": "是什麼顏色？", "file": "u8_q_what_color"},
    {"amis": "Kohecalay ko waco.", "zh": "狗是白色的。", "file": "u8_s_white_dog"},
    {"amis": "Kahengangay ko cidal.", "zh": "太陽是紅色的。", "file": "u8_s_red_sun"}
]

# --- 1.5 智慧語音核心 ---
def play_audio(text, filename_base=None):
    if filename_base:
        path_m4a = f"audio/{filename_base}.m4a"
        if os.path.exists(path_m4a):
            st.audio(path_m4a, format='audio/mp4')
            return
        path_mp3 = f"audio/{filename_base}.mp3"
        if os.path.exists(path_mp3):
            st.audio(path_mp3, format='audio/mp3')
            return

    try:
        # 使用印尼語 (id) 模擬南島語系發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    except:
        st.caption("🔇 (無聲)")

# --- 2. 狀態管理 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0

# --- 3. 學習模式 ---
def show_learning_mode():
    st.markdown("<h2 style='text-align: center;'>Sakafalo: O cengel</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>繽紛的顏色 🎨</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    words = list(VOCABULARY.items())
    
    for idx, (amis, data) in enumerate(words):
        with (col1 if idx % 2 == 0 else col2):
            with st.container():
                # 使用 HTML 畫出顏色圓圈
                st.markdown(f"""
                <div class="card">
                    <div class="color-circle" style="background-color: {data['color']};"></div>
                    <div class="big-font">{amis}</div>
                    <div class="med-font">{data['zh']}</div>
                </div>
                """, unsafe_allow_html=True)
                play_audio(amis, filename_base=data.get('file'))

    st.markdown("---")
    st.markdown("### 🗣️ 句型練習")
    
    # 問句
    st.markdown("#### ❓ 詢問顏色")
    q1 = SENTENCES[0]
    st.info(f"🔹 {q1['amis']} ({q1['zh']})")
    play_audio(q1['amis'], filename_base=q1.get('file'))
    
    # 描述句 (結合之前的單字)
    st.markdown("#### 🐶 描述事物")
    s2 = SENTENCES[1]
    st.warning(f"🔹 {s2['amis']} ({s2['zh']})")
    play_audio(s2['amis'], filename_base=s2.get('file'))

    s3 = SENTENCES[2]
    st.success(f"🔹 {s3['amis']} ({s3['zh']})")
    play_audio(s3['amis'], filename_base=s3.get('file'))

# --- 4. 測驗模式 ---
def show_quiz_mode():
    st.markdown("<h2 style='text-align: center;'>🎮 Sakafalo 顏色大師</h2>", unsafe_allow_html=True)
    progress = st.progress(st.session_state.current_q / 3)
    
    # 第一關：聽音辨色
    if st.session_state.current_q == 0:
        st.markdown("### 第一關：這是什麼顏色？")
        st.write("請聽單字：")
        play_audio("kohetingay", filename_base="u8_kohetingay")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⚫ 黑色"):
                st.balloons()
                st.success("答對了！ Kohetingay 是黑色！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c2:
            if st.button("⚪ 白色"): st.error("不對喔，白色是 kohecalay！")

    # 第二關：句子理解 (聽力)
    elif st.session_state.current_q == 1:
        st.markdown("### 第二關：狗是什麼顏色？")
        st.markdown("#### 請聽句子：")
        play_audio("Kohecalay ko waco.", filename_base="u8_s_white_dog")
        
        st.write("請問你聽到了什麼？")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🐶 黑色的狗"): st.error("不對喔！")
        with c2:
            if st.button("🐶 白色的狗"):
                st.snow()
                st.success("沒錯！ Kohecalay (白的) ko waco.")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()

    # 第三關：看圖問答
    elif st.session_state.current_q == 2:
        st.markdown("### 第三關：看圖回答")
        st.markdown("#### Q: O maan ko cengel? (這是什麼顏色？)")
        play_audio("O maan ko cengel?", filename_base="u8_q_what_color") 
        
        # 顯示紅色太陽
        st.markdown("<div style='font-size:80px; text-align:center;'>☀️</div>", unsafe_allow_html=True)
        st.caption("提示：太陽 (cidal)")
        
        options = ["Kahengangay (紅色)", "Langdaway (藍色)", "Kohetingay (黑色)"]
        choice = st.radio("請選擇：", options)
        
        if st.button("確定送出"):
            if "Kahengangay" in choice:
                st.balloons()
                st.success("太厲害了！全部答對！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.error("再看一次喔，太陽通常是紅色的 (kahengangay)！")

    else:
        st.markdown(f"<div style='text-align: center;'><h1>🏆 挑戰完成！</h1><h2>得分：{st.session_state.score}</h2></div>", unsafe_allow_html=True)
        if st.button("再玩一次"):
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.rerun()

# --- 5. 主程式入口 ---
st.sidebar.title("Unit 8: O cengel 🎨")
mode = st.sidebar.radio("選擇模式", ["📖 學習單詞", "🎮 練習挑戰"])

if mode == "📖 學習單詞":
    show_learning_mode()
else:
    show_quiz_mode()
