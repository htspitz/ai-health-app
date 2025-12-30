from regex import E
import spacy
import re
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
import requests

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


# Docker内部からホストPCのOllamaを呼ぶための魔法のURL
OLLAMA_URL = "http://host.docker.internal:11434/api/generate"

def ask_ai(user_input: str) -> str:
    prompt = f"""あなたは優秀な保健師です。個人情報がマスキングされた健康診断結果を受け取り、ユーザーに寄り添ったポジティブな要約と改善アドバイスを提供してください。

    以下のデータを要約してください：{user_input}
    """

    payload = {
        "model": "qwen2.5:3b",
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
    


'''
def summarize_with_ai(cleaned_text, model_choice):
    # 環境変数から直接取ってきて、明示的に渡す
    # api_key = os.getenv("ANTHROPIC_API_KEY")
    """AIによる要約生成"""
    target_model = "claude-sonnet-4-5" if "Sonnet" in model_choice else "claude-haiku-4-5"
    llm = ChatAnthropic(model=target_model, temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "あなたは優秀な保健師です。個人情報がマスキングされた健康診断結果を受け取り、ユーザーに寄り添ったポジティブな要約と改善アドバイスを提供してください。"),
        ("user", "以下のデータを要約してください：\n\n{data}")
    ])
    chain = prompt | llm
    response = chain.invoke({"data": cleaned_text})
    return response.content
'''