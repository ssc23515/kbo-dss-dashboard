"""
KBO DSS 대시보드 — 1학기 최종 시연용
실행: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import json, os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="KBO DSS — 처방적 분석 대시보드",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .main-title { font-size: 2rem; font-weight: 700; color: #1a1a2e; margin-bottom: 0.2rem; }
    .sub-title  { font-size: 1rem; color: #666; margin-bottom: 1.5rem; }
    .module-badge {
        display: inline-block; padding: 3px 10px; border-radius: 12px;
        font-size: 0.8rem; font-weight: 600; margin-right: 6px;
    }
    .badge-a { background: #e8f4fd; color: #1565c0; }
    .badge-b { background: #fce8e8; color: #b71c1c; }
    .badge-c { background: #e8f5e9; color: #2e7d32; }
    .rec-box {
        background: #f0f7ff; border-left: 4px solid #1565c0;
        padding: 12px 16px; border-radius: 4px; margin: 8px 0;
    }
    .rec-box-b {
        background: #fff5f5; border-left: 4px solid #b71c1c;
        padding: 12px 16px; border-radius: 4px; margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# 데이터 상수
# ════════════════════════════════════════════════════════════════════

MODULE_A_CACHE_PATH = os.path.join(
    r"D:\Documents\신상철학교\2026-1\대회겸졸프\02_All_Models",
    "module_a_cache.json"
)

def load_module_a():
    if os.path.exists(MODULE_A_CACHE_PATH):
        with open(MODULE_A_CACHE_PATH, "r", encoding="utf-8") as f:
            cache = json.load(f)
        entry = cache.get("20260064", {})
        return {
            "actual_re": entry.get("actual_re", 0.5280),
            "order_re":  entry.get("order_re",  0.7267),
            "bench_re":  entry.get("bench_re",  0.7789),
        }
    return {"actual_re": 0.5280, "order_re": 0.7267, "bench_re": 0.7789}

A = load_module_a()
A["delta_re_order"] = A["order_re"] - A["actual_re"]
A["delta_re_bench"] = A["bench_re"] - A["actual_re"]
A["delta_runs_order"] = A["delta_re_order"] * 9
A["delta_runs_bench"] = A["delta_re_bench"] * 9

MODULE_A_GAME = {
    "s_no": "20260064", "date": "2026-04-11",
    "away_team": "KIA (2002)", "home_team": "한화 (7002)",
    "away_sp": "이의리", "home_sp": "왕옌청",
    "target_team": "한화 이글스 (7002)",
}

# 타순: (타순, 이름, 포지션)
A_ACTUAL_LINEUP = [
    ("1번", "이원석",  "중견수"),
    ("2번", "페라자",  "우익수"),
    ("3번", "문현빈",  "좌익수"),
    ("4번", "강백호",  "지명타자"),
    ("5번", "채은성",  "1루수"),
    ("6번", "노시환",  "3루수"),
    ("7번", "하주석",  "2루수"),
    ("8번", "허인서",  "포수"),
    ("9번", "심우준",  "유격수"),
]

# Module A [B] 선발 9인 순서 최적화 결과 (셀3 출력)
A_ORDER_LINEUP = [
    ("1번", "페라자",  "우익수",   True),
    ("2번", "심우준",  "유격수",   True),
    ("3번", "문현빈",  "좌익수",   False),
    ("4번", "허인서",  "포수",     True),
    ("5번", "강백호",  "지명타자", True),
    ("6번", "노시환",  "3루수",    False),
    ("7번", "하주석",  "2루수",    False),
    ("8번", "이원석",  "중견수",   True),
    ("9번", "채은성",  "1루수",    True),
]

# ── Module B 데이터 (한화 이글스 불펜, 홈, 7002) ─────────────────
BULLPEN_RAW = [
    {"투수": "조동욱",  "TBF": 44, "IP": 23.3, "G": 29, "SV": 0, "HLD": 7, "IP/G": 0.80,
     "raw_risp_era": 5.40,  "역할": "셋업"},
    {"투수": "이상규",  "TBF": 31, "IP": 25.7, "G": 21, "SV": 0, "HLD": 5, "IP/G": 1.22,
     "raw_risp_era": 6.00,  "역할": "셋업"},
    {"투수": "김종수",  "TBF": 35, "IP": 18.0, "G": 25, "SV": 0, "HLD": 4, "IP/G": 0.72,
     "raw_risp_era": 6.48,  "역할": "셋업"},
    {"투수": "윤산흠",  "TBF": 35, "IP": 21.3, "G": 21, "SV": 0, "HLD": 2, "IP/G": 1.02,
     "raw_risp_era": 8.64,  "역할": "미들릴리프"},
    {"투수": "강건우",  "TBF": 26, "IP": 11.3, "G": 9,  "SV": 0, "HLD": 0, "IP/G": 1.26,
     "raw_risp_era": 12.71, "역할": "미들릴리프"},
    {"투수": "박준영",  "TBF": 33, "IP": 22.0, "G": 19, "SV": 0, "HLD": 0, "IP/G": 1.16,
     "raw_risp_era": 16.50, "역할": "미들릴리프"},
    {"투수": "박상원",  "TBF": 35, "IP": 20.0, "G": 24, "SV": 1, "HLD": 7, "IP/G": 0.83,
     "raw_risp_era": 16.71, "역할": "셋업"},
    {"투수": "정우주",  "TBF": 39, "IP": 26.7, "G": 27, "SV": 0, "HLD": 5, "IP/G": 0.99,
     "raw_risp_era": 16.50, "역할": "셋업"},
    {"투수": "김서현",  "TBF": 29, "IP": 8.0,  "G": 12, "SV": 1, "HLD": 0, "IP/G": 0.67,
     "raw_risp_era": 24.30, "역할": "미들릴리프"},
]

LEAGUE_RISP_ERA = 4.50

MODULE_B_EVAL = {
    "game": "20260064", "date": "2026-04-11",
    "starter_name": "왕옌청", "starter_risp_era": 8.40, "starter_tbf": 68,
    "recommend_name": "조동욱", "recommend_era": 5.12,
    "delta_ra_per_inning": 0.365,
}

MODULE_B_GAME = {
    "s_no": "20260064", "date": "2026-04-11",
    "away_team": "KIA (2002)", "home_team": "한화 (7002)",
    "away_sp": "이의리", "home_sp": "왕옌청",
}

# ── Module C ───────────────────────────────────────────────────────
PITCHER_NAMES = {
    16313: "폰세",    16153: "와이스",  10590: "류현진",
    15013: "문동주",  11318: "엄상백",  16107: "황준서",  16108: "조동욱",
}

SCHEDULE_RAW = [
    ("05-02",2002,"원정",11318,16153), ("05-04",2002,"원정",16313,16313),
    ("05-05",1001,"홈",16153,10590),  ("05-06",1001,"홈",10590,15013),
    ("05-07",1001,"홈",15013,16153),  ("05-09",10001,"원정",11318,16313),
    ("05-10",10001,"원정",16313,10590),("05-11",10001,"원정",16153,15013),
    ("05-13",6002,"홈",10590,16153),  ("05-14",6002,"홈",15013,16107),
    ("05-15",6002,"홈",11318,15013),  ("05-17",9002,"홈",16313,10590),
    ("05-17",9002,"홈",16153,16313),  ("05-18",9002,"홈",10590,16153),
    ("05-20",11001,"원정",15013,15013),("05-21",11001,"원정",16107,10590),
    ("05-22",11001,"원정",16313,16107),("05-23",3001,"홈",16153,16153),
    ("05-24",3001,"홈",10590,16313),  ("05-25",3001,"홈",15013,15013),
    ("05-27",5002,"원정",16107,10590),("05-28",5002,"원정",16313,16107),
    ("05-29",5002,"원정",16153,16313),("05-30",11001,"원정",10590,16153),
    ("05-31",11001,"원정",11318,15013),("06-01",11001,"원정",16107,10590),
    ("06-03",12001,"홈",16313,16313), ("06-04",12001,"홈",16153,16153),
    ("06-05",12001,"홈",10590,16107), ("06-06",2002,"원정",11318,15013),
    ("06-07",2002,"원정",16107,16313),("06-08",2002,"원정",16313,10590),
    ("06-10",6002,"홈",16153,16153),  ("06-11",6002,"홈",16108,15013),
    ("06-12",6002,"홈",11318,16313),  ("06-14",5002,"홈",16313,10590),
    ("06-15",5002,"홈",15013,16153),  ("06-17",3001,"원정",16153,16313),
    ("06-18",3001,"원정",11318,10590),("06-19",3001,"원정",16107,16153),
    ("06-22",10001,"홈",16313,16313), ("06-25",1001,"원정",16153,15013),
    ("06-26",1001,"원정",15013,16313),("06-27",9002,"원정",11318,10590),
    ("06-28",9002,"원정",16313,16107),("06-29",9002,"원정",10590,16153),
]

MODULE_C_SUMMARY = {
    "n_games": 46, "actual_score": 26.5131, "ilp_score": 32.0256,
    "delta": 5.5125, "n_changed": 38, "violations": 0,
    "period": "2025년 5~6월", "team": "한화 이글스",
}

def build_schedule_df():
    rows = []
    for date, opp, ha, actual, ilp in SCHEDULE_RAW:
        rows.append({
            "날짜": date,
            "상대": opp,
            "홈/원정": ha,
            "실제 선발": PITCHER_NAMES.get(actual, str(actual)),
            "ILP 처방": PITCHER_NAMES.get(ilp, str(ilp)),
            "변경": "★" if actual != ilp else "",
        })
    return pd.DataFrame(rows)

@st.cache_data
def compute_bullpen_ranking(k: int) -> pd.DataFrame:
    rows = []
    for p in BULLPEN_RAW:
        tbf = p["TBF"]
        shrunk = (p["raw_risp_era"] * tbf + k * LEAGUE_RISP_ERA) / (tbf + k)
        rows.append({
            "투수":         p["투수"],
            "역할":         p["역할"],
            "보정ERA":      round(shrunk, 2),
            "원본RISP ERA": round(p["raw_risp_era"], 2),
            "TBF":          tbf,
            "G":            p["G"],
        })
    df = pd.DataFrame(rows).sort_values("보정ERA").reset_index(drop=True)
    df.insert(0, "순위", [f"{'★' if i==0 else '☆' if i==1 else ' '} {i+1}위"
                          for i in range(len(df))])
    return df

# ════════════════════════════════════════════════════════════════════
# 헤더
# ════════════════════════════════════════════════════════════════════

st.markdown('<div class="main-title">⚾ KBO DSS — 처방적 분석 대시보드</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">홍익대학교 산업데이터공학과 · 시스템 분석 및 설계 · C321036 신상철</div>',
    unsafe_allow_html=True,
)

tab_summary, tab_a, tab_b, tab_c = st.tabs([
    "📊 종합 요약",
    "🏏 Module A — 타순 최적화",
    "⚾ Module B — 불펜 교체 처방",
    "📅 Module C — 선발 로테이션 ILP",
])

# ════════════════════════════════════════════════════════════════════
# TAB 1: 종합 요약
# ════════════════════════════════════════════════════════════════════

with tab_summary:
    st.subheader("DSS 3모듈 — 처방 효과 종합")
    st.caption("분석 대상 팀: 한화 이글스 | 경기 기준: 2026-04-11 vs KIA (Module A·B) / 2025년 5~6월 시즌 (Module C)")
    st.markdown("---")

    _c_per = MODULE_C_SUMMARY['delta'] / MODULE_C_SUMMARY['n_games']
    _c_actual_per = MODULE_C_SUMMARY['actual_score'] / MODULE_C_SUMMARY['n_games']
    _c_ilp_per    = MODULE_C_SUMMARY['ilp_score']    / MODULE_C_SUMMARY['n_games']

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<span class="module-badge badge-a">Module A</span> **타순 순서 최적화**', unsafe_allow_html=True)
        st.metric("기대득점/이닝 (RE)", f"{A['order_re']:.4f}",
                  delta=f"감독 {A['actual_re']:.4f} → DSS {A['order_re']:.4f} (+{A['delta_re_order']:.4f})")
        st.caption(f"9이닝 기준 +{A['delta_runs_order']:.2f}점 기대")
    with col2:
        st.markdown('<span class="module-badge badge-b">Module B</span> **불펜 교체 처방**', unsafe_allow_html=True)
        st.metric("RISP ERA 개선", f"{MODULE_B_EVAL['starter_risp_era']:.2f} → {MODULE_B_EVAL['recommend_era']:.2f}",
                  delta=f"이닝당 {MODULE_B_EVAL['delta_ra_per_inning']:.3f}점 절감")
        st.caption(f"{MODULE_B_EVAL['starter_name']}(ERA {MODULE_B_EVAL['starter_risp_era']:.2f}) → {MODULE_B_EVAL['recommend_name']}(보정ERA {MODULE_B_EVAL['recommend_era']:.2f})")
    with col3:
        st.markdown('<span class="module-badge badge-c">Module C</span> **선발 로테이션 ILP**', unsafe_allow_html=True)
        st.metric("P(win) 합 (46경기)", f"{MODULE_C_SUMMARY['ilp_score']:.2f}",
                  delta=f"감독 {MODULE_C_SUMMARY['actual_score']:.2f} → ILP {MODULE_C_SUMMARY['ilp_score']:.2f} (+{MODULE_C_SUMMARY['delta']:.2f})")
        st.caption(f"경기당 평균 +{_c_per:.3f} | 위반 0건 ✅")

    st.markdown("---")
    st.subheader("모듈별 처방 효과 비교")

    _viz_tab1, _viz_tab2 = st.tabs(["📈 모듈별 전후 비교", "📊 Module C — 누적 P(win)"])

    with _viz_tab1:
        # % 개선율 기준 단일 차트 — 직관적, 단위 통일
        # 3-subplot: 모듈별 자연 단위 전후 비교
        _b_before_runs = MODULE_B_EVAL['starter_risp_era'] / 9   # 기대실점/이닝
        _b_after_runs  = MODULE_B_EVAL['recommend_era'] / 9

        fig_sub = make_subplots(
            rows=1, cols=3,
            subplot_titles=[
                "Module A — 타순 최적화",
                "Module B — 불펜 교체 처방<br><sup style='color:#b71c1c'>왕옌청 80구+ · RISP 발생 시 → 조동욱 투입</sup>",
                "Module C — 선발 로테이션 ILP",
            ],
            horizontal_spacing=0.12,
        )

        # A: RE 기대득점 (높을수록 좋음)
        for _x, _y, _col, _lg in [
            ("감독 실제", A['actual_re'],  "#bdbdbd", True),
            ("DSS 처방",  A['order_re'],   "#1565c0", True),
        ]:
            fig_sub.add_trace(go.Bar(
                name=_x, x=[_x], y=[_y],
                text=[f"{_y:.4f}"], textposition="outside",
                marker_color=_col, showlegend=_lg,
            ), row=1, col=1)
        fig_sub.update_yaxes(title_text="RE (↑좋음)",
                             title_font=dict(size=11),
                             title_standoff=8,
                             range=[0, A['order_re'] * 1.38], row=1, col=1)

        # B: 기대실점/이닝 = RISP ERA / 9 (낮을수록 좋음)
        for _x, _y, _col, _lbl in [
            ("감독 유지\n(왕옌청)", _b_before_runs, "#e53935",
             f"RISP ERA {MODULE_B_EVAL['starter_risp_era']:.2f}\n→ {_b_before_runs:.3f}점/이닝"),
            ("DSS 교체\n(조동욱)",  _b_after_runs,  "#43a047",
             f"보정ERA {MODULE_B_EVAL['recommend_era']:.2f}\n→ {_b_after_runs:.3f}점/이닝"),
        ]:
            fig_sub.add_trace(go.Bar(
                name=_x, x=[_x], y=[_y],
                text=[_lbl], textposition="outside",
                marker_color=_col, showlegend=False,
            ), row=1, col=2)
        fig_sub.update_yaxes(title_text="기대실점/이닝 (↓좋음)",
                             title_font=dict(size=11),
                             title_standoff=8,
                             range=[0, _b_before_runs * 1.38], row=1, col=2)

        # C: P(win)/경기 (높을수록 좋음)
        for _x, _y, _col, _lg in [
            ("감독 로테이션", _c_actual_per, "#bdbdbd", False),
            ("ILP 처방",     _c_ilp_per,    "#2e7d32", False),
        ]:
            fig_sub.add_trace(go.Bar(
                name=_x, x=[_x], y=[_y],
                text=[f"{_y:.3f}"], textposition="outside",
                marker_color=_col, showlegend=_lg,
            ), row=1, col=3)
        fig_sub.update_yaxes(title_text="P(win)/경기 (↑좋음)",
                             title_font=dict(size=11),
                             title_standoff=8,
                             range=[0, _c_ilp_per * 1.38], row=1, col=3)

        fig_sub.update_layout(
            height=430, barmode="group",
            margin=dict(l=10, r=10, t=60, b=50),
            legend=dict(x=0.35, y=-0.16, orientation="h"),
            plot_bgcolor="white", paper_bgcolor="white",
        )
        st.plotly_chart(fig_sub, width='stretch')
        st.caption(
            "Module B: 기대실점/이닝 = RISP ERA ÷ 9  |  "
            "빨강(감독 유지) 막대가 초록(DSS 교체)보다 높을수록 교체 이득이 큼  |  "
            "Module C: 2025시즌 검증 기준 (완료 시즌)"
        )

    with _viz_tab2:
        _n = MODULE_C_SUMMARY['n_games']
        _game_idx   = list(range(1, _n + 1))
        _actual_cum = [MODULE_C_SUMMARY['actual_score'] / _n * i for i in _game_idx]
        _ilp_cum    = [MODULE_C_SUMMARY['ilp_score']    / _n * i for i in _game_idx]

        fig_c = go.Figure()
        fig_c.add_trace(go.Scatter(x=_game_idx, y=_actual_cum, mode="lines",
            name="감독 실제", line=dict(color="#888", width=2, dash="dot")))
        fig_c.add_trace(go.Scatter(x=_game_idx, y=_ilp_cum, mode="lines",
            name="ILP 처방", line=dict(color="#2e7d32", width=2.5),
            fill="tonexty", fillcolor="rgba(46,125,50,0.08)"))
        fig_c.add_annotation(x=_n, y=MODULE_C_SUMMARY['ilp_score'],
            text=f"ILP: {MODULE_C_SUMMARY['ilp_score']:.2f}", showarrow=False,
            xanchor="right", font=dict(color="#2e7d32", size=12))
        fig_c.add_annotation(x=_n, y=MODULE_C_SUMMARY['actual_score'],
            text=f"감독: {MODULE_C_SUMMARY['actual_score']:.2f}", showarrow=False,
            xanchor="right", yshift=-14, font=dict(color="#666", size=12))
        fig_c.update_layout(
            height=300, margin=dict(l=10, r=30, t=20, b=40),
            xaxis=dict(title="경기 수 (누적)", showgrid=True, gridcolor="#eee"),
            yaxis=dict(title="P(win) 누적 합", showgrid=True, gridcolor="#eee"),
            legend=dict(x=0.02, y=0.95),
            plot_bgcolor="white", paper_bgcolor="white",
        )
        st.plotly_chart(fig_c, width='stretch')
        st.caption(
            f"**두 선의 차이 = ILP 처방의 누적 효과.** "
            f"감독 로테이션({MODULE_C_SUMMARY['actual_score']:.2f})은 고ERA 투수(엄상백 ERA 6.25)를 과다 기용하는 반면, "
            f"ILP 처방({MODULE_C_SUMMARY['ilp_score']:.2f})은 저ERA·충분한 휴식 투수에 등판을 집중시켜 "
            f"46경기 누적 P(win)을 **+{MODULE_C_SUMMARY['delta']:.2f}** 끌어올립니다."
        )

    st.markdown("---")
    _summary_df = pd.DataFrame([
        {"모듈": "A — 타순 순서 최적화", "처방": "동일 선수, 타순 변경",
         "핵심 지표": "ΔRE/이닝", "결과": f"+{A['delta_re_order']:.4f} (+{A['delta_runs_order']:.2f} runs/9이닝)"},
        {"모듈": "B — 불펜 교체 처방", "처방": "교체 시점/투수 선택",
         "핵심 지표": "ΔRISP ERA / Δ실점",
         "결과": f"ERA {MODULE_B_EVAL['starter_risp_era']:.2f}→{MODULE_B_EVAL['recommend_era']:.2f} / 이닝당 {MODULE_B_EVAL['delta_ra_per_inning']:.3f}점 절감"},
        {"모듈": "C — 선발 로테이션 ILP", "처방": "46경기 투수 배정 변경",
         "핵심 지표": "ΔP(win) 합",
         "결과": f"+{MODULE_C_SUMMARY['delta']:.2f} (경기당 +{_c_per:.3f}) | 위반 0건"},
    ])
    st.dataframe(_summary_df, width='stretch', hide_index=True)


# ════════════════════════════════════════════════════════════════════
# TAB 2: Module A
# ════════════════════════════════════════════════════════════════════

with tab_a:
    st.subheader("Module A — 타순 최적화 (Markov Chain)")
    st.caption(f"대상: {MODULE_A_GAME['target_team']} | {MODULE_A_GAME['date']} vs {MODULE_A_GAME['away_team']} | 상대 선발: {MODULE_A_GAME['away_sp']}")

    # ── RE 메트릭 ─────────────────────────────────────────────────────
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("감독 실제 타순 RE", f"{A['actual_re']:.4f}", delta="기준")
    with col_b:
        st.metric("DSS: 순서 최적화 RE", f"{A['order_re']:.4f}",
                  delta=f"+{A['delta_re_order']:.4f} (+{A['delta_runs_order']:.2f} runs/9이닝)")

    st.markdown("---")

    # ── 타순 비교 테이블 (핵심 결과) ──────────────────────────────────
    st.subheader("📋 타순 비교")

    col_l1, col_l2 = st.columns(2)

    with col_l1:
        st.markdown("**[A] 감독 실제 타순**")
        st.caption(f"RE = {A['actual_re']:.4f} (기준)")
        df_act = pd.DataFrame(
            [(r[0], r[1], r[2]) for r in A_ACTUAL_LINEUP],
            columns=["타순", "선수", "포지션"]
        )
        st.dataframe(df_act, hide_index=True, width='content')

    with col_l2:
        st.markdown("**[B] DSS: 순서 최적화**")
        st.caption(f"RE = {A['order_re']:.4f}  ΔRE = +{A['delta_re_order']:.4f}  (+{A['delta_runs_order']:.2f} runs/9이닝)")
        rows_b = []
        for t, name, pos, changed in A_ORDER_LINEUP:
            rows_b.append({"타순": t, "선수": ("→ " if changed else "   ") + name, "포지션": pos})
        df_ord = pd.DataFrame(rows_b)
        st.dataframe(df_ord, hide_index=True, width='content')

    st.caption("→ = 감독 타순 대비 변경된 자리  |  ※ [C] 벤치 포함 최적화는 외국인 투수 타격 보정 이슈로 발표 제외 (2학기 개선 예정)")

    with st.expander("▶ 방법론 상세"):
        st.markdown("""
