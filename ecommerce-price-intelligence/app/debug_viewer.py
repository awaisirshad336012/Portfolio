"""
Debug viewer — NOT the final dashboard (that's Phase 6).

This is a throwaway tool to inspect raw HTML the scraper saved
(e.g. debug_page_1.html) so we can find the right CSS selectors
for real product cards, without pasting huge HTML blobs back and
forth in chat.

Run from the project root:
    streamlit run app/debug_viewer.py
"""

import glob
import os

import streamlit as st
from bs4 import BeautifulSoup

st.set_page_config(page_title="Daraz Scraper Debugger", layout="wide")
st.title("🔍 Daraz Scraper Debugger")
st.caption("Inspect saved debug HTML to find the right selectors for product cards.")

# --- Find debug files ---
debug_files = sorted(glob.glob("debug_page_*.html")) + sorted(glob.glob("*/debug_page_*.html"))

uploaded = st.file_uploader("Or upload a debug_page_*.html file", type="html")

html = None
source_label = None

if uploaded is not None:
    html = uploaded.read().decode("utf-8", errors="replace")
    source_label = uploaded.name
elif debug_files:
    choice = st.selectbox("Found debug files in this folder:", debug_files)
    if choice:
        with open(choice, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
        source_label = choice
else:
    st.warning(
        "No `debug_page_*.html` found in the project root. "
        "Run the scraper first (`python -m scraper.selenium_scraper \"laptop\" --pages 1`), "
        "or upload a file above."
    )

if html:
    st.success(f"Loaded: {source_label} ({len(html):,} characters)")
    soup = BeautifulSoup(html, "lxml")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Elements with `data-qa-locator`")
        locators = soup.find_all(attrs={"data-qa-locator": True})
        if locators:
            unique_locators = sorted(set(el["data-qa-locator"] for el in locators))
            st.write(f"Found {len(locators)} elements, {len(unique_locators)} unique locator values:")
            st.code("\n".join(unique_locators))
        else:
            st.error("No `data-qa-locator` attributes found at all — the page may be a "
                      "CAPTCHA/interstitial rather than real search results.")

    with col2:
        st.subheader("Product grid check")
        grid = soup.find("div", {"data-qa-locator": "general-products"})
        if grid:
            st.success("Found grid container: `data-qa-locator='general-products'`")
            direct_children = grid.find_all("div", recursive=False)
            st.write(f"Direct child `<div>`s: **{len(direct_children)}**")
            if direct_children:
                st.write("First child's classes:")
                st.code(direct_children[0].get("class", "(no class attr)"))
        else:
            st.error("Grid container NOT found. Daraz may have renamed this locator, "
                      "or the page didn't load real results.")

    st.subheader("Look for likely product links")
    product_links = [a["href"] for a in soup.find_all("a", href=True) if "/products/" in a["href"] or "-i" in a["href"]]
    st.write(f"Found {len(product_links)} links that look like product URLs.")
    if product_links:
        st.code("\n".join(product_links[:10]))

    with st.expander("🔎 Search raw HTML for a keyword (e.g. a price you saw on the site, like '249,999')"):
        keyword = st.text_input("Keyword")
        if keyword:
            idx = html.find(keyword)
            if idx == -1:
                st.warning("Not found in the raw HTML — this confirms it's not present in the static markup Selenium captured.")
            else:
                snippet = html[max(0, idx - 300): idx + 300]
                st.code(snippet, language="html")

    with st.expander("📄 View full raw HTML"):
        st.code(html[:50000], language="html")  # cap to keep the browser responsive
        if len(html) > 50000:
            st.caption(f"Truncated — showing first 50,000 of {len(html):,} characters.")
