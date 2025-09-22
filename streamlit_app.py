import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

# ----------------------------
# 페이지 설정
# ----------------------------
st.set_page_config(
    page_title="멈추지 않는 에어컨과 해수면 상승",
    layout="wide"
)

# ----------------------------
# 제목 & 서론
# ----------------------------
st.title("❄️ 멈추지 않는 에어컨과 해수면 상승")
st.subheader("과도한 냉방 사용이 불러온 지구의 뜨거운 대가")

st.markdown("""
여름이 되면 우리는 더위를 피하기 위해 무심코 에어컨을 켠다.  
시원함은 당장 손에 잡히지만, 그 이면에서 보이지 않는 대가는 지구가 치르고 있다.  

에어컨은 단순한 가전제품이 아니라 **온실가스 배출의 주요 원인 중 하나**이다.  
전기를 만들기 위해 화석연료가 대량으로 소비되고, 이산화탄소는 대기 중에 쌓여 지구의 온도를 높인다.  
그 결과 바닷물은 열을 머금어 팽창하고, 빙하가 녹아내리며 **해수면은 점점 상승**한다.  

이 변화는 단순히 과학적 수치에 머무르지 않는다.  
우리가 방학 때 찾는 해수욕장, 세계의 유명 관광지, 그리고 미래에 살 집과 학교까지도 위협받고 있다.  
즉, 오늘의 작은 냉방 습관이 내일의 삶의 터전을 바꾸고 있는 것이다.  

따라서 우리는 **에어컨 사용과 해수면 상승의 연관성을 데이터로 직접 확인**하고,  
**청소년으로서 지금 당장 실천할 수 있는 방법**을 찾아야 한다.  
이 탐구는 단순한 공부가 아니라, 우리의 미래를 지키는 행동 지침이 될 것이다.
""")

# ----------------------------
# 데이터 불러오기
# ----------------------------
@st.cache_data
def load_sea_level_data():
    url = "https://raw.githubusercontent.com/datasets/sea-level-rise/master/data/epa-sea-level.csv"
    df = pd.read_csv(url)
    df = df.rename(columns={"Year": "year", "CSIRO Adjusted Sea Level": "sea_level"})
    df = df.dropna(subset=["sea_level"])
    return df

sea_df = load_sea_level_data()

# ----------------------------
# 공통 보고서 + 체크리스트
# ----------------------------
def report_and_checklist(tab_name):
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
        c1 = st.checkbox("에어컨 온도 26도 유지하기", key=f"{tab_name}_c1")
        c2 = st.checkbox("선풍기와 병행 사용하기", key=f"{tab_name}_c2")
        c3 = st.checkbox("불필요한 조명 끄기", key=f"{tab_name}_c3")
        c4 = st.checkbox("대중교통 이용하기", key=f"{tab_name}_c4")
        c5 = st.checkbox("분리수거 철저히 하기", key=f"{tab_name}_c5")
    with col2:
        c6 = st.checkbox("사용하지 않는 전자기기 플러그 뽑기", key=f"{tab_name}_c6")
        c7 = st.checkbox("냉방 시 문 닫아 효율 높이기", key=f"{tab_name}_c7")
        c8 = st.checkbox("계단 이용하기", key=f"{tab_name}_c8")
        c9 = st.checkbox("재사용 물품 활용하기", key=f"{tab_name}_c9")
        c10 = st.checkbox("텀블러 사용하기", key=f"{tab_name}_c10")

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

# ----------------------------
# Tabs
# ----------------------------
tabs = st.tabs(["해수면 상승 추이", "지역별 위험", "에어컨 시뮬레이션", "위험 시각화"])

