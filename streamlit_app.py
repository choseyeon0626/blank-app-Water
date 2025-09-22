import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import folium
from streamlit_folium import st_folium
import matplotlib.cm as cm
import matplotlib.colors as colors

# 페이지 설정
st.set_page_config(
    page_title="멈추지 않는 에어컨과 해수면 상승",
    layout="wide"
)

# ----------------------------
# 제목 & 서론
# ----------------------------
st.title("❄️ 멈추지 않는 에어컨과 해수면 상승")
st.subheader("과한 에어컨 사용에 의한 해수온, 해수면 높이 상승이 우리 삶에 미치는 영향")

st.markdown("""
여름마다 우리는 습관처럼 에어컨을 켠다. 그러나 이 편리한 습관이 바다와 연결되어 있다는 사실은 잘 인식되지 않는다.  
무분별한 전기 사용은 온실가스 배출을 가속화하고, 이는 결국 지구 평균 기온 상승과 해수면 상승으로 이어진다.  

이미 해수온 상승은 빠르게 진행 중이며, 해수면은 매년 꾸준히 높아지고 있다.  
이 변화는 우리가 여름에 떠나는 피서지와 미래의 생활 공간을 위협하는 실질적 문제다.  

따라서 우리는 **에어컨 사용과 해수면 상승의 연관성을 데이터로 확인**하고,  
**청소년으로서 어떤 실천을 할 수 있을지 탐구**할 필요가 있다.
""")

# ----------------------------
# 데이터 준비
# ----------------------------
years = list(range(1993, 2024))
levels = [
    0.0, 2.4, 4.5, 6.3, 8.2, 10.4, 12.5, 14.1, 16.3, 18.2,
    20.4, 22.1, 24.5, 26.8, 29.3, 31.1, 33.6, 36.1, 38.4, 41.0,
    43.2, 46.0, 48.5, 51.0, 54.2, 56.9, 59.5, 62.0, 65.1, 67.4,
    68.9
]
sea_df = pd.DataFrame({"연도": years, "해수면 상승(mm)": levels})

cities = [
    {"city": "서울", "lat": 37.5665, "lon": 126.9780},
    {"city": "부산", "lat": 35.1796, "lon": 129.0756},
    {"city": "도쿄", "lat": 35.6762, "lon": 139.6503},
    {"city": "상하이", "lat": 31.2304, "lon": 121.4737},
    {"city": "자카르타", "lat": -6.2088, "lon": 106.8456},
    {"city": "런던", "lat": 51.5074, "lon": -0.1278},
    {"city": "암스테르담", "lat": 52.3676, "lon": 4.9041},
    {"city": "뉴욕", "lat": 40.7128, "lon": -74.0060},
    {"city": "마이애미", "lat": 25.7617, "lon": -80.1918},
    {"city": "리우데자네이루", "lat": -22.9068, "lon": -43.1729},
    {"city": "케이프타운", "lat": -33.9249, "lon": 18.4241},
    {"city": "시드니", "lat": -33.8688, "lon": 151.2093}
]

tourism_risks = {
    "한국": "인천·김포 저지대 침수로 김포공항 접근 불가, 부산 해운대와 광안리 관광지 침수 위험, 제주 해안 관광지 축소 우려.",
    "일본": "도쿄 디즈니랜드와 오다이바 침수 위험, 요코하마 항구 일부 기능 상실, 오사카 만 지역 주요 상업시설 침수.",
    "중국": "상하이 와이탄 관광지 침수, 푸둥 금융 지구 접근 차단, 항저우 만 일대 농경지 손실.",
    "미국": "뉴욕 자유의 여신상 주변 침수, 마이애미 비치 절반 이상 사라짐, 뉴올리언스 도심 기능 상실.",
    "네덜란드": "암스테르담 운하 지대 침수, 로테르담 항구 기능 저하, 튤립 농업지대 피해 확대.",
    "인도네시아": "자카르타 도심 1/3 이상 침수, 주요 도로 교통 마비, 항만 기능 마비.",
    "영국": "런던 템스강 수위 상승으로 시티 금융가 침수 위협, 웨스트민스터 궁전 침수 우려, 관광산업 큰 타격.",
    "호주": "시드니 오페라하우스 주변 침수, 본다이 비치 해안선 후퇴, 항구 도시 기반시설 손상.",
    "브라질": "리우 코파카바나 해변 침수, 슈거로프 마운틴 관광지 접근 제한, 리우 항만 물류 기능 위축.",
    "남아프리카공화국": "케이프타운 워터프런트 침수, 어업과 관광산업 피해, 해안 주거지 상실 위험."
}

