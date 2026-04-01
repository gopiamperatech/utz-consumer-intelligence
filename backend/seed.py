from __future__ import annotations

from datetime import datetime, timedelta

from database import bulk_insert, init_db


def seed() -> None:
    init_db()

    now = datetime(2026, 3, 31, 9, 0, 0)
    consumer_queries = [
        {
            "id": 1,
            "text": "Where can I find Utz Cheese Balls near Orlando?",
            "channel": "Website Search",
            "location": "Orlando, FL",
            "state": "Florida",
            "intent": "Where to Buy",
            "product": "Cheese Balls",
            "retailer": "Walmart",
            "sentiment": "Neutral",
            "priority": "High",
            "timestamp_label": "5 mins ago",
            "created_at": (now - timedelta(minutes=5)).isoformat(),
            "resolved": 0,
        },
        {
            "id": 2,
            "text": "Are Utz Original Chips gluten free?",
            "channel": "Chatbot",
            "location": "Atlanta, GA",
            "state": "Georgia",
            "intent": "Product Info",
            "product": "Original Potato Chips",
            "retailer": "Direct",
            "sentiment": "Positive",
            "priority": "Medium",
            "timestamp_label": "9 mins ago",
            "created_at": (now - timedelta(minutes=9)).isoformat(),
            "resolved": 1,
        },
        {
            "id": 3,
            "text": "Your sour cream flavor is missing from my Target again",
            "channel": "Review",
            "location": "Dallas, TX",
            "state": "Texas",
            "intent": "Out of Stock",
            "product": "Sour Cream & Onion",
            "retailer": "Target",
            "sentiment": "Negative",
            "priority": "High",
            "timestamp_label": "12 mins ago",
            "created_at": (now - timedelta(minutes=12)).isoformat(),
            "resolved": 0,
        },
        {
            "id": 4,
            "text": "Which Utz snack is healthier for kids lunch?",
            "channel": "Social",
            "location": "Charlotte, NC",
            "state": "North Carolina",
            "intent": "Recommendation",
            "product": "Mixed Portfolio",
            "retailer": "General",
            "sentiment": "Neutral",
            "priority": "Medium",
            "timestamp_label": "18 mins ago",
            "created_at": (now - timedelta(minutes=18)).isoformat(),
            "resolved": 1,
        },
        {
            "id": 5,
            "text": "Why is Utz more expensive than Lay's at Kroger?",
            "channel": "Social",
            "location": "Nashville, TN",
            "state": "Tennessee",
            "intent": "Price Compare",
            "product": "Classic Chips",
            "retailer": "Kroger",
            "sentiment": "Negative",
            "priority": "High",
            "timestamp_label": "24 mins ago",
            "created_at": (now - timedelta(minutes=24)).isoformat(),
            "resolved": 0,
        },
        {
            "id": 6,
            "text": "Looking for Utz party mix bulk pack near me",
            "channel": "Website Search",
            "location": "Tampa, FL",
            "state": "Florida",
            "intent": "Where to Buy",
            "product": "Party Mix",
            "retailer": "Publix",
            "sentiment": "Positive",
            "priority": "Medium",
            "timestamp_label": "29 mins ago",
            "created_at": (now - timedelta(minutes=29)).isoformat(),
            "resolved": 1,
        },
        {
            "id": 7,
            "text": "Do you have a spicy version similar to Doritos?",
            "channel": "Chatbot",
            "location": "Phoenix, AZ",
            "state": "Arizona",
            "intent": "Competitor Compare",
            "product": "Portfolio Discovery",
            "retailer": "General",
            "sentiment": "Neutral",
            "priority": "Low",
            "timestamp_label": "35 mins ago",
            "created_at": (now - timedelta(minutes=35)).isoformat(),
            "resolved": 1,
        },
        {
            "id": 8,
            "text": "Store locator shows product but shelf was empty",
            "channel": "Contact Center",
            "location": "Houston, TX",
            "state": "Texas",
            "intent": "Findability Failure",
            "product": "Cheddar Popcorn",
            "retailer": "Walmart",
            "sentiment": "Negative",
            "priority": "High",
            "timestamp_label": "42 mins ago",
            "created_at": (now - timedelta(minutes=42)).isoformat(),
            "resolved": 0,
        },
        {
            "id": 9,
            "text": "Why can't I find the family size bag in Miami?",
            "channel": "Website Search",
            "location": "Miami, FL",
            "state": "Florida",
            "intent": "Where to Buy",
            "product": "Family Size Potato Chips",
            "retailer": "Target",
            "sentiment": "Negative",
            "priority": "High",
            "timestamp_label": "50 mins ago",
            "created_at": (now - timedelta(minutes=50)).isoformat(),
            "resolved": 0,
        },
        {
            "id": 10,
            "text": "Are there coupons for Utz at Walmart this week?",
            "channel": "Chatbot",
            "location": "Jacksonville, FL",
            "state": "Florida",
            "intent": "Promotion",
            "product": "Mixed Portfolio",
            "retailer": "Walmart",
            "sentiment": "Positive",
            "priority": "Low",
            "timestamp_label": "55 mins ago",
            "created_at": (now - timedelta(minutes=55)).isoformat(),
            "resolved": 1,
        },
        {
            "id": 11,
            "text": "My Walmart app says in stock but store had none",
            "channel": "Review",
            "location": "San Antonio, TX",
            "state": "Texas",
            "intent": "Findability Failure",
            "product": "Cheese Balls",
            "retailer": "Walmart",
            "sentiment": "Negative",
            "priority": "High",
            "timestamp_label": "1 hr ago",
            "created_at": (now - timedelta(hours=1)).isoformat(),
            "resolved": 0,
        },
        {
            "id": 12,
            "text": "Best Utz snack for school lunch boxes?",
            "channel": "Social",
            "location": "Raleigh, NC",
            "state": "North Carolina",
            "intent": "Recommendation",
            "product": "Mixed Portfolio",
            "retailer": "General",
            "sentiment": "Positive",
            "priority": "Medium",
            "timestamp_label": "1 hr ago",
            "created_at": (now - timedelta(hours=1, minutes=4)).isoformat(),
            "resolved": 1,
        },
    ]

    products = [
        {"id": 1, "sku": "UTZ-CB-001", "product_name": "Cheese Balls", "category": "Snacks", "pack_type": "Canister", "health_positioning": "Indulgent", "core_region": "Southeast"},
        {"id": 2, "sku": "UTZ-SCO-002", "product_name": "Sour Cream & Onion", "category": "Potato Chips", "pack_type": "Bag", "health_positioning": "Classic", "core_region": "South"},
        {"id": 3, "sku": "UTZ-PM-003", "product_name": "Party Mix", "category": "Snacks", "pack_type": "Bag", "health_positioning": "Sharing", "core_region": "Southeast"},
        {"id": 4, "sku": "UTZ-CP-004", "product_name": "Cheddar Popcorn", "category": "Popcorn", "pack_type": "Bag", "health_positioning": "Family", "core_region": "South"},
        {"id": 5, "sku": "UTZ-OPC-005", "product_name": "Original Potato Chips", "category": "Potato Chips", "pack_type": "Bag", "health_positioning": "Classic", "core_region": "National"},
        {"id": 6, "sku": "UTZ-FAM-006", "product_name": "Family Size Potato Chips", "category": "Potato Chips", "pack_type": "Bag", "health_positioning": "Value", "core_region": "South"},
    ]

    retailer_availability = [
        {"id": 1, "retailer": "Walmart", "state": "Florida", "product_name": "Cheese Balls", "in_stock_score": 0.61, "store_locator_accuracy": 0.72, "promo_flag": 1},
        {"id": 2, "retailer": "Publix", "state": "Florida", "product_name": "Party Mix", "in_stock_score": 0.79, "store_locator_accuracy": 0.85, "promo_flag": 0},
        {"id": 3, "retailer": "Target", "state": "Texas", "product_name": "Sour Cream & Onion", "in_stock_score": 0.52, "store_locator_accuracy": 0.66, "promo_flag": 0},
        {"id": 4, "retailer": "Walmart", "state": "Texas", "product_name": "Cheddar Popcorn", "in_stock_score": 0.48, "store_locator_accuracy": 0.58, "promo_flag": 1},
        {"id": 5, "retailer": "Kroger", "state": "Tennessee", "product_name": "Classic Chips", "in_stock_score": 0.84, "store_locator_accuracy": 0.88, "promo_flag": 1},
        {"id": 6, "retailer": "Target", "state": "Florida", "product_name": "Family Size Potato Chips", "in_stock_score": 0.57, "store_locator_accuracy": 0.68, "promo_flag": 0},
    ]

    clusters = [
        {"id": 1, "cluster_name": "Where-to-buy friction", "region": "Florida", "signal_volume": 82, "opportunity_score": 68, "notes": "High store-locator usage and failed discovery in Orlando, Tampa, Miami"},
        {"id": 2, "cluster_name": "Out-of-stock escalation", "region": "Texas", "signal_volume": 76, "opportunity_score": 61, "notes": "Retail shelf mismatch across Walmart and Target"},
        {"id": 3, "cluster_name": "Product education", "region": "Georgia", "signal_volume": 49, "opportunity_score": 45, "notes": "Gluten-free and product attribute questions"},
        {"id": 4, "cluster_name": "Family-snacking recommendations", "region": "North Carolina", "signal_volume": 41, "opportunity_score": 39, "notes": "Health and lunchbox-related parent intent"},
        {"id": 5, "cluster_name": "Competitive value comparisons", "region": "Tennessee", "signal_volume": 34, "opportunity_score": 31, "notes": "Lay's comparisons concentrated in Kroger discussions"},
    ]

    actions = [
        {"id": 1, "pattern": "Where-to-buy intent rising in Florida", "evidence": "27% week-over-week increase in store lookup behavior", "action": "Promote store locator and retailer-specific landing pages", "owner": "Brand + Digital", "impact": "High", "metric": "Store locator CTR"},
        {"id": 2, "pattern": "Cheese Balls out-of-stock mentions in Texas", "evidence": "41 unresolved mentions across Target and Walmart", "action": "Retail alert and shelf-availability escalation", "owner": "Sales + Retail Ops", "impact": "High", "metric": "Out-of-stock reduction"},
        {"id": 3, "pattern": "Healthy-snack questions among parents", "evidence": "Kids lunch / better-for-you themes up 18%", "action": "Launch content bundle around family snack choices", "owner": "Content + Campaigns", "impact": "Medium", "metric": "Engagement rate"},
        {"id": 4, "pattern": "Price comparison vs Lay's at Kroger", "evidence": "Negative sentiment concentrated in value-seeking shoppers", "action": "Refresh messaging around value, size, and promo positioning", "owner": "Brand + Trade Marketing", "impact": "Medium", "metric": "Promo response lift"},
    ]

    bulk_insert("consumer_queries", consumer_queries)
    bulk_insert("products", products)
    bulk_insert("retailer_availability", retailer_availability)
    bulk_insert("insight_clusters", clusters)
    bulk_insert("recommended_actions", actions)


if __name__ == "__main__":
    seed()
