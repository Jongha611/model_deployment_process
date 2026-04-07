```
### Day 8 최종 체크포인트

Q1. 본인의 프로젝트에서 Pydantic 검증은 어떤 잘못된 입력을 막아줍니까?
- 잘못된 타입의 입력

Q2. Depends(verify_api_key)를 제거하면 어떤 위험이 있습니까?
- 디펜즈가 추론전 베리파이 함수를 호출하지 않으므로 인증없이 무분별하게 자원이 쓰일 수 있습니다.

Q3. run_in_executor를 사용한 이유는 무엇입니까?
- 우리는 hub서버를 설계하는 것이 아니라 연산이 들어가는 엔드포인트를 서빙하기 때문에 cpu bound을 할 공간이 필요

Q4. Day 1~8 중 가장 많이 참고한 Day는 어디였습니까? 왜?
- day3 비동기: 관심이 많기 때문입니다. 그리고 이해가 잘 안됐습니다.

Q5. 이 서비스를 실제로 배포하려면 추가로 무엇이 필요합니까?
- 결제 모듈

### 이미지
<img width="1919" height="835" alt="image" src="https://github.com/user-attachments/assets/3eb3e057-848b-4f5d-8510-37ef3b22ce54" />
