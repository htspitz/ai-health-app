# check_mask.py (一時的な確認用)
import engine

def test_masking():
    # 1. テスト用の「生データ」を準備
    # GiNZAが反応しやすい個人情報（氏名、場所、日付、血圧）を盛り込みます
    test_cases = [
        "私は長谷川です。2025年12月30日に東久留米市の病院へ行きました。",
        "田中太郎と言います。血圧は 145/95 でした。昨日は東京都港区にいました。",
        "佐藤花子です。聖路加国際病院で健診を受け、日付は 2024/01/05 です。"
    ]

    print("=== 匿名化エンジン テスト開始 ===\n")

    for i, raw_text in enumerate(test_cases, 1):
        # 2. engine.py の mask_entities 関数を呼び出す
        masked_text = engine.mask_entities(raw_text)

        print(f"【テストケース {i}】")
        print(f"入力: {raw_text}")
        print(f"出力: {masked_text}")
        print("-" * 30)

if __name__ == "__main__":
    test_masking()