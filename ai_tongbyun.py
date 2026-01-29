"""
AI 통변 모듈 - Claude API 연동
천명 VIP 프리미엄 사주 해석 시스템

Copyright 2026 JEMINA AI
"""

import os
from datetime import datetime

# =====================================================
# VIP 프리미엄 통변 시스템 프롬프트
# =====================================================

SYSTEM_PROMPT = """당신은 대한민국 상위 1%의 고객만을 상대하는 심층 사주 명리학 전문가 '천명 VIP'입니다. 
당신의 고객은 단순한 통변이 아니라, 인생의 깊은 통찰과 구체적인 해결책을 원합니다.

따라서 당신은 모든 답변을 **'VIP 프리미엄 모드'**로 작성해야 합니다. 
이는 기존 답변보다 **최소 2배 이상의 분량과 깊이**를 제공해야 함을 의미합니다.

### [핵심 행동 지침]

1. **단답형 금지 및 상세한 풀이:**
   - "재물운이 좋습니다" 같은 짧은 문장은 절대 금지합니다.
   - "사주 원국의 오행 구성상 '수(水)' 기운이 재물을 뜻하는데, 올해 세운에서 이 기운이 들어와 흐름이 트이므로~"와 같이 논리적 근거(원국, 대운, 세운의 상호작용)를 5~6문장 이상 상세히 서술하십시오.

2. **구조화된 리포트 형식:**
   - 답변은 마치 '유료 심층 상담 보고서'를 받아보는 것처럼 체계적으로 목차를 나누어 작성하십시오.
   
   **[표준 보고서 구조]**
   1. 타고난 기질과 성격 분석
   2. 일간(日干) 심층 해석
   3. 격국(格局) 및 용신(用神) 분석
   4. 현재 대운의 흐름과 영향
   5. 올해/내년 세운 분석
   6. 분야별 운세 (직업/재물/건강/인간관계/연애운)
   7. 월별 상세 운세 (필요시)
   8. VIP 개운법 및 맞춤 조언

3. **전문 용어와 쉬운 풀이 병행:**
   - 전문적인 사주 용어(예: 격국, 용신, 충/합/형/파)를 사용하여 신뢰감을 주되, 
   - 반드시 그 뜻을 고객이 이해하기 쉽게 풀어서 설명하십시오.
   
   예시: "월주에 정관(正官)이 있어 조직 내에서 인정받는 기질이 있습니다. 
   정관이란 나를 바르게 이끄는 기운으로, 직장이나 사회에서 안정적 지위를 얻기 좋은 구조입니다."

4. **풍부한 표현력:**
   - 문체는 정중하고 진지하며, 고객의 마음을 어루만지는 상담가의 태도를 유지하십시오.
   - 분량을 늘리기 위해 무의미한 말을 반복하지 말고, 다양한 관점에서 해석을 덧붙여 내용을 풍성하게 만드십시오.

5. **출력물 길이:**
   - 사용자가 별도의 길이 요청을 하지 않아도, **A4 용지 2~3장 분량**에 해당하는 긴 호흡의 답변을 생성하십시오.

### [분석 시 필수 고려사항]

1. **오행의 균형과 불균형:**
   - 과다한 오행, 부족한 오행을 파악하고 그것이 성격과 운에 미치는 영향 설명
   
2. **십신의 배치:**
   - 각 주(柱)에 배치된 십신의 의미와 상호작용 분석
   - 특히 월주(사회운), 시주(말년운, 자녀운)의 십신 중점 해석

3. **충(沖), 합(合), 형(刑), 파(破):**
   - 원국 내 지지 간의 충/합/형/파 관계 분석
   - 대운, 세운과의 충합 관계 분석

4. **공망(空亡), 신살(神煞):**
   - 주요 신살(역마, 도화, 천을귀인 등) 언급

5. **시점 기반 분석:**
   - 현재 날짜를 기준으로 대운, 세운 분석
   - 상반기면 올해 중심, 하반기면 내년 중심으로 비중 조절

### [말투 및 톤]
- 존칭 사용 (합쇼체)
- 따뜻하고 격려하는 어조
- 부정적 해석도 희망적 대안과 함께 제시
- "~하십시오", "~됩니다", "~하시기 바랍니다" 등 정중한 표현 사용

이제 사용자가 사주 정보를 제공하면, 위 지침에 따라 즉시 **VIP 프리미엄 해석**을 시작하십시오.
"""


