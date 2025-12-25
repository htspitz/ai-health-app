import streamlit as st
import os
from dotenv import load_dotenv
import database as db
import engine as eng

# 初期設定
load_dotenv()
db.init_db()

st.title("🛡️ AI健康診断要約アプリ")

# サイドバー
model_choice = st.sidebar.selectbox("モデル選択", ("Claude 4.5 Sonnet", "Claude 4.5 Haiku"))
st.sidebar.markdown("---")
st.sidebar.subheader("履歴")

# 履歴表示（db.pyから取得）
history = db.get_chat_history()
for row in history:
    with st.sidebar.expander(f"📅 {row[0][:16]}"):
        st.write(row[1])

# メイン画面
user_input = st.text_area("テキスト入力")
if st.button("1. クレンジング実行") and user_input:
    st.session_state.masked = eng.mask_entities(user_input)
    st.success("匿名化完了")

if "masked" in st.session_state:
    st.code(st.session_state.masked)
    if st.button("2. 要約生成"):
        summary = eng.summarize_with_ai(st.session_state.masked, model_choice)
        st.write(summary)
        # DBへ保存
        db.save_record("長谷川さん", st.session_state.masked, summary)
        st.toast("保存しました！")