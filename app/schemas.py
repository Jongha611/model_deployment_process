from pydantic import BaseModel, Field


class PredictRequest(BaseModel):

    text: str = Field(
        min_length=1,
        description="최대 글자 수 입력 제한은 없지만, 500자 이후로는 자동으로로 잘려서 처리됩니다.",
    )


class PredictResponse(BaseModel):

    label: str
    score: float


