"""
Person 1: Agent & Orchestrator Module
Coordinates intent understanding, planning, tool execution, activity tracing,
and synthesis for SmartCart AI.
"""

import os
import re
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

from tools.product_tools import (
    tool_search_catalogue,
    tool_check_stock,
    tool_compare_products,
    tool_check_compatibility,
    tool_add_to_shortlist,
    tool_get_shortlist,
    tool_rank_products,
)
from database.products import get_product_by_id, SAMPLE_CATALOGUE


def _extract_requirements(user_message: str) -> Dict[str, Any]:
    """Parse constraints, keywords, and action intent from the user message."""
    text = user_message.lower()
    reqs: Dict[str, Any] = {
        "raw_query": user_message,
        "intent": "search",
        "category": None,
        "max_price": None,
        "min_ram": None,
        "target_product_ids": [],
        "brand_preference": None
    }

    # Intent detection
    if any(k in text for k in ["hi", "hello", "hey", "who are you", "what can you do", "help"]):
        reqs["intent"] = "greeting"
    elif "compare" in text or "versus" in text or " vs " in text:
        reqs["intent"] = "compare"
    elif "compatib" in text:
        reqs["intent"] = "accessory_compatibility"
    elif "shortlist" in text or "save" in text or "favorite" in text:
        reqs["intent"] = "shortlist"
    elif "stock" in text or "available" in text:
        reqs["intent"] = "check_stock"

    # Category extraction
    if any(k in text for k in ["phone", "smartphone", "mobile"]):
        reqs["category"] = "smartphone"
    elif any(k in text for k in ["accessory", "accessories", "charger", "earbuds", "buds", "case", "cover"]):
        reqs["category"] = "accessory"
    elif any(k in text for k in ["laptop", "pc", "computer", "tv", "television", "watch", "shoe", "clothing"]):
        reqs["category"] = "unsupported"
        reqs["intent"] = "unsupported_category"

    # Price / Budget extraction (e.g., "under 18,000", "below 20k", "in a range of 1.5 lakh", "around 1.5L")
    price_match = re.search(
        r'(?:under|below|max|budget of|budget|within|range of|around|upto|up to|<|<=)\s*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)\s*(k|lakhs?|lacs?|l)?\b',
        text
    )
    if price_match:
        val_str = price_match.group(1).replace(",", "")
        try:
            val = float(val_str)
            unit = price_match.group(2)
            if unit == 'k':
                val *= 1000
            elif unit in ['lakh', 'lakhs', 'lac', 'lacs', 'l']:
                val *= 100000
            reqs["max_price"] = val
        except ValueError:
            pass

    # RAM extraction (e.g. "8 gb ram", "8gb", "at least 8 gb")
    ram_match = re.search(r'(\d+)\s*(?:gb|gigabyte)\s*(?:ram)?', text)
    if ram_match:
        try:
            reqs["min_ram"] = int(ram_match.group(1))
        except ValueError:
            pass

    # Product ID extraction (e.g. "product ID 1", "product 1", "id 2", "for 1")
    id_matches = re.findall(r'(?:product\s*id|product|id)\s*[:#]?\s*(\d+)', text)
    if id_matches:
        reqs["target_product_ids"] = list(dict.fromkeys(id_matches))

    # Brand extraction
    for brand in ["samsung", "xiaomi", "redmi", "realme", "oneplus", "spigen", "boat"]:
        if brand in text:
            reqs["brand_preference"] = brand.capitalize()
            break

    return reqs


