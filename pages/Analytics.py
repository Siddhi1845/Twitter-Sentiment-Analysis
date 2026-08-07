import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

st.title("📈 Analytics Dashboard")

# ----------------------------
# Load Dataset
# ----------------------------

df = pd.read_csv(
    "datasets/Tweets.csv"
)

df = df[["airline_sentiment", "text"]]

df.columns = ["Sentiment", "Tweet"]

df = df.dropna()

# ----------------------------
# KPI Cards
# ----------------------------

total = len(df)
positive = len(df[df["Sentiment"] == "positive"])
negative = len(df[df["Sentiment"] == "negative"])
neutral = len(df[df["Sentiment"] == "neutral"])

c1, c2, c3, c4 = st.columns(4)

c1.metric("Tweets", total)
c2.metric("😊 Positive", positive)
c3.metric("😡 Negative", negative)
c4.metric("😐 Neutral", neutral)

st.divider()

# ----------------------------
# Charts
# ----------------------------

col1, col2 = st.columns(2)

counts = df["Sentiment"].value_counts()

with col1:

    fig = px.pie(
        values=counts.values,
        names=counts.index,
        hole=0.45,
        title="Sentiment Distribution"
    )

    st.plotly_chart(fig, width="stretch")

with col2:

    fig = px.bar(
        x=counts.index,
        y=counts.values,
        color=counts.index,
        text=counts.values,
        title="Sentiment Count"
    )

    st.plotly_chart(fig, width="stretch")

st.divider()

# ----------------------------
# Word Cloud
# ----------------------------

st.subheader("☁️ Word Cloud")

from wordcloud import STOPWORDS

text = " ".join(df["Tweet"].fillna("").astype(str))

text = re.sub(r"http\S+", "", text)
text = re.sub(r"@\w+", "", text)
text = re.sub(r"[^a-zA-Z ]", "", text)

stopwords = set(STOPWORDS)

stopwords.update([
    "flight",
    "flights",
    "airline",
    "americanair",
    "usairways",
    "jetblue",
    "united",
    "virginamerica",
    "southwestair",
    "amp",
    "http",
    "https",
    "co"
])

wordcloud = WordCloud(
    width=1200,
    height=600,
    background_color="white",
    stopwords=stopwords
).generate(text)

fig, ax = plt.subplots(figsize=(14,6))

ax.imshow(wordcloud)

ax.axis("off")

st.pyplot(fig)

st.divider()

# ----------------------------
# Top Words
# ----------------------------

st.subheader("🔥 Top 20 Frequent Words")

text = re.sub(r"[^a-zA-Z ]", "", text.lower())

words = text.split()

stopwords = {
    "the","a","an","is","are","to","of","and","for","in","on",
    "my","i","it","you","we","our","your","this","that","be",
    "have","has","had","was","were","am","with","at","as"
}

words = [w for w in words if w not in stopwords]

top = Counter(words).most_common(20)

top_df = pd.DataFrame(top, columns=["Word","Count"])

fig = px.bar(
    top_df,
    x="Word",
    y="Count",
    color="Count",
    title="Top 20 Words"
)

st.plotly_chart(fig, width="stretch")

st.divider()

# ----------------------------
# Dataset Preview
# ----------------------------

st.subheader("📋 Dataset Preview")

search = st.text_input(
    "🔍 Search Tweets",
    placeholder="Type any word..."
)

if search:

    filtered = df[
        df["Tweet"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

    st.write(f"Found {len(filtered)} tweets")

    st.dataframe(
        filtered,
        width="stretch"
    )

else:

    st.dataframe(
        df.head(20),
        width="stretch"
    )

st.divider()

st.subheader("📏 Tweet Length Analysis")

df["Tweet Length"] = df["Tweet"].astype(str).apply(len)

fig = px.histogram(
    df,
    x="Tweet Length",
    nbins=40,
    title="Distribution of Tweet Lengths",
    color_discrete_sequence=["#2563EB"]
)

fig.update_layout(
    xaxis_title="Tweet Length (Characters)",
    yaxis_title="Number of Tweets"
)

st.plotly_chart(
    fig,
    width="stretch"
)


st.divider()

st.subheader("📥 Download Dataset")

csv = df.to_csv(index=False)

st.download_button(
    label="📄 Download CSV",
    data=csv,
    file_name="Twitter_Sentiment_Dataset.csv",
    mime="text/csv"
)