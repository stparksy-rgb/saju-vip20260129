# 🔮 천명 VIP - 프리미엄 사주 분석 시스템

대한민국 상위 1% 고객을 위한 AI 기반 심층 사주 분석 서비스

## ✨ 주요 기능

### 1. 정밀 만세력 계산
- **절기 기준** 정확한 연주/월주 계산
- 음력 ↔ 양력 자동 변환
- 윤달 지원
- 1900년 ~ 2100년 지원

### 2. 자동 분석
- 오행(五行) 분포 분석
- 십신(十神) 배치 분석
- 대운(大運) 자동 계산
- 지장간(地藏干) 분석

### 3. AI 심층 통변 (Claude API 연동)
- VIP 프리미엄 수준의 A4 2~3장 분량 해석
- 종합운세 / 올해운세 / 내년운세
- 직업운 / 재물운 / 연애운 / 건강운
- 맞춤형 개운법 제공

---

## 🚀 설치 방법

### 1. 저장소 클론 또는 파일 다운로드
```bash
git clone [your-repo-url]
cd saju_project
```

### 2. 필요 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. (선택) Claude API 키 설정
AI 통변 기능을 사용하려면 Anthropic API 키가 필요합니다.
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 4. 앱 실행
```bash
streamlit run app.py
```

---

## 📁 파일 구조

```
saju_project/
├── app.py                 # Streamlit 메인 앱
├── manseryuk_engine.py    # 만세력 계산 엔진
├── ai_tongbyun.py         # AI 통변 모듈 (Claude API)
├── requirements.txt       # 의존성 패키지
└── README.md              # 이 문서
```

---

## 💻 사용 방법

### 기본 사용
1. 앱 실행 후 왼쪽 사이드바에서 생년월일시 입력
2. 양력/음력 선택 (음력인 경우 윤달 여부 체크)
3. 성별 선택
4. "사주 분석 시작" 버튼 클릭

### AI 통변 사용
1. 사주 분석 후 하단에 생성된 "AI 심층 통변 요청용 데이터" 복사
2. Claude에게 전달하여 심층 분석 요청
3. 또는 API 연동 버전에서 자동 분석

---

## 🔧 Streamlit Cloud 배포

### 1. GitHub에 코드 업로드

### 2. Streamlit Cloud 접속
https://share.streamlit.io

### 3. 새 앱 생성
- Repository 선택
- Branch: main
- Main file path: app.py

### 4. Secrets 설정 (API 키)
```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```

---

## 🎯 유료화 버전 업그레이드 계획

### Phase 1: 기본 기능 (현재)
- [x] 만세력 자동 계산
- [x] 오행/십신/대운 분석
- [x] 기본 UI

### Phase 2: AI 통변 연동
- [ ] Claude API 실시간 연동
- [ ] 분석 유형별 선택 (종합/직업/재물/연애/건강)
- [ ] 후속 질문 기능

### Phase 3: 유료 결제 시스템
- [ ] 회원가입/로그인
- [ ] 결제 시스템 연동 (토스페이먼츠/카카오페이)
- [ ] 분석 횟수 제한 및 구독 플랜

### Phase 4: 고급 기능
- [ ] 궁합 분석
- [ ] 택일 (결혼/이사/개업 등)
- [ ] PDF 리포트 다운로드
- [ ] 분석 이력 저장

---

## 📞 문의

JEMINA AI TV
- YouTube: @jemina-ai-tv
- Website: myfunwithai.com

---

## ⚠️ 주의사항

이 서비스는 참고용 엔터테인먼트 목적으로 제공됩니다.
중요한 인생 결정은 전문가와 상담하시기 바랍니다.

---

© 2026 JEMINA AI. All rights reserved.