# ----------------------------
# Tab1: 해수면 상승 추이
# ----------------------------
with tabs[0]:
    st.sidebar.header("Tab1 조작")
    start_year, end_year = st.sidebar.slider(
        "연도 선택", int(sea_df["year"].min()), int(sea_df["year"].max()), (1950, 2020)
    )
    filtered = sea_df[(sea_df["year"] >= start_year) & (sea_df["year"] <= end_year)]

    coef = np.polyfit(filtered["year"], filtered["sea_level"], 1)
    poly1d_fn = np.poly1d(coef)
    trendline = poly1d_fn(filtered["year"])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered["year"], y=filtered["sea_level"],
                             mode="markers+lines", name="실제 데이터", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=filtered["year"], y=trendline,
                             mode="lines", name="추세선 (예측)", line=dict(color="red", dash="dash")))

    fig.update_layout(title="전세계 해수면 상승 추이 (NOAA 기반 데이터)",
                      xaxis_title="연도", yaxis_title="상대 해수면 (mm)")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ### 📊 분석
    데이터를 보면 해수면은 꾸준히 상승해 왔으며, 추세선은 앞으로도 증가세가 이어질 것임을 보여준다.  
    이는 단순한 일시적 변동이 아니라 **장기적·구조적인 상승**임을 의미한다.  
    따라서 지금 행동하지 않는다면, 앞으로의 세대는 더 큰 피해를 맞이할 수밖에 없다.
    """)

    report_and_checklist("tab1")

# ----------------------------
# Tab2: 지역별 위험 (5단계 색상)
# ----------------------------
with tabs[1]:
    st.sidebar.header("Tab2 조작")
    year = st.sidebar.slider("예상 연도", 2020, 2100, 2050, step=10)

    city_base_risks = {
        "서울": {"coords": [37.5665, 126.9780], "risk": 25},
        "부산": {"coords": [35.1796, 129.0756], "risk": 70},
        "도쿄": {"coords": [35.6895, 139.6917], "risk": 55},
        "상하이": {"coords": [31.2304, 121.4737], "risk": 85},
        "자카르타": {"coords": [-6.2088, 106.8456], "risk": 95},
        "런던": {"coords": [51.5074, -0.1278], "risk": 35},
        "암스테르담": {"coords": [52.3676, 4.9041], "risk": 80},
        "뉴욕": {"coords": [40.7128, -74.0060], "risk": 65},
        "마이애미": {"coords": [25.7617, -80.1918], "risk": 90},
        "리우데자네이루": {"coords": [-22.9068, -43.1729], "risk": 45},
        "케이프타운": {"coords": [-33.9249, 18.4241], "risk": 50},
        "시드니": {"coords": [-33.8688, 151.2093], "risk": 40}
    }

    factor = (year - 2020) / (2100 - 2020)
    city_data = {k: {"coords": v["coords"], "risk": min(100, int(v["risk"] * factor))} for k, v in city_base_risks.items()}

    def risk_to_color(risk):
        if risk <= 20: return "green"
        elif risk <= 40: return "lightgreen"
        elif risk <= 60: return "yellow"
        elif risk <= 80: return "orange"
        else: return "red"

    m = folium.Map(location=[20, 0], zoom_start=2)
    for city_name, info in city_data.items():
        folium.CircleMarker(
            location=info["coords"], radius=8,
            popup=f"{city_name} (위험도: {info['risk']})",
            color=risk_to_color(info["risk"]), fill=True,
            fill_color=risk_to_color(info["risk"]), fill_opacity=0.8
        ).add_to(m)

    st.subheader(f"세계 주요 도시 위험도 ({year}년 기준)")
    st_folium(m, width=700, height=500)

    st.markdown("""
    ### 🌍 분석
    연도를 조절하면 위험도가 점점 높아지는 것을 확인할 수 있다.  
    특히 **해안가 도시(자카르타, 마이애미, 상하이, 암스테르담 등)**는 빨간색에 가까워지며,  
    이는 실제로도 이미 침수 위험이 보고된 지역들이다.  
    반면 내륙에 위치한 도시(서울, 런던 등)는 상대적으로 낮은 위험을 보인다.  
    그러나 해안 경제와 연결된 글로벌 도시는 **세계적 충격을 불러올 수 있는 위험 요인**이 된다.
    """)

    report_and_checklist("tab2")

# ----------------------------
# Tab3: 에어컨 시뮬레이션
# ----------------------------
with tabs[2]:
    st.sidebar.header("Tab3 조작")
    hours = st.sidebar.slider("하루 사용 시간 (시간)", 0, 24, 8)
    days = st.sidebar.slider("사용 일수", 0, 365, 120)

    co2_per_hour = 1.2
    energy_per_hour = 1.5
    total_co2 = hours * days * co2_per_hour
    total_energy = hours * days * energy_per_hour
    impact = total_co2 * 0.0000015

    st.subheader("에어컨 사용 시뮬레이션 결과")
    st.write(f"- 총 CO₂ 배출량: **{total_co2:.1f} kg**")
    st.write(f"- 총 전력 사용량: **{total_energy:.1f} kWh**")
    st.write(f"- 예상 해수면 상승 기여: **{impact:.3f} mm**")

    st.markdown(f"""
    ### 🔎 분석
    단순히 하루 {hours}시간, {days}일 동안의 사용만으로도 상당한 양의 CO₂가 배출된다.  
    이는 개개인의 사용이 모이면 **국가 단위의 엄청난 배출량**으로 이어진다는 점을 시사한다.  
    따라서 냉방 습관을 바꾸는 것은 곧바로 **탄소 감축 실천**으로 이어질 수 있다.
    """)

    report_and_checklist("tab3")

# ----------------------------
# Tab4: 위험 시각화
# ----------------------------
with tabs[3]:
    st.sidebar.header("Tab4 조작")
    risk_value = st.sidebar.slider("위험 지수 (0=안전, 100=위험)", 0, 100, 50)

    color = "green"
    if risk_value > 80: color = "red"
    elif risk_value > 60: color = "orange"
    elif risk_value > 40: color = "yellow"
    elif risk_value > 20: color = "lightgreen"

    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=risk_value,
        title={"text": "해수면 상승 위험 지표"},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": color}}
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    ### ⚠️ 분석
    위험 지수를 {risk_value}로 설정했을 때, 이는 단순한 수치가 아니라  
    **사회·경제·환경적 위험 수준**을 가늠하는 지표가 될 수 있다.  
    예를 들어 80 이상일 경우, **기후난민 발생·주거지 상실·경제적 충격** 등이 현실화될 수 있다.  
    이 지표는 곧바로 행동의 필요성을 상기시켜 준다.
    """)

    report_and_checklist("tab4")