**Markov Chain 기반 이닝 기대득점 (RE) 계산**

- **24 game states**: 아웃카운트(0·1·2) × 주자 배치(8가지) 조합
- **전이 확률**: playerSituation si=3 주자 상황별 스탯 → 상태 전이 행렬
- **최적화**: Greedy swap 탐색 (Phase 1: 순서, Phase 2: 벤치 교체)
- **소표본 처리**: PA 부족 선수 → 해당 주자 상황 리그 평균으로 보간
""")


# ════════════════════════════════════════════════════════════════════
# TAB 3: Module B
# ════════════════════════════════════════════════════════════════════

with tab_b:
    st.subheader("Module B — 불펜 교체 처방 (Bayesian Shrinkage)")
    st.caption(
        f"대상: 한화 이글스 불펜 (홈) | {MODULE_B_GAME['date']} vs {MODULE_B_GAME['away_team']} | "
        f"한화 선발: {MODULE_B_GAME['home_sp']}"
    )

    st.markdown("---")

    # ── k 슬라이더 ────────────────────────────────────────────────────
    st.markdown("### 🎚️ Shrinkage 강도 조절 (k)")
    st.caption("k = 소표본 보정 강도 | k↑ 리그 평균 의존 (시즌 초) · k↓ 실측 데이터 반영 (시즌 후)")

    col_sl, col_sl_info = st.columns([2, 1.5])
    with col_sl:
        k_val = st.slider(
            "k 값",
            min_value=5, max_value=150, value=20, step=5,
            key="bullpen_k_slider",
            label_visibility="collapsed",
        )
    with col_sl_info:
        if k_val <= 15:
            st.info(f"**k={k_val}** — 시즌 후반: 실측 반영")
        elif k_val <= 40:
            st.info(f"**k={k_val}** — 시즌 중반 균형 (기본값)")
        else:
            st.info(f"**k={k_val}** — 시즌 초반: 리그 평균 의존")

    # ── 불펜 순위표 ───────────────────────────────────────────────────
    df_bullpen = compute_bullpen_ranking(k_val)
    st.markdown(f"**한화 이글스 불펜 — Bayesian 보정ERA 순위** (k={k_val})")
    st.dataframe(df_bullpen, hide_index=True, width='stretch')

    # 순위 변동 표시
    df_base = compute_bullpen_ranking(20)
    base_ranks = {r["투수"]: i+1 for i, r in df_base.iterrows()}
    cur_ranks  = {r["투수"]: i+1 for i, r in df_bullpen.iterrows()}
    changed    = {p: base_ranks[p]-cur_ranks[p] for p in base_ranks if base_ranks[p] != cur_ranks[p]}
    if changed:
        msgs = [f"**{p}** {'▲' if v>0 else '▼'}{abs(v)}위" for p, v in changed.items()]
        st.caption(f"k=20 대비 순위 변동: {', '.join(msgs)}")
    else:
        st.caption("k=20 대비 순위 변동 없음")

    st.markdown("---")

    # ── 교체 처방 ─────────────────────────────────────────────────────
    st.subheader("📌 교체 처방 결과")

    top = df_bullpen.iloc[0]
    _sp_era      = MODULE_B_EVAL['starter_risp_era']
    _rec_era     = top['보정ERA']
    _delta_inn   = (_sp_era - _rec_era) / 9   # 이닝당 기대실점 절감

    # ① 임계점 (WHEN)
    st.markdown("**① 교체 임계점 — 언제 바꿔야 하나?**")
    st.info(
        f"**{MODULE_B_EVAL['starter_name']}** 80구 초과 또는 5이닝 이상 투구 후 "
        f"**득점권(RISP) 위기 상황** 발생 시 교체 검토\n\n"
        f"— 역대 경기 기록 분석: 80구 이후 ERA 유의미하게 상승 (셀4 임계점 분석 기반)"
    )

    # ② WHO + 효과
    st.markdown("**② 추천 투수 — 누구로 바꿔야 하나?**")
    col_sp, col_arr, col_rec = st.columns([5, 1, 5])

    with col_sp:
        st.markdown(f"""
