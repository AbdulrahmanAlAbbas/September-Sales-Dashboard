import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="September Sales Dashboard", layout="wide")

# ---- Title with Logo ----
col1, col2 = st.columns([7, 1]) 

with col1:
    st.markdown(
        """
        <h1 style="color:#000000; font-size:36px; margin-top:15px; margin-bottom:5px;">
            📊 September Sales Dashboard
        </h1>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThAsJgb1nN-XLqXMsXh6DYAE-qTUf1lEG2tw&s",
        width=100
    )

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("sales_sept_2025.csv")
    return df

df = load_data()

# ---- Custom CSS ----
st.markdown("""
    <style>
        .metric-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            text-align: center;
            height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .metric-card h4 {
            font-size: 16px;
            color: #666;
            margin-bottom: 6px;
        }
        .metric-card h2 {
            font-size: 28px;
            margin: 0;
            color: #222;
        }
        .metric-card p {
            font-size: 13px;
            margin-top: 4px;
        }
        .positive { color: green; }
        .negative { color: red; }
        .neutral { color: gray; }
        .main-container {
            max-width: 90%;
            margin: auto;
        }
        [data-testid="stPlotlyChart"] > div {
            background: white;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            padding: 10px;
            margin: 10px 0;
            overflow: hidden;
        }
                
        [data-testid="stSelectbox"] {
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        padding: 10px;
        margin: 10px 0;
        }
        
        [data-testid="stSelectbox"] {
            margin-bottom: 2px !important;  
        }
        
        [data-testid="stPlotlyChart"] > div,
            .stPlotlyChart > div,
            .plot-card {
            background: #fff !important;
            border-radius: 15px !important;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2) !important;
            padding: 10px !important;
            margin: 10px 0 !important;            
            overflow: hidden !important;
            max-width: 98.4% !important;      
        }

        .plot-card .js-plotly-plot,
        .stPlotlyChart .js-plotly-plot {
        border-radius: 15px !important;
        } 
         </style>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border:2px solid #007BFF'>", unsafe_allow_html=True)

# ---- KPIs ----
total_net = df["Net_Sales"].sum()
total_discount = df["Discount_Amount"].sum()
total_orders = df["Orders"].sum()

# ---- العنوان ----
st.subheader("📊 September Month Total Numbers")

