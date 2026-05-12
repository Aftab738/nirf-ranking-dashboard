import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import re

# =============================================================================
# 1. PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="NIRF Rankings Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 2. THEME CONFIGURATION (PREMIUM FUTURISTIC DARK)
# =============================================================================

# Define Ultra-Premium 'SaaS-Elite' Dark Theme variables
primary_bg = "#050505"
secondary_bg = "#0f1116"
text_color = "#f8f9fa"
sub_text = "#94a3b8"
accent_main = "#00f2ff"  # Electric Cyan
accent_mid = "#3b82f6"   # Royal Blue
accent_deep = "#7000ff"  # Hyper Purple
premium_gradient = "linear-gradient(135deg, #00f2ff 0%, #3b82f6 50%, #7000ff 100%)"
card_bg = "rgba(15, 17, 22, 0.7)"
card_border = "rgba(255, 255, 255, 0.08)"
card_hover_border = "rgba(0, 242, 255, 0.4)"
card_glow = "rgba(59, 130, 246, 0.15)"
plotly_template = "plotly_dark"
grid_color = "rgba(255, 255, 255, 0.03)"

# Inject Global CSS
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@500;600;700;800&display=swap');

    /* Global Base & Immersive Background */
    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Inter', sans-serif;
        background-color: {primary_bg};
        background-image: 
            radial-gradient(at 0% 0%, rgba(0, 242, 255, 0.06) 0px, transparent 40%),
            radial-gradient(at 100% 0%, rgba(112, 0, 255, 0.06) 0px, transparent 40%),
            radial-gradient(at 50% 50%, rgba(59, 130, 246, 0.03) 0px, transparent 60%);
        color: {text_color};
    }}

    /* Animated Gradient Keyframes */
    @keyframes gradient-move {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* Premium Sidebar & Navigation */
    section[data-testid="stSidebar"] {{
        background: rgba(10, 12, 16, 0.9) !important;
        backdrop-filter: blur(40px) !important;
        -webkit-backdrop-filter: blur(40px) !important;
        border-right: 1px solid {card_border};
        width: 360px !important;
    }}
    section[data-testid="stSidebar"] .stMarkdown h3 {{
        font-family: 'Outfit', sans-serif;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        color: {accent_main};
        margin-top: 2.5rem;
        opacity: 0.9;
        font-weight: 700;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding-bottom: 10px;
    }}
    /* Sidebar Padding Fixes */
    [data-testid="stSidebarUserContent"] {{
        padding: 2.5rem 1.5rem !important;
    }}

    /* Ultra-Modern Card Styling */
    div[data-testid="metric-container"] {{
        background: {card_bg};
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {card_border};
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
    }}
    div[data-testid="metric-container"]::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 2px;
        background: {premium_gradient};
        opacity: 0;
        transition: opacity 0.5s ease;
    }}
    div[data-testid="metric-container"]:hover {{
        transform: translateY(-12px);
        border-color: {card_hover_border};
        box-shadow: 0 20px 50px {card_glow};
    }}
    div[data-testid="metric-container"]:hover::before {{
        opacity: 1;
    }}
    div[data-testid="metric-container"] label {{
        color: {sub_text} !important;
        font-size: 0.75rem !important;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }}
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {{
        font-family: 'Outfit', sans-serif;
        color: #ffffff !important;
        font-size: 2.4rem !important;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-top: 8px;
    }}

    /* SaaS Pill Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 12px;
        background-color: rgba(255, 255, 255, 0.02);
        padding: 10px;
        border-radius: 100px;
        width: fit-content;
        border: 1px solid {card_border};
        margin: 3rem auto;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        border-radius: 100px;
        color: {sub_text};
        font-weight: 600;
        padding: 12px 32px;
        border: none;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        font-family: 'Outfit', sans-serif;
        letter-spacing: 0.02em;
    }}
    .stTabs [aria-selected="true"] {{
        background: {premium_gradient} !important;
        background-size: 200% auto !important;
        animation: gradient-move 3s ease infinite !important;
        color: #ffffff !important;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
    }}
    .stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {{
        color: #ffffff;
        background: rgba(255, 255, 255, 0.05);
    }}

    /* Branding & Hero Header */
    .hero-section {{
        text-align: center;
        padding: 2rem 0 3rem 0;
        position: relative;
    }}
    .logo-container {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 80px; height: 80px;
        background: {premium_gradient};
        border-radius: 22px;
        margin-bottom: 1.5rem;
        box-shadow: 0 15px 35px rgba(0, 242, 255, 0.3);
        transform: rotate(-5deg);
        transition: all 0.5s ease;
    }}
    .logo-container:hover {{
        transform: rotate(0deg) scale(1.1);
        box-shadow: 0 20px 45px rgba(112, 0, 255, 0.4);
    }}
    .logo-icon {{
        font-size: 40px;
        filter: drop-shadow(0 0 10px rgba(255,255,255,0.5));
    }}
    .main-title {{
        font-family: 'Outfit', sans-serif;
        background: {premium_gradient};
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-move 4s linear infinite;
        font-size: 3.8rem !important;
        font-weight: 900 !important;
        letter-spacing: -0.04em !important;
        margin: 0 !important;
        line-height: 1.1;
    }}
    .sub-title {{
        color: {sub_text};
        font-size: 1.25rem;
        font-weight: 500;
        margin-top: 1rem;
        letter-spacing: 0.02em;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }}

    /* Buttons & Controls */
    .stButton>button {{
        border-radius: 16px;
        border: 1px solid {card_border};
        background: rgba(255, 255, 255, 0.03);
        color: #ffffff;
        padding: 12px 28px;
        font-weight: 700;
        font-family: 'Outfit', sans-serif;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 0.08em;
    }}
    .stButton>button:hover {{
        background: {premium_gradient};
        border-color: transparent;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
        transform: translateY(-4px) scale(1.05);
    }}

    /* Global Overrides & Accessibility */
    .block-container {{
        padding: 4rem 8% 12rem 8% !important;
        max-width: 1700px;
    }}
    footer {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    
    /* Keep Sidebar Toggle Accessible but Hide Header Background */
    header {{
        background-color: transparent !important;
    }}
    [data-testid="stHeader"] {{
        background: transparent !important;
    }}
    button[kind="header"] {{
        color: {accent_main} !important;
        background: rgba(255,255,255,0.05) !important;
        border-radius: 10px !important;
    }}

    /* Footer Styling */
    .footer {{
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: rgba(5, 5, 5, 0.95);
        border-top: 1px solid {card_border};
        color: {sub_text};
        backdrop-filter: blur(30px);
        font-size: 0.85rem;
        padding: 24px;
        text-align: center;
        z-index: 999;
        font-weight: 500;
        letter-spacing: 0.05em;
    }}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 3. HELPER FUNCTIONS & MAPS
# =============================================================================

_CITY_ALIASES = {
    "Bangalore": "Bengaluru", "Bombay": "Mumbai", "Calcutta": "Kolkata",
    "Trivandrum": "Thiruvananthapuram",
    "Mysore": "Mysuru", "Poona": "Pune"
}

_INST_ALIASES = {
    "Indian Institute Of Technology Madras": "IIT Madras",
    "Indian Institute Of Technology Chennai": "IIT Madras",
    "Indian Institute Of Technology Bombay": "IIT Bombay",
    "Indian Institute Of Technology Mumbai": "IIT Bombay",
    "Indian Institute Of Technology Delhi": "IIT Delhi",
    "Indian Institute Of Technology Kharagpur": "IIT Kharagpur",
    "Indian Institute Of Technology Kanpur": "IIT Kanpur",
    "Indian Institute Of Technology Roorkee": "IIT Roorkee",
    "Indian Institute Of Technology Guwahati": "IIT Guwahati",
    "Indian Institute Of Technology Hyderabad": "IIT Hyderabad",
    "Indian Institute Of Science": "IISc Bengaluru",
    "Indian Institute Of Science Bengaluru": "IISc Bengaluru",
    "Jawaharlal Nehru University": "JNU New Delhi",
    "University Of Delhi": "Delhi University",
    "Jadavpur University": "Jadavpur Univ.",
    "Vellore Institute Of Technology": "VIT Vellore",
    "Birla Institute Of Technology & Science": "BITS Pilani"
}

def standardize_name(name: str) -> str:
    if not isinstance(name, str): return name
    name = re.sub(r'\s+', ' ', name.strip())
    name = re.sub(r',\s*(?=[A-Za-z])', ' ', name)
    name = re.sub(r',\s*\)', ')', name)
    name = name.rstrip(',').strip()
    name = re.sub(r'\s{2,}', ' ', name).title()
    for alias, canonical in _CITY_ALIASES.items():
        name = re.sub(rf'\b{re.escape(alias)}\b', canonical, name, flags=re.IGNORECASE)
    return name

def apply_short_alias(name: str) -> str:
    return _INST_ALIASES.get(name, name)

def ranked_label(rank_num: int, name: str, max_len: int = 38) -> str:
    prefix = f"#{int(rank_num)}  "
    aliased = apply_short_alias(name)
    trunc = aliased if len(aliased) <= max_len else aliased[:max_len-1].rstrip() + "…"
    return prefix + trunc

# =============================================================================
# 4. DATA LOADING
# =============================================================================

@st.cache_data
def load_data():
    file_path = os.path.join("data", "cleaned", "nirf_merged.csv")
    try:
        df = pd.read_csv(file_path)
    except Exception:
        return pd.DataFrame()

    if "Institute Name" in df.columns:
        df["Institute Name"] = df["Institute Name"].apply(standardize_name)

    numeric_cols = ["Score", "TLR", "RPC", "GO", "OI", "PERCEPTION"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Rank" in df.columns:
        df["Numeric_Rank"] = df["Rank"].astype(str).str.extract(r"(\d+)")[0].pipe(pd.to_numeric, errors="coerce")

    if "Year" in df.columns and "Score" in df.columns:
        df = df.sort_values("Score", ascending=False).drop_duplicates(subset=["Institute Name", "Year"]).reset_index(drop=True)

    for col in ["State", "City"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown").str.strip()
    
    return df

df = load_data()
if df.empty:
    st.error("Dataset not found or empty.")
    st.stop()

# =============================================================================
# 5. SIDEBAR FILTERS
# =============================================================================

st.sidebar.divider()
st.sidebar.subheader("🎯 Primary Filters")

all_years = sorted(df["Year"].dropna().unique().tolist(), reverse=True)
selected_year = st.sidebar.selectbox("📅 Select Year", ["All Years"] + all_years)
df_y = df if selected_year == "All Years" else df[df["Year"] == selected_year]

all_states = sorted(df_y["State"].unique().tolist())
selected_state = st.sidebar.selectbox("📍 Select State", ["All States"] + all_states)
df_s = df_y if selected_state == "All States" else df_y[df_y["State"] == selected_state]

with st.sidebar.expander("📊 Visualization Settings", expanded=False):
    top_n = st.selectbox("Show Top N Institutes", options=[10, 25, 50, 100], index=0)

st.sidebar.divider()
st.sidebar.subheader("🔍 Institute Lookup")
search_q = st.sidebar.text_input("Search Name", placeholder="e.g. IIT Madras")
inst_list = sorted(df_s["Institute Name"].dropna().unique().tolist())
if search_q:
    inst_list = [i for i in inst_list if search_q.lower() in i.lower()]
selected_inst = st.sidebar.selectbox("Select Institute", ["All Institutes"] + inst_list)

filtered_df = df_s.copy()
if selected_inst != "All Institutes":
    filtered_df = filtered_df[filtered_df["Institute Name"] == selected_inst]

st.sidebar.divider()
st.sidebar.markdown(f"✅ **{len(filtered_df):,}** entries loaded")

# =============================================================================
# 6. MAIN HEADER
# =============================================================================

h_col1, h_col2 = st.columns([0.85, 0.15])
with h_col1:
    st.markdown(f"""
        <div class="hero-section">
            <div class="logo-container">
                <span class="logo-icon">🎓</span>
            </div>
            <h1 class="main-title">Analysis of NIRF Rankings for Indian Universities</h1>
            <p class="sub-title">An interactive data visualization dashboard for analyzing NIRF rankings, institutional performance, and ranking trends across Indian universities.</p>
        </div>
    """, unsafe_allow_html=True)

with h_col2:
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Data", width="stretch"):
        st.cache_data.clear()
        st.rerun()

st.divider()

# =============================================================================
# 7. TABS
# =============================================================================

tabs = st.tabs(["📖 Introduction", "📊 Overview", "🗺️ State Analysis", "📈 Score Analysis", "📉 Ranking Trends", "💡 Key Insights", "📁 Dataset Explorer"])
tab_intro, tab_overview, tab_state, tab_scores, tab_trends, tab_insights, tab_data = tabs

# --- TAB 1: INTRODUCTION ---
with tab_intro:
    st.header("About NIRF")
    il, ir = st.columns([2, 1])
    with il:
        st.markdown(f"""
        <div style="background:{card_bg}; padding:30px; border-radius:20px; border:1px solid {card_border}; margin-bottom:30px; backdrop-filter: blur(10px);">
        The <b>National Institutional Ranking Framework (NIRF)</b> was launched by the Ministry of Education in 2015 to rank higher-education institutions across India using a robust, transparent methodology.
        </div>
        
        ### 📊 The Five Ranking Parameters
        | Parameter | Full Name | Weight |
        |-----------|-----------|--------|
        | **TLR** | Teaching, Learning & Resources | ~30% |
        | **RPC** | Research and Professional Practice | ~30% |
        | **GO** | Graduation Outcomes | ~20% |
        | **OI** | Outreach and Inclusivity | ~10% |
        | **PERCEPTION** | Peer Perception | ~10% |
        """, unsafe_allow_html=True)
    with ir:
        st.info("📌 **Tip:** Use the sidebar to filter by Year and State. All charts update instantly.")
        st.success(f"📦 **Dataset:** {df['Institute Name'].nunique():,} unique institutes · {df['Year'].nunique()} years")

# --- TAB 2: OVERVIEW ---
with tab_overview:
    y_label = f"— {selected_year}" if selected_year != "All Years" else "— All Years"
    st.header(f"Dataset Overview {y_label}")
    
    if filtered_df.empty:
        st.warning("No data found for the current selection.")
    else:
        # Metrics Row 1
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("🏢 Total Institutes", f"{filtered_df['Institute Name'].nunique():,}")
        m2.metric("📈 Avg. Overall Score", f"{filtered_df['Score'].mean():.2f}")
        m3.metric("📍 States Covered", f"{filtered_df['State'].nunique()}")
        m4.metric("🗓️ Years Covered", f"{filtered_df['Year'].nunique()}")
        
        top_inst = "N/A"
        if not filtered_df.empty and not filtered_df["Numeric_Rank"].isnull().all():
            top_inst = str(filtered_df.sort_values("Numeric_Rank")["Institute Name"].iloc[0])
            top_inst = (top_inst[:25] + "...") if len(top_inst) > 28 else top_inst
        m5.metric("🥇 Top Ranked", top_inst)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"#### 🚀 Performance Leaders {y_label}")
        
        # Metrics Row 2
        l1, l2, l3 = st.columns(3)
        if filtered_df["Score"].notna().any():
            row = filtered_df.loc[filtered_df["Score"].idxmax()]
            l1.metric("🌟 Highest Score", f"{row['Score']:.2f}", help=f"By: {row['Institute Name']}")
        if filtered_df["RPC"].notna().any():
            row = filtered_df.loc[filtered_df["RPC"].idxmax()]
            l2.metric("🔬 Best Research (RPC)", f"{row['RPC']:.2f}", help=f"By: {row['Institute Name']}")
        if filtered_df["TLR"].notna().any():
            row = filtered_df.loc[filtered_df["TLR"].idxmax()]
            l3.metric("📚 Best Teaching (TLR)", f"{row['TLR']:.2f}", help=f"By: {row['Institute Name']}")

        st.divider()
        st.subheader(f"🏆 Top {top_n} Institutes by Overall Score")
        
        top_n_df = filtered_df.sort_values("Score", ascending=False).drop_duplicates("Institute Name").head(top_n).reset_index(drop=True).copy()
        if not top_n_df.empty:
            top_n_df["Chart_Rank"] = range(1, len(top_n_df) + 1)
            top_n_df["Y_Label"] = top_n_df.apply(lambda r: ranked_label(r["Chart_Rank"], r["Institute Name"]), axis=1)
            
            fig = px.bar(top_n_df, x="Score", y="Y_Label", orientation="h", color="Score", color_continuous_scale="Blues", text="Score",
                         custom_data=["Institute Name", "State", "Score", "TLR", "RPC", "GO", "OI", "PERCEPTION"],
                         height=min(max(420, top_n * 32), 2800))
            fig.update_traces(texttemplate="%{text:.2f}", textposition="outside",
                              hovertemplate="<b>%{customdata[0]}</b><br>Overall Score: %{customdata[2]:.2f}<br>State: %{customdata[1]}<br>TLR: %{customdata[3]:.2f}<br>RPC: %{customdata[4]:.2f}<extra></extra>")
            fig.update_layout(yaxis=dict(categoryorder="total ascending", title=""), xaxis=dict(title="Score", gridcolor=grid_color),
                              template=plotly_template, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=70, t=20, b=20), coloraxis_showscale=False)
            st.plotly_chart(fig, width="stretch")

# --- TAB 3: STATE ANALYSIS ---
with tab_state:
    st.header("State-wise Analysis")
    if filtered_df.empty:
        st.warning("No data available.")
    else:
        sl, sr = st.columns(2)
        with sl:
            st.subheader("Institute Count by State")
            counts = filtered_df["State"].value_counts().reset_index()
            counts.columns = ["State", "Count"]
            fig = px.treemap(counts, path=["State"], values="Count", color="Count", color_continuous_scale="Teal")
            fig.update_layout(template=plotly_template, paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig, use_container_width=True)
        with sr:
            st.subheader(f"Avg Score (Top {top_n} Institutes)")
            top_state_df = filtered_df.sort_values("Score", ascending=False).drop_duplicates("Institute Name").head(top_n)
            avg = top_state_df.groupby("State")["Score"].mean().reset_index().sort_values("Score", ascending=True)
            fig = px.bar(avg, x="Score", y="State", orientation="h", color="Score", color_continuous_scale="Blues", text="Score")
            fig.update_layout(
                template=plotly_template, 
                paper_bgcolor="rgba(0,0,0,0)", 
                plot_bgcolor="rgba(0,0,0,0)", 
                xaxis=dict(gridcolor=grid_color, title="Average Score"),
                yaxis=dict(title=""),
                coloraxis_showscale=False,
                margin=dict(l=0, r=40, t=10, b=10)
            )
            st.plotly_chart(fig, width="stretch")

# --- TAB 4: SCORE ANALYSIS ---
with tab_scores:
    st.header("Score Breakdown & Correlations")
    sc = ["Score", "TLR", "RPC", "GO", "OI", "PERCEPTION"]
    vdf = filtered_df.dropna(subset=sc, how="all")
    if len(vdf) < 3:
        st.warning("Insufficient data for correlation analysis.")
    else:
        cl, cr = st.columns(2)
        with cl:
            st.subheader("TLR vs RPC (Size = Perception)")
            fig = px.scatter(vdf, x="TLR", y="RPC", color="Score", size=vdf["PERCEPTION"].clip(lower=1), 
                             hover_name="Institute Name", color_continuous_scale="Viridis", size_max=25)
            fig.update_layout(
                template=plotly_template, 
                paper_bgcolor="rgba(0,0,0,0)", 
                plot_bgcolor="rgba(0,0,0,0)", 
                xaxis=dict(gridcolor=grid_color), 
                yaxis=dict(gridcolor=grid_color),
                margin=dict(l=0, r=0, t=20, b=0)
            )
            st.plotly_chart(fig, width="stretch")
        with cr:
            st.subheader("Correlation Heatmap")
            corr = vdf[sc].corr().round(2)
            fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r")
            fig.update_layout(
                template=plotly_template, 
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=20, b=0)
            )
            st.plotly_chart(fig, width="stretch")
        
        st.divider()
        st.subheader("Parameter Distribution")
        p = st.selectbox("Select Parameter", sc)
        fig = px.histogram(vdf, x=p, nbins=30, marginal="box", color_discrete_sequence=["#3b82f6"])
        fig.update_layout(template=plotly_template, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(gridcolor=grid_color), yaxis=dict(gridcolor=grid_color))
        st.plotly_chart(fig, width="stretch")

