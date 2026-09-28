import streamlit as st
from db import init_db, load_cases, insert_case, next_patient_id
from demo_seed import seed_demo
from similarity import retrieve, revise_summary

st.set_page_config(
    page_title="ScolioCBR | Clinical Decision Support",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
:root {
  --bg: #f6f8fc;
  --card: #ffffff;
  --text: #102033;
  --muted: #66758a;
  --primary: #2f6fed;
  --primary2: #6b8cff;
  --accent: #8b5cf6;
  --border: #e7ebf2;
}

.stApp {
  background:
    radial-gradient(circle at 12% 0%, rgba(47,111,237,.08), transparent 30%),
    radial-gradient(circle at 92% 4%, rgba(139,92,246,.07), transparent 28%),
    var(--bg);
  color: var(--text);
}

.block-container {
  padding-top: 1.3rem;
  padding-bottom: 2.5rem;
  max-width: 1450px;
}

section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
  border-right: 1px solid rgba(255,255,255,.06);
}
section[data-testid="stSidebar"] * { color: #eef2ff !important; }

.hero {
  background: linear-gradient(135deg, #2f6fed 0%, #5e6df4 54%, #8b5cf6 100%);
  color: white;
  border-radius: 24px;
  padding: 2rem 2.2rem;
  margin-bottom: 1.35rem;
  box-shadow: 0 18px 50px rgba(63,73,220,.20);
  position: relative;
  overflow: hidden;
}
.hero:after {
  content: "";
  position: absolute;
  width: 260px; height: 260px;
  right: -70px; top: -95px;
  border-radius: 50%;
  background: rgba(255,255,255,.10);
}
.hero h1 { margin: 0; color: white; font-size: 2.15rem; letter-spacing: -.02em; }
.hero p { margin: .5rem 0 0; color: rgba(255,255,255,.9); font-size: 1rem; }
.badge {
  display: inline-block;
  padding: .28rem .58rem;
  border-radius: 999px;
  font-size: .76rem;
  font-weight: 800;
  background: rgba(255,255,255,.16);
  margin-bottom: .7rem;
}

.flow {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: .8rem;
  margin: .9rem 0 1.35rem;
}
.flow-step {
  background: rgba(255,255,255,.96);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1rem 1.05rem;
  box-shadow: 0 8px 24px rgba(15,23,42,.04);
}
.flow-step strong { display:block; color: var(--primary); margin-bottom: .18rem; }
.flow-step span { color: var(--muted); font-size: .84rem; }

.section-card {
  background: rgba(255,255,255,.96);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 1.15rem 1.2rem;
  box-shadow: 0 8px 24px rgba(15,23,42,.04);
  margin-bottom: 1rem;
}
.section-title { font-size: 1.07rem; font-weight: 850; color: var(--text); }
.section-subtitle { color: var(--muted); font-size: .88rem; margin: .15rem 0 .7rem; }

.note {
  background: #fff8e8;
  border: 1px solid #fde7b0;
  border-radius: 14px;
  padding: .9rem 1rem;
  color: #8a5a00;
}
.success-box {
  background: #effcf4;
  border: 1px solid #bfe9cd;
  color: #166534;
  border-radius: 14px;
  padding: .95rem 1rem;
}

[data-testid="stMetric"] {
  background: rgba(255,255,255,.96);
  border: 1px solid var(--border);
  padding: 1rem 1.1rem;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(15,23,42,.04);
}
[data-testid="stDataFrame"] {
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
  background: white;
  box-shadow: 0 8px 24px rgba(15,23,42,.04);
}
.stButton > button {
  border: 0;
  border-radius: 12px;
  padding: .65rem 1rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary), var(--primary2));
  color: white;
  box-shadow: 0 8px 20px rgba(47,111,237,.18);
}
.stButton > button:hover { transform: translateY(-1px); }
.stDownloadButton > button { border-radius: 12px; }

