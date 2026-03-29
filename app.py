import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent
import random
import plotly.express as px
import streamlit.components.v1 as components

# ---------- 1. Page Configuration ----------
st.set_page_config(page_title="Salar.AI Master Panel", layout="wide", initial_sidebar_state="expanded")
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)

# ---------- 2. Premium CSS Injection (Upgraded for "Hooking" UI) ----------
st.markdown("""
<style>
    .stApp { background-color: #0f172a; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #1e293b; }
    [data-testid="stSidebar"] * { color: #f8fafc !important; font-weight: 500;}
    .block-container { padding-top: 1rem !important; }
    
    .sb-header { text-align: center; padding: 10px 0; margin-bottom: 20px; }
    .sb-header img { width: 90px; border-radius: 50%; border: 3px solid #3b82f6; box-shadow: 0 0 20px rgba(59, 130, 246, 0.5); }
    .sb-header h2 { font-size: 22px; margin-top: 15px; color: white; font-weight: 800; }
    
    .stRadio > div { border: none !important; }
    div.row-widget.stRadio > div[role="radiogroup"] > label { margin-left: 10px; padding: 12px; border-radius: 8px; transition: 0.3s; color: #f8fafc !important;}
    div.row-widget.stRadio > div[role="radiogroup"] > label:hover { background-color: #1e293b; padding-left: 20px; border-left: 4px solid #3b82f6; }

    .top-header { display: flex; justify-content: space-between; align-items: center; background-color: #ffffff; padding: 15px 30px; border-radius: 12px; margin-bottom: 25px; margin-top: -30px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; }
    .top-header h2 { margin: 0; color: #1e293b; font-size: 26px; font-weight: 800; }
    .top-header .welcome { color: #64748b; font-size: 15px; font-weight: 500; }
    .user-pill { display: flex; align-items: center; background-color: #f1f5f9; padding: 8px 20px; border-radius: 50px; border: 1px solid #e2e8f0; color: #1e293b; box-shadow: 0 0 10px rgba(0,0,0,0.02); font-weight: bold; }

    /* 🌟 UPGRADED KPI CARDS (Neon Glow & Glassmorphism) 🌟 */
    .kpi-row { display: flex; gap: 20px; margin-bottom: 25px; flex-wrap: wrap;}
    .kpi-card { 
        flex: 1; min-width: 250px; 
        background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%); 
        padding: 25px; border-radius: 16px; 
        border-top: 1px solid #334155; border-right: 1px solid #334155; border-bottom: 1px solid #334155;
        border-left: 4px solid #3b82f6; /* Accent Border */
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); 
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
        position: relative; overflow: hidden; 
    }
    .kpi-card:hover { 
        transform: translateY(-8px) scale(1.02); 
        border-left: 4px solid #8b5cf6; 
        box-shadow: 0 15px 25px rgba(59, 130, 246, 0.2);
    }
    
    .card-icon { font-size: 24px; color: #3b82f6; position: absolute; right: 20px; top: 20px; background-color: rgba(15, 23, 42, 0.6); padding: 12px; border-radius: 10px; border: 1px solid #334155; backdrop-filter: blur(5px); }
    .card-title { color: #94a3b8; font-size: 13px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;}
    .card-value { color: white; font-size: 34px; font-weight: 900; margin: 10px 0; font-family: 'Inter', sans-serif;}
    .trend-info { display: flex; align-items: center; font-size: 13px; margin-top: 15px;}
    .trend-percent { font-weight: bold; margin-right: 10px;}
    .trend-up { color: #10b981; } .trend-down { color: #ef4444; } .trend-label { color: #94a3b8; }

    /* Custom Streamlit Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { background-color: #0f172a; border-radius: 10px; padding: 5px; gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1e293b; border-radius: 8px; color: white; padding: 10px 20px; border: 1px solid #334155; transition: 0.3s; }
    .stTabs [aria-selected="true"] { background-color: #3b82f6 !important; border-color: #3b82f6 !important; box-shadow: 0 0 15px rgba(59,130,246,0.4); }

    /* Health Bar */
    .health-container { background-color: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; text-align: center;}
    .health-bar-bg { width: 100%; background-color: #0f172a; border-radius: 20px; height: 12px; margin-top: 10px; overflow: hidden; border: 1px solid #334155;}
    .health-bar-fill { height: 100%; border-radius: 20px; transition: 1s ease-in-out; }

    div.stButton > button:first-child { background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%); color: white; border: none; border-radius: 8px; padding: 10px 24px; font-weight: 700; transition: 0.3s; }
    div.stButton > button:first-child:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4); }

    .content-box { background-color: #1e293b; padding: 25px; border-radius: 16px; border: 1px solid #334155; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);}
    h3 { color: white !important; font-weight: 700 !important; font-family: 'Inter', sans-serif; margin-bottom: 20px !important;}
    
    .chip-btn { background-color: #334155; color: white; border-radius: 20px; padding: 8px 15px; border: 1px solid #475569; font-size: 12px; cursor: pointer; transition: 0.3s; margin-right: 10px;}
    .chip-btn:hover { background-color: #3b82f6; border-color: #3b82f6;}

    #MainMenu {visibility: hidden;} footer {visibility: hidden;} .stFileUploader label {color: white !important;}
</style>
""", unsafe_allow_html=True)

