# ==========================================================
# ADVANCED INCIDENT CLUSTER ENGINE
# MULTI-ARTICLE INCIDENT MATCHING
# ==========================================================

import pandas as pd

from sentence_transformers import (

    SentenceTransformer,
    util
)

from datetime import datetime

# ==========================================================
# LOAD SEMANTIC MODEL
# ==========================================================

semantic_model = SentenceTransformer(

    "paraphrase-multilingual-MiniLM-L12-v2"
)

print("✅ INCIDENT CLUSTER ENGINE LOADED")

# ==========================================================
# THRESHOLDS
# ==========================================================

SEMANTIC_CLUSTER_THRESHOLD = 80

# ==========================================================
# NORMALIZE TEXT
# ==========================================================

def normalize_text(text):

    text = str(text).lower()

    text = text.strip()

    return text

# ==========================================================
# TEXT SIMILARITY
# ==========================================================

def calculate_similarity(

    text1,
    text2
):

    embedding1 = semantic_model.encode(

        text1,

        convert_to_tensor=True
    )

    embedding2 = semantic_model.encode(

        text2,

        convert_to_tensor=True
    )

    similarity = util.cos_sim(

        embedding1,

        embedding2
    )

    score = similarity.item() * 100

    return round(score, 2)

# ==========================================================
# LOAD DATABASE
# ==========================================================

def load_database(

    database_file
):

    try:

        df = pd.read_csv(
            database_file
        )

        return df

    except:

        return pd.DataFrame()

# ==========================================================
# TIME MATCH
# ==========================================================

def check_time_similarity(

    existing_timestamp
):

    try:

        existing_time = datetime.strptime(

            existing_timestamp.split(".")[0],

            "%Y-%m-%d %H:%M:%S"
        )

        now = datetime.now()

        difference = abs(

            (now - existing_time)
            .total_seconds()
        )

        hours = difference / 3600

        # Same incident window

        if hours <= 72:

            return True

        return False

    except:

        return False

# ==========================================================
# LOCATION MATCH
# ==========================================================

def location_match(

    location1,
    location2
):

    location1 = normalize_text(
        location1
    )

    location2 = normalize_text(
        location2
    )

    if location1 in location2:

        return True

    if location2 in location1:

        return True

    return False

# ==========================================================
# CRIME TYPE MATCH
# ==========================================================

def crime_type_match(

    crime1,
    crime2
):

    crime1 = normalize_text(
        crime1
    )

    crime2 = normalize_text(
        crime2
    )

    return crime1 == crime2

# ==========================================================
# GENERATE NEW CLUSTER
# ==========================================================

def generate_cluster_id():

    timestamp = datetime.now().strftime(

        "%Y%m%d%H%M%S"
    )

    return f"CLUSTER-{timestamp}"

# ==========================================================
# INCIDENT CLUSTER ENGINE
# ==========================================================

def cluster_incident(

    title,
    summary,
    primary_location,
    crime_type,
    database_file
):

    # ======================================
    # LOAD DATABASE
    # ======================================

    df = load_database(
        database_file
    )

    # ======================================
    # NO DATA
    # ======================================

    if len(df) == 0:

        return {

            "cluster_found": False,

            "cluster_id":

            generate_cluster_id(),

            "similarity": 0
        }

    # ======================================
    # CURRENT ARTICLE
    # ======================================

    current_text = (

        title + " " + summary
    )

    current_text = normalize_text(
        current_text
    )

    best_similarity = 0

    best_cluster = None

    # ======================================
    # LOOP DATABASE
    # ======================================

    for _, row in df.iterrows():

        try:

            existing_text = (

                str(row["title"])
                + " "
                + str(row["summary"])
            )

            existing_text = normalize_text(
                existing_text
            )

            # ==============================
            # SEMANTIC SIMILARITY
            # ==============================

            similarity = calculate_similarity(

                current_text,

                existing_text
            )

            # ==============================
            # LOCATION CHECK
            # ==============================

            location_ok = location_match(

                primary_location,

                row.get(
                    "primary_location",
                    ""
                )
            )

            # ==============================
            # CRIME MATCH
            # ==============================

            crime_ok = crime_type_match(

                crime_type,

                row.get(
                    "crime_type",
                    ""
                )
            )

            # ==============================
            # TIME CHECK
            # ==============================

            time_ok = check_time_similarity(

                row.get(
                    "timestamp",
                    ""
                )
            )

            # ==============================
            # FINAL CLUSTER DECISION
            # ==============================

            if (

                similarity >=
                SEMANTIC_CLUSTER_THRESHOLD

                and location_ok

                and crime_ok

                and time_ok
            ):

                if similarity > best_similarity:

                    best_similarity = similarity

                    best_cluster = row.get(

                        "incident_cluster",

                        None
                    )

        except:

            continue

    # ======================================
    # EXISTING CLUSTER FOUND
    # ======================================

    if best_cluster:

        return {

            "cluster_found": True,

            "cluster_id":

            best_cluster,

            "similarity":

            best_similarity
        }

    # ======================================
    # NEW CLUSTER
    # ======================================

    return {

        "cluster_found": False,

        "cluster_id":

        generate_cluster_id(),

        "similarity":

        best_similarity
    }

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    result = cluster_incident(

        title=(

            "Tiger poachers arrested "
            "in Assam"
        ),

        summary=(

            "Forest officials seized "
            "leopard skin near "
            "Kaziranga"
        ),

        primary_location="Assam",

        crime_type="Poaching",

        database_file=(

            "../data/wildlife_crimes.csv"
        )
    )

    print("\n===================")

    for key, value in result.items():

        print(f"{key}: {value}")

    print("===================")