def create_analysis_prompt(saju_data, analysis_type="종합운세", specific_question=None):
    """
    사주 데이터를 기반으로 분석 프롬프트 생성
    
    Parameters:
    - saju_data: dict, 만세력 엔진에서 계산된 사주 데이터
    - analysis_type: str, 분석 유형 (종합운세, 올해운세, 내년운세, 직업운, 재물운, 연애운, 건강운)
    - specific_question: str, 특정 질문 (선택)
    
    Returns:
    - str: Claude API에 전달할 프롬프트
    """
    
    today = datetime.now()
    current_year = today.year
    
    # 기본 사주 정보 구성
    saju_info = f"""
【의뢰인 기본 정보】
- 양력 생년월일: {saju_data['solar_date']}
- 음력 생년월일: {saju_data['lunar_date']}
- 태어난 시간: {saju_data['birth_time']}
- 성별: {saju_data['gender']}
- 띠: {saju_data['animal']}띠

【사주팔자 원국】
┌──────┬──────┬──────┬──────┐
│ 시주 │ 일주 │ 월주 │ 연주 │
├──────┼──────┼──────┼──────┤
│  {saju_data['hour_pillar'][0]}   │  {saju_data['day_pillar'][0]}   │  {saju_data['month_pillar'][0]}   │  {saju_data['year_pillar'][0]}   │  ← 천간
│  {saju_data['hour_pillar'][1]}   │  {saju_data['day_pillar'][1]}   │  {saju_data['month_pillar'][1]}   │  {saju_data['year_pillar'][1]}   │  ← 지지
├──────┼──────┼──────┼──────┤
│{saju_data['hour_pillar_kr']}  │{saju_data['day_pillar_kr']}  │{saju_data['month_pillar_kr']}  │{saju_data['year_pillar_kr']}  │
└──────┴──────┴──────┴──────┘

【일간(나)】
{saju_data['day_gan_kr']}

【오행 분포】
• 木(목): {saju_data['ohaeng_count']['木']}
• 火(화): {saju_data['ohaeng_count']['火']}
• 土(토): {saju_data['ohaeng_count']['土']}
• 金(금): {saju_data['ohaeng_count']['金']}
• 水(수): {saju_data['ohaeng_count']['水']}

【십신 구성】
• 연주: 천간 {saju_data['sipsin'][0]['gan']}({saju_data['sipsin'][0]['gan_sipsin']}), 지지 {saju_data['sipsin'][0]['ji']}({saju_data['sipsin'][0]['ji_sipsin']})
• 월주: 천간 {saju_data['sipsin'][1]['gan']}({saju_data['sipsin'][1]['gan_sipsin']}), 지지 {saju_data['sipsin'][1]['ji']}({saju_data['sipsin'][1]['ji_sipsin']})
• 일주: 천간 {saju_data['sipsin'][2]['gan']}({saju_data['sipsin'][2]['gan_sipsin']}), 지지 {saju_data['sipsin'][2]['ji']}({saju_data['sipsin'][2]['ji_sipsin']})
• 시주: 천간 {saju_data['sipsin'][3]['gan']}({saju_data['sipsin'][3]['gan_sipsin']}), 지지 {saju_data['sipsin'][3]['ji']}({saju_data['sipsin'][3]['ji_sipsin']})

【대운 흐름】
{' → '.join([f"{d['pillar_kr']}({d['age']}세~)" for d in saju_data['daeun']])}

【현재 시점】
- 오늘 날짜: {today.strftime('%Y년 %m월 %d일')}
- 현재 연도 세운: {current_year}년
"""
    
    # 분석 유형별 추가 지시사항
    analysis_instructions = {
        "종합운세": f"""
위 사주 원국을 바탕으로 다음 순서로 VIP 프리미엄 종합 분석을 진행해주세요:

1. **타고난 기질과 성격** - 일간을 중심으로 본성과 특징 분석
2. **격국과 용신** - 사주의 구조적 특성과 필요한 오행
3. **현재 대운 분석** - 지금 어떤 대운을 지나고 있는지, 그 영향
4. **{current_year}년 세운 분석** - 올해의 전체적 흐름과 주의점
5. **분야별 운세** - 직업/재물/건강/인간관계/연애 각각 상세히
6. **VIP 개운법** - 이 사주에 맞는 맞춤형 개운 전략
""",
        
        "올해운세": f"""
위 사주 원국을 바탕으로 {current_year}년 세운 분석을 집중적으로 진행해주세요:

1. {current_year}년 천간/지지가 원국에 미치는 영향
2. 대운과 세운의 상호작용
3. 분기별/월별 상세 흐름
4. 올해 특히 조심해야 할 시기와 이유
5. 올해 기회가 되는 시기와 활용법
6. 분야별(직업/재물/건강/인간관계) 올해 운세
7. 올해를 잘 보내기 위한 VIP 맞춤 조언
""",
        
        "내년운세": f"""
위 사주 원국을 바탕으로 {current_year + 1}년 세운 분석을 진행해주세요:

1. {current_year + 1}년 천간/지지가 원국에 미치는 영향
2. 대운과 세운의 상호작용
3. 내년 전체 키워드와 주제
4. 분기별 흐름 예측
5. 내년 조심해야 할 점과 기회 요인
6. 분야별(직업/재물/건강/인간관계) 내년 운세
7. 내년을 준비하기 위한 VIP 맞춤 조언
""",
        
        "직업운": """
위 사주 원국을 바탕으로 직업운/사업운을 집중 분석해주세요:

1. 타고난 직업적 성향과 적성
2. 이 사주에 어울리는 업종/직종
3. 사업 vs 직장인 적합도
4. 현재 대운에서의 직업운
5. 올해/내년 직업운 상세 분석
6. 승진/이직/창업 시기 조언
7. 직업 성공을 위한 VIP 맞춤 전략
""",
        
        "재물운": """
위 사주 원국을 바탕으로 재물운을 집중 분석해주세요:

1. 타고난 재물 복과 재물 스타일
2. 돈을 버는 방식과 적합한 재테크
3. 현재 대운에서의 재물운
4. 올해/내년 재물운 상세 분석
5. 재물이 들어오는 시기와 나가는 시기
6. 투자/저축/소비 패턴 조언
7. 부를 축적하기 위한 VIP 맞춤 전략
""",
        
        "연애운": """
위 사주 원국을 바탕으로 연애운/결혼운을 집중 분석해주세요:

1. 타고난 연애 스타일과 이상형
2. 배우자 자리(일지)의 특성 분석
3. 궁합이 잘 맞는 사주 유형
4. 현재 대운에서의 연애/결혼운
5. 올해/내년 연애운 상세 분석
6. 좋은 인연을 만나는 시기
7. 행복한 관계를 위한 VIP 맞춤 조언
""",
        
        "건강운": """
위 사주 원국을 바탕으로 건강운을 집중 분석해주세요:

1. 오행 불균형으로 본 취약 장기/부위
2. 체질적 특성과 건강 관리 포인트
3. 현재 대운에서의 건강운
4. 올해/내년 건강 주의사항
5. 계절별/시기별 건강 관리 조언
6. 이 사주에 좋은 음식/운동/생활습관
7. 건강 장수를 위한 VIP 맞춤 양생법
"""
    }
    
    # 프롬프트 조합
    prompt = saju_info + "\n\n"
    prompt += "=" * 50 + "\n"
    prompt += f"【분석 요청: {analysis_type}】\n"
    prompt += "=" * 50 + "\n\n"
    
    if analysis_type in analysis_instructions:
        prompt += analysis_instructions[analysis_type]
    
    if specific_question:
        prompt += f"\n\n【추가 질문】\n{specific_question}"
    
    prompt += "\n\n위 내용을 바탕으로 VIP 프리미엄 수준의 심층 분석을 진행해주세요."
    
    return prompt


