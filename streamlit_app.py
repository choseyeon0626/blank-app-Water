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

    st.subheader("🔎 분석 및 시사점")
    st.markdown("""
    지난 30년 동안 해수면은 꾸준히 상승하고 있으며, 단순한 자연 변동이 아니라 인류 활동에 의한 기후변화의 직접적 결과임을 보여줍니다.  
    특히 2010년 이후 상승 속도가 더욱 가팔라져, 앞으로 해안 도시와 관광지의 생존 가능성에 큰 위협이 되고 있습니다.  

    이는 우리가 **에어컨 사용과 같은 일상적 습관을 바꾸지 않는다면** 머지않아 여름휴가를 떠나는 해변이나 도시는 더 이상 안전한 공간이 아닐 수 있음을 의미합니다.  
    """)

# -------------------------------
# Tab 2: 세계 도시 위험도
# -------------------------------
with tab2:
    selected_year = st.slider("🌍 지도에 표시할 연도 선택", min_value=1993, max_value=2023, value=2015)
    selected_level = sea_df.loc[sea_df["연도"] == selected_year, "해수면 상승(mm)"].values[0]

    cities = [
        {"city": "부산 (해운대)", "lat": 35.1796, "lon": 129.0756,
         "img_now": "https://upload.wikimedia.org/wikipedia/commons/5/55/Haeundae_Beach_May_2024.jpg",
         "img_future": "https://dummyimage.com/800x400/4682b4/ffffff.png&text=부산+해운대+침수+예측"},
        {"city": "자카르타", "lat": -6.2088, "lon": 106.8456,
         "img_now": "https://upload.wikimedia.org/wikipedia/commons/9/99/Jakarta_skyline.jpg",
         "img_future": "https://dummyimage.com/800x400/ff6347/ffffff.png&text=자카르타+침수+예측"},
        {"city": "마이애미", "lat": 25.7617, "lon": -80.1918,
         "img_now": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Miami_Beach_aerial_2017.jpg",
         "img_future": "https://dummyimage.com/800x400/2e8b57/ffffff.png&text=마이애미+침수+예측"},
        {"city": "암스테르담", "lat": 52.3676, "lon": 4.9041,
         "img_now": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Amsterdam_Canal_Panorama_2018.jpg",
         "img_future": "https://dummyimage.com/800x400/daa520/ffffff.png&text=암스테르담+침수+예측"},
    ]

    norm = colors.Normalize(vmin=0, vmax=max(levels))
    cmap = cm.get_cmap('RdYlBu_r')
    def get_color(value):
        rgba = cmap(norm(value))
        return colors.to_hex(rgba)

    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown("### 도시 선택")
        city_names = [c["city"] for c in cities]
        selected_city = st.selectbox("위험도 확인할 도시 선택", options=city_names)

        city_info = next(c for c in cities if c["city"] == selected_city)
        st.image(city_info["img_now"], caption=f"현재 {city_info['city']} 모습")
        st.image(city_info["img_future"], caption=f"{selected_city} 침수 예측 (참고 이미지)")

    with col2:
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
        m.get_root().html.add_child(folium.Element(legend_html))
        st_data = st_folium(m, width=700, height=500)

    st.subheader("🔎 분석 및 시사점")
    st.markdown("""
    해수면 상승은 단순히 과학 보고서 속 수치가 아니라, 세계 주요 해안 도시와 관광지에 직접적인 위협을 줍니다.  
    - **부산 해운대**: 대표적 해수욕장으로, 침수 시 지역 경제와 관광산업 직격탄.  
    - **자카르타**: 이미 도시 일부가 침수되고 있어, 인도네시아 수도 이전 논의까지 진행 중.  
    - **마이애미**: 세계적 휴양지이자 미국 남부 경제 중심지, 해수면 상승에 매우 취약.  
    - **암스테르담**: 운하 도시로서, 제방 붕괴 시 도시 전역이 물에 잠길 위험.  

    여러분의 **가벼운 에어컨 사용 습관 하나가**, 단순히 집 전기요금이 아니라  
    미래에 우리가 즐길 수 있는 **휴양지와 여행지의 생존 여부**와 직결됩니다.  
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
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 시뮬레이션 옵션")
        hours = st.slider("하루 평균 사용 시간 (시간)", 0, 24, 6)
        days = st.slider("총 사용 일수 (일)", 1, 90, 30)

    with col2:
        energy = hours * days * 0.8
        co2 = round(energy * 0.424, 2)

        st.markdown(f"""
        #### 🧮 결과
        - 🔌 총 전력 사용량: <span style='font-size:24px; color:orange; font-weight:bold'>{energy:.1f} kWh</span>  
        - 🌍 CO₂ 배출량: <span style='font-size:24px; color:red; font-weight:bold'>{co2:.1f} kg</span>  
        """, unsafe_allow_html=True)

        st.caption("※ CO₂ 배출량 계산 기준: 한국 전력 평균 배출계수 0.424 kg/kWh")

    st.subheader("🔎 분석 및 시사점")
    st.markdown("""
    단 한 대의 에어컨만으로도 여름 방학 기간 동안 상당한 양의 CO₂가 배출됩니다.  
    이런 작은 습관이 전 세계 수억 명의 청소년과 가정에서 반복된다면, 해수면 상승 속도는 더욱 가속화될 것입니다.  

    따라서 **에어컨 사용 최소화 + 선풍기 활용** 같은 작은 실천이 모여 지구와 우리의 교실을 지킬 수 있습니다.  
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
