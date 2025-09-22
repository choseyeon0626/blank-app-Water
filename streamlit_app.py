import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import folium
from streamlit_folium import st_folium
import matplotlib.cm as cm
import matplotlib.colors as colors

# 페이지 설정
st.set_page_config(page_title="멈추지 않는 에어컨과 해수면 상승", layout="wide")

# -----------------------------------
# 서론
# -----------------------------------
st.title("❄️ 멈추지 않는 에어컨과 해수면 상승: 과한 에어컨 사용이 해수온·해수면 상승에 미치는 영향")

st.subheader("서론")
st.markdown("""
여름마다 우리는 습관처럼 에어컨을 켠다. 기숙사에서, 교실에서, 집에서 심지어 이불을 덮고 켠 채 잠드는 모습도 흔하다.  
그러나 이 편리한 습관이 바다와 연결되어 있다는 사실은 잘 인식되지 않는다.  

무분별한 전기 사용은 온실가스 배출을 가속화하고, 이는 지구 평균 기온 상승과 해수면 상승으로 이어진다.  
이미 해수온 상승은 빠르게 진행되고 있고, 해수면은 매년 꾸준히 높아지고 있다.  

이 변화는 단순히 과학 뉴스 속 이야기가 아니라, 우리가 여름에 떠나는 피서지와 미래의 생활 공간을 위협하는 실질적 문제다.  
따라서 우리는 에어컨 사용과 해수면 상승의 연관성을 데이터로 확인하고, 청소년으로서 어떤 실천을 할 수 있을지 탐구할 필요가 있다.
""")

# -----------------------------------
# Tabs
# -----------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 해수면 상승 추이",
    "🗺️ 세계 도시 위험도",
    "🔥 폭염과 학습 환경",
    "💨 에어컨 시뮬레이션",
    "📌 결론 및 제언"
])

# -------------------------------
# Tab 1: 해수면 상승 추이
# -------------------------------
with tab1:
    st.sidebar.markdown("### 📊 해수면 상승 추이 옵션")

    years = list(range(1993, 2024))
    levels = [
        0.0, 2.4, 4.5, 6.3, 8.2, 10.4, 12.5, 14.1, 16.3, 18.2,
        20.4, 22.1, 24.5, 26.8, 29.3, 31.1, 33.6, 36.1, 38.4, 41.0,
        43.2, 46.0, 48.5, 51.0, 54.2, 56.9, 59.5, 62.0, 65.1, 67.4,
        68.9
    ]
    sea_df = pd.DataFrame({"연도": years, "해수면 상승(mm)": levels})

    start_year = st.sidebar.selectbox("시작 연도", options=years, index=years.index(2010))
    end_year = st.sidebar.selectbox("종료 연도", options=years, index=len(years)-1)

    if start_year > end_year:
        st.warning("❗ 시작 연도가 종료 연도보다 클 수 없습니다.")
    else:
        filtered_df = sea_df[(sea_df["연도"] >= start_year) & (sea_df["연도"] <= end_year)]
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

    # 분석 내용
    st.markdown("""
    ### 🔎 분석 및 시사점
    - 1993년 이후 해수면은 꾸준히 상승하여 **30년간 약 70mm 이상** 높아졌다.  
    - 이 추세는 단순한 통계가 아니라, 매년 우리가 사는 도시와 해안선을 잠식하는 실질적 위협이다.  
    - 해수면 상승은 곧 **주거지 감소**, **농경지 염해**, **관광지 상실**로 이어지며  
      청소년 세대가 살아갈 미래 환경에 직접적인 영향을 미친다.  

    👉 따라서 **에어컨 사용 습관을 바꾸는 작은 실천**이  
    미래의 해안 도시와 우리의 여행지를 지키는 데 연결된다.
    """)