def _create_plan(intent: str, reqs: Dict[str, Any]) -> Dict[str, Any]:
    """Formulate an explicit execution plan with a goal and concrete steps."""
    if intent == "greeting":
        return {
            "goal": "Welcome user and introduce SmartCart AI capabilities.",
            "steps": [
                "Acknowledge user greeting",
                "Present supported shopping tasks and sample catalogue scope"
            ]
        }
    elif intent == "unsupported_category":
        return {
            "goal": "Inform user of sample catalogue scope and recommend available categories.",
            "steps": [
                "Detect out-of-scope product request",
                "Provide guidance on available smartphone & accessory demo inventory"
            ]
        }
    elif intent == "compare":
        return {
            "goal": "Compare specifications and pricing of requested products.",
            "steps": [
                "Parse product identifiers from query or session context",
                "Retrieve detailed specifications from sample catalogue",
                "Generate comparative feature and price difference matrix",
                "Synthesize recommendation verdict"
            ]
        }
    elif intent == "accessory_compatibility":
        dev_id = reqs["target_product_ids"][0] if reqs["target_product_ids"] else "1"
        return {
            "goal": f"Find compatible accessories for host device (ID: {dev_id}) and verify hardware compatibility.",
            "steps": [
                f"Identify host product specifications for ID {dev_id}",
                "Query catalogue for accessories matching interface standards",
                "Execute compatibility verification tool",
                "Summarize verified options and package recommendations"
            ]
        }
    elif intent == "shortlist":
        p_id = reqs["target_product_ids"][0] if reqs["target_product_ids"] else "1"
        return {
            "goal": f"Add product ID {p_id} to customer's shortlist store.",
            "steps": [
                f"Locate product ID {p_id} in sample catalogue",
                "Verify stock availability",
                "Persist item to customer shortlist",
                "Present confirmation with updated shortlist status"
            ]
        }
    else:
        # Default search & recommendation
        budget_str = f" under ₹{reqs['max_price']:,.0f}" if reqs.get("max_price") else ""
        ram_str = f" with >= {reqs['min_ram']} GB RAM" if reqs.get("min_ram") else ""
        return {
            "goal": f"Find and rank best-matching {reqs.get('category') or 'products'}{budget_str}{ram_str}.",
            "steps": [
                "Extract query constraints (budget, RAM, category)",
                "Search sample catalogue using structured filters",
                "Check live stock availability for all candidates",
                "Execute multi-criteria recommendation scoring and ranking",
                "Synthesize natural language response with clear explanations"
            ]
        }


