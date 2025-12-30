import requests

# 送りたいデータ
data = {
    "user_name": "長谷川",
    "input_text": "血圧が高いです"
}

# 1. データをPOST（送信）して、返事をもらう
response = requests.post("http://localhost:8000/analyze", json={"user_name": "長谷川","input_text": "血圧が高いです"})
print(f"■ヘッダー：{response.headers}")
print(f"■本文：{response.text}")
print(f"■JSON開封dict版：{response.json()}")
print(f"■dictのサマリ：{response.json()['summary']}")

# 2. 返ってきた中身（JSON）を辞書として取り出す
# result = response.json()

# print(result["summary"]) # AIのアドバイスを表示！