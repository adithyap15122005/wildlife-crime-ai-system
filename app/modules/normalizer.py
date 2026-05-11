# ==========================================================
# ADVANCED TEXT NORMALIZATION ENGINE
# INDIA WILDLIFE CRIME AI SYSTEM
# ==========================================================

import re

import unicodedata

from bs4 import BeautifulSoup

# ==========================================================
# REMOVE HTML
# ==========================================================

def remove_html(text):

    try:

        soup = BeautifulSoup(

            text,

            "html.parser"
        )

        return soup.get_text()

    except:

        return text

# ==========================================================
# REMOVE URLS
# ==========================================================

def remove_urls(text):

    return re.sub(

        r"http\S+|www\S+",

        "",

        text
    )

# ==========================================================
# REMOVE EMAILS
# ==========================================================

def remove_emails(text):

    return re.sub(

        r"\S+@\S+",

        "",

        text
    )

# ==========================================================
# REMOVE SPECIAL CHARACTERS
# ==========================================================

def remove_special_characters(text):

    return re.sub(

        r"[^\w\s.,!?;:/()-]",

        " ",

        text
    )

# ==========================================================
# REMOVE EXTRA SPACES
# ==========================================================

def remove_extra_spaces(text):

    return re.sub(

        r"\s+",

        " ",

        text
    ).strip()

# ==========================================================
# NORMALIZE UNICODE
# ==========================================================

def normalize_unicode(text):

    return unicodedata.normalize(

        "NFKD",

        text
    )

# ==========================================================
# LOWERCASE TEXT
# ==========================================================

def lowercase_text(text):

    return text.lower()

# ==========================================================
# REMOVE SHORT GARBAGE TOKENS
# ==========================================================

def remove_noise_tokens(text):

    words = text.split()

    filtered = [

        word

        for word in words

        if len(word) > 1
    ]

    return " ".join(filtered)

# ==========================================================
# REMOVE NEWS SOURCE TAGS
# ==========================================================

def remove_news_source_suffix(text):

    patterns = [

        r"- times of india",
        r"- the hindu",
        r"- ndtv",
        r"- indian express",
        r"- hindustan times",
        r"- india today",
        r"\|.*"
    ]

    for pattern in patterns:

        text = re.sub(

            pattern,

            "",

            text,

            flags=re.IGNORECASE
        )

    return text

# ==========================================================
# REMOVE DUPLICATE WORDS
# ==========================================================

def remove_duplicate_words(text):

    words = text.split()

    unique_words = []

    previous = None

    for word in words:

        if word != previous:

            unique_words.append(word)

        previous = word

    return " ".join(unique_words)

# ==========================================================
# CLEAN ARTICLE TEXT
# ==========================================================

def clean_article_text(text):

    if not text:

        return ""

    text = remove_html(text)

    text = remove_urls(text)

    text = remove_emails(text)

    text = normalize_unicode(text)

    text = lowercase_text(text)

    text = remove_special_characters(text)

    text = remove_news_source_suffix(text)

    text = remove_duplicate_words(text)

    text = remove_noise_tokens(text)

    text = remove_extra_spaces(text)

    return text

# ==========================================================
# COMBINE TITLE + SUMMARY
# ==========================================================

def combine_article(title, summary):

    title = title or ""

    summary = summary or ""

    combined = f"{title} {summary}"

    combined = clean_article_text(

        combined
    )

    return combined

# ==========================================================
# CLEAN FOR ML
# ==========================================================

def normalize_for_ml(text):

    text = clean_article_text(
        text
    )

    # Remove numbers
    text = re.sub(

        r"\d+",

        " ",

        text
    )

    # Remove repeated punctuation
    text = re.sub(

        r"[.,!?]{2,}",

        ".",

        text
    )

    text = remove_extra_spaces(
        text
    )

    return text

# ==========================================================
# CLEAN FOR SEMANTIC SEARCH
# ==========================================================

def normalize_for_semantic(text):

    text = clean_article_text(
        text
    )

    return text

# ==========================================================
# ARTICLE NORMALIZATION PIPELINE
# ==========================================================

def normalization_pipeline(

    title,
    summary
):

    combined = combine_article(

        title,
        summary
    )

    normalized = normalize_for_ml(

        combined
    )

    return normalized

# ==========================================================
# COMPATIBILITY FUNCTION
# REQUIRED BY collector.py
# ==========================================================

def normalize_text(text):

    try:

        return normalize_for_ml(
            text
        )

    except Exception as e:

        print(

            f"Normalization Error: {e}"
        )

        return ""