@media (max-width: 900px) {
  .flow { grid-template-columns: 1fr 1fr; }
}
</style>
""",
    unsafe_allow_html=True,
)


def hero():
    st.markdown(
        """
        <div class="hero">
          <div class="badge">CBR · Clinical Decision Support Prototype</div>
          <h1>ScolioCBR</h1>
          <p>基于相似病例检索、成功治疗复用、差异微调与病例留存的临床决策支持原型</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section(title, subtitle=""):
    st.markdown(
        f'<div class="section-title">{title}</div>'
        f'<div class="section-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )


init_db()
seed_demo(486)
cases = load_cases()

with st.sidebar:
    st.markdown("## 🧬 ScolioCBR")
    st.caption("Case-Based Reasoning System")
    st.markdown("---")
    page = st.radio(
        "系统导航",
        ["总览", "病例库", "新患者检索", "成功病例与微调", "Retain 新病例"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Research prototype · Demo data")

hero()

if page == "总览":
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("病例库规模", len(cases))
    c2.metric("CBR 阶段", "4")
    c3.metric("当前特征数", "5")
    success_rate = cases["successful_outcome"].mean() * 100 if len(cases) else 0
    c4.metric("成功病例占比", f"{success_rate:.1f}%")

    st.markdown(
        """
        <div class="flow">
          <div class="flow-step"><strong>01 Retrieve</strong><span>检索最相似历史病例</span></div>
          <div class="flow-step"><strong>02 Reuse</strong><span>提取成功病例历史方案</span></div>
          <div class="flow-step"><strong>03 Revise</strong><span>识别差异并提示人工微调</span></div>
          <div class="flow-step"><strong>04 Retain</strong><span>把新经验写回病例库</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.15, .85])
    with left:
        section("系统用途", "用于展示 CBR 临床决策支持完整闭环")
        st.markdown(
            """
            <div class="section-card">
              <b>输入</b>：新患者的临床特征<br><br>
              <b>系统处理</b>：局部相似度 → 加权总体相似度 → Top-K 检索 → 成功病例筛选 → 微调优先级<br><br>
              <b>输出</b>：相似病例、历史成功治疗方案、需要重点复核的属性
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        section("研究说明", "当前版本为教学 / 科研原型")
        st.markdown(
            """
            <div class="note">
              当前病例与治疗结果为模拟数据，相似度规则为教学版规则。
              本系统用于算法复现与科研汇报，不可直接用于真实临床诊疗。
            </div>
            """,
            unsafe_allow_html=True,
        )

elif page == "病例库":
    section("病例库", "浏览当前历史病例及其治疗结局")
    c1, c2, c3 = st.columns(3)
    c1.metric("总病例数", len(cases))
    c2.metric("成功病例", int(cases["successful_outcome"].sum()))
    c3.metric("未成功病例", int((~cases["successful_outcome"]).sum()))

    search = st.text_input("🔎 搜索 Patient ID", placeholder="例如：Patient_24")
    view = cases.copy()
    if search.strip():
        view = view[view["patient"].str.contains(search.strip(), case=False, na=False)]

    st.dataframe(view, use_container_width=True, height=540)
    st.download_button(
        "导出病例库 CSV",
        cases.to_csv(index=False).encode("utf-8-sig"),
        "cbr_casebase.csv",
        "text/csv",
    )

elif page == "新患者检索":
    section("新患者检索", "录入 Query Patient 特征并检索 Top-K 相似病例")

    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            mental = st.number_input("Mental distress", 1.0, 3.0, 1.7, 0.1)
            expectations = st.slider("Expectations", 0, 10, 6)
        with c2:
            pain_sites = st.slider("Pain sites", 1, 6, 3)
            sleep = st.selectbox("Sleep", ["Great", "Normal", "Slight", "Moderate"])
        with c3:
            workability = st.slider("Workability", 0, 10, 2)
            top_k = st.slider("Top K", 5, 20, 10)

        query = {
            "mental_distress": mental,
            "expectations": expectations,
            "pain_sites": pain_sites,
            "sleep": sleep,
            "workability": workability,
        }

        run = st.button("🔍 Find Similar Cases", type="primary", use_container_width=True)

    if run:
        st.session_state["query"] = query
        st.session_state["retrieval"] = retrieve(query, cases, top_k=top_k)

    if "retrieval" in st.session_state:
        result = st.session_state["retrieval"]
        top = result.iloc[0]

        st.markdown("### 检索结果")
        c1, c2, c3 = st.columns(3)
        c1.metric("最相似病例", top["patient"])
        c2.metric("最高相似度", f"{top['similarity']:.3f}")
        c3.metric("返回病例数", len(result))

        st.dataframe(result, use_container_width=True)

        merged = result.merge(
            cases[[
                "patient", "treatment_plan", "successful_outcome",
                "pain_baseline", "pain_3m", "function_baseline", "function_3m",
                "mskhq_baseline", "mskhq_3m", "gpe",
            ]],
            on="patient",
            how="left",
        )
        with st.expander("查看相似病例的历史治疗与结局"):
            st.dataframe(merged, use_container_width=True)

elif page == "成功病例与微调":
    section("成功病例与微调", "筛选 successful cases，并形成 Reuse + Revise 决策支持")

    if "retrieval" not in st.session_state:
        st.info("请先到“新患者检索”页面运行一次 Query。")
    else:
        query = st.session_state["query"]
        result = st.session_state["retrieval"]
        merged = result.merge(
            cases[["patient", "treatment_plan", "successful_outcome"]],
            on="patient",
            how="left",
        )
        successful = merged[merged["successful_outcome"] == True].copy()

        if successful.empty:
            st.warning("当前 Top-K 中没有成功病例，可返回检索页增大 Top K。")
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("成功相似病例", len(successful))
            c2.metric("最高成功病例相似度", f"{successful['similarity'].max():.3f}")
            c3.metric("候选治疗方案数", successful["treatment_plan"].nunique())

            st.markdown("#### ① 相似 + 治疗成功病例")
            st.dataframe(successful, use_container_width=True)

            support = (
                successful.groupby("treatment_plan")
                .agg(
                    case_count=("patient", "count"),
                    total_similarity=("similarity", "sum"),
                    mean_similarity=("similarity", "mean"),
                )
                .reset_index()
                .sort_values("total_similarity", ascending=False)
            )
            st.markdown("#### ② 历史成功方案支持情况")
            st.dataframe(support, use_container_width=True)

            revise = revise_summary(query, successful, cases)
            st.markdown("#### ③ Revise 微调优先级")
            st.dataframe(revise, use_container_width=True)

            candidate = support.iloc[0]["treatment_plan"]
            high = revise[
                revise["review_action"] == "High priority review"
            ]["attribute"].tolist()
            st.session_state["candidate_treatment"] = candidate
            st.session_state["high_priority_review"] = high

            st.markdown(
                f"""
                <div class="success-box">
                  <b>候选历史方案</b>：{candidate}<br>
                  <b>高优先级复核属性</b>：{', '.join(high) if high else '无'}
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.caption("候选方案来自教学用模拟历史病例，不代表临床推荐。")

elif page == "Retain 新病例":
    section("Retain 新病例", "治疗结束后，把新患者经验写回案例库")

    if "query" not in st.session_state:
        st.info("请先完成一次新患者检索。")
    else:
        query = st.session_state["query"]
        candidate = st.session_state.get("candidate_treatment", "Multimodal physiotherapy")

        with st.expander("查看当前 Query 特征", expanded=True):
            st.json(query)

        c1, c2 = st.columns([.8, 1.2])
        with c1:
            patient_id = st.text_input("Patient ID", value=next_patient_id())
            treatment = st.text_input("最终采用的治疗方案", value=candidate)
            success = st.checkbox("Successful outcome", value=True)
        with c2:
            a, b = st.columns(2)
            with a:
                pain_b = st.number_input("Pain baseline", 0.0, 10.0, 4.5, 0.1)
                fun_b = st.number_input("Function baseline", 0.0, 10.0, 4.0, 0.1)
                m_b = st.number_input("MSK-HQ baseline", 0.0, 56.0, 24.0, 0.1)
            with b:
                pain_3m = st.number_input("Pain 3m", 0.0, 10.0, 2.0, 0.1)
                fun_3m = st.number_input("Function 3m", 0.0, 10.0, 6.0, 0.1)
                m_3m = st.number_input("MSK-HQ 3m", 0.0, 56.0, 32.0, 0.1)
            gpe = st.slider("GPE", 1, 7, 6)

        if st.button("💾 Retain / 保存到案例库", type="primary", use_container_width=True):
            insert_case({
                "patient": patient_id,
                **query,
                "treatment_plan": treatment,
                "pain_baseline": pain_b,
                "pain_3m": pain_3m,
                "function_baseline": fun_b,
                "function_3m": fun_3m,
                "mskhq_baseline": m_b,
                "mskhq_3m": m_3m,
                "gpe": gpe,
                "successful_outcome": success,
            })
            st.success(f"{patient_id} 已保存到病例库。")
