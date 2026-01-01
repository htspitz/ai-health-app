from regex import E
import spacy
import re
import os
import requests
import json

nlp = spacy.load("ja_ginza")

def mask_entities(text):
    """個人情報の匿名化"""
    doc = nlp(text)
    masked_text = text
    date_pattern = r'\d{2,4}[年/-]\d{1,2}[月/-]\d{1,2}日?'
    blood_pressure = r'(?:血圧)?\s?\d{2,3}/\d{2,3}'

    for ent in reversed(doc.ents):
        if ent.label_ in ["Person", "GPE", "Province", "City", "Title_Other", "Hospital", "School"]:
            masked_text = masked_text[:ent.start_char] + f"[{ent.label_}]" + masked_text[ent.end_char:]

    masked_text = re.sub(date_pattern, '[DATE]', masked_text)
    masked_text = re.sub(blood_pressure, '[BP_VALUE]', masked_text)
    return masked_text

# 環境変数からモデル名を取得
MODEL_NAME = os.getenv("AI_MODEL_NAME", "qwen2.5:3b")
# Docker内部からホストPCのOllamaを呼ぶための魔法のURL
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434/api/generate")

def ask_ai(user_input: str, history: list = None) -> str:
    # 履歴をテキスト化する
    history_context = ""
    if history:
        history_context = "\n### 過去の相談履歴:\n"
        # 古い順に並べてコンテキスト化
        for h in reversed(history):
            history_context += f"- 相談: {h.input_text}\n アドバイス: {h.ai_summary}\n"
            
    # プロンプトの組み立て
    prompt = f"""あなたは親切な健康アドバイザーです。
    過去の履歴がある場合は、それらを踏まえて変化を褒めたり、継続的な改善を促してください。
    個人情報がマスキングされた健康診断結果を受け取り、ユーザーに寄り添ったポジティブな要約と改善アドバイスを提供してください。
    {history_context}
    ### 今回のデータ:
    {user_input}

    ### アドバイス:
    """

    # --- ここに追加！ ---
    print("\n--- [DEBUG] 実際に送信されるプロンプト ---")
    print(prompt)
    print("----------------------------------------\n")
    # ------------------

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "申し訳ありませんが、要約の生成に失敗しました。")
    except Exception as e:
        return f"Error communicating with Ollama: {str(e)}"