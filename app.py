import streamlit as st
import requests
import os
from dotenv import load_dotenv

# FastAPIのURL（ドッカーで動かしている窓口）
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="AI健康診断要約アプリ", layout="wide")

st.title("🛡️ AI健康診断要約アプリ")
st.caption("あなたの健康診断結果に基づき、AIが匿名化してアドバイスします。")

@st.fragment # ← これが魔法の呪文です！
def show_history():
    st.header("最近の相談履歴")
    if st.button("履歴を更新"):
        try:
            response = requests.get(f"{BACKEND_URL}/history")
            if response.status_code == 200:
                history = response.json()
                if not history:
                    st.write("履歴はまだありません。")
                for item in history:
                    with st.expander(f"🕒 {item['timestamp']}"):
                        st.write(f"**相談者:** {item['user_name']}")
                        st.write(f"**AI:** {item['summary']}")
            else:
                st.error("履歴の取得に失敗しました。")
        except Exception as e:
            st.error(f"接続エラー: {e}")

# サイドバー
with st.sidebar:
    show_history()

# --- メイン画面：入力フォーム ---
with st.form("my_form"):
    user_name = st.text_input("お名前", value="長谷川")
    input_text = st.text_area("相談内容や健康診断の結果を入力してください", placeholder="例：血圧が140あります。")
    
    submitted = st.form_submit_button("AI保健師に相談する")

# --- 実行ボタンが押された時の処理 ---
if submitted:
    if not input_text:
        st.warning("相談内容を入力してください。")
    else:
        with st.spinner("AIが分析中..."):
            # FastAPIの /analyze 窓口にデータを送る
            payload = {
                "user_name": user_name,
                "input_text": input_text
            }
            try:
                response = requests.post(f"{BACKEND_URL}/analyze", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("分析が完了しました！")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info("💡 匿名化されたデータ")
                        st.code(result["masked_text"])
                    with col2:
                        st.info("🤖 AIのアドバイス")
                        st.write(result["summary"])
                else:
                    st.error(f"エラーが発生しました（コード: {response.status_code}）")
            except Exception as e:
                st.error(f"サーバーに接続できません: {e}")