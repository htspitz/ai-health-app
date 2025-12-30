from pydantic import BaseModel
from typing import Optional

# リクエスト（送るデータ）の形
class AnalysisRequest(BaseModel):
    user_name: str
    input_text: str
    model_choice: str = "Claude 4.5 Sonnet"

# レスポンス（返すデータ）の形
class AnalysisResponse(BaseModel):
    masked_text: str
    summary: str
    status: str = "success"

# 履歴表示用のスキーマ（必要に応じて追加可能）
class HistoryResponse(BaseModel):
    timestamp: Optional[str] = None
    user_name: str
    summary: str
