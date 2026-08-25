import streamlit as st 

def parse_thinking_stream(stream):
    thinking_expander = st.expander("Show Reasoning", expanded=True)
    thinking_container = thinking_expander.empty()
    response_container = st.empty()

    full_thinking = ""
    full_response = ""
    is_thinking = False

    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        
        if "<think>" in content:
            is_thinking = True
            content = content.replace("<think>", "")
            
        if "</think>" in content:
            is_thinking = False
            content = content.replace("</think>", "")

        if is_thinking:
            full_thinking += content
            thinking_container.markdown(full_thinking)
        else:
            full_response += content
            response_container.markdown(full_response)
            
    return full_thinking, full_response

def render_agent_response(response):
    """
    Renders the built-in <think> monologue, the investigation steps, 
    and the final data/interpretation.
    """

    logger.info("Preparing for final response rendering...")

    if hasattr(response, "content"):
        response = response.content

    if not isinstance(response, dict):
        response = response.model_dump()

    # HANDLE BUILT-IN MODEL THINKING (<think> tags)
    raw_text = response.get("interpretation") or response.get("content", "")
    
    logger.info("Checking for internal throughts 💭...")

    if isinstance(raw_text, str) and "<think>" in raw_text:
        match = re.search(r"<think>(.*?)</think>\s*(.*)", raw_text, re.DOTALL)
        if match:
            think_text = match.group(1).strip()
            final_text = match.group(2).strip()
            
            # with st.expander("💭 Model Internal Monologue", expanded=False):
            st.markdown(think_text)
            
            # Show the "cleaned" interpretation without the tags
            st.markdown(final_text)
        else:
            st.markdown(raw_text)
    else:
        # If no think tags, just show the text
        st.markdown(raw_text)

    logger.info("Gathering investigation steps...")
    if CFG.DEBUG_MODE:
        if "steps" in response and response["steps"]:
            with st.expander("🔍 Investigation Path (Tools used)", expanded=False):
                for i, step in enumerate(response["steps"]):
                    st.markdown(f"**Step {i+1}:** {step}")

    # HANDLE DATA & VISUALS
    logger.info("Finalizing...")
    if response["type"] == "data":
        intent = response.get("intent")

        with st.expander("💻 Generated SQL Query"):
            st.code(response["final_sql"], language="sql")
    
        if intent.value == QueryIntent.CHART.value:
            df = response["data"]
            with st.expander("🖼️ Visualization"):
                # Heuristic Chart Selection
                fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Election Insights")

                cols = df.columns
                num_rows = len(df)
                
                # If we have a category and a number, and only a few rows -> PIE is great for "Parts of a whole"
                if len(cols) >= 2 and num_rows <= 6:
                    fig = px.pie(df, names=cols[0], values=cols[1], title="Election Insights")
                    
                # If we have a single numeric column with many values -> HISTOGRAM for "Frequency"
                elif len(cols) == 1 and pd.api.types.is_numeric_dtype(df[cols[0]]):
                    fig = px.histogram(df, x=cols[0], title="Election Insights")
                    
                # Default fallback: BAR for comparisons
                else:
                    fig = px.bar(df, x=cols[0], y=cols[1] if len(cols) > 1 else None, 
                                title="Election Insights")

                st.plotly_chart(fig, use_container_width=True)

        with st.expander("📊 View Raw Data"):
            st.dataframe(response["data"])

    # if response["type"] == "error":
    #     st.error(response["content"])
