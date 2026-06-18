import streamlit as st
import plotly.express as px
from api_client import (
    get_articles,
    get_market_reports,
    generate_report,
    get_market_snapshot,
    get_market_trends
)
articles_cache = get_articles()

def render_dashboard(snapshot):

    import plotly.express as px

    trends = snapshot["trends"]

    bullish = sum(s["bullish"] for s in trends.values())
    bearish = sum(s["bearish"] for s in trends.values())
    neutral = sum(s["neutral"] for s in trends.values())

    total = bullish + bearish + neutral
    # ======================
    # Market Overview
    # ======================

    st.subheader("📈 Market Overview")

    st.info(
        """
        Indian market sentiment remains positive.

        Technology and Banking sectors are leading
        overall market momentum.

        AI-generated market summary will appear here.
        """
    )
    st.divider()

    # ======================
    # Sentiment Balance
    # ======================  
    left, right = st.columns([1, 2])
    with left:
        st.subheader("📊 Market Coverage")
        st.metric(
            "Coverage",
            total
        )
        st.metric(
            "Bullish",
            bullish
        )
        st.metric(
            "Bearish",
            bearish
        )
        st.metric(
            "Neutral",
            neutral
        )
    with right:
        fig = px.pie(
            names=[
                "Bullish",
                "Bearish",
                "Neutral"
            ],
            values=[
                bullish,
                bearish,
                neutral
            ],
            hole=0.55
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    st.divider()

    # ======================
    # Key Insights
    # ======================
    filtered_trends = {
        k: v
        for k, v in trends.items()
        if k.lower() != "other"
    }

    if filtered_trends:
        strongest_sector = max(
            filtered_trends.items(),
            key=lambda x: (
                x[1]["bullish"] - x[1]["bearish"]
            )
        )[0]
        weakest_sector = min(
            filtered_trends.items(),
            key=lambda x: (
                x[1]["bullish"] - x[1]["bearish"]
            )
        )[0]
        bullish_ratio = bullish / total if total > 0 else 0
        if bullish_ratio >= 0.5:
            market_tone = "Bullish 📈"
        elif bullish_ratio >= 0.3:
            market_tone = "Neutral ⚖"
        else:
            market_tone = "Bearish 📉"

        st.subheader("🔥 Key Insights")

        col1, col2, col3 = st.columns(3)
        col1.metric(
            "Strongest Sector",
            strongest_sector
        )
        col2.metric(
            "Weakest Sector",
            weakest_sector
        )
        col3.metric(
            "Market Tone",
            market_tone
        )
        st.divider()


    # # ======================
    # # Sentiment Pie
    # # ======================
    # fig = px.pie(
    #     names=["Bullish", "Bearish", "Neutral"],
    #     values=[bullish, bearish, neutral],
    #     hole=0.55
    # )
    # st.plotly_chart(fig, use_container_width=True)



    #     # KPI
    # col1, col2, col3, col4 = st.columns(4)

    # col1.metric("📊 Market Coverage", total)
    # col2.metric("🟢 Bullish", bullish)
    # col3.metric("🔴 Bearish", bearish)
    # col4.metric("⚪ Neutral", neutral)

    # st.divider()
