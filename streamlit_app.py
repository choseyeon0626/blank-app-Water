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

# -----------------------------------
# 제목 & 서론
# -----------------------------------
st.title("❄️ 멈추지 않는 에어컨과 해수면 상승")
st.subheader("과한 에어컨 사용에 의한 해수온, 해수면 높이 상승이 우리 삶에 미치는 영향")

st.markdown("""
### 서론  
여름마다 우리는 습관처럼 에어컨을 켠다. 기숙사에서, 교실에서, 집에서  
심지어 이불을 덮고 에어컨을 켠 채 잠드는 모습도 흔하다.  

그러나 이 편리한 습관이 바다와 연결되어 있다는 사실은 잘 인식되지 않는다.  
무분별한 전기 사용은 온실가스 배출을 가속화하고, 이는 결국 지구 평균 기온 상승과 해수면 상승으로 이어진다.  

이미 해수온 상승은 빠르게 진행되고 있고, 해수면은 매년 꾸준히 높아지고 있다.  
이 변화는 단순히 과학 뉴스 속 이야기가 아니라, 우리가 여름에 떠나는 피서지와 미래의 생활 공간을 위협하는 실질적 문제다.  

따라서 우리는 **에어컨 사용과 해수면 상승의 연관성을 데이터로 확인**하고,  
**청소년으로서 어떤 실천을 할 수 있을지 탐구**할 필요가 있다.
""")

# -----------------------------------
# 데이터 준비
# -----------------------------------
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

norm = colors.Normalize(vmin=0, vmax=max(levels))
cmap = cm.get_cmap('RdYlBu_r')  # 낮을수록 파랑, 높을수록 빨강
def get_color(value):
    rgba = cmap(norm(value))
    return colors.to_hex(rgba)

legend_html = """
<div style="position: fixed; 
     bottom: 40px; left: 40px; width: 200px; height: 140px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; padding: 10px;">
<b>🌊 해수면 상승 위험도</b><br>
<span style='color:#08306b;'>●</span> 낮음 (0~20mm)<br>
<span style='color:#2b8cbe;'>●</span> 보통 (20~40mm)<br>
<span style='color:#fdae61;'>●</span> 높음 (40~60mm)<br>
<span style='color:#d73027;'>●</span> 매우 높음 (60mm 이상)
</div>
"""

# -----------------------------------
# 본론 - 탭 구성
# -----------------------------------
st.header("📊 분석 시각화")

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 해수면 상승 추이",
    "🗺️ 도시별 위험도 지도",
    "🔥 폭염과 학습 환경",
    "💨 에어컨 시뮬레이션"
])

