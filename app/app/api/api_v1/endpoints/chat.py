from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.chat import ChatRequest
from app.schemas.product import ProductFilterRequest
from app.models import Product, AttributeMaster, AttributeValue, Category
from app.api.api_v1.endpoints.product import filter_products
import httpx
import re

router = APIRouter()

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-70b-8192"

# Entry point for chatbot search
@router.post("/chatbot/search/")
async def chatbot_search(query: ChatRequest, db: Session = Depends(get_db)):
    try:
        raw_message = query.message.strip().lower()
        filters = extract_filters_from_query(raw_message)

        # Internal search
        internal_results = filter_products(filters=filters, db=db)
        if internal_results:
            return {
                "source": "internal",
                "products": internal_results
            }

        # External AI fallback
        ai_reply = await query_groq_llama(raw_message)
        links = await get_certified_links_from_ai_reply(ai_reply)

        return {
            "source": "external",
            "message": "No matching products found internally. Here's what AI suggests:",
            "ai_response": ai_reply,
            "links": links
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

# ----------------------------------
# 🔍 Extract filters from user query
# ----------------------------------
def extract_filters_from_query(text: str) -> ProductFilterRequest:
    # Attribute map
    attribute_keywords = {
        "leather": ("Strap_Type", "Leather"),
        "metal": ("Strap_Type", "Metal"),
        "steel": ("Case_Material", "Steel"),
        "white": ("Dial_Color", "White"),
        "black": ("Dial_Color", "Black"),
        "gold": ("Case_Material", "Gold"),
    }

    attributes = {}
    for word, (attr, value) in attribute_keywords.items():
        if word in text:
            attributes.setdefault(attr, []).append(value)

    # Price range extraction
    price_match = re.search(r"(under|below)\s*(\d+)", text)
    max_price = int(price_match.group(2)) if price_match else None

    price_match = re.search(r"(above|over|greater than)\s*(\d+)", text)
    min_price = int(price_match.group(2)) if price_match else None

    # Extract primary keyword (first useful word)
    stopwords = {"give", "me", "show", "find", "the", "a", "an", "please", "suggestion", "suggestions", "related", "to"}
    words = re.findall(r"\w+", text)
    keywords = [word for word in words if word not in stopwords]
    keyword = keywords[0] if keywords else None

    return ProductFilterRequest(
        name=keyword,
        attributes=attributes,
        min_price=min_price,
        max_price=max_price
    )

# -----------------------------
# 🤖 Query Groq LLaMA Model
# -----------------------------
async def query_groq_llama(message: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a watch expert. Recommend certified buying links for the best watches matching the user's query."},
            {"role": "user", "content": message}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

# -----------------------------------------------------
# 🌐 Parse External Reply & Extract Certified Links
# -----------------------------------------------------
async def get_certified_links_from_ai_reply(reply: str) -> list:
    # Simple regex to grab URLs (https links only)
    urls = re.findall(r"https?://\S+", reply)
    # Filter certified links (could be more sophisticated)
    certified_domains = ["amazon", "flipkart", "watchstation", "certifiedluxurywatches"]
    certified_links = [url for url in urls if any(domain in url for domain in certified_domains)]
    return certified_links
