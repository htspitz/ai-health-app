from fastapi import FastAPI,HTTPException,Depends
from schemas import AnalysisRequest, AnalysisResponse, HistoryResponse
import engine as eng # 既存のロジックをインポート
import database as db
import traceback
import os

app = FastAPI()

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_health_data(request: AnalysisRequest):
    try:
        # 1. 匿名化処理
        masked = eng.mask_entities(request.input_text)

        # 2. 【追加】AIに渡すための「過去の履歴」をDBから取得
        past_history = db.get_chat_history(limit=3) 
        
        # 3. AIによる要約生成（履歴を渡す）
        summary = eng.ask_ai(masked, history=past_history)

        # 4. 今回の結果をデータベースに保存
        db.save_record(
            user_name=request.user_name,
            input_text=request.input_text,
            ai_summary=summary
        )
        
        return AnalysisResponse(
            masked_text=masked, 
            summary=summary,
            status="success"
        )
    
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history", response_model=list[HistoryResponse])
async def get_history():
    # DBから最新5件の履歴を取得して返す
    history = db.get_chat_history(limit=5)

    return[
        {
            "timestamp": record.created_at.strftime("%Y-%m-%d %H:%M:%S") if record.created_at else None, 
            "user_name": record.user_name,
            "summary": record.ai_summary
        }
        for record in history
    ]