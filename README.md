# KBO DSS 대시보드 — 실행 가이드

## 빠른 시작

```bash
# 1. 의존성 설치 (최초 1회)
pip install -r requirements.txt

# 2. 실행
streamlit run app.py
```

브라우저에서 자동으로 http://localhost:8501 열림.

---

## 다른 노트북에서 시연하는 경우

1. **같은 WiFi** 연결 필수
2. 내 노트북에서 `streamlit run app.py` 실행
3. 터미널에 표시되는 `Network URL: http://192.168.x.x:8501` 복사
4. 상대방 노트북 크롬에 붙여넣기 → 바로 접속

---

## 파일 구조

```
kbo_dss_dashboard/
  app.py              ← 대시보드 메인 (여기만 수정)
  requirements.txt    ← 의존성
  README.md           ← 이 파일
```

---

## JSON 캐시 자동 로드 (선택)

`app.py` 상단의 경로 변수를 실제 경로로 맞추면
노트북에서 생성된 JSON 결과를 자동 로드함.

```python
MODULE_A_CACHE_PATH = r"D:\...\module_a_cache.json"
MODULE_B_RESULTS_PATH = r"D:\...\module_b_results.json"
```

경로에 파일이 없으면 하드코딩 fallback 자동 사용 → 발표 중 오류 없음.

---

## 탭 구성

| 탭 | 내용 |
|----|------|
| 📊 종합 요약 | 3모듈 처방 효과 비교표 |
| 🏏 Module A | 타순 최적화 (RE 비교 + 실제 타순) |
| ⚾ Module B | 불펜 순위 + Δ실점 역산 |
| 📅 Module C | ILP 스케줄 표 (46경기, 월별 필터) |

---

## 업데이트 이력

- 2026-05-24: 초기 버전 (1학기 최종 발표용, 5/27 팀미팅 시연)
