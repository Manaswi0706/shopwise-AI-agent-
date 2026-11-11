import streamlit as st
from agent.orchestrator import run_smartcart_agent
from database.products import compare_products, add_to_shortlist, get_shortlist

st.set_page_config(
    page_title="SmartCart AI",
    page_icon="🛍️",
    layout="wide"
)


def show_product(product, index):
    """Render a single product card in the recommendations section."""
    name = product.get("name") or product.get("title") or f"Product {index + 1}"
    price = product.get("price")
    score = product.get("match_score")
    with st.container(border=True):
        st.subheader(name)
        col1, col2, col3 = st.columns(3)
        col1.metric("Price", f"₹{price:,.0f}" if isinstance(price, (int, float)) else "Not listed")
        col2.metric("RAM", f"{product.get('ram_gb')} GB" if product.get("ram_gb") is not None else "Not listed")
        col3.metric("Match score", f"{score}/100" if score is not None else "Not scored")
        st.write(product.get("recommendation_reason", "Compare the available specifications."))
        st.caption(f"Sample catalogue item • ID: {product.get('product_id', 'not provided')}")


def main():
    st.title("🛍️ SmartCart AI")
    st.caption("An intelligent shopping assistant that plans, uses tools, and explains its recommendations.")
    st.info("Demo notice: catalogue and stock values are sample data, not live marketplace inventory.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "last_result" not in st.session_state:
        st.session_state.last_result = None

    with st.sidebar:
        st.header("Demo controls")
        customer_id = st.text_input("Demo customer ID", value="demo-user")
        st.caption("Use sample data only. Do not enter payment or sensitive personal information.")
        if st.button("Clear conversation"):
            st.session_state.chat_history = []
            st.session_state.last_result = None
            st.rerun()

    for item in st.session_state.chat_history:
        with st.chat_message(item["role"]):
            st.markdown(item["content"])

    prompt = st.chat_input(
        "Example: Find a phone under ₹18,000 with at least 8 GB RAM"
    )
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Understanding your needs and checking the sample catalogue..."):
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

    result = st.session_state.last_result
    if result:
        st.divider()
        st.header("Recommended products")
        products = result.get("ranked_products") or []
        if products:
            for i, product in enumerate(products):
                show_product(product, i)
        else:
            st.warning("No ranked products were returned. Try a broader request or check the sample catalogue.")

        # Section 7: Direct comparison and shortlist actions
        if products:
            ids = [p.get("product_id") for p in products if p.get("product_id") is not None]
            if ids:
                st.subheader("Compare two products")
                if len(ids) >= 2:
                    c1, c2 = st.columns(2)
                    first_id = c1.selectbox("First product", ids, key="compare_first")
                    second_choices = [x for x in ids if x != first_id]
                    second_id = c2.selectbox("Second product", second_choices, key="compare_second")
                    if st.button("Compare selected products"):
                        try:
                            comparison = compare_products(first_id, second_id)
                            st.json(comparison)
                        except Exception as e:
                            st.error(f"Comparison error: {e}")
                else:
                    st.caption("At least two products are needed for comparison.")

                st.subheader("Shortlist actions")
                selected_id = st.selectbox("Add a product to your shortlist", ids, key="shortlist_select")
                if st.button("Add to shortlist"):
                    try:
                        response = add_to_shortlist(selected_id, customer_id or "demo-user")
                        st.success("Shortlist action completed.")
                        st.json(response)
                    except Exception as e:
                        st.error(f"Shortlist error: {e}")

                if st.button("View my shortlist"):
                    try:
                        shortlist = get_shortlist(customer_id or "demo-user")
                        st.json(shortlist)
                    except Exception as e:
                        st.error(f"Error fetching shortlist: {e}")

        # Inspection Expanders
        left, right = st.columns(2)
        with left:
            with st.expander("Agent plan"):
                st.json(result.get("plan", {}))
            with st.expander("Extracted requirements"):
                st.json(result.get("requirements", {}))
        with right:
            with st.expander("Tool results"):
                st.json(result.get("tool_results", []))
            with st.expander("Evaluation"):
                st.json(result.get("evaluation", {}))

        with st.expander("Agent activity trace", expanded=True):
            trace = result.get("execution_trace", [])
            if trace:
                for step_no, step in enumerate(trace, start=1):
                    st.write(f"**Step {step_no}.**")
                    st.json(step)
            else:
                st.write("No execution trace was returned by the agent module.")


if __name__ == "__main__":
    main()