**현재 선발: {MODULE_B_EVAL['starter_name']}**
| 지표 | 값 |
|------|-----|
| RISP ERA (위기상황) | **{_sp_era:.2f} (ERA)** |
| 위기상황 상대 타석(TBF) | {MODULE_B_EVAL['starter_tbf']} |
| 이닝당 기대실점 | {_sp_era/9:.3f}점 |
""")

    with col_arr:
        st.markdown("<br><div style='text-align:center;font-size:2rem;color:#b71c1c'>→</div>", unsafe_allow_html=True)

    with col_rec:
        st.markdown(f"""
**추천 교체: {top['투수']}** ({top['역할']})
| 지표 | 값 |
|------|-----|
| Bayesian 보정ERA (k={k_val}) | **{_rec_era:.2f}** |
| 위기상황 상대 타석(TBF) | {top['TBF']} |
| 이닝당 기대실점 | {_rec_era/9:.3f}점 |
""")

    # ③ 기대 효과
    if _delta_inn > 0:
        st.markdown("**③ 교체 시 기대 효과**")
        st.success(
            f"임계점 도달 후 {top['투수']} 투입 시 이닝당 **{_delta_inn:.3f}점 절감** 기대\n\n"
            f"잔여 2이닝 기준 **{_delta_inn*2:.3f}점**, 잔여 3이닝 기준 **{_delta_inn*3:.3f}점** 절감"
        )
        st.caption(
            f"계산: ({_sp_era:.2f} − {_rec_era:.2f}) ÷ 9 = {_delta_inn:.3f}점/이닝  |  "
            f"슬라이더 k값 변경 시 추천 투수·보정ERA 실시간 반영"
        )

    with st.expander("▶ Bayesian Shrinkage 방법론"):
        st.markdown(f"""
