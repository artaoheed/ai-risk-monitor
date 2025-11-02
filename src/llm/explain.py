from __future__ import annotations
import os
from typing import Dict
from .prompts import BASE_EXPLANATION

def local_explainer(features: Dict) -> str:
    # Simple heuristic message without external API calls.
    risk = features.get("risk_score", 0)
    parts = []
    if features.get("device_change_7d", 0) == 1:
        parts.append("a recent device change")
    if features.get("is_night", 0) == 1:
        parts.append("the late-night timing")
    if features.get("amount", 0) > 1000:
        parts.append("an unusually high amount for this pattern")
    because = ", ".join(parts) if parts else "a pattern that differs from recent activity"
    return (
        f"This transfer looks a bit unusual due to {because}. "
        f"Your risk score for this item is {risk:.0f}/100. "
        "You can review the details or mark it as OK to improve future checks."
    )

def explain(features: Dict) -> str:
    provider = os.getenv("LLM_PROVIDER", "LOCAL").upper()
    if provider == "LOCAL":
        return local_explainer(features)
    # Stubs for providers; user can plug their own client
    if provider == "OPENAI":
        # from openai import OpenAI
        # client = OpenAI()
        # prompt = BASE_EXPLANATION.format(**features)
        # resp = client.chat.completions.create(model="gpt-4o-mini", messages=[
        #     {{ "role":"user", "content": prompt }}
        # ])
        # return resp.choices[0].message.content.strip()
        return local_explainer(features)
    return local_explainer(features)
