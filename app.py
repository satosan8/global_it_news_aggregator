import streamlit as st
import pandas as pd
import feedparser

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Global IT News Aggregator",
    page_icon="💻",
    layout="wide"
)

# ---------- HEADER ----------
col_title, col_search = st.columns(2)

with col_title:
    st.title("💻 Global IT News Aggregator")
    st.write("Created by Nazmi Jor as a portfolio project.")

with col_search:
    keyword = st.text_input("Filter news", "").strip().lower()

st.markdown("---")

# ---------- RSS FETCHING ----------
@st.cache_data(ttl=300)
def get_all_news():
    feeds = [
        {
            "name": "Hacker News",
            "url": "https://news.ycombinator.com/rss"
        },
        {
            "name": "TechCrunch",
            "url": "https://techcrunch.com/feed/"
        },
        {
            "name": "The Verge",
            "url": "https://www.theverge.com/rss/index.xml"
        },
        {
            "name": "Habr 🇷🇺",
            "url": "https://habr.com/ru/rss/all/all/"
        }
    ]

    articles = []

    for feed in feeds:
        parsed = feedparser.parse(feed["url"])

        if not parsed.entries:
            continue

        for entry in parsed.entries[:5]:
            articles.append({
                "Site": feed["name"],
                "Title": entry.get("title", "No title"),
                "Link": entry.get("link", "")
            })

    return pd.DataFrame(articles)

# ---------- LOAD DATA ----------
with st.spinner("Loading news..."):
    df = get_all_news()

# ---------- ERROR STATE ----------
if df.empty:
    st.error("Error loading news. Please try again later.")

else:
    # ---------- FILTER ----------
    if keyword:
        df = df[
            df["Title"].str.lower().str.contains(keyword, na=False) |
            df["Site"].str.lower().str.contains(keyword, na=False)
        ]

    # ---------- DISPLAY ----------
    if not df.empty:
        for site, group in df.groupby("Site"):
            st.subheader(site)
            for _, row in group.iterrows():
                st.markdown(f"- **[{row['Title']}]({row['Link']})**")
            st.markdown("")
    else:
        st.info("No news found for your request.")

# ---------- REFRESH ----------
st.markdown("---")
if st.button("Refresh News"):
    st.cache_data.clear()
    st.rerun()

