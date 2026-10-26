
import streamlit as st
import plotly.express as px
from llm_helper import generate_sql_query, generate_insights
from database import execute_query

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="Enterprise AI Data Analyst",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# 2. CUSTOM CSS
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Color palette */
:root {
    --purple: #7057E8;
    --purple-dark: #5741C8;
    --purple-light: #F3EEFF;
    --navy: #111827;
    --text: #29204D;
    --muted: #64748B;
    --border: #E1D9F7;
}

/* Global typography */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F3EEFF !important;
    color: #29204D;
}

/* Main workspace background */
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: #F3EEFF !important;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ==================================================
   SIDEBAR
   ================================================== */

[data-testid="stSidebar"] {
    background: #111827 !important;
    border-right: 1px solid #293348;
}

[data-testid="stSidebar"] > div:first-child {
    background: #111827 !important;
    padding-top: 1.5rem;
}

/* Sidebar headings and text */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong {
    color: #E2E8F0 !important;
}

/* Sidebar separators */
[data-testid="stSidebar"] hr {
    border-color: #374151 !important;
}

/* Sidebar sample question buttons */
[data-testid="stSidebar"] .stButton > button {
    background: #292D42 !important;
    color: #F8FAFC !important;
    border: 1px solid #454B65 !important;
    border-radius: 10px !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    min-height: 46px;
    padding: 8px 10px;
    text-align: left;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] .stButton > button p {
    color: #F8FAFC !important;
    font-size: 12px !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #454078 !important;
    border-color: #A78BFA !important;
    color: #FFFFFF !important;
}

/* ==================================================
   MAIN HEADER
   ================================================== */

.hero-title {
    color: #29204D;
    font-size: clamp(26px, 3vw, 38px);
    font-weight: 800;
    letter-spacing: -1.2px;
    line-height: 1.3;
    margin-bottom: 8px;
}

.hero-subtitle {
    color: #655B82;
    font-size: 15px;
    line-height: 1.8;
    margin-bottom: 20px;
}

.status-badge {
    display: inline-block;
    background: #DCFCE7;
    color: #166534;
    border-radius: 30px;
    padding: 8px 13px;
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
}

/* ==================================================
   QUESTION PANEL
   ================================================== */

.query-card {
    background: #FAF8FF;
    border: 1px solid #DDD2FF;
    border-radius: 17px;
    padding: 24px;
    margin: 20px 0 15px 0;
    box-shadow: 0 5px 18px rgba(88, 65, 160, 0.05);
}

.query-heading {
    color: #29204D;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 8px;
}

.query-description {
    color: #756A91;
    font-size: 13px;
    line-height: 1.7;
}