# ---- الكاردز ----
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <h4>Total Net Sales</h4>
            <h2 style="display:flex;align-items:center;justify-content:center;gap:6px;">
                {total_net:,.0f}
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Saudi_Riyal_Symbol.svg/500px-Saudi_Riyal_Symbol.svg.png" 
                     alt="SAR" width="25" height="25">
            </h2>
        </div>
        """, unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <h4>Total Orders</h4>
            <h2>{total_orders:,}</h2>
        </div>
        """, unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <h4>Total Discounts</h4>
            <h2 style="display:flex;align-items:center;justify-content:center;gap:6px;">
                {total_discount:,.0f}
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Saudi_Riyal_Symbol.svg/500px-Saudi_Riyal_Symbol.svg.png" 
                     alt="SAR" width="25" height="25">
            </h2>
        </div>
        """, unsafe_allow_html=True
    )

st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

# ---- خط فاصل ----
st.markdown("<hr style='border:2px solid #007BFF'>", unsafe_allow_html=True)

# ---- عرض الجدول كامل ----
# ---- فرز تنازلي حسب صافي المبيعات ----
df = df.sort_values(by="Net_Sales", ascending=False)

# ---- تنسيق الأرقام بدون كسور ----
df["Net_Sales"] = df["Net_Sales"].round(0).astype(int)
df["Orders"] = df["Orders"].round(0).astype(int)
df["Discount_Amount"] = df["Discount_Amount"].round(0).astype(int)

# ---- عرض الجدول ----
st.subheader("📑 Detailed Branch Sales Data - September 2025")
st.dataframe(df, use_container_width=True)

st.markdown("<hr style='border:2px solid #007BFF'>", unsafe_allow_html=True)

# ---- حساب نسبة المساهمة ----
totals_by_branch = df.groupby("Branch").agg({
    "Net_Sales": "sum"
}).reset_index()

total_sales = totals_by_branch["Net_Sales"].sum()
totals_by_branch["Contribution %"] = (totals_by_branch["Net_Sales"] / total_sales * 100).round(2)

# ترتيب تنازلي
totals_by_branch = totals_by_branch.sort_values("Net_Sales", ascending=False).reset_index(drop=True)

# ---- دالة التلوين ----
def highlight_contribution(val):
    if val >= 5:
        return "background-color: #d4edda; color: green;"       # أخضر فاتح
    elif val >= 1:
        return "background-color: #fff3cd; color: #856404;"     # أصفر فاتح
    else:
        return "background-color: #f8d7da; color: red;"         # أحمر فاتح

# ---- عرض الجدول في Streamlit ----
st.subheader("🏬 Contribution of Each Branch to Total Net Sales")
st.dataframe(
    totals_by_branch.style.format({
        "Net_Sales": "{:,.0f}",
        "Contribution %": "{:.2f}%"
    }).applymap(highlight_contribution, subset=["Contribution %"]),
    use_container_width=True
)

st.markdown("<hr style='border:2px solid #007BFF'>", unsafe_allow_html=True)

# ---- حساب AOV لكل فرع ----
aov_by_branch = df.copy()
aov_by_branch["AOV"] = (aov_by_branch["Net_Sales"] / aov_by_branch["Orders"]).round(2)

# ترتيب تنازلي حسب AOV
aov_by_branch = aov_by_branch[["Branch", "Net_Sales", "Orders", "AOV"]].sort_values("AOV", ascending=False).reset_index(drop=True)

# ---- عرض في Streamlit ----
st.subheader("💰 Average Order Value (AOV) per Branch")
st.dataframe(
    aov_by_branch.style.format({
        "Net_Sales": "{:,.0f}",
        "Orders": "{:,.0f}",
        "AOV": "{:,.2f}"
    }),
    use_container_width=True
)

st.markdown("<hr style='border:2px solid #007BFF'>", unsafe_allow_html=True)

# ---- أعلى 10 فروع ----
st.subheader("🏆 Top 10 Branches by Net Sales")
top10 = df.nlargest(10, "Net_Sales")

fig_top10 = px.bar(
    top10,
    x="Branch",
    y="Net_Sales",
    title="🏆 Top 10 Branches by Net Sales",
    text="Net_Sales",
    color="Net_Sales",
    color_continuous_scale="Blues"
)
fig_top10.update_traces(texttemplate="%{text:,.0f}", textposition="inside")
fig_top10.update_layout(yaxis_title="Net Sales", xaxis_title="Branch")

st.plotly_chart(fig_top10, use_container_width=True)

st.markdown("<hr style='border:2px solid #007BFF'>", unsafe_allow_html=True)

# ---- أقل 10 فروع ----
st.subheader("⬇️ Bottom 10 Branches by Net Sales")
bottom10 = df.nsmallest(10, "Net_Sales")

fig_bottom10 = px.bar(
    bottom10,
    x="Branch",
    y="Net_Sales",
    title="⬇️ Bottom 10 Branches by Net Sales",
    text="Net_Sales",
    color="Net_Sales",
    color_continuous_scale="Reds"
)
fig_bottom10.update_traces(texttemplate="%{text:,.0f}", textposition="inside")
fig_bottom10.update_layout(yaxis_title="Net Sales", xaxis_title="Branch")

st.plotly_chart(fig_bottom10, use_container_width=True)

st.markdown("<hr style='border:2px solid #007BFF'>", unsafe_allow_html=True)

st.subheader("📊 Branch Comparison (Net Sales / Discounts / Orders)")

# ---- فلتر لاختيار أكثر من فرع ----
branches_list = df["Branch"].unique()
selected_branches = st.multiselect(
    "Select Branches to Compare", 
    branches_list, 
    default=branches_list[:2]
)

if selected_branches:
    # فلترة حسب الفروع
    branch_multi = df[df["Branch"].isin(selected_branches)]

    # تجميع البيانات
    totals_by_branch = branch_multi.groupby("Branch").agg({
        "Net_Sales": "sum",
        "Discount_Amount": "sum",
        "Orders": "sum"
    }).reset_index()

    # ---- Bar Chart مع أزرار التبديل ----
    fig_compare = go.Figure()

    # Net Sales
    fig_compare.add_trace(go.Bar(
        x=totals_by_branch["Branch"], 
        y=totals_by_branch["Net_Sales"],
        name="Net Sales",
        marker_color="#2ecc71",
        texttemplate="%{y:,.0f}",
        textposition="inside",
        textfont=dict(size=18, color="white")
    ))

    # Discounts
    fig_compare.add_trace(go.Bar(
        x=totals_by_branch["Branch"], 
        y=totals_by_branch["Discount_Amount"],
        name="Discounts",
        marker_color="red",
        visible=False,
        texttemplate="%{y:,.0f}",
        textposition="inside",
        textfont=dict(size=14, color="white")
    ))

    # Orders
    fig_compare.add_trace(go.Bar(
        x=totals_by_branch["Branch"], 
        y=totals_by_branch["Orders"],
        name="Orders",
        marker_color="blue",
        visible=False,
        texttemplate="%{y:,.0f}",
        textposition="inside",
        textfont=dict(size=14, color="white")
    ))

    # ---- إعداد الأزرار ----
    fig_compare.update_layout(
        barmode="group",
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=[
                    dict(label="Net Sales",
                         method="update",
                         args=[{"visible": [True, False, False]},
                               {"title": {"text": "Net Sales by Branch"}}]),
                    dict(label="Discounts",
                         method="update",
                         args=[{"visible": [False, True, False]},
                               {"title": {"text": "Discounts by Branch"}}]),
                    dict(label="Orders",
                         method="update",
                         args=[{"visible": [False, False, True]},
                               {"title": {"text": "Orders by Branch"}}]),
                ],
                x=0.5, y=1.15, xanchor="center", yanchor="top"
            )
        ],
        title={"text": "Branch Comparison"},
        showlegend=True
    )

    fig_compare.update_yaxes(tickformat="d")

    st.plotly_chart(fig_compare, use_container_width=True)
else:
    st.info("Please select at least one branch to display the chart.")