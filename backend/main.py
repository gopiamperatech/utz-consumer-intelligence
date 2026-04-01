from __future__ import annotations

import os
from typing import Any, Optional

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import get_connection
from seed import seed

load_dotenv()

app = FastAPI(title="Utz Consumer Intent Intelligence API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://utz-consumer-intelligence.vercel.app",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    seed()


class CopilotRequest(BaseModel):
    question: str
    context_mode: str = "executive"


class CopilotResponse(BaseModel):
    answer: str
    source: str
    supporting_points: list[str]


COPILOT_FALLBACKS = {
    "struggling": {
        "answer": "Consumers are primarily struggling with product discovery and shelf availability. Florida and Texas show the highest concentration of where-to-buy and out-of-stock signals, especially for Cheese Balls, Party Mix, and Sour Cream & Onion.",
        "supporting_points": [
            "Top friction theme is product findability across Walmart, Target, and Publix.",
            "The largest unresolved clusters are in Florida and Texas.",
            "Store-locator confidence is materially lower than desired for high-intent products.",
            "Marketing and retail operations should coordinate around retailer-aware landing pages and availability alerts.",
        ],
    },
    "campaign": {
        "answer": "A high-ROI next move is a localized 'Find Your Utz Near You' campaign paired with family-snacking content. This addresses both where-to-buy friction and parent-led recommendation intent.",
        "supporting_points": [
            "Use retailer-specific landing pages for Walmart, Target, and Publix.",
            "Target Florida and Texas first because demand friction is highest there.",
            "Pair location content with lunchbox and family-choice messaging.",
            "Measure impact through store-locator CTR, retailer click-throughs, and repeat failed-discovery queries.",
        ],
    },
    "summary": {
        "answer": "Utz is not short on demand; it is missing moments of demand capture. Consumer conversations reveal measurable friction in product discovery, inventory visibility, and competitive positioning.",
        "supporting_points": [
            "Consumer intent is arriving before brand and retail teams can act on it.",
            "Unstructured language can be converted into a decision layer for marketing and sales.",
            "The most urgent commercial gap is product discoverability, not awareness.",
            "This prototype proves the operating model for a scaled pilot.",
        ],
    },
}


def rows_to_dicts(rows: list[Any]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]


def fetch_all(sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute(sql, params).fetchall()
    conn.close()
    return rows_to_dicts(rows)


def fetch_one(sql: str, params: tuple[Any, ...] = ()) -> Optional[dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    row = cur.execute(sql, params).fetchone()
    conn.close()
    return dict(row) if row else None


def build_summary() -> dict[str, Any]:
    total = fetch_one("SELECT COUNT(*) AS count FROM consumer_queries")
    where_to_buy = fetch_one("SELECT COUNT(*) AS count FROM consumer_queries WHERE intent = 'Where to Buy'")
    failed_discovery = fetch_one(
        "SELECT COUNT(*) AS count FROM consumer_queries WHERE intent IN ('Findability Failure', 'Out of Stock')"
    )
    high_priority = fetch_one("SELECT COUNT(*) AS count FROM consumer_queries WHERE priority = 'High'")
    negative = fetch_one("SELECT COUNT(*) AS count FROM consumer_queries WHERE sentiment = 'Negative'")

    total_count = max(total["count"], 1)

    return {
        "kpis": [
            {
                "title": "Where-to-buy queries",
                "value": f"{round((where_to_buy['count'] / total_count) * 100)}%",
                "delta": "+6.4%",
                "note": "Share of all consumer conversations",
            },
            {
                "title": "Failed discovery rate",
                "value": f"{round((failed_discovery['count'] / total_count) * 100)}%",
                "delta": "+2.1%",
                "note": "Consumers unable to locate intended product",
            },
            {
                "title": "High-priority conversations",
                "value": str(high_priority["count"]),
                "delta": "+9.7%",
                "note": "Needs routing to marketing or retail ops",
            },
            {
                "title": "Negative sentiment signals",
                "value": str(negative["count"]),
                "delta": "+4.9%",
                "note": "Commercial friction concentrated in availability and price questions",
            },
        ],
        "executive_pulse": {
            "top_friction_theme": "Product discovery failure",
            "affected_markets": ["Florida", "Texas", "Georgia"],
            "affected_products": ["Cheese Balls", "Party Mix", "Sour Cream & Onion"],
            "immediate_action": "Fix store-locator journeys and trigger retail availability alerts.",
        },
    }


async def maybe_call_llm(question: str, summary_context: dict[str, Any]) -> Optional[CopilotResponse]:
    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    azure_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")

    openai_key = os.getenv("OPENAI_API_KEY")
    openai_model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    openai_base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    prompt = (
        "You are a consumer-intelligence copilot for a CPG executive. "
        "Answer crisply in 1 short paragraph and 4 bullet points. "
        f"Question: {question}\n"
        f"Context: {summary_context}"
    )

    if azure_key and azure_endpoint and azure_deployment:
        url = f"{azure_endpoint.rstrip('/')}/openai/deployments/{azure_deployment}/chat/completions?api-version={azure_version}"
        headers = {"api-key": azure_key, "Content-Type": "application/json"}
        payload = {
            "messages": [
                {"role": "system", "content": "You are an executive marketing analytics copilot."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        }
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code >= 400:
                raise HTTPException(status_code=500, detail=f"Azure OpenAI error: {resp.text}")
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            parts = [p.strip("- ") for p in content.split("\n") if p.strip()]
            return CopilotResponse(answer=parts[0], source="azure_openai", supporting_points=parts[1:5])

    if openai_key:
        url = f"{openai_base.rstrip('/')}/chat/completions"
        headers = {"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"}
        payload = {
            "model": openai_model,
            "messages": [
                {"role": "system", "content": "You are an executive marketing analytics copilot."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        }
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code >= 400:
                raise HTTPException(status_code=500, detail=f"OpenAI error: {resp.text}")
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            parts = [p.strip("- ") for p in content.split("\n") if p.strip()]
            return CopilotResponse(answer=parts[0], source="openai", supporting_points=parts[1:5])

    return None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/queries")
def get_queries(search: str = "", channel: str = "all") -> dict[str, Any]:
    sql = "SELECT * FROM consumer_queries WHERE 1=1"
    params: list[Any] = []

    if search:
        sql += " AND (LOWER(text) LIKE ? OR LOWER(intent) LIKE ? OR LOWER(product) LIKE ? OR LOWER(location) LIKE ?)"
        search_like = f"%{search.lower()}%"
        params.extend([search_like, search_like, search_like, search_like])

    if channel != "all":
        sql += " AND channel = ?"
        params.append(channel)

    sql += " ORDER BY datetime(created_at) DESC"
    rows = fetch_all(sql, tuple(params))
    return {"items": rows, "count": len(rows)}


@app.get("/insights/summary")
def get_summary() -> dict[str, Any]:
    return build_summary()


@app.get("/insights/gaps")
def get_gaps() -> dict[str, Any]:
    gaps = fetch_all(
        "SELECT region, signal_volume AS gap, opportunity_score AS opportunity, cluster_name, notes FROM insight_clusters ORDER BY signal_volume DESC"
    )

    trend = [
        {"day": "Mon", "findability": 48, "outOfStock": 28},
        {"day": "Tue", "findability": 52, "outOfStock": 31},
        {"day": "Wed", "findability": 57, "outOfStock": 36},
        {"day": "Thu", "findability": 61, "outOfStock": 42},
        {"day": "Fri", "findability": 66, "outOfStock": 46},
        {"day": "Sat", "findability": 71, "outOfStock": 52},
        {"day": "Sun", "findability": 69, "outOfStock": 49},
    ]

    intents = fetch_all(
        "SELECT intent AS name, COUNT(*) AS value FROM consumer_queries GROUP BY intent ORDER BY value DESC"
    )
    return {"gaps": gaps, "trend": trend, "intent_distribution": intents}


@app.get("/actions/recommendations")
def get_actions() -> dict[str, Any]:
    rows = fetch_all("SELECT * FROM recommended_actions ORDER BY CASE impact WHEN 'High' THEN 1 ELSE 2 END, id")
    return {"items": rows}


@app.get("/products")
def get_products() -> dict[str, Any]:
    return {"items": fetch_all("SELECT * FROM products ORDER BY product_name")}


@app.get("/retailers/availability")
def get_retailer_availability(state: Optional[str] = Query(default=None)) -> dict[str, Any]:
    if state:
        rows = fetch_all(
            "SELECT * FROM retailer_availability WHERE state = ? ORDER BY in_stock_score ASC",
            (state,),
        )
    else:
        rows = fetch_all("SELECT * FROM retailer_availability ORDER BY in_stock_score ASC")
    return {"items": rows}


@app.post("/copilot/ask", response_model=CopilotResponse)
async def ask_copilot(payload: CopilotRequest) -> CopilotResponse:
    question = payload.question.lower()
    summary_context = {
        "summary": build_summary(),
        "gaps": fetch_all("SELECT cluster_name, region, signal_volume, opportunity_score FROM insight_clusters"),
        "actions": fetch_all("SELECT pattern, action, owner, impact FROM recommended_actions"),
    }

    llm_response = await maybe_call_llm(payload.question, summary_context)
    if llm_response:
        return llm_response

    fallback_key = "summary"
    if "struggling" in question or "problem" in question or "issue" in question:
        fallback_key = "struggling"
    elif "campaign" in question or "launch" in question or "promot" in question:
        fallback_key = "campaign"

    fallback = COPILOT_FALLBACKS[fallback_key]
    return CopilotResponse(answer=fallback["answer"], source="rules", supporting_points=fallback["supporting_points"])


# Optional future extension for FAISS/vector retrieval:
# 1. Generate embeddings for reviews / FAQs / campaign notes.
# 2. Store vectors in FAISS index on disk.
# 3. Add /search/semantic endpoint to retrieve relevant text chunks.
# 4. Feed retrieved chunks into /copilot/ask for grounded responses.
