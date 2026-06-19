import streamlit as st
import sys
import os
# 1. まず最初にプロジェクトのルートディレクトリ（一つ上の階層）を検索パスの先頭に追加する
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 2. その後に通常のインポートを行う
from dashboard import render_dashboard
from api_client import (
    get_articles,
    get_market_reports,
    generate_report,
    get_market_snapshot,
    get_market_trends,
    import_rss
)
import plotly.express as px
from app.services.ppt_service import generate_sample_ppt  # これで正しくルートのappパッケージが見つかります
from io import BytesIO

st.set_page_config(page_title="India Market Watch", layout="wide")

@st.cache_data
def load_articles():
    return get_articles()

articles_cache = load_articles()
# ----------------------
# サイドバー
# ----------------------
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Articles",
        "Market Reports",
        "AI Generate"
    ]
)
# ======================
# #RSS取り込み処理
# ======================
def ensure_articles():
    articles = get_articles()
    if not articles:
        with st.spinner("Importing RSS articles..."):
            import_rss()
        articles = get_articles()
    return articles
# ======================
# Dashboard
# ======================
st.title("📊 India Market Watch Dashboard")
if menu == "Dashboard":
    articles = get_articles()
    if not articles:
        import_rss()
        articles = get_articles()
    snapshot = get_market_snapshot()
    render_dashboard(snapshot)
    # ======================
    # 🧠 sentiment
    # ======================
    import random
    articles = get_articles()
    if not articles:
        with st.spinner("Importing RSS articles..."):
            import_rss()
        articles = get_articles()
    sectors = []
    sentiments = []

    for a in articles:
        sector = a.get("sector") or random.choice(
            ["IT", "Banking", "Energy", "Auto", "Finance"]
        )

        sentiment = a.get("sentiment") or random.choice(
            ["Bullish", "Bearish", "Neutral"]
        )

        sectors.append(sector)
        sentiments.append(sentiment)

    ranking = snapshot.get("ranking", [])
    # ======================
    # Sector ranking
    # ======================
    import pandas as pd
    import plotly.express as px
    st.subheader("🏆 Sector Ranking")

    left, right = st.columns([1, 2])

    with left:
        for idx, sector in enumerate(ranking[:5]):
            rank = idx + 1
            if rank == 1:
                medal = "🥇"
            elif rank == 2:
                medal = "🥈"
            elif rank == 3:
                medal = "🥉"
            else:
                medal = "🏅"
            st.metric(
                label=f"{medal} {sector['sector']}",
                value=sector["bullish_score"]
            )

    with right:
        df = pd.DataFrame(ranking[:5])
        if df.empty:
            st.info("No ranking data yet. Please import RSS articles.")
        else:
            fig = px.bar(
            df,
            y="sector",
            x="bullish_score",
            orientation="h"
            )
            fig.update_layout(
                yaxis=dict(
                    autorange="reversed"
                ),
                showlegend=False
                )
            st.plotly_chart(
                fig,
                use_container_width=True
            )
