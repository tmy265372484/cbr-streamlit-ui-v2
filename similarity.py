from __future__ import annotations
import pandas as pd

WEIGHTS = {
    "mental_distress": 8,
    "expectations": 4,
    "pain_sites": 2,
    "sleep": 4,
    "workability": 4,
}

SLEEP_MATRIX = {
    "Great": {"Great": 1.0, "Slight": 0.8, "Moderate": 0.6, "Normal": 0.6},
    "Slight": {"Great": 0.8, "Slight": 1.0, "Moderate": 0.8, "Normal": 0.6},
    "Moderate": {"Great": 0.6, "Slight": 0.8, "Moderate": 1.0, "Normal": 0.4},
    "Normal": {"Great": 0.6, "Slight": 0.6, "Moderate": 0.4, "Normal": 1.0},
}

def mental_distress_similarity(q, c):
    d = abs(float(q) - float(c))
    if d == 0: return 1.0
    if d <= 0.3: return 0.8
    if d <= 0.5: return 0.6
    if d <= 0.8: return 0.4
    return 0.2

def expectations_similarity(q, c):
    d = abs(float(q) - float(c))
    if d <= 1: return 1.0
    if d == 2: return 0.8
    if d == 3: return 0.6
    if d == 4: return 0.3
    return 0.1

def pain_sites_similarity(q, c):
    d = abs(float(q) - float(c))
    if d == 0: return 1.0
    if d == 1: return 0.8
    if d == 2: return 0.6
    return 0.4

def sleep_similarity(q, c):
    return float(SLEEP_MATRIX[str(q)][str(c)])

def workability_similarity(q, c):
    d = abs(float(q) - float(c))
    if d <= 1: return 1.0
    if d == 2: return 0.8
    if d == 3: return 0.6
    if d == 4: return 0.4
    return 0.2

def local_similarities(query, case):
    return {
        "mental_distress": mental_distress_similarity(query["mental_distress"], case["mental_distress"]),
        "expectations": expectations_similarity(query["expectations"], case["expectations"]),
        "pain_sites": pain_sites_similarity(query["pain_sites"], case["pain_sites"]),
        "sleep": sleep_similarity(query["sleep"], case["sleep"]),
        "workability": workability_similarity(query["workability"], case["workability"]),
    }

def global_similarity(query, case):
    local = local_similarities(query, case)
    score = sum(local[k] * WEIGHTS[k] for k in WEIGHTS) / sum(WEIGHTS.values())
    return score, local

def retrieve(query, casebase, top_k=10):
    rows = []
    for _, r in casebase.iterrows():
        case = r.to_dict()
        score, local = global_similarity(query, case)
        rows.append({
            "patient": case["patient"],
            "similarity": score,
            **{f"{k}_sim": v for k, v in local.items()},
        })
    out = pd.DataFrame(rows).sort_values("similarity", ascending=False).reset_index(drop=True)
    out["rank"] = range(1, len(out) + 1)
    return out.head(top_k)

def revise_summary(query, successful_top, casebase):
    if successful_top.empty:
        return pd.DataFrame(columns=["attribute","review_count","mean_local_similarity","review_rate","revise_priority","review_action"])
    casebase_idx = casebase.set_index("patient")
    attrs = list(WEIGHTS.keys())
    rows = []
    for _, r in successful_top.iterrows():
        name = r["patient"]
        case = casebase_idx.loc[name].to_dict()
        local = local_similarities(query, case)
        for a in attrs:
            rows.append({"patient": name, "attribute": a, "local_similarity": local[a], "needs_review": local[a] < 1.0})
    df = pd.DataFrame(rows)
    s = df.groupby("attribute").agg(
        review_count=("needs_review","sum"),
        mean_local_similarity=("local_similarity","mean")
    ).reset_index()
    n = successful_top["patient"].nunique()
    s["review_rate"] = s["review_count"] / max(n,1)
    s["revise_priority"] = s["review_rate"] * (1 - s["mean_local_similarity"])
    def action(x):
        if x >= 0.15: return "High priority review"
        if x >= 0.05: return "Moderate priority review"
        return "Low priority review"
    s["review_action"] = s["revise_priority"].apply(action)
    return s.sort_values("revise_priority", ascending=False).reset_index(drop=True)