def get_follow_up_prompts():
    """후속 질문 예시 목록"""
    return [
        "올해 상반기와 하반기 중 언제가 더 좋을까요?",
        "제 사주에서 가장 강한 장점은 무엇인가요?",
        "이직/전직을 고려 중인데 적합한 시기가 언제일까요?",
        "투자를 하려는데 올해 재물운이 어떤가요?",
        "결혼 적령기가 언제쯤일까요?",
        "사업을 시작하려는데 제 사주가 사업에 맞나요?",
        "건강상 특별히 주의해야 할 부분이 있나요?",
        "올해 가장 조심해야 할 달은 언제인가요?",
        "제 사주의 용신(用神)과 기신(忌神)은 무엇인가요?",
        "부모님/자녀와의 관계운은 어떤가요?",
    ]


# =====================================================
# Claude API 호출 함수 (실제 연동 시 사용)
# =====================================================

def call_claude_api(prompt, api_key=None):
    """
    Claude API 호출
    
    Parameters:
    - prompt: str, 분석 프롬프트
    - api_key: str, Anthropic API 키
    
    Returns:
    - str: AI 분석 결과
    """
    try:
        import anthropic
        
        if api_key is None:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
        
        if not api_key:
            return "API 키가 설정되지 않았습니다. 환경변수 ANTHROPIC_API_KEY를 설정하거나 API 키를 직접 입력해주세요."
        
        client = anthropic.Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
        
    except ImportError:
        return "anthropic 라이브러리가 설치되지 않았습니다. 'pip install anthropic'을 실행해주세요."
    except Exception as e:
        return f"API 호출 중 오류가 발생했습니다: {str(e)}"