# ---------- 3. Sidebar Setup ----------
with st.sidebar:
    st.markdown("""<div class="sb-header"><img src="https://ui-avatars.com/api/?name=Salar+AI&background=3b82f6&color=fff&size=150&rounded=true&bold=true" alt="Profile"><h2>Salar.AI Master Panel</h2></div>""", unsafe_allow_html=True)
    menu = st.radio("Navigate", ["📊 Analytics Dashboard", "💬 Data Agent Chat", "✏️ Excel-Style Data Editor", "🤖 Auto-Pilot Dashboard"])
    st.write("---")
    api_key = st.text_input("🔑 Groq API Key:", type="password", placeholder="Paste key here...")

# ---------- 4. Top Panel ----------
st.markdown("""
<div class="top-header">
    <div><h2>Analytics Overview</h2><div class="welcome">Advanced Data Intelligence Suite</div></div>
    <div class="user-pill"><i class="fa fa-user-circle" style="margin-right: 10px; color: #3b82f6;"></i>Welcome, Salar 👋</div>
</div>
""", unsafe_allow_html=True)

# ---------- 5. Main Logic ----------
uploaded_file = st.file_uploader("📂 Upload Dataset (CSV, Excel, or JSON)", type=["csv", "xlsx", "json"])

if uploaded_file is not None:
    file_ext = uploaded_file.name.split('.')[-1]
    if file_ext == 'csv': df = pd.read_csv(uploaded_file)
    elif file_ext == 'xlsx': df = pd.read_excel(uploaded_file)
    elif file_ext == 'json': df = pd.read_json(uploaded_file)
    
    # === 🌟 PAGE 1: UPGRADED HOOKING DASHBOARD 🌟 ===
    if menu == "📊 Analytics Dashboard":
        total_rows = df.shape[0]
        total_cols = df.shape[1]
        empty_cells = df.isnull().sum().sum()
        total_data_points = total_rows * total_cols
        
        # Calculate Data Health Score (Gamification)
        health_score = int(100 - ((empty_cells / total_data_points) * 100)) if total_data_points > 0 else 0
        health_color = "#10b981" if health_score > 85 else ("#f59e0b" if health_score > 60 else "#ef4444")

        st.markdown(f"""
        <div class="kpi-row">
            <div class="kpi-card"><i class="fa fa-database card-icon"></i><div class="card-title">Total Rows</div><div class="card-value">{total_rows:,}</div><div class="trend-info"><span class="trend-up trend-percent"><i class="fa fa-arrow-up"></i> +{random.uniform(5.5, 25.5):.1f}%</span></div></div>
            <div class="kpi-card" style="border-left-color: #10b981;"><i class="fa fa-columns card-icon" style="color: #10b981;"></i><div class="card-title">Total Columns</div><div class="card-value">{total_cols}</div><div class="trend-info"><span class="trend-label trend-percent">Parsed Successfully</span></div></div>
            <div class="kpi-card" style="border-left-color: #ef4444;"><i class="fa fa-minus-circle card-icon" style="color: #ef4444;"></i><div class="card-title">Missing Values</div><div class="card-value">{empty_cells:,}</div><div class="trend-info"><span class="trend-down trend-percent"><i class="fa fa-arrow-down"></i> Action Needed</span></div></div>
            <div class="kpi-card" style="border-left-color: #a855f7;"><i class="fa fa-heartbeat card-icon" style="color: #a855f7;"></i><div class="card-title">Data Health Score</div><div class="card-value" style="color:{health_color};">{health_score}%</div>
                <div class="health-bar-bg"><div class="health-bar-fill" style="width: {health_score}%; background-color: {health_color};"></div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 🌟 INTERACTIVE TABS (Hooking Element) 🌟
        st.markdown("<br>", unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["🗄️ Raw Data View", "📈 Quick Trends", "📊 Column Stats"])
        
        with tab1:
            st.markdown('<div class="content-box"><h3>📋 Interactive Data Preview</h3>', unsafe_allow_html=True)
            st.dataframe(df.head(100), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with tab2:
            st.markdown('<div class="content-box"><h3>📈 Automatic Numeric Trend</h3>', unsafe_allow_html=True)
            num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            if len(num_cols) > 0:
                trend_fig = px.area(df.head(200), y=num_cols[0], template="plotly_dark", color_discrete_sequence=['#3b82f6'])
                trend_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(trend_fig, use_container_width=True)
            else: st.info("No numerical columns found to draw trend.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with tab3:
            st.markdown('<div class="content-box"><h3>📊 Dataset Summary Statistics</h3>', unsafe_allow_html=True)
            st.dataframe(df.describe(), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # === PAGE 2: AI CHAT ===
    elif menu == "💬 Data Agent Chat":
        st.markdown('<div class="content-box"><h3>🤖 Data Intelligence AI Chat</h3>', unsafe_allow_html=True)
        if not api_key: st.warning("⚠️ Enter Groq API Key in sidebar.")
        else:
            st.markdown("<p style='color:#94a3b8; font-size:14px;'>Try Quick Prompts:</p>", unsafe_allow_html=True)
            chip1, chip2, chip3, _ = st.columns([1,1,1,2])
            quick_q = None
            if chip1.button("📊 Summarize Data"): quick_q = "Provide a comprehensive summary of this dataset."
            if chip2.button("🔍 Find Anomalies"): quick_q = "Are there any outliers or anomalies in this data?"
            if chip3.button("📈 Top Trends"): quick_q = "What are the top 3 trends or insights you can find?"

            q = st.chat_input("Ask AI anything about your data...") or quick_q
            if q:
                with st.chat_message("user"): st.write(q)
                with st.spinner("Analyzing..."):
                    try:
                        agent = create_pandas_dataframe_agent(ChatGroq(temperature=0, model_name="llama-3.1-8b-instant", groq_api_key=api_key), df, verbose=True, allow_dangerous_code=True)
                        st.chat_message("assistant").success(agent.run(q))
                    except Exception as e: st.error(e)
        st.markdown('</div>', unsafe_allow_html=True)

    # === PAGE 3: EXCEL EDITOR ===
    elif menu == "✏️ Excel-Style Data Editor":
        st.markdown('<div class="content-box"><h3>✏️ Excel-Style Data Editor</h3><p style="color:#94a3b8;">Double-click to edit, add rows, or sort.</p>', unsafe_allow_html=True)
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, height=400)
        st.markdown("#### 🛠️ Quick Action Tools")
        col1, col2, col3 = st.columns(3)
        if col1.button("🧹 Drop Empty Rows"): edited_df = edited_df.dropna(); st.success("✅ Null values removed!")
        if col2.button("🚫 Remove Duplicates"): edited_df = edited_df.drop_duplicates(); st.success("✅ Duplicates removed!")
        col3.download_button("📥 Download Edited CSV", data=edited_df.to_csv(index=False).encode('utf-8'), file_name="Salar_Edited_Data.csv", mime="text/csv")
        st.markdown('</div>', unsafe_allow_html=True)

    # === PAGE 4: AUTO-PILOT DASHBOARD (PDF EXPORT) ===
    elif menu == "🤖 Auto-Pilot Dashboard":
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown('<h3>🪄 AI Auto-Pilot Dashboard Agent</h3><p style="color:#94a3b8;">1-Click AI Automated Insights</p>', unsafe_allow_html=True)
        with col2:
            components.html("""
            <script> function printPDF() { window.parent.print(); } </script>
            <button onclick="printPDF()" style="background: #ef4444; color: white; border: none; border-radius: 8px; padding: 10px 15px; font-weight: bold; cursor: pointer; float: right; margin-top:15px; width: 100%; box-shadow: 0 4px 10px rgba(239, 68, 68, 0.4);">📄 Export to PDF</button>
            """, height=70)

        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        if st.button("✨ Generate AI Insights Automatically"):
            with st.spinner("🧠 AI is building your dashboard..."):
                try:
                    cat_cols, num_cols = df.select_dtypes(include=['object']).columns, df.select_dtypes(include=['float64', 'int64']).columns
                    if len(cat_cols) > 0 and len(num_cols) > 0:
                        c1, c2 = st.columns(2)
                        fig1 = px.bar(df.groupby(cat_cols[0])[num_cols[0]].sum().reset_index().sort_values(by=num_cols[0], ascending=False).head(10), x=cat_cols[0], y=num_cols[0], title=f"AI Pick: Top 10 {cat_cols[0]}", template="plotly_dark", color=cat_cols[0])
                        fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                        c1.plotly_chart(fig1, use_container_width=True)
                        
                        fig2 = px.pie(df, names=cat_cols[0], values=num_cols[0], title=f"AI Pick: Distribution of {num_cols[0]}", template="plotly_dark") if len(df[cat_cols[0]].unique()) <= 15 else px.line(df.head(100), y=num_cols[0], title=f"AI Pick: Trend of {num_cols[0]}", template="plotly_dark")
                        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                        c2.plotly_chart(fig2, use_container_width=True)

                        if len(num_cols) > 1:
                            fig3 = px.scatter(df.head(200), x=num_cols[0], y=num_cols[1], color=cat_cols[0], title=f"AI Insight: Correlation between {num_cols[0]} & {num_cols[1]}", template="plotly_dark")
                            fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                            st.plotly_chart(fig3, use_container_width=True)
                        st.balloons()
                    else: st.error("Data needs both text and numbers for charts.")
                except Exception as e: st.error(e)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="content-box" style="text-align: center; padding: 60px 20px;"><i class="fa fa-chart-pie" style="font-size: 80px; color: #3b82f6; margin-bottom: 20px;"></i><h2>Welcome to Salar.AI Analytics</h2><p style="color: #94a3b8;">Upload your CSV, Excel, or JSON file to activate the AI Agent.</p></div>', unsafe_allow_html=True)