# ======================
# Articles
# ======================
elif menu == "Articles":
    st.header("📰 Articles")

    import random  # STEP2用（仮セクター・センチメント）
    
    articles = get_articles()
    if not articles:
        with st.spinner("Importing RSS articles..."):
            import_rss()
        articles = get_articles()
    if st.button("🔄 Refresh Articles"):
        st.rerun()

    if not articles:
        st.warning("No articles found")
    else:
        for article in articles:
            with st.container():
                st.markdown("---")

                # 🧾 Title
                st.markdown(f"### {article.get('title', 'No Title')}")

                # 📌 Meta Info
                col1, col2 = st.columns(2)

                with col1:
                    st.caption(f"📡 Source: {article.get('source', 'Unknown')}")

                with col2:
                    st.caption(f"🕒 {article.get('published_at', 'N/A')}")

                # 🧠 Summary（最初の3行）
                content = article.get("content", "")
                summary = "\n".join(content.split("\n")[:3]) if content else ""

                st.write(summary)



                # ======================
                # 🏷 Sector / Sentiment (STEP2)
                # ======================

                sector = article.get("sector")
                sentiment = article.get("sentiment")

                # fallback（API未実装対策）
                if not sector:
                    sector = random.choice([
                        "IT", "Banking", "Energy", "Auto", "Finance"
                    ])
                if not sentiment:
                    sentiment = random.choice([
                        "Bullish", "Bearish", "Neutral"
                    ])
                col3, col4 = st.columns(2)
                with col3:
                    st.markdown(f"🏷 **Sector:** `{sector}`")
                with col4:
                    if sentiment == "Bullish":
                        st.success(f"📈 {sentiment}")
                    elif sentiment == "Bearish":
                        st.error(f"📉 {sentiment}")
                    else:
                        st.info(f"⚖ {sentiment}")
                # 🔽 Expand
                with st.expander("Read more"):
                    st.write(content if content else "No content available")
# ======================
# Market Reports
# ======================
elif menu == "Market Reports":
    st.header("📈 Market Reports")

    if st.button("🔄 Refresh Reports"):
        st.rerun()

    reports = get_market_reports()

    if not reports:
        st.warning("No reports found")
    else:
       
        for r in reports:

            report_text = r.get("report_text", {})
            st.subheader(
                f"Market Report #{r.get('id')}"
            )
            st.write(
                report_text.get(
                    "summary",
                    "No summary available"
                )
            )
            st.caption(
                r.get("created_at", "")
            )
