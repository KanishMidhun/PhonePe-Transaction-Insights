import pandas as pd
import plotly.express as px
import streamlit as st

# ===============================
# 📌 Load Data
# ===============================
df = pd.read_csv("agg_trans.csv")  

# Ensure correct types
df["Year"] = df["Year"].astype(int)
df["Quarter"] = df["Quarter"].astype(int)
df["Transaction_amount"] = pd.to_numeric(df["Transaction_amount"], errors="coerce").fillna(0)
df["Transaction_count"] = pd.to_numeric(df["Transaction_count"], errors="coerce").fillna(0)

# Create Period label
df["Period"] = df["Year"].astype(str) + "-Q" + df["Quarter"].astype(str)

# ===============================
# 📌 Aggregate by State + Period
# ===============================
agg = df.groupby(["State", "Year", "Quarter"], as_index=False).agg(
    Total_Amount=("Transaction_amount", "sum"),
    Total_Count=("Transaction_count", "sum")
)
agg["Avg_Transaction"] = agg["Total_Amount"] / agg["Total_Count"]
agg["Period"] = agg["Year"].astype(str) + "-Q" + agg["Quarter"].astype(str)

# ===============================
# 📌 Streamlit UI
# ===============================
st.title("📊 PhonePe Transaction Dynamics with India Map")

year = st.selectbox("Select Year", sorted(agg["Year"].unique()))
quarter = st.selectbox("Select Quarter", sorted(agg["Quarter"].unique()))
metric = st.radio("Select Metric", ["Total_Amount", "Avg_Transaction"])

# Filter data
filtered = agg[(agg["Year"] == year) & (agg["Quarter"] == quarter)]

# ===============================
# 📌 Choropleth Map
# ===============================
# India states GeoJSON (official boundaries)
india_states_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

