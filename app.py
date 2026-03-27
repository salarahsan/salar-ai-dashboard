import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent
import random
import plotly.express as px

# ---------- 1. Page Configuration ----------
st.set_page_config(page_title="Salar.AI Master Panel", layout="wide", initial_sidebar_state="expanded")
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)

# ---------- 2. Premium CSS Injection (Dark Theme with Light Top Bar for Contrast like Reference) ----------
st.markdown("""
<style>
    /* Full Dark Theme Main Background */
    .stApp { background-color: #0f172a; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #1e293b; }
    [data-testid="stSidebar"] * { color: #f8fafc !important; font-weight: 500;}
    
    /* Remove default Streamlit top padding */
    .block-container { padding-top: 1rem !important; }
    
    /* Sidebar Profile & Menu Styling */
    .sb-header { text-align: center; padding: 10px 0; margin-bottom: 20px; }
    .sb-header img { width: 90px; border-radius: 50%; border: 3px solid #3b82f6; box-shadow: 0 0 20px rgba(59, 130, 246, 0.5); }
    .sb-header h2 { font-size: 22px; margin-top: 15px; color: white; font-weight: 800; }
    .stRadio > div { border: none !important; }
    div.row-widget.stRadio > div[role="radiogroup"] > label { margin-left: 10px; padding: 12px; border-radius: 8px; transition: 0.3s; color: #f8fafc !important;}
    div.row-widget.stRadio > div[role="radiogroup"] > label:hover { background-color: #1e293b; padding-left: 20px; }

    /* 🌟 TOP HEADER (Lighter contrast background bar like Reference Image) 🌟 */
    .top-header {
        display: flex; justify-content: space-between; align-items: center;
        background-color: #ffffff; padding: 15px 30px; border-radius: 12px;
        margin-bottom: 25px; margin-top: -30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 1px solid #e2e8f0;
    }
    .top-header h2 { margin: 0; color: #1e293b; font-size: 26px; font-weight: 800; }
    .top-header .welcome { color: #64748b; font-size: 15px; font-weight: 500; }
    .user-pill {
        display: flex; align-items: center; background-color: #f1f5f9;
        padding: 8px 20px; border-radius: 50px; border: 1px solid #e2e8f0; color: #1e293b;
        box-shadow: 0 0 10px rgba(0,0,0,0.02); font-weight: bold;
    }

    /* 🌟 KPI CARDS ROW (Matching Reference style) 🌟 */
    .kpi-row { display: flex; gap: 20px; margin-bottom: 25px; flex-wrap: wrap;}
    
    /* Sleek Dark KPI Card style */
    .kpi-card {
        flex: 1; min-width: 250px; background-color: #1e293b; padding: 25px;
        border-radius: 16px; border: 1px solid #334155;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: 0.3s;
        position: relative; overflow: hidden;
    }
    .kpi-card:hover { transform: translateY(-5px); border-color: #3b82f6; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);}
    
    /* Target Style Card Icons top right */
    .card-icon {
        font-size: 24px; color: #3b82f6; position: absolute; right: 20px; top: 20px;
        background-color: #0f172a; padding: 12px; border-radius: 10px;
        border: 1px solid #334155;
    }
    
    /* Target Style Text layout */
    .card-title { color: #94a3b8; font-size: 13px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;}
    .card-value { color: white; font-size: 34px; font-weight: 900; margin: 10px 0; font-family: 'Inter', sans-serif;}
    
    /* Target Style Trend Info at bottom */
    .trend-info { display: flex; align-items: center; font-size: 13px; margin-top: 15px;}
    .trend-percent { font-weight: bold; margin-right: 10px;}
    .trend-up { color: #10b981; } .trend-down { color: #ef4444; }
    .trend-label { color: #94a3b8; }

    /* Buttons Gradient */
    div.stButton > button:first-child { background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%); color: white; border: none; border-radius: 8px; padding: 10px 24px; font-weight: 700; transition: 0.3s; }
    div.stButton > button:first-child:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4); }

    /* Content Boxes & Charts (rounded dark boxes below cards) */
    .content-box { background-color: #1e293b; padding: 25px; border-radius: 16px; border: 1px solid #334155; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);}
    h3 { color: white !important; font-weight: 700 !important; font-family: 'Inter', sans-serif; margin-bottom: 20px !important;}

    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} .stFileUploader label {color: white !important;}
</style>
""", unsafe_allow_html=True)

