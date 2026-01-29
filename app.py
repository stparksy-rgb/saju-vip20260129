"""
천명 VIP - 프리미엄 사주 분석 시스템
통합 버전 v1.0

만세력 자동 계산 + AI 심층 통변
Copyright 2026 JEMINA AI
"""

import streamlit as st
from datetime import datetime, date
from manseryuk_engine import (
    calculate_saju, format_saju_display,
    CHEONGAN_OHAENG, OHAENG_KR, OHAENG,
    CHEONGAN_HANJA, JIJI_HANJA, JIJI_ANIMAL
)

# =====================================================
# 페이지 설정
# =====================================================
st.set_page_config(
    page_title="천명 VIP - 프리미엄 사주 분석",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 커스텀 CSS
# =====================================================
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* 메인 타이틀 */
    .main-title {
        text-align: center;
        color: #ffd700;
        font-size: 2.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 10px;
    }
    
    .sub-title {
        text-align: center;
        color: #e0e0e0;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    
    /* 사주 박스 */
    .saju-box {
        background: linear-gradient(145deg, #2d2d44, #1e1e2f);
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
    }
    
    /* 사주 테이블 */
    .saju-table {
        width: 100%;
        text-align: center;
        font-size: 1.2rem;
    }
    
    .saju-table th {
        color: #ffd700;
        padding: 10px;
        border-bottom: 1px solid #ffd700;
    }
    
    .saju-table td {
        color: #fff;
        padding: 15px;
        font-size: 1.8rem;
    }
    
    /* 천간/지지 글자 */
    .cheongan {
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    .jiji {
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    /* 오행별 색상 */
    .wood { color: #4CAF50; }
    .fire { color: #f44336; }
    .earth { color: #ffeb3b; }
    .metal { color: #fff; }
    .water { color: #2196F3; }
    
    /* 오행 바 */
    .ohaeng-bar {
        background: #333;
        border-radius: 10px;
        padding: 5px 10px;
        margin: 5px 0;
    }
    
    /* VIP 뱃지 */
    .vip-badge {
        background: linear-gradient(135deg, #ffd700, #ffaa00);
        color: #000;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    /* 분석 결과 박스 */
    .analysis-box {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #ffd700;
        padding: 20px;
        margin: 15px 0;
        border-radius: 0 10px 10px 0;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #ffd700, #ffaa00);
        color: #000;
        font-weight: bold;
        border: none;
        padding: 15px 30px;
        font-size: 1.1rem;
        border-radius: 30px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# 헤더
# =====================================================
st.markdown('<h1 class="main-title">🔮 천명 VIP</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">대한민국 상위 1% 프리미엄 사주 분석 서비스</p>', unsafe_allow_html=True)

# =====================================================
# 사이드바 - 입력 폼
# =====================================================
with st.sidebar:
    st.markdown("### 📝 생년월일시 입력")
    
    # 달력 유형 선택
    calendar_type = st.radio(
        "달력 유형",
        ["양력", "음력"],
        horizontal=True
    )
    is_lunar = (calendar_type == "음력")
    
    # 윤달 여부 (음력인 경우만)
    is_leap = False
    if is_lunar:
        is_leap = st.checkbox("윤달")
    
    # 생년월일
    col1, col2, col3 = st.columns(3)
    with col1:
        birth_year = st.number_input("년", min_value=1900, max_value=2100, value=1985)
    with col2:
        birth_month = st.number_input("월", min_value=1, max_value=12, value=1)
    with col3:
        birth_day = st.number_input("일", min_value=1, max_value=31, value=1)
    
    # 생시
    col4, col5 = st.columns(2)
    with col4:
        birth_hour = st.number_input("시", min_value=0, max_value=23, value=12)
    with col5:
        birth_minute = st.number_input("분", min_value=0, max_value=59, value=0)
    
    # 성별
    gender = st.radio("성별", ["남", "여"], horizontal=True)
    
    # 시간 모름 옵션
    time_unknown = st.checkbox("태어난 시간을 모릅니다")
    
    st.markdown("---")
    
    # 분석 버튼
    analyze_btn = st.button("🔮 사주 분석 시작", use_container_width=True)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888; font-size: 0.8rem;'>
    ⓒ 2026 JEMINA AI<br>
    천명 VIP 프리미엄 서비스
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# 메인 컨텐츠
# =====================================================
if analyze_btn:
    try:
        # 시간 모름인 경우 12시로 설정 (시주 제외 분석)
        if time_unknown:
            birth_hour = 12
            birth_minute = 0
        
        # 사주 계산
        with st.spinner("만세력을 계산하고 있습니다..."):
            saju = calculate_saju(
                birth_year, birth_month, birth_day,
                birth_hour, birth_minute,
                is_lunar=is_lunar, is_leap=is_leap,
                gender=gender
            )
        
        # 결과 표시
        st.success("✅ 사주팔자 계산 완료!")
        
        # 기본 정보
        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.metric("양력", saju['solar_date'])
        with col_info2:
            st.metric("음력", saju['lunar_date'])
        with col_info3:
            st.metric("띠", f"{saju['animal']}띠 ({saju['year_pillar'][1]})")
        
        st.markdown("---")
        
        # =====================================================
        # 사주팔자 표시
        # =====================================================
        st.markdown("### 📜 사주팔자 (四柱八字)")
        
        # 오행 색상 함수
        def get_ohaeng_color(char):
            ohaeng_colors = {
                '木': '#4CAF50',  # 녹색
                '火': '#f44336',  # 빨강
                '土': '#FFC107',  # 노랑
                '金': '#ffffff',  # 흰색
                '水': '#2196F3',  # 파랑
            }
            if char in ['甲', '乙', '寅', '卯']:
                return ohaeng_colors['木']
            elif char in ['丙', '丁', '巳', '午']:
                return ohaeng_colors['火']
            elif char in ['戊', '己', '辰', '未', '戌', '丑']:
                return ohaeng_colors['土']
            elif char in ['庚', '辛', '申', '酉']:
                return ohaeng_colors['金']
            elif char in ['壬', '癸', '亥', '子']:
                return ohaeng_colors['水']
            return '#fff'
        
        # 사주 테이블 생성
        pillars = [
            ('시주(時柱)', saju['hour_pillar'], saju['hour_pillar_kr']),
            ('일주(日柱)', saju['day_pillar'], saju['day_pillar_kr']),
            ('월주(月柱)', saju['month_pillar'], saju['month_pillar_kr']),
            ('연주(年柱)', saju['year_pillar'], saju['year_pillar_kr']),
        ]
        
        cols = st.columns(4)
        for i, (name, pillar, pillar_kr) in enumerate(pillars):
            with cols[i]:
                gan_color = get_ohaeng_color(pillar[0])
                ji_color = get_ohaeng_color(pillar[1])
                
                # 일주 강조
                border_style = "3px solid #ffd700" if name == '일주(日柱)' else "1px solid #444"
                bg_color = "rgba(255, 215, 0, 0.1)" if name == '일주(日柱)' else "rgba(255, 255, 255, 0.05)"
                
                st.markdown(f"""
                <div style='
                    background: {bg_color};
                    border: {border_style};
                    border-radius: 15px;
                    padding: 20px;
                    text-align: center;
                    margin: 5px;
                '>
                    <div style='color: #ffd700; font-size: 0.9rem; margin-bottom: 10px;'>{name}</div>
                    <div style='color: {gan_color}; font-size: 3rem; font-weight: bold;'>{pillar[0]}</div>
                    <div style='color: {ji_color}; font-size: 3rem; font-weight: bold; margin-top: 10px;'>{pillar[1]}</div>
                    <div style='color: #888; font-size: 1rem; margin-top: 10px;'>{pillar_kr}</div>
                </div>
                """, unsafe_allow_html=True)
        
        if time_unknown:
            st.warning("⚠️ 태어난 시간을 모르므로 시주(時柱)는 참고용입니다.")
        
        st.markdown("---")
        
        # =====================================================
        # 일간 (나) 정보
        # =====================================================
        day_gan = saju['day_gan']
        day_ohaeng = CHEONGAN_OHAENG[day_gan]
        day_color = get_ohaeng_color(day_gan)
        
        st.markdown(f"""
        ### 🌟 일간(日干) - 나를 나타내는 글자
        <div style='
            background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,215,0,0.05));
            border: 2px solid #ffd700;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
        '>
            <span style='color: {day_color}; font-size: 4rem; font-weight: bold;'>{day_gan}</span>
            <div style='color: #fff; font-size: 1.5rem; margin-top: 10px;'>
                {saju['day_gan_kr']} | 오행: {day_ohaeng}({OHAENG_KR[OHAENG.index(day_ohaeng)]})
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # =====================================================
        # 오행 분석
        # =====================================================
        st.markdown("### 🔥 오행(五行) 분포")
        
        ohaeng_colors = {
            '木': '#4CAF50', '火': '#f44336', '土': '#FFC107', 
            '金': '#E0E0E0', '水': '#2196F3'
        }
        
        total = sum(saju['ohaeng_count'].values())
        
        cols = st.columns(5)
        for i, (oh, count) in enumerate(saju['ohaeng_count'].items()):
            with cols[i]:
                percentage = (count / total * 100) if total > 0 else 0
                color = ohaeng_colors[oh]
                
                st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px;'>
                    <div style='color: {color}; font-size: 2rem; font-weight: bold;'>{oh}</div>
                    <div style='color: #888; font-size: 0.9rem;'>{OHAENG_KR[i]}</div>
                    <div style='color: #fff; font-size: 1.5rem; margin-top: 10px;'>{count}</div>
                    <div style='background: #333; border-radius: 10px; height: 10px; margin-top: 10px;'>
                        <div style='background: {color}; width: {percentage}%; height: 100%; border-radius: 10px;'></div>
                    </div>
                    <div style='color: #888; font-size: 0.8rem; margin-top: 5px;'>{percentage:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # =====================================================
        # 십신 분석
        # =====================================================
        st.markdown("### 📊 십신(十神) 분석")
        
        sipsin_explain = {
            '비견': '나와 같은 기운, 형제/친구/경쟁자',
            '겁재': '나를 도우면서 빼앗는 기운, 동료/경쟁',
            '식신': '내가 낳는 기운, 재능/표현/자녀',
            '상관': '내가 강하게 표출하는 기운, 예술/반항',
            '편재': '내가 지배하는 불안정한 재물, 투자/부업',
            '정재': '내가 지배하는 안정된 재물, 월급/저축',
            '편관': '나를 지배하는 불안정한 기운, 권위/스트레스',
            '정관': '나를 지배하는 안정된 기운, 직장/규율',
            '편인': '나를 낳는 불안정한 기운, 공부/종교',
            '정인': '나를 낳는 안정된 기운, 어머니/학문',
        }
        
        for s in saju['sipsin']:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"**{s['pillar']}**")
            with col2:
                st.markdown(f"""
                천간 {s['gan']}: **{s['gan_sipsin']}** ({sipsin_explain.get(s['gan_sipsin'], '')})  
                지지 {s['ji']}: **{s['ji_sipsin']}** ({sipsin_explain.get(s['ji_sipsin'], '')})
                """)
        
        st.markdown("---")
        
        # =====================================================
        # 대운
        # =====================================================
        st.markdown("### 🌊 대운(大運) 흐름")
        
        daeun_cols = st.columns(len(saju['daeun']))
        for i, d in enumerate(saju['daeun']):
            with daeun_cols[i]:
                st.markdown(f"""
                <div style='text-align: center; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 10px; margin: 2px;'>
                    <div style='color: #888; font-size: 0.8rem;'>{d['age']}세~</div>
                    <div style='color: #fff; font-size: 1.2rem; font-weight: bold;'>{d['pillar']}</div>
                    <div style='color: #ffd700; font-size: 0.8rem;'>{d['pillar_kr']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # =====================================================
        # AI 통변을 위한 프롬프트 데이터 생성
        # =====================================================
        st.markdown("### 🤖 AI 심층 통변 요청용 데이터")
        
        prompt_data = f"""
【사주 원국 정보】
- 양력: {saju['solar_date']} {saju['birth_time']}
- 음력: {saju['lunar_date']}
- 성별: {saju['gender']}
- 띠: {saju['animal']}띠

【사주팔자】
        시주    일주    월주    연주
천간:    {saju['hour_pillar'][0]}      {saju['day_pillar'][0]}      {saju['month_pillar'][0]}      {saju['year_pillar'][0]}
지지:    {saju['hour_pillar'][1]}      {saju['day_pillar'][1]}      {saju['month_pillar'][1]}      {saju['year_pillar'][1]}
한글:    {saju['hour_pillar_kr']}    {saju['day_pillar_kr']}    {saju['month_pillar_kr']}    {saju['year_pillar_kr']}

【일간(나)】
- {saju['day_gan_kr']} / 오행: {CHEONGAN_OHAENG[saju['day_gan']]}

【오행 분포】
- 木(목): {saju['ohaeng_count']['木']}
- 火(화): {saju['ohaeng_count']['火']}
- 土(토): {saju['ohaeng_count']['土']}
- 金(금): {saju['ohaeng_count']['金']}
- 水(수): {saju['ohaeng_count']['水']}

【십신 구성】
- 연주: 천간 {saju['sipsin'][0]['gan']}({saju['sipsin'][0]['gan_sipsin']}), 지지 {saju['sipsin'][0]['ji']}({saju['sipsin'][0]['ji_sipsin']})
- 월주: 천간 {saju['sipsin'][1]['gan']}({saju['sipsin'][1]['gan_sipsin']}), 지지 {saju['sipsin'][1]['ji']}({saju['sipsin'][1]['ji_sipsin']})
- 일주: 천간 {saju['sipsin'][2]['gan']}({saju['sipsin'][2]['gan_sipsin']}), 지지 {saju['sipsin'][2]['ji']}({saju['sipsin'][2]['ji_sipsin']})
- 시주: 천간 {saju['sipsin'][3]['gan']}({saju['sipsin'][3]['gan_sipsin']}), 지지 {saju['sipsin'][3]['ji']}({saju['sipsin'][3]['ji_sipsin']})

【대운】
{' → '.join([f"{d['pillar_kr']}({d['age']}세~)" for d in saju['daeun']])}
"""
        
        st.code(prompt_data, language=None)
        
        st.info("""
        💡 **사용법**: 위 데이터를 복사하여 AI에게 "이 사주를 심층 분석해주세요"라고 요청하시면 
        상세한 통변을 받으실 수 있습니다.
        
        🔜 **다음 업데이트**: Claude API 연동으로 자동 심층 통변 기능이 추가될 예정입니다!
        """)
        
        # 세션에 사주 저장
        st.session_state['current_saju'] = saju
        st.session_state['prompt_data'] = prompt_data
        
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
        st.info("입력 정보를 확인해주세요. 음력 날짜가 올바른지 확인해주세요.")

# =====================================================
# 초기 화면 (분석 전)
# =====================================================
else:
    st.markdown("""
    <div style='
        text-align: center;
        padding: 50px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        margin: 20px 0;
    '>
        <div style='font-size: 4rem;'>🔮</div>
        <h2 style='color: #ffd700; margin: 20px 0;'>프리미엄 사주 분석을 시작하세요</h2>
        <p style='color: #888;'>
            왼쪽 사이드바에서 생년월일시를 입력하고<br>
            '사주 분석 시작' 버튼을 클릭하세요.
        </p>
        <div style='margin-top: 30px; color: #666;'>
            <p>✓ 절기 기준 정확한 만세력 계산</p>
            <p>✓ 오행/십신/대운 자동 분석</p>
            <p>✓ AI 심층 통변 지원</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 서비스 특징
    st.markdown("### 🌟 천명 VIP 서비스 특징")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; height: 200px;'>
            <h4 style='color: #ffd700;'>📐 정밀 만세력</h4>
            <p style='color: #ccc;'>
            절기 기준으로 정확하게 계산된 사주팔자를 제공합니다. 
            더 이상 외부 사이트에서 명조를 확인할 필요가 없습니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; height: 200px;'>
            <h4 style='color: #ffd700;'>🤖 AI 심층 통변</h4>
            <p style='color: #ccc;'>
            단순한 해석이 아닌, A4 1~2장 분량의 프리미엄 분석을 제공합니다.
            격국, 용신, 대운까지 전문가 수준의 통변을 경험하세요.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; height: 200px;'>
            <h4 style='color: #ffd700;'>💎 VIP 전용</h4>
            <p style='color: #ccc;'>
            대한민국 상위 1%만을 위한 프리미엄 서비스입니다.
            당신의 인생에 깊은 통찰과 구체적 해결책을 제시합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