# 색상 매핑
norm = colors.Normalize(vmin=0, vmax=max(levels))
cmap = cm.get_cmap('RdYlBu_r')
def get_color(value):
    rgba = cmap(norm(value))
    return colors.to_hex(rgba)

legend_html = """
<div style="position: fixed; bottom: 40px; left: 40px; width: 220px; height: 140px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; padding: 10px;">
<b>🌊 해수면 상승 위험도</b><br>
<span style='color:#08306b;'>●</span> 낮음 (0~20mm)<br>
<span style='color:#2b8cbe;'>●</span> 보통 (20~40mm)<br>
<span style='color:#fdae61;'>●</span> 높음 (40~60mm)<br>
<span style='color:#d73027;'>●</span> 매우 높음 (60mm 이상)
</div>
"""

# ----------------------------
# 본론 - 탭 구성
# ----------------------------
st.header("📊 분석 시각화")
tab1, tab2, tab3 = st.tabs([
    "📈 해수면 상승 추이",
    "🗺️ 연도별 도시 위험도 지도",
    "💨 에어컨 시뮬레이션"
])

# Tab1
with tab1:
    st.subheader("전 세계 해수면 상승 추이 (1993~2023)")
    col1, col2 = st.columns([1, 5])
    with col1:
        start_year = st.selectbox("시작 연도", options=years, index=years.index(2010))
        end_year = st.selectbox("종료 연도", options=years, index=len(years)-1)
    if start_year > end_year:
        st.warning("❗ 시작 연도가 종료 연도보다 클 수 없습니다.")
    else:
        filtered_df = sea_df[(sea_df["연도"] >= start_year) & (sea_df["연도"] <= end_year)]
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=filtered_df["연도"], y=filtered_df["해수면 상승(mm)"],
                mode='lines+markers', line=dict(color='royalblue'), marker=dict(size=8)
            ))
            fig.update_layout(
                title=f"{start_year}년 ~ {end_year}년 해수면 상승 추이",
                xaxis_title="연도", yaxis_title="해수면 상승 (mm)", height=500
            )
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("> ✅ **출처**: NASA Global Mean Sea Level (1993–2023)")

# Tab2
with tab2:
    st.subheader("연도별 세계 도시 해수면 위험도")
    map_year = st.sidebar.slider("🌍 지도에 표시할 연도 선택", min_value=1993, max_value=2023, value=2015)
    selected_country = st.sidebar.selectbox("나라 선택", list(tourism_risks.keys()))
    selected_level = sea_df.loc[sea_df["연도"] == map_year, "해수면 상승(mm)"].values[0]
    m = folium.Map(location=[20, 0], zoom_start=2)
    for city in cities:
        color = get_color(selected_level)
        folium.CircleMarker(
            location=[city["lat"], city["lon"]], radius=10,
            color=color, fill=True, fill_color=color, fill_opacity=0.8,
            popup=f"{city['city']}<br>해수면 상승: {selected_level:.1f} mm"
        ).add_to(m)
    m.get_root().html.add_child(folium.Element(legend_html))
    st_folium(m, width=900, height=550)
    st.info(f"{selected_country}: {tourism_risks[selected_country]}")

# Tab3
with tab3:
    st.subheader("에어컨의 역설: 간단한 소비/배출 시뮬레이터")
    st.sidebar.subheader("에어컨 사용량 입력")
    hours_per_day = st.sidebar.slider("하루 사용 시간 (시간)", 1, 24, 5)
    days_used = st.sidebar.slider("사용 일수 (일)", 1, 365, 150)
    power_per_hour = 1.5
    co2_per_kwh = 0.4
    total_energy = hours_per_day * days_used * power_per_hour
    total_co2 = total_energy * co2_per_kwh
    st.metric("총 전력 소비량 (kWh)", f"{total_energy:,.0f}")
    st.metric("총 CO₂ 배출량 (kg)", f"{total_co2:,.0f}")
    if total_co2 < 50:
        risk_level, color = "안전", "green"
    elif total_co2 < 150:
        risk_level, color = "주의", "yellow"
    elif total_co2 < 300:
        risk_level, color = "위험", "orange"
    else:
        risk_level, color = "심각", "red"
    st.markdown(f"<h3 style='color:{color}'>위험도: {risk_level}</h3>", unsafe_allow_html=True)