**보정ERA 계산식**

```
보정ERA = (실제RISP ERA × TBF + k × 리그평균ERA) / (TBF + k)
```

- **RISP ERA**: 주자 득점권 상황(si=3) 실측 방어율
- **TBF**: 위기상황 총 상대 타석 수
- **k**: Shrinkage 강도 — TBF가 적을수록 k 영향 ↑
- **리그평균 RISP ERA**: {LEAGUE_RISP_ERA}

강건우 (TBF={[p for p in BULLPEN_RAW if p['투수']=='강건우'][0]['TBF']}): 불펜 중 최소표본 — k값 변화에 따른 보정 폭 가장 큼
""")

    with st.expander("▶ 2학기 고도화"):
        st.info("gmLI(Leverage Index) 가중치 도입, 좌우 매치업 구조 확장")


# ════════════════════════════════════════════════════════════════════
# TAB 4: Module C
# ════════════════════════════════════════════════════════════════════

with tab_c:
    st.subheader("Module C — 선발 로테이션 최적화 (ILP)")
    st.caption("대상: 한화 이글스 (7002) | 2025년 5~6월 46경기 | 방법론 검증용 완료 시즌 사용")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("감독 P(win) 합", f"{MODULE_C_SUMMARY['actual_score']:.2f}", delta="기준")
    with c2: st.metric("ILP P(win) 합",  f"{MODULE_C_SUMMARY['ilp_score']:.2f}",
                       delta=f"+{MODULE_C_SUMMARY['delta']:.2f}")
    with c3: st.metric("변경 경기",      f"{MODULE_C_SUMMARY['n_changed']}경기",
                       delta=f"/ {MODULE_C_SUMMARY['n_games']}경기 중")
    with c4: st.metric("최소휴식 위반",  f"{MODULE_C_SUMMARY['violations']}건",
                       delta="✅ 0건")

    st.markdown("---")

    with st.expander("▶ 최적화 제약식 4종"):
        st.markdown("""