# ======================
# AI Generate
# ======================
elif menu == "AI Generate":
    st.header("🤖 AI Report Generator")
    
    # 1. セッション状態（st.session_state）の初期化
    if "ai_report_result" not in st.session_state:
        st.session_state.ai_report_result = None
    if "ppt_generated" not in st.session_state:
        st.session_state.ppt_generated = False
    if "ppt_file_path" not in st.session_state:
        st.session_state.ppt_file_path = None

    if st.button("🚀 Generate Report"):
        with st.spinner("Generating Report..."):
            st.session_state.ai_report_result = generate_report()
            # レポートが再生成されたら、古いPPTの状態はリセットする
            st.session_state.ppt_generated = False
            st.session_state.ppt_file_path = None
        st.success("Report Generated")
    
    # レポートが生成されている場合のみ、中身やPPTダウンロード領域を表示
    if st.session_state.ai_report_result is not None:
        result = st.session_state.ai_report_result
        
        # ======================
        # AI Summary
        # ======================
        st.subheader("🧠 AI Market Summary")
        st.write(result["summary"])

        ranking = result["snapshot"]["ranking"]
        
        # ======================
        # AI Commentary
        # ======================
        st.divider()
        st.subheader("💡 AI Commentary")

        if ranking:
            commentary = f"""
            Market sentiment is currently concentrated in {ranking[0]["sector"]}.
            The ranking suggests investors are showing stronger interest in this sector compared with the rest of the market.
            Continued monitoring is recommended if the bullish trend persists.
            """
            st.info(commentary)

        # ======================
        # Key Insights
        # ======================
        st.divider()
        st.subheader("🔥 Key Insights")

        if ranking:
            top_sector = ranking[0]["sector"]
            st.success(f"Strongest Sector Today: {top_sector}")

            if len(ranking) > 1:
                second_sector = ranking[1]["sector"]
                st.info(f"Secondary Momentum: {second_sector}")

        # ======================
        # Sector Ranking
        # ======================
        st.divider()
        st.subheader("🏆 Sector Ranking")

        for idx, sector in enumerate(ranking):
            rank = idx + 1
            name = sector["sector"]
            score = sector["bullish_score"]

            if rank == 1:
                label = f"🥇 #{rank} {name}"
            elif rank == 2:
                label = f"🥈 #{rank} {name}"
            elif rank == 3:
                label = f"🥉 #{rank} {name}"
            else:
                label = f"#{rank} {name}"

            st.metric(label=label, value=score)

        # ======================
        # Downloadボタン・PPT生成（★完全互換版）
        # ======================
        st.divider()
        st.subheader("📊 Export PPT Report")

        from datetime import datetime
        # 例: india_market_watch_20260615_1622.pptx のようなファイル名にする
        current_time = datetime.now().strftime("%Y%m%d_%H%M")
        dynamic_filename = f"india_market_watch_{current_time}.pptx"

        if st.button("📥 Generate PPT Report"):
            with st.spinner("Generating PPT..."):
                result_data = result
                snapshot = result_data["snapshot"]
                ranking = snapshot["ranking"]

                # 1. ppt_service.py が str 判定を処理しやすいよう、カンマ区切りの文字列に変換して渡す
                sectors_str = ",".join([str(s["sector"]) for s in ranking])
                scores_str = ",".join([str(s["bullish_score"]) for s in ranking])

                strongest_sector = ranking[0]["sector"] if ranking else "N/A"
                weakest_sector = ranking[-1]["sector"] if ranking else "N/A"

                # 2. ランキングテキストの整形
                ranking_text = "\n".join([f"{s['sector']}: {s['bullish_score']}" for s in ranking])

                # 3. coverageデータの安全な抽出（キー欠落対策）
                coverage = snapshot.get("coverage")
                if coverage:
                    bullish_c = coverage.get("bullish", 0)
                    bearish_c = coverage.get("bearish", 0)
                    neutral_c = coverage.get("neutral", 0)
                else:
                    bullish_c = snapshot.get("bullish", 0)
                    bearish_c = snapshot.get("bearish", 0)
                    neutral_c = snapshot.get("neutral", 0)

                # 🚨 円グラフ用：すべて0の場合は仮データを割り当てて Matplotlib の ValueError を防ぐ
                if bullish_c == 0 and bearish_c == 0 and neutral_c == 0:
                    bullish_c, neutral_c, bearish_c = 1, 1, 1

                coverage_text = f"Bullish: {bullish_c}\nBearish: {bearish_c}\nNeutral: {neutral_c}"

                # 4. 構築した完璧なデータを代入して呼び出し
                st.session_state.ppt_file_path = generate_sample_ppt(
                    summary=result_data.get("summary", "No summary available"),
                    strongest_sector=strongest_sector,
                    weakest_sector=weakest_sector,
                    market_tone="Auto",
                    ranking_text=ranking_text,
                    coverage_text=coverage_text,
                    sectors=sectors_str,  # 文字列で渡す
                    scores=scores_str,    # 文字列で渡す
                    bullish_count=str(bullish_c),
                    bearish_count=str(bearish_c),
                    neutral_count=str(neutral_c),
                    headline_text="\n".join([a.get("title", "") for a in result_data.get("articles", [])[:5]])
                )
                st.session_state.ppt_generated = True

    # else:
    #     # まだ最初の「🚀 Generate Report」自体を押していない時の案内
    #     st.info("💡 「🚀 Generate Report」ボタンを押すと、AIレポートの確認とPPTのダウンロードができるようになります。")

        # # ======================
    # # INSIGHTS LAYER（修正版）
    # # ======================

    # filtered_trends = {
    #     k: v for k, v in trends.items()
    #     if k.lower() != "other"
    # }

    # # 安全対策（全部Otherだった場合）
    # if filtered_trends:

    #     strongest = max(filtered_trends.items(), key=lambda x: x[1]["bullish"])
    #     weakest = max(filtered_trends.items(), key=lambda x: x[1]["bearish"])

    #     st.subheader("🔥 Key Insights")

    #     st.write(f"🔥 Strongest Sector: **{strongest[0]}**")
    #     st.write(f"⚠ Weakest Sector: **{weakest[0]}**")

    # else:
    #     st.subheader("🔥 Key Insights")
    #     st.write("No valid sector data available")
