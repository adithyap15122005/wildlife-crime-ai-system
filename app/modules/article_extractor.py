# ==========================================================
# FAST ARTICLE EXTRACTION ENGINE
# OPTIMIZED FOR MULTILINGUAL NEWS
# ==========================================================

import requests
from bs4 import BeautifulSoup
import re

# ==========================================================
# HEADERS
# ==========================================================

HEADERS = {

    "User-Agent":

    (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64)"
    )
}

# ==========================================================
# CLEAN TEXT
# ==========================================================

def clean_text(text):

    if not text:

        return ""

    text = re.sub(

        r"\s+",

        " ",

        text
    )

    text = re.sub(

        r"[ \t\r\f\v]+",

        " ",

        text
    )

    return text.strip()

# ==========================================================
# REMOVE JUNK
# ==========================================================

def remove_junk(text):

    junk_patterns = [

        "advertisement",
        "subscribe",
        "follow us",
        "click here",
        "read more",
        "download app",
        "share this article",
        "copyright"
    ]

    text_lower = text.lower()

    for junk in junk_patterns:

        text_lower = text_lower.replace(
            junk,
            ""
        )

    return text_lower

# ==========================================================
# EXTRACT ARTICLE
# ==========================================================

def extract_article(url):

    try:

        response = requests.get(

            url,

            headers=HEADERS,

            timeout=10
        )

        html = response.text

        soup = BeautifulSoup(

            html,

            "html.parser"
        )

        # ======================================
        # TITLE
        # ======================================

        title = ""

        if soup.title:

            title = soup.title.get_text()

        # ======================================
        # REMOVE SCRIPTS
        # ======================================

        for tag in soup([

            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside"
        ]):

            tag.decompose()

        # ======================================
        # PARAGRAPHS
        # ======================================

        paragraphs = soup.find_all("p")

        article_text = " ".join(

            p.get_text(
                strip=True
            )

            for p in paragraphs
        )

        # ======================================
        # CLEANING
        # ======================================

        title = clean_text(title)

        article_text = clean_text(

            article_text
        )

        article_text = remove_junk(

            article_text
        )

        return {

            "title": title,

            "text": article_text
        }

    except Exception as e:

        print(

            f"Extraction Error: {e}"
        )

        return {

            "title": "",

            "text": ""
        }

# ==========================================================
# VALIDATION
# ==========================================================

def validate_article(text):

    if not text:

        return False

    if len(text) < 200:

        return False

    if len(text.split()) < 40:

        return False

    return True

# ==========================================================
# MAIN CONTENT
# ==========================================================

def extract_main_content(url):

    article = extract_article(
        url
    )

    return article.get(
        "text",
        ""
    )

# ==========================================================
# COMPLETE ARTICLE
# ==========================================================

def extract_complete_article(url):

    article = extract_article(
        url
    )

    text = article.get(
        "text",
        ""
    )

    return {

        "title":

        article.get(
            "title",
            ""
        ),

        "text":

        text,

        "valid":

        validate_article(
            text
        )
    }

# ==========================================================
# SUMMARY
# ==========================================================

def generate_short_summary(text):

    try:

        sentences = text.split(".")

        summary = sentences[:4]

        return ". ".join(summary)

    except:

        return text[:400]

# ==========================================================
# EXTRACT + SUMMARY
# ==========================================================

def extract_and_summarize(url):

    article = extract_complete_article(
        url
    )

    summary = generate_short_summary(

        article["text"]
    )

    return {

        "title":

        article["title"],

        "text":

        article["text"],

        "summary":

        summary,

        "valid":

        article["valid"]
    }

# ==========================================================
# COMPATIBILITY FUNCTION
# REQUIRED BY collector.py
# ==========================================================

def extract_clean_article(url):

    try:

        return extract_main_content(
            url
        )

    except Exception as e:

        print(

            f"Clean Extraction Error: {e}"
        )

        return ""