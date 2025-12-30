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
        # 1. AIによる匿名化と要約生成
        masked = eng.mask_entities(request.input_text)
        summary = eng.ask_ai(masked)

        # 2. データベースに保存
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