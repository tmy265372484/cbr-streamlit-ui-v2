import numpy as np
from db import init_db, count_cases, insert_case

TREATMENTS = [
    "Exercise therapy",
    "Manual therapy + exercise",
    "Education + self-management",
    "Multimodal physiotherapy",
]

def _success_label(pain_b, pain_3m, fun_b, fun_3m, m_b, m_3m, gpe):
    checks = [
        (pain_b - pain_3m) >= 2,
        (fun_3m - fun_b) >= 1,
        (m_3m - m_b) >= 5,
        gpe >= 5,
    ]
    return sum(checks) >= 3

def seed_demo(n=486):
    init_db()
    if count_cases() > 0:
        return
    rng = np.random.default_rng(42)
    for i in range(1, n+1):
        mental = round(float(rng.uniform(1.0,3.0)),1)
        expectations = int(rng.integers(0,11))
        pain_sites = int(rng.integers(1,7))
        sleep = str(rng.choice(["Great","Normal","Slight","Moderate"]))
        workability = int(rng.integers(0,11))
        pain_b = float(np.clip(rng.normal(5,2),0,10))
        pain_3m = float(np.clip(pain_b-rng.normal(1.5,1.5),0,10))
        fun_b = float(np.clip(rng.normal(5,2),0,10))
        fun_3m = float(np.clip(fun_b+rng.normal(1.2,1.5),0,10))
        m_b = float(np.clip(28 + workability*1.5 + expectations*0.7 - mental*4 - pain_sites*1.3 + rng.normal(0,3),0,56))
        m_3m = float(np.clip(m_b+rng.normal(5,5),0,56))
        gpe = int(rng.integers(1,8))
        treatment = str(rng.choice(TREATMENTS))
        success = _success_label(pain_b,pain_3m,fun_b,fun_3m,m_b,m_3m,gpe)
        insert_case({
            "patient": f"Patient_{i}",
            "mental_distress": mental,
            "expectations": expectations,
            "pain_sites": pain_sites,
            "sleep": sleep,
            "workability": workability,
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