# ----------------------------
# 보고서 + 체크리스트 (탭 끝난 뒤 한 번만)
# ----------------------------
st.markdown("""
## 본론 1  
전력 소비는 단순한 숫자가 아니라 바다와 직결된다. 에어컨을 오래 켤수록 발전소는 더 많은 화석연료를 태우고, 이 과정에서 나온 이산화탄소는 지구의 온도를 끌어올린다.  
온도가 오르면 해수는 팽창하고, 극지방 빙하는 녹아 바다 수위는 점점 높아진다.  
즉, 우리가 방 안에서 버튼 하나로 시원함을 택할 때마다, 바닷가는 한 걸음씩 우리 땅을 향해 다가오고 있는 것이다.  

## 본론 2  
실제 데이터는 이를 뒷받침한다. 1993년부터 꾸준히 상승해 온 해수면은 이미 수십 mm나 올랐다.  
도시별 지도를 보면 세계의 주요 관광지가 잠길 위기에 있음을 알 수 있다.  
뉴욕의 자유의 여신상, 도쿄 디즈니랜드, 부산 해운대 해수욕장 등, 우리가 꿈꾸던 여행지가 바닷물에 잠길 수 있다.  
또한 에어컨 시뮬레이터에서 확인했듯, 일상 속 작은 사용도 누적되면 큰 배출로 이어진다.  

## 결론 및 제언  
바다의 온도가 오르면 교실도 끓는다. 해수면이 오르면 우리의 미래 공간은 줄어든다.  
하지만 우리는 이 변화를 막을 마지막 세대일 수도 있다.  
따라서 지금 당장의 작은 실천이 무엇보다 중요하다. 에너지 절약과 탄소 배출 감축은 먼 미래의 이야기가 아니라, 오늘 우리 손에 달려 있다.  

우리가 실천할 수 있는 방안으로는 여름철 에어컨 온도를 26도로 유지하고, 선풍기와 병행하여 사용하며, 대중교통을 더 자주 이용하는 것이다.  
또한 불필요한 전자기기 플러그를 뽑고, 재사용 가능한 물품을 생활 속에서 습관적으로 사용하는 것도 중요하다.  
학교나 가정에서는 함께 참여할 수 있는 절약 캠페인을 만들어 작은 성과를 쌓아 나가야 한다.  
결국, 청소년 한 명의 실천이 모이면 큰 변화를 만들 수 있으며, 그것이 바로 우리의 미래를 지켜낼 가장 확실한 방법이다.
""")

st.markdown("## 🌱 에너지 절약 실천 체크리스트")
col1, col2 = st.columns(2)
with col1:
    c1 = st.checkbox("에어컨 온도 26도 유지하기")
    c2 = st.checkbox("선풍기와 병행 사용하기")
    c3 = st.checkbox("불필요한 조명 끄기")
    c4 = st.checkbox("대중교통 이용하기")
    c5 = st.checkbox("분리수거 철저히 하기")
with col2:
    c6 = st.checkbox("사용하지 않는 전자기기 플러그 뽑기")
    c7 = st.checkbox("냉방 시 문 닫아 효율 높이기")
    c8 = st.checkbox("계단 이용하기")
    c9 = st.checkbox("재사용 물품 활용하기")
    c10 = st.checkbox("텀블러 사용하기")

checked = sum([c1,c2,c3,c4,c5,c6,c7,c8,c9,c10])
progress = checked / 10
st.progress(progress)

if progress == 1:
    st.success("🎉 모든 실천을 완료했어요! 멋집니다, 지구가 환하게 웃고 있어요!")
elif progress >= 0.8:
    st.info("🌟 80% 달성! 거의 다 왔어요, 조금만 더 힘내요!")
elif progress >= 0.6:
    st.info("💪 60% 달성! 잘하고 있어요, 꾸준함이 중요해요!")
elif progress >= 0.4:
    st.info("✨ 40% 달성! 시작이 반이에요, 계속 실천해봐요!")
else:
    st.write("아직 실천이 적지만, 작은 시작이 큰 변화를 만듭니다 🌱")