# 탭1 - 해수면 상승 추이
with tab1:
    st.subheader("전 세계 해수면 상승 추이 (1993~2023)")

    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown("### 연도 선택")
        start_year = st.selectbox("시작 연도", options=years, index=years.index(2010))
        end_year = st.selectbox("종료 연도", options=years, index=len(years)-1)

    if start_year > end_year:
        st.warning("❗ 시작 연도가 종료 연도보다 클 수 없습니다.")
    else:
        filtered_df = sea_df[(sea_df["연도"] >= start_year) & (sea_df["연도"] <= end_year)]
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=filtered_df["연도"],
                y=filtered_df["해수면 상승(mm)"],
                mode='lines+markers',
                line=dict(color='royalblue'),
                marker=dict(size=8)
            ))
            fig.update_layout(
                title=f"{start_year}년 ~ {end_year}년 해수면 상승 추이",
                xaxis_title="연도",
                yaxis_title="해수면 상승 (mm)",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("> ✅ **출처**: [NASA Global Mean Sea Level (1993–2023)](https://climate.nasa.gov/vital-signs/sea-level/)")

# 탭2 - 도시별 위험도 지도
with tab2:
    st.subheader("연도별 세계 도시 해수면 위험도")

    selected_year = st.slider("🌍 지도에 표시할 연도 선택", min_value=1993, max_value=2023, value=2015)
    selected_level = sea_df.loc[sea_df["연도"] == selected_year, "해수면 상승(mm)"].values[0]

    m = folium.Map(location=[20, 0], zoom_start=2)

    for city in cities:
        color = get_color(selected_level)
        folium.CircleMarker(
            location=[city["lat"], city["lon"]],
            radius=10,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=f"{city['city']}<br>해수면 상승: {selected_level:.1f} mm"
        ).add_to(m)

    m.get_root().html.add_child(folium.Element(legend_html))
    st_folium(m, width=900, height=550)

    # ✅ 지도 밑에 해설 추가
    st.markdown("""
    ---
    ## 🌍 해설: 에어컨 사용과 해수면 상승의 연결고리  

    연도별 데이터를 보면 1993년 0mm였던 해수면 상승이 2023년에는 **68.9mm**에 도달했습니다.  
    지도에서 보듯이 서울, 뉴욕, 마이애미, 자카르타 등 주요 해안 도시는 모두 위험 수준이 점차 심각해지고 있습니다.  

    해수면 상승은 단순히 바닷물이 늘어나는 문제가 아닙니다.  
    - 해수온 상승 → 바닷물 팽창 & 빙하 융해 → 해수면 상승  
    - 해수온 상승의 주요 원인 → **온실가스 증가**  
    - 온실가스 증가의 큰 요인 중 하나 → **에어컨 전력 소비**  

    결국 여름마다 켜는 에어컨은 **지구 평균 기온 상승 → 해수온 상승 → 해수면 상승**이라는 고리에 직접 연결되어 있습니다.  

    ### 📌 우리의 삶에 미치는 영향
    1. **도시 침수 위험** – 마이애미, 자카르타 같은 저지대 도시는 실제 거주 자체가 위협받습니다.  
    2. **학습 환경 악화** – 폭염이 심해지면 교실 온도가 높아져 청소년의 집중력과 성취도가 떨어집니다.  
    3. **악순환** – 폭염 때문에 에어컨 사용 증가 → 더 많은 CO₂ 배출 → 해수온 상승 가속화.  

    따라서 에어컨 사용을 효율적으로 줄이는 작은 실천이 곧 **바다와 교실을 함께 지키는 행동**이 됩니다.
    """)


# 탭3 - 폭염과 학습 환경
with tab3:
    st.subheader("폭염은 교실을 데운다")

    st.markdown("""
    ### 🔹 폭염과 학습 집중력

    - 기온 1도 상승 → **집중력 10% 감소**  
    - 폭염 시 **학업 성취도 평균 15% 하락**
    - 실내 온도 28도 초과 시, **인지 능력 저하** 급격히 증가

    > 💬 *"폭염 날씨에는 쉬는 시간 후 교실에 들어가는 것만으로도 숨이 막혀요"* – 고등학생 인터뷰
    """)

# 탭4 - 에어컨 시뮬레이션
with tab4:
    st.subheader("에어컨의 역설")

    st.markdown("가정용 에어컨 **1대**는 1시간 가동 시 약 **0.8kWh**의 전력을 소비합니다.")

    col3, col4 = st.columns(2)
    with col3:
        hours = st.slider("하루 평균 사용 시간 (시간)", 0, 24, 6)
    with col4:
        days = st.slider("총 사용 일수 (일)", 1, 90, 30)

    energy = hours * days * 0.8
    co2 = round(energy * 0.424, 2)

    st.markdown(f"""
    #### 🧮 결과
    - 🔌 총 전력 사용량: <span style='font-size:24px; color:orange; font-weight:bold'>{energy:.1f} kWh</span>  
    - 🌍 CO₂ 배출량: <span style='font-size:24px; color:red; font-weight:bold'>{co2:.1f} kg</span>  
    """, unsafe_allow_html=True)

    st.caption("※ CO₂ 배출량 계산 기준: 한국 전력 평균 배출계수 0.424 kg/kWh")

# -----------------------------------
# 결론
# -----------------------------------
st.header("📌 결론 및 제언")

st.markdown("""
- **교실 온도 26도 유지 캠페인**
- **에어컨 최소화 & 선풍기 병행 사용**
- **불필요한 전기 소모 줄이기**
- **여름 방학 기간 기후교육 강화**

> 청소년의 작은 실천이 **몰디브 해안도 지키고**,  
> **우리 교실의 온도도 지킬 수 있습니다.**
""")

st.caption("📚 출처: NASA, KOEM, 뉴스펭귄, 비즈니스포스트, 국립해양조사원, YTN Science")
