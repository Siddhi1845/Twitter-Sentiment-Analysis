import streamlit as st
import pandas as pd
from utils.predict import predict_sentiment
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Twitter Sentiment Analysis",
    page_icon="💬",
    layout="wide"
)

# Store prediction history
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar
with st.sidebar:

    page = option_menu(

        menu_title="Twitter Sentiment",

        options=[
            "Home",
            "Predict",
            "Dashboard",
            "Analytics",
            "About"
        ],

        icons=[
            "house-fill",
            "chat-dots-fill",
            "speedometer2",
            "bar-chart-fill",
            "info-circle-fill"
        ],

        menu_icon="robot",

        default_index=0,

        styles={

            "container":{
                "padding":"8px",
                "background-color":"#111827"
            },

            "icon":{
                "color":"#00E5FF",
                "font-size":"18px"
            },

            "nav-link":{
                "font-size":"16px",
                "text-align":"left",
                "margin":"4px",
                "--hover-color":"#1F2937"
            },

            "nav-link-selected":{
                "background-color":"#2563EB",
                "color":"white"
            }

        }

    )

# ---------------- HOME ----------------

if page == "Home":

    st.markdown("""
    # 💬 Twitter Sentiment Analysis

    ### AI-Powered NLP Dashboard

    Analyze the sentiment of tweets using Machine Learning and Natural Language Processing.

    ---
    """)

    c1, c2, c3 = st.columns(3)

    c1.info("😊 **Positive Tweets**")

    c2.warning("😐 **Neutral Tweets**")

    c3.error("😡 **Negative Tweets**")

    st.markdown("---")

    st.subheader("🚀 Features")

    col1, col2 = st.columns(2)

    with col1:
        st.success("✔ Real-Time Sentiment Prediction")
        st.success("✔ Machine Learning Model")
        st.success("✔ Interactive Dashboard")
        st.success("✔ Analytics")

    with col2:
        st.success("✔ Pie Charts")
        st.success("✔ Bar Charts")
        st.success("✔ Prediction Confidence")
        st.success("✔ Professional UI")

# ---------------- PREDICT ----------------

elif page == "Predict":

    st.title("💬 Sentiment Prediction")

    st.write("Enter a tweet below and let the AI predict its sentiment.")

    tweet = st.text_area(
        "✍ Enter Tweet",
        height=180,
        placeholder="Example: I absolutely love this new phone!"
    )

    analyze = st.button(
        "🚀 Analyze Sentiment",
        use_container_width=True
    )

    if analyze:

        if tweet.strip():

            sentiment, confidence = predict_sentiment(tweet)

            st.divider()

            if sentiment == "Positive":

                st.success("😊 Positive")

                st.progress(
                    min(int(confidence),100)
                )

            elif sentiment == "Negative":

                st.error("😡 Negative")

                st.progress(
                    min(int(confidence),100)
                )

            else:

                st.warning("😐 Neutral")

                st.progress(
                    min(int(confidence),100)
                )

            st.metric(
                "Confidence",
                f"{confidence:.2f}%"
            )

            st.session_state.history.append(
                {
                    "Tweet": tweet,
                    "Prediction": sentiment,
                    "Confidence": f"{confidence:.2f}%"
                }
            )

            st.subheader("🤖 AI Insight")

            if sentiment=="Positive":

                st.success(
                    "This tweet expresses a positive opinion."
                )

            elif sentiment=="Negative":

                st.error(
                    "This tweet expresses a negative opinion."
                )

            else:

                st.info(
                    "This tweet appears neutral."
                )

        else:

            st.warning("Please enter a tweet.")

# ---------------- DASHBOARD ----------------

elif page == "Dashboard":

    exec(open("pages/Dashboard.py", encoding="utf-8").read())

# ---------------- ANALYTICS ----------------

elif page == "Analytics":

    exec(open("pages/Analytics.py", encoding="utf-8").read())

# ---------------- ABOUT ----------------

elif page == "About":

    exec(open("pages/About.py", encoding="utf-8").read())