/* Input label */
.stTextInput label {
    color: #40345F !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

/* Main question input */
.stTextInput input {
    min-height: 49px;
    background: #FFFFFF !important;
    color: #29204D !important;
    border: 1px solid #C4B5FD !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    transition: all 0.2s ease;
}

.stTextInput input::placeholder {
    color: #8B83A1 !important;
    opacity: 1 !important;
}

.stTextInput input:focus {
    border-color: #7057E8 !important;
    box-shadow: 0 0 0 3px rgba(112, 87, 232, 0.13) !important;
}

/* ==================================================
   BUTTONS
   ================================================== */

.stButton > button {
    min-height: 44px;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease;
}

/* Primary Analyze button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7057E8, #9B5CF6) !important;
    color: #FFFFFF !important;
    border: none !important;
    box-shadow: 0 5px 15px rgba(112, 87, 232, 0.22);
}

.stButton > button[kind="primary"] p {
    color: #FFFFFF !important;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #5741C8, #8244DB) !important;
    box-shadow: 0 7px 18px rgba(112, 87, 232, 0.3);
    transform: translateY(-1px);
}

/* Other main buttons */
[data-testid="stMain"] .stButton > button:not([kind="primary"]) {
    background: #FFFFFF;
    color: #514477;
    border: 1px solid #D8CEF4;
}

[data-testid="stMain"] .stButton > button:not([kind="primary"]):hover {
    background: #F0E9FF;
    border-color: #A78BFA;
}

/* ==================================================
   DASHBOARD HEADINGS
   ================================================== */

.section-heading {
    color: #29204D;
    font-size: 21px;
    font-weight: 750;
    letter-spacing: -0.4px;
    margin-top: 24px;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #756A91;
    font-size: 13px;
    margin-bottom: 17px;
}

/* ==================================================
   KPI CARDS
   ================================================== */

.metric-card {
    background: #FFFFFF;
    border: 1px solid #E1D9F7;
    border-radius: 15px;
    padding: 21px;
    min-height: 112px;
    box-shadow: 0 4px 15px rgba(88, 65, 160, 0.04);
}

.metric-label {
    color: #756A91;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 12px;
}

.metric-value {
    color: #29204D;
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.6px;
    overflow-wrap: anywhere;
}

/* ==================================================
   TABS, SQL, TABLES, EXPANDERS
   ================================================== */

[data-testid="stTabs"] button {
    font-weight: 600;
    font-size: 13px;
}

[data-testid="stTabs"] [aria-selected="true"] {
    color: #5741C8 !important;
}

[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #D8CEF4;
    border-radius: 12px;
}

[data-testid="stDataFrame"] {
    background: #FFFFFF;
    border: 1px solid #E1D9F7;
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Download buttons */
[data-testid="stDownloadButton"] button {
    background: #FFFFFF;
    color: #5741C8;
    border: 1px solid #C4B5FD;
    border-radius: 10px;
}

/* Footer */
.footer {
    color: #8B83A1;
    font-size: 12px;
    text-align: center;
    padding-top: 35px;
}

/* Responsive layout */
@media (max-width: 768px) {
    .block-container {
        padding: 1.2rem 1rem 2rem 1rem;
    }

    .query-card {
        padding: 18px;
    }

    .metric-card {
        padding: 15px;
    }

    .metric-value {
        font-size: 21px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# 3. SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown("""
    <div style="padding: 5px 0 18px 0;">
        <div style="font-size: 29px; margin-bottom: 9px;">
            🤖
        </div>
        <div style="font-size: 20px; font-weight: 800; color: #FFFFFF;">
            AI Data Assistant
        </div>
        <div style="font-size: 12px; color: #A5B4CC; margin-top: 6px;">
            Intelligent business analytics
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 💡 Sample Questions")

    sample_questions = [
        "Show total sales revenue by product",
        "List top customers by total spending",
        "Show total sales per category",
        "Which product has the highest unit price?"
    ]

    for i, question in enumerate(sample_questions):
        if st.button(
            question,
            key=f"sample_question_{i}",
            use_container_width=True
        ):
            st.session_state["business_question"] = question
            st.rerun()

    st.divider()

    st.markdown("### 🧰 Technology Stack")

    st.markdown("""
    - 🐍 Python & Streamlit
    - 🧠 Google Gemini & LangChain
    - 🗄️ SQL Database
    - 🐼 Pandas
    - 📊 Plotly
    """)

    st.divider()

    st.markdown("""
    <div style="font-size: 12px; line-height: 2; color: #CBD5E1;">
        <b style="color: #FFFFFF;">How it works</b><br>
        01 &nbsp; Ask a business question<br>
        02 &nbsp; Generate SQL using AI<br>
        03 &nbsp; Execute the query<br>
        04 &nbsp; Explore charts and insights
    </div>
    """, unsafe_allow_html=True)


# ==================================================
# 4. MAIN HEADER
# ==================================================

header_left, header_right = st.columns([5, 1.4])

with header_left:

    st.markdown(
        '<div class="hero-title">🤖 Enterprise AI Data Analyst</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-subtitle">'
        'Transform plain-English business questions into SQL queries, '
        'interactive charts, and actionable insights.'
        '</div>',
        unsafe_allow_html=True
    )

with header_right:

    st.markdown(
        '<div style="text-align:right; padding-top:10px;">'
        '<span class="status-badge">● AI Assistant</span>'
        '</div>',
        unsafe_allow_html=True
    )

st.divider()


# ==================================================
# 5. BUSINESS QUESTION INPUT
# ==================================================

st.markdown("""
<div class="query-card">
    <div class="query-heading">
        ✨ Ask your database anything
    </div>
    <div class="query-description">
        Describe the business information you need.
        AI will generate the SQL and analyze your results.
    </div>
</div>
""", unsafe_allow_html=True)

user_question = st.text_input(
    "Business question",
    key="business_question",
    placeholder="e.g. Show monthly revenue grouped by product category",
    label_visibility="collapsed"
)

button_col, hint_col = st.columns([1.35, 4])

with button_col:
    run_analysis = st.button(
        "✨ Analyze Question",
        type="primary",
        use_container_width=True
    )

with hint_col:
    st.markdown(
        "<div style='color:#756A91; font-size:12px; padding-top:13px;'>"
        "Tip: Ask about sales, customers, products, revenue, or trends."
        "</div>",
        unsafe_allow_html=True
    )


# ==================================================
# 6. RUN AI ANALYSIS
# ==================================================

if run_analysis:

    if not user_question.strip():

        st.warning(
            "Please enter a business question before starting the analysis."
        )

    else:

        try:

            # Generate SQL query
            with st.spinner(
                "🧠 AI is analyzing your question and generating SQL..."
            ):
                sql_query = generate_sql_query(user_question)

            if not sql_query or not str(sql_query).strip():
                st.error(
                    "The AI did not return a SQL query. "
                    "Please try rephrasing your question."
                )
                st.stop()

            # SQL preview
            with st.expander(
                "🛠️ View Generated SQL Query",
                expanded=False
            ):
                st.code(sql_query, language="sql")

            # Execute database query
            with st.spinner("⚡ Executing query against your database..."):
                df = execute_query(sql_query)

            if df is None:
                st.error("The database did not return a valid result.")
                st.stop()

            if df.empty:
                st.info(
                    "The query executed successfully but returned no rows."
                )
                st.stop()

            # Determine column types
            numeric_cols = df.select_dtypes(
                include=["number"]
            ).columns.tolist()

            text_cols = df.select_dtypes(
                include=["object", "category", "string"]
            ).columns.tolist()

            # ==================================================
            # 7. DASHBOARD OVERVIEW
            # ==================================================

            st.markdown(
                '<div class="section-heading">📊 Analysis Dashboard</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="section-subtitle">'
                'An overview of your query results and business findings.'
                '</div>',
                unsafe_allow_html=True
            )

            metric_cols = st.columns(3)

            metric_data = [
                ("📋 Total Rows", f"{len(df):,}"),
                ("🧩 Total Columns", f"{len(df.columns):,}"),
                ("🔢 Numeric Fields", f"{len(numeric_cols):,}")
            ]

            for col, (label, value) in zip(metric_cols, metric_data):

                with col:

                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.write("")

            # ==================================================
            # 8. RESULT TABS
            # ==================================================

            tab_dashboard, tab_data, tab_sql = st.tabs([
                "📈 Insights & Visualizations",
                "📋 Query Data",
                "💻 SQL Query"
            ])

            # --------------------------------------------------
            # DASHBOARD TAB
            # --------------------------------------------------

            with tab_dashboard:

                st.markdown(
                    '<div class="section-heading">💡 Executive Insights</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="section-subtitle">'
                    'AI-generated interpretation of your query results.'
                    '</div>',
                    unsafe_allow_html=True
                )

                with st.spinner("💡 Generating executive insights..."):

                    summary = generate_insights(
                        user_question,
                        sql_query,
                        df.head(100).to_string(index=False)
                    )

                if summary:
                    st.info(summary)
                else:
                    st.warning("No executive insights were generated.")

                # Visual analytics
                st.markdown(
                    '<div class="section-heading">📈 Visual Analytics</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="section-subtitle">'
                    'Choose the fields and chart type to explore your results.'
                    '</div>',
                    unsafe_allow_html=True
                )

                if numeric_cols and text_cols:

                    chart_col, options_col = st.columns([3, 1])

                    with options_col:

                        selected_x = st.selectbox(
                            "Category",
                            options=text_cols,
                            key="chart_category"
                        )

                        selected_y = st.selectbox(
                            "Measure",
                            options=numeric_cols,
                            key="chart_measure"
                        )

                        chart_type = st.selectbox(
                            "Chart Type",
                            options=["Bar", "Line", "Scatter"],
                            key="chart_visual_type"
                        )

                    with chart_col:

                        title = (
                            f"{selected_y.replace('_', ' ').title()} "
                            f"by {selected_x.replace('_', ' ').title()}"
                        )

                        if chart_type == "Bar":

                            fig = px.bar(
                                df,
                                x=selected_x,
                                y=selected_y,
                                title=title,
                                template="plotly_white",
                                color=selected_y,
                                color_continuous_scale=[
                                    "#DDD6FE",
                                    "#A78BFA",
                                    "#7057E8",
                                    "#4C1D95"
                                ],
                                hover_data=[selected_x, selected_y]
                            )

                        elif chart_type == "Line":

                            fig = px.line(
                                df,
                                x=selected_x,
                                y=selected_y,
                                title=title,
                                template="plotly_white",
                                markers=True
                            )

                            fig.update_traces(
                                line=dict(color="#7057E8", width=3),
                                marker=dict(size=7)
                            )

                        else:

                            fig = px.scatter(
                                df,
                                x=selected_x,
                                y=selected_y,
                                title=title,
                                template="plotly_white",
                                color=selected_y,
                                color_continuous_scale="Purples"
                            )

                        fig.update_layout(
                            paper_bgcolor="#FFFFFF",
                            plot_bgcolor="#FFFFFF",
                            font=dict(
                                family="Inter, sans-serif",
                                color="#40345F",
                                size=12
                            ),
                            title_font_size=17,
                            title_font_color="#29204D",
                            margin=dict(
                                l=20,
                                r=20,
                                t=65,
                                b=35
                            ),
                            height=430,
                            coloraxis_showscale=False,
                            xaxis=dict(
                                showgrid=False,
                                title=selected_x.replace("_", " ").title()
                            ),
                            yaxis=dict(
                                gridcolor="#EEE9F8",
                                zeroline=False,
                                title=selected_y.replace("_", " ").title()
                            )
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                elif numeric_cols:

                    st.info(
                        "Your results contain numeric columns but no "
                        "categorical columns for a category-based chart."
                    )

                    for col in numeric_cols[:3]:

                        total = df[col].sum()

                        st.metric(
                            label=f"Sum of {col.replace('_', ' ').title()}",
                            value=f"{total:,.2f}"
                        )

                else:

                    st.info(
                        "No numeric columns were found for visualization. "
                        "View your results in the Query Data tab."
                    )

            # --------------------------------------------------
            # QUERY DATA TAB
            # --------------------------------------------------

            with tab_data:

                st.markdown(
                    '<div class="section-heading">📋 Query Result Dataset</div>',
                    unsafe_allow_html=True
                )

                st.caption(
                    f"{len(df):,} rows · {len(df.columns):,} columns"
                )

                st.dataframe(
                    df,
                    use_container_width=True,
                    height=450,
                    hide_index=True
                )

                csv_data = df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    label="⬇️ Download Results as CSV",
                    data=csv_data,
                    file_name="ai_analysis_results.csv",
                    mime="text/csv"
                )

            # --------------------------------------------------
            # SQL TAB
            # --------------------------------------------------

            with tab_sql:

                st.markdown(
                    '<div class="section-heading">💻 Generated SQL</div>',
                    unsafe_allow_html=True
                )

                st.caption(
                    "Review the SQL generated for your business question."
                )

                st.code(sql_query, language="sql")

                st.download_button(
                    label="⬇️ Download SQL Query",
                    data=str(sql_query),
                    file_name="generated_query.sql",
                    mime="text/plain"
                )

        except Exception as e:

            st.error(
                "Something went wrong while analyzing your question. "
                "Check the error details below."
            )

            with st.expander("View error details"):
                st.exception(e)


# ==================================================
# 9. FOOTER
# ==================================================

st.markdown("""
<div class="footer">
    Enterprise AI Data Analyst
    &nbsp;·&nbsp;
    Powered by Python, SQL, Streamlit & AI
</div>
""", unsafe_allow_html=True)

