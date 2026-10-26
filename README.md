# 🤖 Enterprise AI Data Analyst Assistant (Text-to-SQL)

An enterprise-grade, AI-powered Natural Language to SQL analytics application that transforms plain English business questions into executable SQL queries, interactive dashboards, and executive insights instantly.

![Python](https://img.shields.io/badge/Python-3.13%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=flat-square&logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-green?style=flat-square)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-orange?style=flat-square&logo=google)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?style=flat-square&logo=sqlite)

---

## 🌟 Key Features
* **Natural Language to SQL Translation:** Powered by LangChain and Google Gemini, dynamically reads database schemas to construct accurate SQLite queries.
* **Executive AI Summaries:** Automatically generates contextual business insights from query output data.
* **Interactive Visual Analytics:** Seamlessly switches between dynamic Bar charts, Line charts, and Scatter plots using Plotly.
* **Modern SaaS UI:** Custom-styled dark/light theme with a gradient aesthetic, metric summary cards, and multi-tab results views.
* **Data Export:** Supports downloading queried datasets as CSV files and raw SQL scripts.

---

## 🛠️ Tech Stack
* **Frontend/UI:** Streamlit, Custom CSS
* **Orchestration & LLM:** LangChain, Google Gemini API (`gemini-3.8-flash`)
* **Database & Processing:** SQLite, Pandas, NumPy
* **Visualization:** Plotly Express

---

## 📂 Project Architecture
```text
nl-to-sql-assistant/
│
├── styles/
│   └── style.css         # Custom SaaS UI styling
├── app.py                # Main Streamlit application entry point
├── database.py           # SQLite database connection & execution utilities
├── llm_helper.py         # LangChain & Gemini prompt generation/parsing logic
├── setup_db.py           # Database initializer & Northwind sample data loader
├── northwind.db          # SQLite sample database
├── requirements.txt      # Project dependencies
└── .env                  # API keys (ignored in version control)
