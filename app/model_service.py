from fastapi import FastAPI, HTTPException, Depends
from app.schemas import PredictRequest, PredictResponse
from transformers import pipeline
import asyncio
from app.auth import verify_api_key


try:
    pipe = pipeline("text-classification", model="snunlp/KR-FinBert-SC")

    print("파이프라인 로드 완료")
except Exception as e:
    pipe = None

    print(f"파이프라인 로드 실패: {e}")
    

app = FastAPI(
    title="뉴스 분석",
    description="뉴스 원문 문자열을 넣으면 뉴스의 성격을 추론합니다.",
)


@app.post(path="/predict", response_model=PredictResponse)
async def predict(
    request: PredictRequest,
    user: str = Depends(verify_api_key)
 ) -> PredictResponse:

    if not pipe:
        raise HTTPException(
            status_code=503,
            detail="파이프라인 없음"
        )

    try:
        loop = asyncio.get_running_loop()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"비동기 루프가 생성되지 않았습니다: {e}"
        )

    truncated_text = request.text[:500] 

    try:
        response = await loop.run_in_executor(
            None,
            pipe,
            truncated_text,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"응답에 문제 발생: {e}"
        )

    return PredictResponse(
        label=response[0]["label"],
        score=round(number=response[0]["score"], ndigits=4),
    )