# =====================================================
# 테스트
# =====================================================

if __name__ == "__main__":
    # 테스트용 사주 데이터
    test_saju = {
        'solar_date': '1985년 03월 15일',
        'lunar_date': '1985년 1월 24일',
        'birth_time': '07시 30분',
        'gender': '남',
        'animal': '소',
        'year_pillar': '乙丑',
        'month_pillar': '己卯',
        'day_pillar': '癸未',
        'hour_pillar': '丙辰',
        'year_pillar_kr': '을축',
        'month_pillar_kr': '기묘',
        'day_pillar_kr': '계미',
        'hour_pillar_kr': '병진',
        'day_gan': '癸',
        'day_gan_kr': '계(癸)',
        'ohaeng_count': {'木': 2.9, '火': 1.3, '土': 4.9, '金': 0.3, '水': 1.6},
        'sipsin': [
            {'pillar': '연주', 'gan': '乙', 'ji': '丑', 'gan_sipsin': '식신', 'ji_sipsin': '편관'},
            {'pillar': '월주', 'gan': '己', 'ji': '卯', 'gan_sipsin': '편관', 'ji_sipsin': '식신'},
            {'pillar': '일주', 'gan': '癸', 'ji': '未', 'gan_sipsin': '비견', 'ji_sipsin': '편관'},
            {'pillar': '시주', 'gan': '丙', 'ji': '辰', 'gan_sipsin': '정재', 'ji_sipsin': '정관'},
        ],
        'daeun': [
            {'age': 10, 'pillar': '戊寅', 'pillar_kr': '무인'},
            {'age': 20, 'pillar': '丁丑', 'pillar_kr': '정축'},
            {'age': 30, 'pillar': '丙子', 'pillar_kr': '병자'},
            {'age': 40, 'pillar': '乙亥', 'pillar_kr': '을해'},
            {'age': 50, 'pillar': '甲戌', 'pillar_kr': '갑술'},
        ]
    }
    
    # 프롬프트 생성 테스트
    prompt = create_analysis_prompt(test_saju, "종합운세")
    print("=" * 60)
    print("생성된 프롬프트:")
    print("=" * 60)
    print(prompt)
