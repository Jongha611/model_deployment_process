import streamlit as st
import requests


## Streamlit의 모든 기능은 st 모듈을 통해 접근합니다.
## 페이지 설정입니다. 브라우저 탭 제목, 아이콘, 레이아웃을 지정합니다. 반드시 스크립트의 가장 첫 번째 Streamlit 호출이어야 합니다.
st.set_page_config(
    page_title="News Classification Page",
    layout="centered",
)


API_BASE = "http://localhost:8000"


def call_api(url, api_key, json_data=None, method="post"):
    """API를 호출하고, 실패 시 에러 메시지를 표시합니다."""
    headers = {
        "X-API-KEY": api_key
    }

    try:
        if method == "get":
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=json_data, headers=headers, timeout=30)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("**서버에 연결할 수 없습니다.** FastAPI 서버가 실행 중인지 확인하세요.")

        return None
    except requests.exceptions.Timeout:
        st.warning("⏱**응답 시간 초과.** 잠시 후 다시 시도하세요.")

        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"**서버 에러** (HTTP {e.response.status_code})")

        return None
    except Exception as e:
        st.error(f"**오류:** {type(e).__name__}")
        
        return None


## 텍스트 출력 함수들입니다. st.write()는 입력 타입에 따라 자동으로 렌더링합니다.
st.title("뉴스의 성격을 분석합니다")
st.write("한국어 지원")

# 구분선
st.divider()


# 사이드바에 API 키 입력창 생성
with st.sidebar:
    st.title("🔑 인증 설정")
    api_key = st.text_input("API Key를 입력하세요", type="password", placeholder="테스트키: test-key-001")
    st.info("유효한 키가 있어야 분석이 가능합니다.")


## 입력 위젯입니다. 사용자가 값을 입력하면 스크립트가 재실행되면서 name 변수에 새 값이 들어옵니다.
news = st.text_input("뉴스 원문 텍스트를 입력하세요: ", placeholder="여기에 입력")

## 상태별 메시지 박스입니다. API 응답 결과를 사용자에게 보여줄 때 유용합니다.
if news:
    payload = {"text": news}
    
    with st.spinner("분석중입니다..."):
        result = call_api(
            url="http://localhost:8000/predict", 
            api_key=api_key,
            json_data=payload,
        )

    if result:
        st.success(f"분석이 완료되었습니다")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="분석 결과", value=result["label"])
    with col2:
        st.metric(label="신뢰도 점수", value=f"{result['score']:.4f}")
        
    # 추가적인 시각적 피드백
    if result["label"] == "neutral":
        st.info("이 뉴스는 중립적인 성격을 띠고 있습니다.")
    elif "positive" in result["label"].lower():
        st.write("이 뉴스는 긍정적인 성격을 띠고 있습니다.")
    else:
        st.write("이 뉴스는 부정적인 성격을 띠고 있습니다.")

else:
    st.info("분석할 뉴스 내용을 입력하고 Enter를 눌러주세요.")

# 버튼
if st.button("날짜 확인"):
    from datetime import datetime

    now = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")

    st.write(f"현재 시각: {now}")