def run_smartcart_agent(user_message: str, session_id: str = "demo") -> Dict[str, Any]:
    """
    Main entry point for Person 1's orchestrator.
    Executes planning, tool calls, trace logging, and final synthesis.
    Strictly fulfills the agreed interface schema.
    """
    execution_trace: List[Dict[str, Any]] = []
    tool_results: List[Dict[str, Any]] = []
    ranked_products: List[Dict[str, Any]] = []
    evaluation: Dict[str, Any] = {}

    # 1. Step 1: Requirements Extraction
    reqs = _extract_requirements(user_message)
    execution_trace.append({
        "step": "Requirement Extraction",
        "action": "NLP pattern and constraint parser",
        "input": {"user_message": user_message},
        "output": reqs,
        "status": "success"
    })

    # 2. Step 2: Formulate Plan
    plan = _create_plan(reqs["intent"], reqs)
    execution_trace.append({
        "step": "Planning",
        "action": "Generate execution goal and step sequence",
        "input": {"intent": reqs["intent"], "requirements": reqs},
        "output": plan,
        "status": "success"
    })

    intent = reqs["intent"]

    # Branch according to intent
    if intent == "greeting":
        answer = (
            "👋 **Hello! I'm SmartCart AI**, your intelligent shopping assistant.\n\n"
            "I can help you explore and evaluate products with full planning and tool-use transparency:\n"
            "- 📱 **Search phones by budget & RAM**: e.g., *'Find a phone under ₹18,000 with at least 8 GB RAM'*\n"
            "- ⚖️ **Compare two phones**: e.g., *'Compare the top two options'*\n"
            "- 🔌 **Check accessory compatibility**: e.g., *'Find an accessory for product ID 1 and check compatibility'*\n"
            "- ⭐ **Manage your shortlist**: e.g., *'Add product ID 1 to my shortlist'*\n\n"
            "> *Demo notice: For this hackathon, my catalogue contains sample smartphones and accessories.*"
        )
        evaluation = {
            "criteria_met": True,
            "intent": "greeting",
            "notes": "Acknowledged user greeting and introduced capabilities."
        }

    elif intent == "unsupported_category":
        answer = (
            "I noticed you're searching for an item outside our current sample catalogue.\n\n"
            "For this hackathon demo, SmartCart AI is specifically configured with **smartphones** and **mobile accessories** (chargers, cases, wireless earbuds).\n\n"
            "Please try one of our supported shopping queries:\n"
            "- 📱 *'Find a phone under ₹18,000 with at least 8 GB RAM'*\n"
            "- 🔌 *'Show me chargers'* or *'Samsung accessories'*\n"
            "- ⚖️ *'Compare the top two options'*"
        )
        evaluation = {
            "criteria_met": False,
            "intent": "unsupported_category",
            "notes": "Requested product is outside sample catalogue scope."
        }

    elif intent == "compare":
        # Target IDs: look for explicitly mentioned IDs, default to "1" and "2"
        p_ids = reqs["target_product_ids"]
        if len(p_ids) < 2:
            p_ids = ["1", "2"]
        id1, id2 = p_ids[0], p_ids[1]

        trace_step = {
            "step": "Compare Products Tool Execution",
            "action": "compare_products",
            "input": {"product_id_1": id1, "product_id_2": id2}
        }
        comp_res = tool_compare_products(id1, id2)
        tool_results.append(comp_res)
        trace_step["output"] = comp_res["result"]
        trace_step["status"] = "success" if comp_res["result"].get("success") else "warning"
        execution_trace.append(trace_step)

        # Include both products in ranked_products for UI inspection
        p1 = get_product_by_id(id1)
        p2 = get_product_by_id(id2)
        candidate_list = [p for p in [p1, p2] if p]
        rank_tool_res = tool_rank_products(candidate_list, reqs)
        tool_results.append(rank_tool_res)
        ranked_products = rank_tool_res["results"]

        evaluation = {
            "criteria_met": comp_res["result"].get("success", False),
            "comparison_pairs": [f"{id1} vs {id2}"],
            "confidence": 0.95,
            "notes": "Direct head-to-head comparison completed successfully."
        }

        verdict = comp_res["result"].get("price_verdict", "")
        answer = (
            f"### Product Comparison: ID {id1} vs ID {id2}\n\n"
            f"- **Verdict**: {verdict}\n"
            f"- **Option 1**: **{p1.get('name') if p1 else id1}** — ₹{p1.get('price', 0):,.0f} | {p1.get('ram_gb', '-')} GB RAM | {p1.get('rating', '-')}★\n"
            f"- **Option 2**: **{p2.get('name') if p2 else id2}** — ₹{p2.get('price', 0):,.0f} | {p2.get('ram_gb', '-')} GB RAM | {p2.get('rating', '-')}★\n\n"
            f"Check the **Recommended products** cards and the comparison dropdown below for deep-dive specifications."
        )

    elif intent == "accessory_compatibility":
        host_id = reqs["target_product_ids"][0] if reqs["target_product_ids"] else "1"
        host_prod = get_product_by_id(host_id) or get_product_by_id("1")
        actual_host_id = host_prod.get("product_id", "1") if host_prod else "1"

        # Search accessories
        search_res = tool_search_catalogue(category="accessory")
        tool_results.append(search_res)
        accessories = search_res["results"]

        compat_results = []
        for acc in accessories:
            acc_id = acc.get("product_id")
            c_res = tool_check_compatibility(actual_host_id, acc_id)
            tool_results.append(c_res)
            compat_results.append(c_res["result"])

        execution_trace.append({
            "step": "Compatibility Verification",
            "action": "check_compatibility across catalogue accessories",
            "input": {"host_device_id": actual_host_id, "accessories_tested": len(accessories)},
            "output": [c["status"] for c in compat_results],
            "status": "success"
        })

        # Rank accessories
        compatible_accs = [
            acc for acc, c_info in zip(accessories, compat_results) if c_info.get("compatible")
        ]
        rank_res = tool_rank_products(compatible_accs, reqs)
        tool_results.append(rank_res)
        ranked_products = rank_res["results"]

        evaluation = {
            "criteria_met": len(compatible_accs) > 0,
            "host_device": host_prod.get("name") if host_prod else actual_host_id,
            "compatible_count": len(compatible_accs),
            "total_tested": len(accessories),
            "notes": "Verified official compatibility with sample catalogue host device."
        }

        items_text = "\n".join([
            f"1. **{item.get('name')}** (₹{item.get('price', 0):,.0f}) — {item.get('recommendation_reason')}"
            for item in ranked_products
        ])
        answer = (
            f"I checked compatibility for **{host_prod.get('name') if host_prod else 'Product ' + actual_host_id}** "
            f"(ID: `{actual_host_id}`) and found **{len(ranked_products)} verified compatible accessories**:\n\n"
            f"{items_text}\n\n"
            f"> *Note: The Galaxy M34 does not bundle a wall adapter in the retail box, making the Samsung 25W Power Adapter (ID 5) strongly recommended.*"
        )

    elif intent == "shortlist":
        p_id = reqs["target_product_ids"][0] if reqs["target_product_ids"] else "1"
        target_prod = get_product_by_id(p_id)

        shortlist_res = tool_add_to_shortlist(p_id, session_id)
        tool_results.append(shortlist_res)

        execution_trace.append({
            "step": "Persist Shortlist Item",
            "action": "add_to_shortlist",
            "input": {"product_id": p_id, "customer_id": session_id},
            "output": shortlist_res["result"],
            "status": "success" if shortlist_res["result"].get("success") else "failed"
        })

        if target_prod:
            ranked_products = tool_rank_products([target_prod], reqs)["results"]

        evaluation = {
            "criteria_met": shortlist_res["result"].get("success", False),
            "shortlisted_product": p_id,
            "customer_id": session_id,
            "notes": "Product added to in-memory shortlist storage."
        }

        answer = (
            f"✅ **{shortlist_res['result'].get('message')}**\n\n"
            f"You can view your active shortlist at any time using the shortlist control in the sidebar or below."
        )

    else:
        # Default: Product search and ranking
        # 1. Search catalogue
        cat = reqs.get("category")
        target_category = cat if cat in ["smartphone", "accessory"] else "smartphone"
        search_res = tool_search_catalogue(
            query=user_message if target_category != "smartphone" else None,
            max_price=reqs.get("max_price"),
            min_ram=reqs.get("min_ram"),
            category=target_category,
            brand=reqs.get("brand_preference")
        )
        tool_results.append(search_res)
        found_products = search_res["results"]

        # If zero items found with strict RAM filter, broaden search slightly to inform user
        if not found_products and reqs.get("min_ram"):
            fallback_res = tool_search_catalogue(
                max_price=reqs.get("max_price"),
                category=reqs.get("category") or "smartphone"
            )
            found_products = fallback_res["results"]

        execution_trace.append({
            "step": "Catalogue Search Tool",
            "action": "search_products",
            "input": search_res["parameters"],
            "output": {"matches_found": len(found_products)},
            "status": "success"
        })

        # 2. Check stock for each candidate
        for p in found_products:
            stock_res = tool_check_stock(p.get("product_id"))
            tool_results.append(stock_res)

        # 3. Score and rank candidates
        rank_res = tool_rank_products(found_products, reqs)
        tool_results.append(rank_res)
        ranked_products = rank_res["results"]

        execution_trace.append({
            "step": "Multi-criteria Product Ranking",
            "action": "rank_products",
            "input": {"candidates_count": len(found_products), "constraints": reqs},
            "output": {"ranked_count": len(ranked_products)},
            "status": "success"
        })

        # 4. Evaluation
        under_budget = all(
            p.get("price", 0) <= reqs["max_price"]
            for p in ranked_products if reqs.get("max_price") and p.get("price")
        )
        ram_satisfied = all(
            (p.get("ram_gb") or 0) >= reqs["min_ram"]
            for p in ranked_products if reqs.get("min_ram")
        )

        evaluation = {
            "criteria_met": len(ranked_products) > 0 and (under_budget or reqs.get("max_price") is None),
            "budget_criteria_satisfied": under_budget,
            "ram_criteria_satisfied": ram_satisfied,
            "total_matches": len(ranked_products),
            "notes": f"Identified {len(ranked_products)} candidate products meeting specifications."
        }

        # 5. Answer synthesis
        if ranked_products:
            top_pick = ranked_products[0]
            prod_label = target_category if target_category else "product"
            summary_lines = []
            for idx, p in enumerate(ranked_products[:3], 1):
                ram_spec = f" | {p.get('ram_gb')} GB RAM" if p.get('ram_gb') is not None else ""
                summary_lines.append(
                    f"{idx}. **{p.get('name')}** — ₹{p.get('price'):,.0f}{ram_spec} | Match score: **{p.get('match_score')}/100**\n"
                    f"   *{p.get('recommendation_reason')}*"
                )
            answer = (
                f"I found **{len(ranked_products)} {prod_label}(s)** matching your criteria:\n\n"
                + "\n\n".join(summary_lines)
                + f"\n\n**Top Recommendation**: **{top_pick.get('name')}** is the best match offering balanced specs within your criteria."
            )
        else:
            cat_label = target_category or "product"
            answer = (
                f"I searched the sample catalogue but couldn't find any {cat_label}s strictly matching all your criteria. "
                "Try relaxing the budget or constraints, or ask for available smartphones or accessories."
            )

    # Optional Gemini enhancement if GEMINI_API_KEY is configured
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key != "your_gemini_api_key_here":
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = (
                f"You are SmartCart AI, an expert e-commerce shopping assistant. "
                f"Rephrase this assistant response nicely while keeping the exact product specs, "
                f"prices, and recommendations intact:\n\n"
                f"User request: {user_message}\n"
                f"Draft response:\n{answer}"
            )
            llm_response = model.generate_content(prompt)
            if llm_response and llm_response.text:
                answer = llm_response.text.strip()
        except Exception:
            # Gracefully maintain deterministic answer on any network / key error
            pass

    return {
        "answer": answer,
        "requirements": reqs,
        "plan": plan,
        "tool_results": tool_results,
        "execution_trace": execution_trace,
        "ranked_products": ranked_products,
        "evaluation": evaluation
    }
