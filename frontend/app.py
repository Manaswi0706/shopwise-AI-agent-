"""
Frontend Module for SmartCart AI
Streamlit User Interface & Interactive Integration Dashboard
"""

import streamlit as st
import pandas as pd
from agent.orchestrator import run_smartcart_agent
from database.products import compare_products, add_to_shortlist, get_shortlist

st.set_page_config(
    page_title="SmartCart AI — Intelligent Shopping Assistant",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Sleek, Modern UI
CUSTOM_CSS = """
<style>
    /* Global font & smooth rendering */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hero Banner styling */
    .hero-container {
        padding: 1.5rem 1.8rem;
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.08) 0%, rgba(147, 51, 234, 0.06) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(8px);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(90deg, #60a5fa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-top: 0.35rem;
        margin-bottom: 0;
    }

    /* Product card highlights */
    div[data-testid="stMetricValue"] {
        font-weight: 700;
        font-size: 1.45rem !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #94a3b8 !important;
    }

    /* Pill Badges */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-blue { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
    .badge-green { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-purple { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
    .badge-amber { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }

    /* Trace timeline card */
    .trace-card {
        padding: 0.8rem 1rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        margin-bottom: 0.6rem;
    }

    /* Buttons polish */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def show_product(product, index):
    """Render a single product card in the recommendations section with rich styling."""
    name = product.get("name") or product.get("title") or f"Product {index + 1}"
    price = product.get("price")
    score = product.get("match_score")
    category = (product.get("category") or "product").capitalize()
    brand = product.get("brand")
    rating = product.get("rating")
    stock = product.get("stock")

    with st.container(border=True):
        col_header, col_score = st.columns([3, 1])
        with col_header:
            st.subheader(f"{index + 1}. {name}")
            badges_html = f'<span class="badge badge-blue">{category}</span>'
            if brand:
                badges_html += f'<span class="badge badge-purple">{brand}</span>'
            if rating:
                badges_html += f'<span class="badge badge-amber">★ {rating} / 5.0</span>'
            st.markdown(badges_html, unsafe_allow_html=True)

        with col_score:
            if score is not None:
                color = "#10b981" if score >= 85 else ("#3b82f6" if score >= 70 else "#f59e0b")
                st.markdown(
                    f"""
                    <div style="text-align: right; padding: 6px 12px; background: {color}15; border: 1px solid {color}40; border-radius: 10px;">
                        <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Match Score</div>
                        <div style="font-size: 1.45rem; font-weight: 700; color: {color}; line-height: 1.1;">{score}<span style="font-size: 0.85rem; color: #94a3b8; font-weight: normal;">/100</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Price", f"₹{price:,.0f}" if isinstance(price, (int, float)) else "Not listed")
        col2.metric("RAM", f"{product.get('ram_gb')} GB" if product.get('ram_gb') is not None else "Not listed")
        col3.metric("Match score", f"{score}/100" if score is not None else "Not scored")

        # Specific highlights if available
        specs = product.get("specs") or {}
        if specs:
            key_specs = []
            if "display" in specs:
                key_specs.append(f"📱 {specs['display']}")
            if "battery" in specs:
                key_specs.append(f"🔋 {specs['battery']}")
            if "processor" in specs:
                key_specs.append(f"⚡ {specs['processor']}")
            if "power_output" in specs:
                key_specs.append(f"⚡ {specs['power_output']}")
            if key_specs:
                st.caption(" • ".join(key_specs))

        st.write(f"💡 **Recommendation Rationale:** {product.get('recommendation_reason', 'Compare the available specifications.')}")
        st.caption(f"Sample catalogue item • ID: `{product.get('product_id', 'not provided')}` • Stock: {stock if stock is not None else 'Available'} units")


def main():
    # Hero Title Section
    st.markdown(
        """
        <div class="hero-container">
            <h1 class="hero-title">🛍️ SmartCart AI</h1>
            <p class="hero-subtitle">An intelligent shopping assistant that plans, uses tools, and explains its recommendations with full transparency.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.info("ℹ️ **Demo notice**: Catalogue and stock values are sample demo data for hackathon evaluation, not live marketplace inventory.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "last_result" not in st.session_state:
        st.session_state.last_result = None

    # Sidebar Controls & Quick Demos
    with st.sidebar:
        st.header("⚙️ Demo Controls")
        customer_id = st.text_input("Demo customer ID", value="demo-user")
        st.caption("🔒 Use sample data only. Do not enter payment or sensitive personal information.")

        if st.button("🗑️ Clear conversation", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.last_result = None
            st.rerun()

        st.divider()
        st.subheader("🚀 Quick Demo Prompts")
        st.caption("Click any preset prompt below to run it instantly:")

        quick_prompts = [
            ("📱 Phone < ₹18,000 & 8GB RAM", "Find a phone under ₹18,000 with at least 8 GB RAM"),
            ("⚖️ Compare top two options", "Compare the top two options"),
            ("🔌 Accessory & Compatibility", "Find an accessory for product ID 1 and check compatibility"),
            ("⭐ Shortlist Product ID 1", "Add product ID 1 to my shortlist"),
        ]

        active_quick_prompt = None
        for label, prompt_text in quick_prompts:
            if st.button(label, use_container_width=True):
                active_quick_prompt = prompt_text

        st.divider()
        st.markdown(
            """
            **Integrated Architecture:**
            * **P1**: Orchestrator & Trace
            * **P2**: Catalogue & Comparison DB
            * **P3**: Match Scorer & Compatibility
            * **P4**: Streamlit Dashboard & UI
            """
        )

    # Render previous conversation history
    for item in st.session_state.chat_history:
        with st.chat_message(item["role"]):
            st.markdown(item["content"])

    # Chat input box or quick prompt trigger
    chat_prompt = st.chat_input("Example: Find a phone under ₹18,000 with at least 8 GB RAM")
    prompt = active_quick_prompt or chat_prompt

    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("🤖 Understanding your needs, executing agent plan, and querying sample catalogue..."):
                try:
                    result = run_smartcart_agent(prompt, session_id=customer_id or "demo")
                    st.session_state.last_result = result
                    answer = result.get("answer") or "I checked the available sample data."
                    st.markdown(answer)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": answer}
                    )
                except Exception as exc:
                    st.error("The agent could not complete this request.")
                    st.exception(exc)
                    st.caption("Check the agent configuration and module imports.")

    # Results section
    result = st.session_state.last_result
    if result:
        intent = result.get("requirements", {}).get("intent")
        products = result.get("ranked_products") or []

        # Only display the recommendations section if products were returned,
        # or if the user performed a product search that yielded no matches.
        if products:
            st.divider()
            st.header("🎯 Recommended products")
            for i, product in enumerate(products):
                show_product(product, i)
        elif intent not in ["greeting", "unsupported_category"]:
            st.divider()
            st.header("🎯 Recommended products")
            st.warning("No ranked products were returned. Try a broader request or check the sample catalogue.")

        # Section 7: Interactive Comparison and Shortlist actions
        if products:
            ids = [p.get("product_id") for p in products if p.get("product_id") is not None]
            if ids:
                st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
                action_tab1, action_tab2 = st.tabs(["⚖️ Compare Two Products", "⭐ Customer Shortlist Actions"])

                with action_tab1:
                    st.subheader("Side-by-side Product Comparison")
                    if len(ids) >= 2:
                        c1, c2 = st.columns(2)
                        first_id = c1.selectbox("First product", ids, key="compare_first")
                        second_choices = [x for x in ids if x != first_id]
                        second_id = c2.selectbox("Second product", second_choices, key="compare_second")

                        if st.button("🔍 Compare selected products", use_container_width=True):
                            try:
                                comparison = compare_products(first_id, second_id)
                                if comparison.get("success"):
                                    st.success(f"**Verdict:** {comparison.get('price_verdict')}")
                                    matrix = comparison.get("matrix", {})
                                    if matrix:
                                        p1_name = comparison.get("product_1", {}).get("name", f"ID {first_id}")
                                        p2_name = comparison.get("product_2", {}).get("name", f"ID {second_id}")
                                        rows = []
                                        for spec_k, spec_vals in matrix.items():
                                            rows.append({
                                                "Feature": spec_k,
                                                p1_name: spec_vals.get(p1_name, "-"),
                                                p2_name: spec_vals.get(p2_name, "-")
                                            })
                                        df = pd.DataFrame(rows)
                                        st.dataframe(df, use_container_width=True, hide_index=True)

                                with st.expander("Inspect Comparison JSON payload"):
                                    st.json(comparison)
                            except Exception as e:
                                st.error(f"Comparison error: {e}")
                    else:
                        st.caption("At least two products are needed for comparison.")

                with action_tab2:
                    st.subheader("Manage Shortlisted Favorites")
                    c_short1, c_short2 = st.columns([2, 1])
                    with c_short1:
                        selected_id = st.selectbox("Select product to add to shortlist", ids, key="shortlist_select")
                    with c_short2:
                        st.write("")  # alignment spacer
                        st.write("")
                        add_clicked = st.button("➕ Add to shortlist", use_container_width=True)

                    if add_clicked:
                        try:
                            response = add_to_shortlist(selected_id, customer_id or "demo-user")
                            if response.get("success"):
                                st.success(f"✅ {response.get('message')}")
                            else:
                                st.warning(response.get("message"))
                            with st.expander("Shortlist API response"):
                                st.json(response)
                        except Exception as e:
                            st.error(f"Shortlist error: {e}")

                    st.markdown("---")
                    if st.button("📋 View my current shortlist", use_container_width=True):
                        try:
                            shortlist = get_shortlist(customer_id or "demo-user")
                            items = shortlist.get("items", [])
                            if items:
                                st.markdown(f"**Active Shortlist for `{shortlist.get('customer_id')}` ({len(items)} items):**")
                                for s_idx, item in enumerate(items, 1):
                                    st.markdown(
                                        f"{s_idx}. 🛍️ **{item.get('name')}** (ID: `{item.get('product_id')}`) — "
                                        f"**₹{item.get('price'):,.0f}** | RAM: {item.get('ram_gb', '-')} GB | Stock: {item.get('stock', 0)} units"
                                    )
                            else:
                                st.info("Your shortlist is currently empty. Add products above!")
                            with st.expander("Inspect Shortlist Raw Data"):
                                st.json(shortlist)
                        except Exception as e:
                            st.error(f"Error fetching shortlist: {e}")

        # Inspection Expanders with Structured Displays
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        st.subheader("🔍 Agent Inner-Loop & Inspection")
        left, right = st.columns(2)

        with left:
            with st.expander("📋 Agent Plan", expanded=False):
                plan_data = result.get("plan", {})
                goal = plan_data.get("goal")
                steps = plan_data.get("steps", [])
                if goal:
                    st.info(f"🎯 **Goal:** {goal}")
                if steps:
                    st.markdown("**Planned Steps:**")
                    for s_num, s_desc in enumerate(steps, 1):
                        st.markdown(f"**{s_num}.** {s_desc}")
                st.caption("Raw JSON Plan:")
                st.json(plan_data)

            with st.expander("🎯 Extracted Requirements", expanded=False):
                reqs_data = result.get("requirements", {})
                req_chips = []
                if reqs_data.get("category"):
                    req_chips.append(f"🏷️ Category: `{reqs_data.get('category')}`")
                if reqs_data.get("max_price"):
                    req_chips.append(f"💰 Max Price: `₹{reqs_data.get('max_price'):,.0f}`")
                if reqs_data.get("min_ram"):
                    req_chips.append(f"⚡ Min RAM: `{reqs_data.get('min_ram')} GB`")
                if reqs_data.get("intent"):
                    req_chips.append(f"🎯 Intent: `{reqs_data.get('intent')}`")
                if req_chips:
                    st.markdown(" • ".join(req_chips))
                st.caption("Raw JSON Requirements:")
                st.json(reqs_data)

        with right:
            with st.expander("🛠️ Tool Results", expanded=False):
                tool_res = result.get("tool_results", [])
                st.markdown(f"**Executed {len(tool_res)} Tool Invocations**")
                tool_names = [t.get("tool_name", "unknown") for t in tool_res if isinstance(t, dict)]
                if tool_names:
                    badges = "".join([f'<span class="badge badge-purple">{name}</span>' for name in set(tool_names)])
                    st.markdown(badges, unsafe_allow_html=True)
                st.caption("Raw Tool Outputs:")
                st.json(tool_res)

            with st.expander("📊 Evaluation Verdict", expanded=False):
                eval_data = result.get("evaluation", {})
                met = eval_data.get("criteria_met")
                if met is True:
                    st.success("✅ **Criteria Evaluation**: Successfully met all criteria.")
                elif met is False:
                    st.warning("⚠️ **Criteria Evaluation**: Partial or constraint mismatch.")
                notes = eval_data.get("notes")
                if notes:
                    st.markdown(f"*{notes}*")
                st.caption("Raw Evaluation JSON:")
                st.json(eval_data)

        with st.expander("📜 Agent Activity Trace", expanded=True):
            trace = result.get("execution_trace", [])
            if trace:
                st.markdown(f"**Execution Pipeline ({len(trace)} Steps Completed):**")
                for step_no, step in enumerate(trace, start=1):
                    step_name = step.get("step", f"Step {step_no}")
                    action = step.get("action", "")
                    status = step.get("status", "success")
                    status_icon = "✅" if status == "success" else ("⚠️" if status == "warning" else "⚙️")

                    with st.container(border=True):
                        c_title, c_stat = st.columns([4, 1])
                        c_title.markdown(f"**Step {step_no}: {step_name}**")
                        c_stat.markdown(f"<span style='float:right;'>{status_icon} <code>{status}</code></span>", unsafe_allow_html=True)
                        if action:
                            st.caption(f"Action: `{action}`")
                        st.json(step)
            else:
                st.write("No execution trace was returned by the agent module.")


if __name__ == "__main__":
    main()