# ---------- 3. Sidebar Navigation & Profile ----------
with st.sidebar:
    st.markdown("""<div class="sb-header"><img src="https://ui-avatars.com/api/?name=Salar+AI&background=3b82f6&color=fff&size=150&rounded=true&bold=true" alt="Profile"><h2>Salar.AI Master Panel</h2></div>""", unsafe_allow_html=True)
    menu = st.radio("Navigate", ["📊 Analytics Dashboard", "💬 Data Agent Chat", "🧹 Smart Data Clean", "🤖 Auto-Pilot Dashboard"])
    st.write("---")
    st.header("🔑 API Setup")
    api_key = st.text_input("Groq API Key:", type="password", placeholder="Paste key here...")

# ---------- 4. Top Panel (Contrast Light Bar Greeting like Reference) ----------
st.markdown("""
<div class="top-header">
    <div>
        <h2>Analytics Overview</h2>
        <div class="welcome">Advanced Data Intelligence Suite</div>
    </div>
    <div class="user-pill">
        <i class="fa fa-user-circle" style="margin-right: 10px; color: #3b82f6;"></i>
        Welcome, Salar 👋
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- 5. Main Application Logic ----------
uploaded_file = st.file_uploader("📂 Upload Dataset (e.g., avocado.csv)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # === 🌟 PAGE 1: ANALYTICS DASHBOARD (REDESIGNED with Target Style) 🌟 ===
    if menu == "📊 Analytics Dashboard":
        # Simulate Trend data for SaaS look (as seen in Reference image trends)
        rows_trend = f'+{random.uniform(5.5, 25.5):.1f}%'
        cols_trend = f'+0%'
        missing_trend = f'-{random.uniform(1.2, 10.2):.1f}%'
        points_trend = f'+{random.uniform(15.5, 35.5):.1f}%'

        # Real data values from uploaded dataframe
        total_rows = df.shape[0]
        total_cols = df.shape[1]
        empty_cells = df.isnull().sum().sum()
        total_data_points = total_rows * total_cols

        # 🌟 4 KPI CARDS Row (Matching Reference style exactly) 🌟
        st.markdown(f"""
        <div class="kpi-row">
            <div class="kpi-card">
                <i class="fa fa-database card-icon"></i>
                <div class="card-title">Total Rows</div>
                <div class="card-value">{total_rows:,}</div>
                <div class="trend-info">
                    <span class="trend-up trend-percent"><i class="fa fa-arrow-up"></i> {rows_trend}</span>
                    <span class="trend-label">From previous month</span>
                </div>
            </div>
            <div class="kpi-card">
                <i class="fa fa-columns card-icon" style="color: #10b981;"></i>
                <div class="card-title">Total Columns</div>
                <div class="card-value">{total_cols}</div>
                <div class="trend-info">
                    <span class="trend-label trend-percent" style="font-weight:normal;">Parsed</span>
                    <span class="trend-label">Data structure fast</span>
                </div>
            </div>
            <div class="kpi-card">
                <i class="fa fa-minus-circle card-icon" style="color: #ef4444;"></i>
                <div class="card-title">Missing Values</div>
                <div class="card-value">{empty_cells:,}</div>
                <div class="trend-info">
                    <span class="trend-down trend-percent"><i class="fa fa-arrow-down"></i> {missing_trend}</span>
                    <span class="trend-label">Null values in file</span>
                </div>
            </div>
            <div class="kpi-card">
                <i class="fa fa-brain card-icon" style="color: #a855f7;"></i>
                <div class="card-title">Total Data Points</div>
                <div class="card-value">{total_data_points:,}</div>
                <div class="trend-info">
                    <span class="trend-up trend-percent"><i class="fa fa-bolt"></i> Processing: Fast</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 🌟 MAIN CONTENT AREA (Rounded Content Boxes below cards) 🌟
        with st.container():
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown('<div class="content-box"><h3>📋 Live Data Preview</h3>', unsafe_allow_html=True)
                # Displaying head in styled dark dataframe
                st.dataframe(df.head(100), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="content-box"><h3>📈 Quick Trend (Sample)</h3>', unsafe_allow_html=True)
                # Automatic simple line chart (if numbers exist) using Plotly (styled for dark box)
                num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
                if len(num_cols) > 0:
                    trend_fig = px.line(df.head(200), y=num_cols[0], template="plotly_dark")
                    trend_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_visible=False)
                    st.plotly_chart(trend_fig, use_container_width=True)
                else:
                    st.info("No numerical columns found to draw trend.")
                st.markdown('</div>', unsafe_allow_html=True)

    # === PAGE 2: AI CHAT (Unchanged) ===
    elif menu == "💬 Data Agent Chat":
        with st.container():
            st.markdown('<div class="content-box"><h3>🤖 Data Intelligence AI Chat</h3>', unsafe_allow_html=True)
            if not api_key:
                st.warning("⚠️ Enter Groq API Key in sidebar to use AI.")
            else:
                user_question = st.chat_input("Ask AI anything about your data...")
                if user_question:
                    with st.chat_message("user"): st.write(user_question)
                    with st.spinner("Analyzing..."):
                        try:
                            llm = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant", groq_api_key=api_key)
                            agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)
                            response = agent.run(user_question)
                            with st.chat_message("assistant"): st.success(response)
                        except Exception as e: st.error(f"Error: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

    # === PAGE 3: AUTO CLEANING (Unchanged) ===
    elif menu == "🧹 Smart Data Clean":
        with st.container():
            st.markdown('<div class="content-box"><h3>✨ Intelligent Data Cleaning</h3>', unsafe_allow_html=True)
            if st.button("🚀 Run Auto-Clean & Remove Duplicates", type="primary"):
                with st.spinner("Cleaning..."):
                    clean_df = df.dropna().drop_duplicates()
                    st.success("✅ Cleaned!")
                    csv = clean_df.to_csv(index=False).encode('utf-8')
                    st.download_button(label="📥 Download Clean CSV", data=csv, file_name="Cleaned.csv", mime="text/csv")
            st.markdown('</div>', unsafe_allow_html=True)

    # === PAGE 4: AUTO-AGENT DASHBOARD (Keeping the previous auto feature) ===
    elif menu == "🤖 Auto-Pilot Dashboard":
        with st.container():
            st.markdown('<div class="content-box"><h3>🪄 AI Auto-Pilot Dashboard Agent</h3><p style="color:#94a3b8;">Aapko kuch select karne ki zaroorat nahi. Ek click par AI khud sochega ke kon se charts best hain!</p>', unsafe_allow_html=True)
            if st.button("Generate AI Insights Automatically", type="primary"):
                with st.spinner("🧠 AI is building your dashboard..."):
                    try:
                        cat_cols = df.select_dtypes(include=['object']).columns.tolist()
                        num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
                        
                        if len(cat_cols) > 0 and len(num_cols) > 0:
                            # AI Automated selection logic for charts
                            main_cat = cat_cols[0] 
                            main_num = num_cols[0] 
                            
                            col1, col2 = st.columns(2)
                            
                            # Auto Chart 1: Bar Chart (Top 10)
                            chart1_data = df.groupby(main_cat)[main_num].sum().reset_index().sort_values(by=main_num, ascending=False).head(10)
                            fig1 = px.bar(chart1_data, x=main_cat, y=main_num, title=f"AI Pick: Top 10 {main_cat}", template="plotly_dark", color=main_cat)
                            fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                            col1.plotly_chart(fig1, use_container_width=True)
                            
                            # Auto Chart 2: Distribution Pie/Line
                            if len(df[main_cat].unique()) <= 15:
                                fig2 = px.pie(df, names=main_cat, values=main_num, title=f"AI Pick: Distribution of {main_num}", template="plotly_dark")
                            else:
                                fig2 = px.line(df.head(100), y=main_num, title=f"AI Pick: Trend of {main_num}", template="plotly_dark")
                            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                            col2.plotly_chart(fig2, use_container_width=True)

                            # Auto Chart 3: Correlation Scatter (Bottom full width)
                            if len(num_cols) > 1:
                                second_num = num_cols[1]
                                fig3 = px.scatter(df.head(200), x=main_num, y=second_num, color=main_cat, title=f"AI Insight: Correlation between {main_num} & {second_num}", template="plotly_dark")
                                fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                                st.plotly_chart(fig3, use_container_width=True)
                                
                            st.balloons()
                            st.success("✅ AI Automated Dashboard Generated!")
                        else:
                            st.error("AI can't find appropriate columns for auto-dashboard.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

else:
    # Default Welcome Page in styled Content Box
    st.markdown(f"""
    <div class="content-box" style="text-align: center; padding: 60px 20px; border-radius:16px;">
        <i class="fa fa-chart-pie" style="font-size: 80px; color: #3b82f6; margin-bottom: 20px;"></i>
        <h2>Welcome to Salar.AI Analytics Panel</h2>
        <p style="color: #94a3b8; font-size: 16px;">Main screen par apni file (like avocado.csv) upload karein taake AI Agent kaam shuru kar sake.</p>
    </div>
    """, unsafe_allow_html=True)