fig = px.choropleth(
    filtered,
    geojson=india_states_url,
    featureidkey="properties.ST_NM",
    locations="State",
    color=metric,
    color_continuous_scale="Viridis",
    title=f"India Map of {metric.replace('_',' ')} - Q{quarter} {year}"
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(height=600, title_font=dict(size=24, color="#6739b7"))

st.plotly_chart(fig, use_container_width=True)

# ===============================
# 📌 Extra: Show Table
# ===============================
st.subheader("📋 Data Table")
st.dataframe(filtered[["State", "Total_Amount", "Total_Count", "Avg_Transaction"]].sort_values(by=metric, ascending=False))


# ===============================
# 📌 Sidebar Navigation
# ===============================
st.sidebar.title("📊 PhonePe Dashboard")
scenario = st.sidebar.radio(
    "Choose Scenario",
    [
        "1. Transaction Dynamics",
        "2. Device Dominance",
        "3. Insurance Penetration",
        "4. Transaction Expansion",
        "5. Insurance Engagement"
    ])






# ===============================
# 📌1. Payment Categories Across States
# ===============================
if scenario.startswith("1"):

    df1 = pd.read_csv("agg_trans.csv")

    # Ensure proper types
    df1["Year"] = df1["Year"].astype(int)
    df1["Quarter"] = df1["Quarter"].astype(int)
    df1["Transaction_amount"] = pd.to_numeric(df1["Transaction_amount"], errors="coerce").fillna(0)
    df1["Transaction_count"] = pd.to_numeric(df1["Transaction_count"], errors="coerce").fillna(0)

    df1["Period"] = df1["Year"].astype(str) + "-Q" + df1["Quarter"].astype(str)

    # ===============================
    # 📌 Streamlit UI
    # ===============================
    st.title("💳 Payment Categories Across States")

    # Sidebar filters
    year = st.selectbox("Select Year", sorted(df1["Year"].unique()),key="payment_category_year")
    quarter = st.selectbox("Select Quarter", sorted(df1["Quarter"].unique()),key="payment_category_quarter")
    state = st.selectbox("Select State", ["All States"] + sorted(df1["State"].unique()),key="payment_category_state")

    # Filter by Year + Quarter (+ State if chosen)
    filtered = df1[(df1["Year"] == year) & (df1["Quarter"] == quarter)]
    if state != "All States":
        filtered = filtered[filtered["State"] == state]

    # ===============================
    # 📊 Visualization : Category Split (Bar Chart)
    # ===============================
    st.subheader(f"📊 Payment Categories in {state if state!='All States' else 'All States'} - Q{quarter} {year}")

    fig_bar = px.bar(
        filtered,
        x="Transaction_type",
        y="Transaction_amount",
        color="Transaction_type",
        text="Transaction_amount",
        title="Transaction Amount by Payment Category",
        labels={"Transaction_amount": "Total Amount"}
    )
    fig_bar.update_traces(texttemplate='%{text:.2s}', textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)
    # ===============================
    # 📊 Visualization : Trend Over Time
    # ===============================
    st.subheader("📈 Category Trend Over Time (Nationwide)")
    trend = df1.groupby(["Period", "Transaction_type"], as_index=False).agg({"Transaction_amount": "sum"})

    fig_line = px.line(
        trend,
        x="Period",
        y="Transaction_amount",
        color="Transaction_type",
        markers=True,
        title="Trend of Payment Categories Over Time"
    )
    st.plotly_chart(fig_line, use_container_width=True)
    # ===============================
    # 📋 Data Table
    # ===============================
    st.subheader("📋 Filtered Data")
    st.dataframe(filtered.sort_values(by="Transaction_amount", ascending=False))


# ===============================
# 📌2. Device Dominance & User Engagement
# ===============================

elif scenario.startswith("2"):
    df_user=pd.read_csv("agg_user.csv")
    st.title("📱 Device Dominance & User Engagement")
    state = st.selectbox("Select State", df_user["State"].unique())
    year = st.selectbox("Select Year", sorted(df_user["Year"].unique())) 
    filtered = df_user[(df_user["State"] == state) & (df_user["Year"] == year)]
    fig = px.pie(filtered, names="Brands", values="Count",
                    title=f"Device Brand Share in {state}, {year}")
    st.plotly_chart(fig, use_container_width=True)



# ===============================
# 📌3.Insurance Penetration & Growth
# ===============================

elif scenario.startswith("3"):
    df_ins=pd.read_csv("agg_ins.csv")
    st.title("🛡 Insurance Penetration & Growth")
    state = st.selectbox("Select State", ["All States"] + sorted(df_ins["State"].unique()), key="agg_ins_s")
    if state == "All States":
        trend = df_ins.groupby("Year")[["Count", "Amount"]].sum().reset_index()
    else:
        trend = df_ins[df_ins["State"] == state].groupby("Year")[["Count", "Amount"]].sum().reset_index()
    fig = px.line(trend, x="Year", y="Amount", markers=True,
                    title="Insurance Amount Growth ")
    st.plotly_chart(fig, use_container_width=True)


    st.subheader("🏆 State-wise Insurance Penetration")
    year_selected = st.selectbox("Select Year for Comparison", sorted(df_ins["Year"].unique()), key="ins_year_compare")
    statewise = df_ins[df_ins["Year"] == year_selected].groupby("State")[["Count", "Amount"]].sum().reset_index()

    fig_bar = px.bar(
    statewise.sort_values(by="Amount", ascending=False),
    x="State",
    y="Amount",
    color="State",
    title=f"State-wise Insurance Amount ({year_selected})",
    text="Amount"
    )
    fig_bar.update_traces(texttemplate='%{text:.2s}', textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)




# ===============================
# 📌 4.Transactions Across Districts
# ===============================

elif scenario.startswith("4"):
                         
    df_map_trans=pd.read_csv("map_trans.csv")
    st.title("🌍 Transactions Across Districts")
    state = st.selectbox("Select State", df_map_trans["State"].unique(),key="map_trans_s")
    year = st.selectbox("Select Year", sorted(df_map_trans["Year"].unique()),key="map_trans_y")
    filtered = df_map_trans[(df_map_trans["Year"] == year) & (df_map_trans["State"] == state)]
    top_districts = filtered.groupby("District")["Amount"].sum().nlargest(15).reset_index()
    fig = px.bar(top_districts, x="District", y="Amount",
                    title=f"Top Districts by Transaction Amount - {year}")
    st.plotly_chart(fig, use_container_width=True)


# ===============================
# 📌 6.Insurance Engagement Across District
# ===============================

elif scenario.startswith("5"):

    df_map_ins=pd.read_csv("map_ins.csv")
    st.title("🛡 Insurance Engagement Across Districts")
    year = st.selectbox("Select Year", sorted(df_map_ins["Year"].unique()),key="map_ins_y")
    state=st.selectbox("Select State",sorted(df_map_ins["State"].unique()),key="map_ins_s")
    filtered = df_map_ins[(df_map_ins["Year"] == year) & (df_map_ins["State"]==state)]
    top_districts = filtered.groupby("District")["Amount"].sum().nlargest(15).reset_index()
    fig = px.bar(top_districts, x="District", y="Amount",
                    title=f"Top Districts by Insurance Amount - {year}")
    st.plotly_chart(fig, use_container_width=True)


