import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# -------------------------------
# Title
# -------------------------------

st.title("📊 Dashboard")
st.caption("Overview of the Twitter Sentiment Dataset")

# -------------------------------
# Load Dataset
# -------------------------------

try:
    df = pd.read_csv(
        "datasets/twitter_training.csv",
        names=["ID", "Entity", "Sentiment", "Tweet"]
    )

except Exception as e:
    st.error(f"Unable to load dataset.\n\n{e}")
    st.stop()

# Keep only required sentiments
df = df[df["Sentiment"].isin(["Positive", "Negative", "Neutral"])]

# -------------------------------
# Statistics
# -------------------------------

total = len(df)
positive = len(df[df["Sentiment"] == "Positive"])
negative = len(df[df["Sentiment"] == "Negative"])
neutral = len(df[df["Sentiment"] == "Neutral"])

positive_percent = round((positive / total) * 100, 1)
negative_percent = round((negative / total) * 100, 1)
neutral_percent = round((neutral / total) * 100, 1)

# -------------------------------
# KPI Cards
# -------------------------------

st.subheader("📌 Dataset Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="
    background:#2563EB;
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;">
    <h4>Total Tweets</h4>
    <h2>{}</h2>
    </div>
    """.format(f"{total:,}"), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
    background:#16A34A;
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;">
    <h4>Positive</h4>
    <h2>{}</h2>
    </div>
    """.format(f"{positive:,}"), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="
    background:#DC2626;
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;">
    <h4>Negative</h4>
    <h2>{}</h2>
    </div>
    """.format(f"{negative:,}"), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="
    background:#D97706;
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;">
    <h4>Neutral</h4>
    <h2>{}</h2>
    </div>
    """.format(f"{neutral:,}"), unsafe_allow_html=True)

st.divider()

# -------------------------------
# Charts
# -------------------------------

left, right = st.columns([1, 1])

with left:

    st.subheader("🥧 Sentiment Distribution")

    pie = px.pie(
        df,
        names="Sentiment",
        hole=0.5,
        color="Sentiment",
        color_discrete_map={
            "Positive": "#2ECC71",
            "Negative": "#E74C3C",
            "Neutral": "#F1C40F"
        }
    )

    pie.update_layout(
        height=420,
        legend_title="Sentiment"
    )

    st.plotly_chart(pie, width="stretch")

with right:

    st.subheader("📈 Sentiment Count")

    counts = df["Sentiment"].value_counts().reset_index()
    counts.columns = ["Sentiment", "Count"]

    bar = px.bar(
        counts,
        x="Sentiment",
        y="Count",
        color="Sentiment",
        text="Count",
        color_discrete_map={
            "Positive": "#2ECC71",
            "Negative": "#E74C3C",
            "Neutral": "#F1C40F"
        }
    )

    bar.update_layout(height=420)

    st.plotly_chart(bar, width="stretch")

st.divider()

# -------------------------------
# Dataset Preview
# -------------------------------

st.subheader("📋 Dataset Preview")

st.dataframe(
    df.head(20),
    width="stretch",
    hide_index=True
)

st.divider()

# -------------------------------
# Recent Tweets
# -------------------------------

st.subheader("💬 Sample Tweets")

sample = df.sample(5, random_state=42)

for _, row in sample.iterrows():

    if row["Sentiment"] == "Positive":
        st.success(row["Tweet"])

    elif row["Sentiment"] == "Negative":
        st.error(row["Tweet"])

    else:
        st.warning(row["Tweet"])

st.divider()

# -------------------------------
# Footer
# -------------------------------

st.caption(
    "Twitter Sentiment Analysis Dashboard • Built using Python, Streamlit, Plotly & Scikit-learn"
)