- **C1**: 경기당 투수 1인 배정
- **C2**: 과부하 패널티 (등판 수 상한 초과 시 목적함수 감점)
- **C3**: 최소 휴식 4일 (더블헤더 gap=0 포함, v2 패치)
- **C4**: 정규시즌 등록 투수만 배정
- **목적함수**: ERA 기반 P(win) 합 최대화
""")

    col_f1, _ = st.columns([1, 3])
    with col_f1:
        month_filter = st.selectbox("월 필터", ["전체", "5월", "6월"])

    df_sched = build_schedule_df()
    if month_filter == "5월":
        df_show = df_sched[df_sched["날짜"].str.startswith("05")]
    elif month_filter == "6월":
        df_show = df_sched[df_sched["날짜"].str.startswith("06")]
    else:
        df_show = df_sched

    st.dataframe(df_show, width='stretch', hide_index=True, height=420)
    n_chg = len(df_show[df_show["변경"] == "★"])
    st.caption(f"표시: {len(df_show)}경기 | 변경: {n_chg}경기 (★)")

    st.markdown("**투수 범례**")
    st.dataframe(
        pd.DataFrame([{"p_no": k, "이름": v} for k, v in PITCHER_NAMES.items()]),
        hide_index=True, width='content',
    )

    with st.expander("▶ 패치 이력"):
        st.warning("C3 제약 gap=0 버그 수정 (2026-05-23): 더블헤더 휴식 위반 6건→0건. C3 제약 763→812개.")

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8rem'>"
    "KBO DSS · 홍익대학교 산업데이터공학과 · 지도교수: 김경도 · C321036 신상철"
    "</div>",
    unsafe_allow_html=True,
)