# -------------------------------
# Tab 2: 세계 도시 위험도
# -------------------------------
with tab2:
    st.sidebar.markdown("### 🗺️ 도시 위험도 옵션")
    selected_year = st.sidebar.slider("연도 선택", min_value=1993, max_value=2023, value=2015)

    years = list(range(1993, 2024))
    levels = [
        0.0, 2.4, 4.5, 6.3, 8.2, 10.4, 12.5, 14.1, 16.3, 18.2,
        20.4, 22.1, 24.5, 26.8, 29.3, 31.1, 33.6, 36.1, 38.4, 41.0,
        43.2, 46.0, 48.5, 51.0, 54.2, 56.9, 59.5, 62.0, 65.1, 67.4,
        68.9
    ]
    sea_df = pd.DataFrame({"연도": years, "해수면 상승(mm)": levels})
    selected_level = sea_df.loc[sea_df["연도"] == selected_year, "해수면 상승(mm)"].values[0]

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
    cmap = cm.get_cmap('RdYlBu_r')
    def get_color(value):
        rgba = cmap(norm(value))
        return colors.to_hex(rgba)

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

    st_data = st_folium(m, width=900, height=550)

    # 분석 내용
    st.markdown("""
    ### 📊 분석 및 시사점

    - 해수면 상승은 단순히 수치상의 문제가 아니라, **우리가 살아가는 도시와 미래 세대가 누릴 공간을 직접적으로 위협**합니다.  
    - 특히 관광지와 문화유산은 많은 사람들이 즐겨 찾는 공간인 동시에, 침수에 가장 취약한 지역이기도 합니다.  

    - 예를 들어:  
      - 🇰🇷 **부산**: 해운대, 광안리 해수욕장이 물에 잠기면 여름철 대표 피서지가 사라짐  
      - 🇨🇳 **상하이**: 황푸강 외탄(와이탄), 디즈니랜드 같은 랜드마크가 침수 위험  
      - 🇮🇩 **자카르타**: 구시가지 코타 투아, 안쫄 드림랜드 같은 명소가 바닷속으로 사라질 가능성  
      - 🇺🇸 **마이애미**: 세계적으로 유명한 사우스 비치와 마이애미 항구가 치명적 타격  
      - 🇳🇱 **암스테르담**: 세계문화유산 운하 지구가 방조 시스템의 한계를 넘어서면 침수 위험  
      - 🇺🇸 **뉴욕**: 자유의 여신상, 맨해튼 해안가 같은 미국의 상징적인 공간도 안전하지 않음  

    ---

    ### 💡 우리가 잃게 될 것
    - 해수면이 계속 오르면 단순히 **주거 공간이 줄어드는 문제**뿐 아니라,  
      **여름마다 떠나는 여행지, 우리가 꿈꾸는 미래의 관광지까지 사라질 수 있습니다.**  
    - 결국 지금 우리가 무심코 사용하는 **에어컨 한 대, 하루 몇 시간의 전기 낭비가  
      우리의 삶의 터전과 여행지를 앗아가는 원인**이 될 수 있습니다.  

    👉 **작은 절약과 습관 변화**가 곧, 우리의 집과 미래 여행지를 지키는 길입니다.  
    """)

# -------------------------------
# Tab 3: 폭염과 학습 환경
# -------------------------------
with tab3:
    st.markdown("""
    ### 🔹 폭염과 학습 집중력
    - 기온 1도 상승 → **집중력 10% 감소**  
    - 폭염 시 **학업 성취도 평균 15% 하락**  
    - 실내 온도 28도 초과 시, **인지 능력 저하** 급격히 증가  

    > 💬 *"폭염 날씨에는 쉬는 시간 후 교실에 들어가는 것만으로도 숨이 막혀요"* – 고등학생 인터뷰
    """)

# -------------------------------
# Tab 4: 에어컨 시뮬레이션
# -------------------------------
with tab4:
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

    # 분석 추가
    st.markdown("""
    ### 🔎 분석 및 시사점
    - 단순히 하루 몇 시간의 사용 차이가 **수십 kg의 CO₂ 배출 차이**로 이어진다.  
    - 이는 곧 해수면 상승, 폭염 심화와 같은 기후 위기를 가속화시킨다.  
    - **개인의 작은 습관 변화**가 지구 환경에 미치는 파급력은 매우 크다.  

    👉 에어컨 사용을 줄이고 선풍기, 자연 환기와 병행하는 습관이 필요하다.  
    """)

# -------------------------------
# Tab 5: 결론 및 제언
# -------------------------------
with tab5:
    st.header("📌 결론 및 제언")

    st.markdown("""
    해수온과 해수면 상승은 지구 차원의 기후 문제이자, 우리의 **교실과 일상에 직접 연결된 문제**입니다.  
    에어컨 사용으로 인한 온실가스 배출은 단순한 전기요금 문제가 아니라, **청소년의 학습권·건강·미래 삶의 공간**까지 위협합니다.  

    따라서 우리는 에어컨 사용을 줄이는 것에서 멈추지 않고,  
    **기후위기에 대응하는 생활 습관**을 만들어 나가야 합니다.
    """)

    st.markdown("""
    ---
    - **교실 온도 26도 유지 캠페인**  
    - **에어컨 최소화 & 선풍기 병행 사용**  
    - **불필요한 전기 소모 줄이기**  
    - **여름 방학 기간 기후교육 강화**  

    > 청소년의 작은 실천이 **몰디브 해안도 지키고**,  
    > **우리 교실의 온도도 지킬 수 있습니다.**
    """)

    st.caption("📚 출처: NASA, KOEM, 뉴스펭귄, 비즈니스포스트, 국립해양조사원, YTN Science")