# --- TAB 5: TRENDS ---
with tab_trends:
    st.header("Historical Ranking Trends")
    if selected_inst != "All Institutes":
        ts = df[df["Institute Name"] == selected_inst].copy()
    else:
        ly = df["Year"].max()
        top5 = df[df["Year"] == ly].sort_values("Numeric_Rank").drop_duplicates("Institute Name").head(5)["Institute Name"]
        ts = df[df["Institute Name"].isin(top5)].copy()
        st.info("ℹ️ Showing Top 5 institutes by default. Select one in sidebar for details.")
    
    if ts.empty or ts["Numeric_Rank"].isnull().all():
        st.warning("No trend data available.")
    else:
        ts = ts.sort_values("Year")
        # Apply short aliases for the legend labels
        ts["Display_Name"] = ts["Institute Name"].apply(apply_short_alias)
        
        fig = px.line(
            ts, 
            x="Year", 
            y="Numeric_Rank", 
            color="Display_Name", 
            markers=True,
            custom_data=["Institute Name", "Score"], # Pass full name and score for hover
            height=500,
            labels={"Numeric_Rank": "Rank", "Year": "Year", "Display_Name": "Institute"}
        )
        
        # Invert Y-axis and ensure integer ticks only
        fig.update_yaxes(
            autorange="reversed", 
            gridcolor=grid_color,
            dtick=1, # Force integer steps
            tickformat="d" # Display as integer
        )
        
        fig.update_xaxes(type="category", gridcolor=grid_color)
        
        # Custom hover tooltip: Full Name, Year, Rank, Score
        fig.update_traces(
            connectgaps=True,
            line=dict(width=3),
            marker=dict(size=10),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Year: %{x}<br>"
                "Rank: %{y}<br>"
                "Score: %{customdata[1]:.2f}"
                "<extra></extra>"
            )
        )
        
        fig.update_layout(
            template=plotly_template, 
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)", 
            legend=dict(
                bgcolor="rgba(21, 25, 33, 0.8)",
                title="",
                font=dict(size=11),
                bordercolor=card_border,
                borderwidth=1
            ),
            margin=dict(l=40, r=20, t=40, b=40)
        )
        st.plotly_chart(fig, width="stretch")

