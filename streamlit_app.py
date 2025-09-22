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
st.title("❄️ 멈추지 않는 에어컨과 해수면 상승: 과한 에어컨 사용에 의한 해수온, 해수면 높이 상승이 우리 삶에 미치는 영향")

st.subheader("서론")
st.markdown("""
여름마다 우리는 습관처럼 에어컨을 켠다. 기숙사에서, 교실에서, 집에서 심지어 이불을 덮고 에어컨을 켠 채 잠드는 모습도 흔하다.  
그러나 이 편리한 습관이 바다와 연결되어 있다는 사실은 잘 인식되지 않는다.  

무분별한 전기 사용은 온실가스 배출을 가속화하고, 이는 결국 지구 평균 기온 상승과 해수면 상승으로 이어진다.  
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
    years = list(range(1993, 2024))
    levels = [
        0.0, 2.4, 4.5, 6.3, 8.2, 10.4, 12.5, 14.1, 16.3, 18.2,
        20.4, 22.1, 24.5, 26.8, 29.3, 31.1, 33.6, 36.1, 38.4, 41.0,
        43.2, 46.0, 48.5, 51.0, 54.2, 56.9, 59.5, 62.0, 65.1, 67.4,
        68.9
    ]
    sea_df = pd.DataFrame({"연도": years, "해수면 상승(mm)": levels})

    with st.sidebar:
        st.markdown("## 📊 해수면 데이터 옵션")
        start_year, end_year = st.slider("기간 선택", 1993, 2023, (2010, 2023))
        show_trend = st.checkbox("추세선 표시", True)

    filtered_df = sea_df[(sea_df["연도"] >= start_year) & (sea_df["연도"] <= end_year)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_df["연도"],
        y=filtered_df["해수면 상승(mm)"],
        mode='lines+markers',
        line=dict(color='royalblue'),
        marker=dict(size=8)
    ))
    if show_trend:
        coeffs = pd.Series(filtered_df["해수면 상승(mm)"]).rolling(window=3).mean()
        fig.add_trace(go.Scatter(
            x=filtered_df["연도"],
            y=coeffs,
            mode='lines',
            line=dict(color='red', dash='dot'),
            name="추세선"
        ))

    fig.update_layout(
        title=f"{start_year}년 ~ {end_year}년 해수면 상승 추이",
        xaxis_title="연도",
        yaxis_title="해수면 상승 (mm)",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("> ✅ **출처**: [NASA Global Mean Sea Level (1993–2023)](https://climate.nasa.gov/vital-signs/sea-level/)")

    st.markdown("""
    ### 📌 데이터 분석 및 시사점
    - 1993년 이후 해수면은 꾸준히 상승하고 있으며, 30년 동안 약 **70mm 이상 상승**했다.  
    - 이는 단순한 수치 증가가 아니라, **세계 해안 도시의 침수 가능성을 높이는 심각한 신호**이다.  
    - 에어컨 사용을 포함한 과도한 에너지 소비는 온실가스 배출을 가속화하여 결국 해수면 상승을 부추긴다.  

    👉 우리가 지금 당장 전기 사용을 줄이지 않는다면, 여름 피서지는 물론이고 **우리 교실과 삶의 공간**도 위협받게 된다.
    """)

# -------------------------------
# Tab 2: 세계 도시 위험도
# -------------------------------
with tab2:
    st.header("🌍 세계 주요 도시와 관광지의 위험도")

    selected_year = st.slider("🌍 지도에 표시할 연도 선택", min_value=1993, max_value=2023, value=2015)
    selected_level = sea_df.loc[sea_df["연도"] == selected_year, "해수면 상승(mm)"].values[0]

    cities = [
        {"city": "부산", "lat": 35.1796, "lon": 129.0756},
        {"city": "상하이", "lat": 31.2304, "lon": 121.4737},
        {"city": "자카르타", "lat": -6.2088, "lon": 106.8456},
        {"city": "마이애미", "lat": 25.7617, "lon": -80.1918},
        {"city": "암스테르담", "lat": 52.3676, "lon": 4.9041},
        {"city": "뉴욕", "lat": 40.7128, "lon": -74.0060}
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

    # 관광지 사진 비교
    st.markdown("### 🖼️ 도시별 관광지와 해수면 상승 영향")
    selected_city = st.selectbox(
        "도시 선택 (관광지 사진 보기)",
        ["부산", "상하이", "자카르타", "마이애미", "암스테르담", "뉴욕"]
    )

    if selected_city == "부산":
        st.image("https://upload.wikimedia.org/wikipedia/commons/5/55/Haeundae_Beach_May_2024.jpg",
                 caption="부산 해운대 해변 현재 모습 (출처: 위키피디아)")
        st.image("https://dummyimage.com/800x400/87ceeb/000000.png&text=부산+해운대+침수+예측+(참고용)",
                 caption="부산 해운대 침수 가능성 (참고용)")

    elif selected_city == "상하이":
        st.image("https://upload.wikimedia.org/wikipedia/commons/0/0a/The_Bund_in_Shanghai_at_night.jpg",
                 caption="상하이 외탄 현재 모습 (출처: 위키피디아)")
        st.image("https://dummyimage.com/800x400/4682b4/ffffff.png&text=상하이+외탄+침수+예측+(참고용)",
                 caption="상하이 외탄 침수 가능성 (참고용)")

    elif selected_city == "자카르타":
        st.image("https://upload.wikimedia.org/wikipedia/commons/a/ab/Fatahillah_Square_Jakarta.jpg",
                 caption="자카르타 코타 투아 현재 모습 (출처: 위키피디아)")
        st.image("https://dummyimage.com/800x400/2e8b57/ffffff.png&text=자카르타+구시가지+침수+예측+(참고용)",
                 caption="자카르타 구시가지 침수 가능성 (참고용)")

    elif selected_city == "마이애미":
        st.image("https://upload.wikimedia.org/wikipedia/commons/4/45/Miami_Beach_Ocean_Drive.jpg",
                 caption="마이애미 사우스 비치 현재 모습 (출처: 위키피디아)")
        st.image("https://dummyimage.com/800x400/ff6347/ffffff.png&text=마이애미+사우스비치+침수+예측+(참고용)",
                 caption="마이애미 사우스 비치 침수 가능성 (참고용)")

    elif selected_city == "암스테르담":
        st.image("https://upload.wikimedia.org/wikipedia/commons/2/26/Amsterdam_Canals_-_July_2022.jpg",
                 caption="암스테르담 운하 현재 모습 (출처: 위키피디아)")
        st.image("https://dummyimage.com/800x400/1e90ff/ffffff.png&text=암스테르담+운하+침수+예측+(참고용)",
                 caption="암스테르담 운하 침수 가능성 (참고용)")

    elif selected_city == "뉴욕":
        st.image("https://upload.wikimedia.org/wikipedia/commons/d/d6/Statue_of_Liberty_7.jpg",
                 caption="뉴욕 자유의 여신상 현재 모습 (출처: 위키피디아)")
        st.image("https://dummyimage.com/800x400/708090/ffffff.png&text=뉴욕+자유의여신상+침수+예측+(참고용)",
                 caption="뉴욕 자유의 여신상 침수 가능성 (참고용)")

    # 분석 및 시사점 (디벨롭)
    st.markdown("""
    ### 📊 분석 및 시사점

    - 해수면 상승은 단순히 해안선을 잠기게 하는 것이 아니라, **세계적인 관광지와 문화유산을 사라지게 만들 수 있는 심각한 위협**이다.  
    - 부산 해운대, 상하이 외탄, 마이애미 사우스비치, 암스테르담 운하, 뉴욕 자유의 여신상 등은 단순한 명소가 아니라  
      **도시의 정체성과 경제를 지탱하는 핵심 자산**이다.  

    ---
    ### 🌐 우리가 잃을 수 있는 것
    - **경제적 손실**: 관광 수입 급감, 일자리 상실  
    - **문화적 손실**: 수백 년간 이어온 도시의 역사와 상징이 침수 위험  
    - **사회적 손실**: 해안 지역 거주민의 이주, 도시 붕괴 위험  

    ---
    ### ⚠️ 청소년 세대에게 주는 메시지
    - 우리가 무심코 켜는 **에어컨 한 대, 몇 시간의 전력 낭비**가  
      결국은 **살 곳을 줄이고, 즐길 여행지를 빼앗는 결과**로 이어질 수 있다.  
    - 기후위기는 거창한 문제가 아니라, **곧 우리의 일상과 미래 여름방학 여행지의 문제**이다.  

    👉 지금의 작은 실천(적정 온도 유지, 에어컨 절약, 기후 교육 참여)이  
    곧 우리의 **삶의 터전과 여행지를 지키는 힘**이 된다.
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

    st.markdown("""
    ### 📌 분석 및 시사점
    - 단 한 대의 에어컨만 사용해도 수십 kg의 CO₂가 배출된다.  
    - 여름철 전국적으로 수백만 대가 동시에 사용되면, 그 양은 기하급수적으로 증가한다.  
    - 이는 곧 해수온 상승과 해수면 상승을 가속화하는 요인이 된다.  

    👉 우리의 작은 절약이 곧, **몰디브 해안도 지키고 우리 교실의 온도도 지킬 수 있는 실천**이다.
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
