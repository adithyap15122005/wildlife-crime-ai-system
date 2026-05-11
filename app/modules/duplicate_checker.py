# ==========================================================
# ADVANCED DUPLICATE CHECKER
# SEMANTIC INCIDENT MATCHING
# ==========================================================

import hashlib
import pandas as pd

from sentence_transformers import (

    SentenceTransformer,
    util
)

# ==========================================================
# LOAD SEMANTIC MODEL
# ==========================================================

semantic_model = SentenceTransformer(

    "paraphrase-multilingual-MiniLM-L12-v2"
)

print("✅ DUPLICATE ENGINE LOADED")

# ==========================================================
# THRESHOLDS
# ==========================================================

EXACT_DUPLICATE_THRESHOLD = 100

SEMANTIC_DUPLICATE_THRESHOLD = 85

NEAR_DUPLICATE_THRESHOLD = 75

# ==========================================================
# HASH GENERATION
# ==========================================================

def generate_hash(text):

    return hashlib.md5(

        text.encode(
            "utf-8"
        )

    ).hexdigest()

# ==========================================================
# NORMALIZE TEXT
# ==========================================================

def normalize_text(text):

    text = text.lower()

    text = text.strip()

    return text

# ==========================================================
# EXACT DUPLICATE CHECK
# ==========================================================

def exact_duplicate_check(

    article_text,
    existing_hashes
):

    article_text = normalize_text(
        article_text
    )

    article_hash = generate_hash(
        article_text
    )

    if article_hash in existing_hashes:

        return {

            "is_duplicate": True,

            "duplicate_type":

            "EXACT_DUPLICATE",

            "similarity": 100
        }

    return {

        "is_duplicate": False
    }

# ==========================================================
# SEMANTIC DUPLICATE CHECK
# ==========================================================

def semantic_duplicate_check(

    article_text,
    existing_articles
):

    if len(existing_articles) == 0:

        return {

            "is_duplicate": False
        }

    # ======================================
    # EMBEDDINGS
    # ======================================

    article_embedding = semantic_model.encode(

        article_text,

        convert_to_tensor=True
    )

    existing_embeddings = semantic_model.encode(

        existing_articles,

        convert_to_tensor=True
    )

    # ======================================
    # SIMILARITIES
    # ======================================

    similarities = util.cos_sim(

        article_embedding,

        existing_embeddings
    )

    max_similarity = similarities.max().item()

    similarity_percent = round(

        max_similarity * 100,
        2
    )

    # ======================================
    # DUPLICATE LOGIC
    # ======================================

    if similarity_percent >= SEMANTIC_DUPLICATE_THRESHOLD:

        return {

            "is_duplicate": True,

            "duplicate_type":

            "SEMANTIC_DUPLICATE",

            "similarity":

            similarity_percent
        }

    if similarity_percent >= NEAR_DUPLICATE_THRESHOLD:

        return {

            "is_duplicate": True,

            "duplicate_type":

            "NEAR_DUPLICATE",

            "similarity":

            similarity_percent
        }

    return {

        "is_duplicate": False,

        "similarity":

        similarity_percent
    }

# ==========================================================
# LOAD EXISTING ARTICLES
# ==========================================================

def load_existing_articles(csv_file):

    try:

        df = pd.read_csv(csv_file)

        texts = []

        hashes = []

        if "title" in df.columns:

            titles = df["title"].fillna("").tolist()

            texts.extend(titles)

        if "summary" in df.columns:

            summaries = df["summary"].fillna("").tolist()

            texts.extend(summaries)

        if "hash" in df.columns:

            hashes = df["hash"].tolist()

        return {

            "texts": texts,

            "hashes": hashes
        }

    except:

        return {

            "texts": [],

            "hashes": []
        }

# ==========================================================
# MAIN DUPLICATE ENGINE
# ==========================================================

def check_duplicate(

    title,
    summary,
    csv_file
):

    # ======================================
    # COMBINE TEXT
    # ======================================

    article_text = (

        title + " " + summary
    )

    article_text = normalize_text(
        article_text
    )

    # ======================================
    # LOAD EXISTING DATA
    # ======================================

    existing_data = load_existing_articles(
        csv_file
    )

    existing_texts = existing_data["texts"]

    existing_hashes = existing_data["hashes"]

    # ======================================
    # EXACT CHECK
    # ======================================

    exact_result = exact_duplicate_check(

        article_text,

        existing_hashes
    )

    if exact_result["is_duplicate"]:

        return exact_result

    # ======================================
    # SEMANTIC CHECK
    # ======================================

    semantic_result = semantic_duplicate_check(

        article_text,

        existing_texts
    )

    return semantic_result

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    title = (

        "Tiger poachers arrested "
        "in Assam forest"
    )

    summary = (

        "Forest officials caught "
        "wildlife traffickers near "
        "Kaziranga reserve"
    )

    result = check_duplicate(

        title,
        summary,
        "../data/wildlife_crimes.csv"
    )

    print("\n===================")

    for key, value in result.items():

        print(f"{key}: {value}")

    print("===================")
    # ==========================================================
# COMPATIBILITY FUNCTION
# REQUIRED BY collector.py
# ==========================================================

def is_duplicate(

    title,
    summary,
    database_file
):

    try:

        result = check_duplicate(

            title,

            summary,

            database_file
        )

        return {

            "is_duplicate":

            result.get(
                "is_duplicate",
                False
            ),

            "similarity":

            result.get(
                "similarity",
                0
            ),

            "duplicate_type":

            result.get(
                "duplicate_type",
                "NONE"
            )
        }

    except Exception as e:

        print(
            f"Duplicate Engine Error: {e}"
        )

        return {

            "is_duplicate": False,

            "similarity": 0,

            "duplicate_type": "ERROR"
        }