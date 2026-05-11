# ==========================================================
# MULTILINGUAL FAST RSS FETCHER
# PRODUCTION OPTIMIZED
# ==========================================================

import feedparser
import urllib.parse
from datetime import datetime

# ==========================================================
# USER AGENT
# ==========================================================

USER_AGENT = (

    "Mozilla/5.0 "
    "(Windows NT 10.0; Win64; x64)"
)

# ==========================================================
# BLACKLIST SOURCES
# ==========================================================

BLACKLIST_SOURCES = [

    "wwf",
    "traffic.org",
    "clearias",
    "vajiram",
    "drishti",
    "insightsias",
    "un.org",
    "down to earth",
    "mongabay"
]

# ==========================================================
# REJECTION KEYWORDS
# ==========================================================

REJECT_TERMS = [

    "awareness",
    "workshop",
    "essay",
    "seminar",
    "training",
    "conference",
    "conservation",
    "environment day",
    "biodiversity"
]

# ==========================================================
# MULTILINGUAL RSS CONFIG
# ==========================================================

RSS_CONFIG = [

    # ENGLISH

    {

        "query":

        "wildlife trafficking india",

        "language":

        "en-IN",

        "ceid":

        "IN:en"
    },

    {

        "query":

        "tiger skin seizure india",

        "language":

        "en-IN",

        "ceid":

        "IN:en"
    },

    {

        "query":

        "pangolin trafficking india",

        "language":

        "en-IN",

        "ceid":

        "IN:en"
    },

    # HINDI

    {

        "query":

        "वन्यजीव तस्करी",

        "language":

        "hi-IN",

        "ceid":

        "IN:hi"
    },

    # TAMIL

    {

        "query":

        "வனவிலங்கு கடத்தல்",

        "language":

        "ta-IN",

        "ceid":

        "IN:ta"
    },

    # TELUGU

    {

        "query":

        "వన్యప్రాణుల అక్రమ రవాణా",

        "language":

        "te-IN",

        "ceid":

        "IN:te"
    },

    # KANNADA

    {

        "query":

        "ವನ್ಯಜೀವಿ ಕಳ್ಳಸಾಗಣೆ",

        "language":

        "kn-IN",

        "ceid":

        "IN:kn"
    },

    # MALAYALAM

    {

        "query":

        "വന്യജീവി കടത്ത്",

        "language":

        "ml-IN",

        "ceid":

        "IN:ml"
    },

    # BENGALI

    {

        "query":

        "বন্যপ্রাণী পাচার",

        "language":

        "bn-IN",

        "ceid":

        "IN:bn"
    }
]

# ==========================================================
# BUILD RSS URL
# ==========================================================

def build_rss_url(

    query,
    language,
    ceid
):

    query = urllib.parse.quote(
        query
    )

    return (

        "https://news.google.com/rss/search?"

        f"q={query}"

        f"&hl={language}"

        "&gl=IN"

        f"&ceid={ceid}"
    )

# ==========================================================
# CLEAN TEXT
# ==========================================================

def clean_text(text):

    if not text:

        return ""

    text = text.replace(
        "\n",
        " "
    )

    text = " ".join(
        text.split()
    )

    return text.strip()

# ==========================================================
# SOURCE FILTER
# ==========================================================

def is_blacklisted(source):

    source = source.lower()

    for blocked in BLACKLIST_SOURCES:

        if blocked in source:

            return True

    return False

# ==========================================================
# JUNK FILTER
# ==========================================================

def is_junk(title):

    title = title.lower()

    for word in REJECT_TERMS:

        if word in title:

            return True

    return False

# ==========================================================
# REMOVE DUPLICATES
# ==========================================================

def remove_duplicates(records):

    seen = set()

    clean = []

    for item in records:

        url = item.get(
            "url",
            ""
        )

        if url in seen:

            continue

        seen.add(url)

        clean.append(item)

    return clean

# ==========================================================
# FETCH SINGLE RSS
# ==========================================================

def fetch_single_feed(

    query,
    language,
    ceid
):

    rss_url = build_rss_url(

        query,
        language,
        ceid
    )

    print(
        f"\nFETCHING: {query}"
    )

    feed = feedparser.parse(

        rss_url,

        agent=USER_AGENT
    )

    articles = []

    for entry in feed.entries:

        try:

            title = clean_text(

                entry.get(
                    "title",
                    ""
                )
            )

            summary = clean_text(

                entry.get(
                    "summary",
                    ""
                )
            )

            url = clean_text(

                entry.get(
                    "link",
                    ""
                )
            )

            source = "Unknown"

            if hasattr(entry, "source"):

                source = clean_text(

                    entry.source.title
                )

            # ==================================
            # FILTERS
            # ==================================

            if is_blacklisted(source):

                continue

            if is_junk(title):

                continue

            if not title:

                continue

            if not url:

                continue

            articles.append({

                "title":

                title,

                "summary":

                summary,

                "url":

                url,

                "source":

                source,

                "language":

                language,

                "published":

                str(datetime.now())
            })

        except Exception as e:

            print(
                "Entry Error:",
                e
            )

    return articles

# ==========================================================
# FETCH ALL RSS
# ==========================================================

def fetch_rss_articles():

    all_articles = []

    for config in RSS_CONFIG:

        try:

            articles = fetch_single_feed(

                config["query"],

                config["language"],

                config["ceid"]
            )

            all_articles.extend(
                articles
            )

        except Exception as e:

            print(
                "RSS Error:",
                e
            )

    all_articles = remove_duplicates(

        all_articles
    )

    print(

        f"\nTOTAL ARTICLES: "
        f"{len(all_articles)}"
    )

    return all_articles

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    articles = fetch_rss_articles()

    for item in articles[:5]:

        print("\n================")

        print(item["title"])

        print(item["language"])

        print(item["source"])

        print("================")