# --- TAB 6: INSIGHTS ---
with tab_insights:
    st.header("💡 Key Insights")
    avg_s = df.groupby("State")["Score"].mean().sort_values(ascending=False)
    ti = df.sort_values("Score", ascending=False).drop_duplicates("Institute Name").iloc[0]
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div style="background:{card_bg}; padding:25px; border-radius:15px; border:1px solid {card_border}; backdrop-filter: blur(5px);">
        #### 📌 Quick Stats
        | Metric | Value |
        |--------|-------|
        | Total unique institutes | {df['Institute Name'].nunique():,} |
        | Highest overall score | {ti['Score']:.2f} ({ti['Institute Name']}) |
        | Top state by avg score | {avg_s.index[0]} ({avg_s.iloc[0]:.2f}) |
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style="background:{card_bg}; padding:25px; border-radius:15px; border:1px solid {card_border}; backdrop-filter: blur(5px);">
        - 🔬 <b>Research drives top ranks.</b> RPC scores are strong predictors of overall standing.
        - 📍 <b>Regional clusters.</b> TN, MH, and DL dominate the Top 100.
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("Share of Top-50 Institutes by State (Latest Year)")
    ly = df["Year"].max()
    t50 = df[df["Year"] == ly].sort_values("Numeric_Rank").drop_duplicates("Institute Name").head(50)
    ss = t50["State"].value_counts().reset_index()
    ss.columns = ["State", "Count"]
    fig = px.pie(ss, names="State", values="Count", hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(template=plotly_template, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, width="stretch")

# --- TAB 7: EXPLORER ---
with tab_data:
    st.header("📁 Dataset Explorer")
    cols = ["Institute Name", "Year", "State", "City", "Rank", "Score", "TLR", "RPC", "GO", "OI", "PERCEPTION"]
    st.dataframe(filtered_df[[c for c in cols if c in filtered_df.columns]].reset_index(drop=True), width="stretch", height=450)
    st.download_button("📥 Download Filtered CSV", data=filtered_df.to_csv(index=False).encode("utf-8"), file_name="nirf_filtered.csv", mime="text/csv")

# =============================================================================
# 8. FOOTER
# =============================================================================
st.markdown("""<div class="footer">NIRF Rankings Dashboard &nbsp;|&nbsp; Streamlit &bull; Plotly &bull; Pandas</div>""", unsafe_allow_html=True)
