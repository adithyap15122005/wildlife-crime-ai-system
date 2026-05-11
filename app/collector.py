# ==========================================================
# INDIA WILDLIFE CRIME AI SYSTEM
# FAST MULTILINGUAL ENTERPRISE COLLECTOR
# FINAL OPTIMIZED VERSION
# ==========================================================

import time

from datetime import datetime

# ==========================================================
# CONFIG
# ==========================================================

from config import DATABASE_FILE

# ==========================================================
# MODULES
# ==========================================================

from modules.rss_fetcher import (
    fetch_rss_articles
)

from modules.translator import (
    translate_to_english
)

from modules.article_extractor import (
    extract_clean_article
)

from modules.normalizer import (
    normalize_text
)

from modules.ml_classifier import (
    classify_article
)

from modules.semantic_engine import (
    semantic_crime_score
)

from modules.action_validator import (
    validate_wildlife_crime
)

from modules.location_extractor import (
    extract_location_entities
)

from modules.geolocation import (
    geocode_location
)

from modules.confidence_engine import (
    final_confidence_score
)

from modules.duplicate_checker import (
    is_duplicate
)

from modules.incident_cluster import (
    cluster_incident
)

from modules.database import (
    save_to_database
)

from modules.logger import (

    log_article_accepted,
    log_article_rejected,
    log_ml_prediction,
    log_semantic_score,
    log_database_save,
    log_system_start,
    log_pipeline_error
)

# ==========================================================
# START SYSTEM
# ==========================================================

log_system_start()

print(

    "\nWILDLIFE AI SYSTEM STARTED\n"
)

# ==========================================================
# MAIN LOOP
# ==========================================================

while True:

    try:

        # ==============================================
        # FETCH ALL MULTILINGUAL RSS ARTICLES
        # ==============================================

        articles = fetch_rss_articles()

        print(

            f"\nTOTAL ARTICLES: "
            f"{len(articles)}"
        )

        # ==============================================
        # ARTICLE LOOP
        # ==============================================

        for article in articles:

            try:

                # ======================================
                # BASIC DATA
                # ======================================

                title = article.get(

                    "title",
                    ""
                )

                summary = article.get(

                    "summary",
                    ""
                )

                url = article.get(

                    "url",
                    ""
                )

                language = article.get(

                    "language",
                    "en-IN"
                )

                print(

                    f"\nARTICLE: {title}"
                )

                # ======================================
                # FAST RSS TEXT
                # ======================================

                initial_text = (

                    title
                    + " "
                    + summary
                )

                # ======================================
                # TRANSLATE ONLY IF NEEDED
                # ======================================

                if language != "en-IN":

                    english_text = (

                        translate_to_english(
                            initial_text
                        )
                    )

                else:

                    english_text = (
                        initial_text
                    )

                # ======================================
                # NORMALIZATION
                # ======================================

                normalized_text = (

                    normalize_text(
                        english_text
                    )
                )

                # ======================================
                # VALIDATION
                # ======================================

                validation_result = (

                    validate_wildlife_crime(
                        normalized_text
                    )
                )

                if not validation_result.get(

                    "is_valid",
                    False
                ):

                    log_article_rejected(

                        title,

                        validation_result.get(
                            "reason",
                            "Validation failed"
                        )
                    )

                    continue

                # ======================================
                # FAST ML CLASSIFIER
                # ======================================

                ml_result = (

                    classify_article(
                        normalized_text
                    )
                )

                prediction = (

                    ml_result.get(
                        "prediction",
                        "other"
                    )
                )

                ml_probability = (

                    ml_result.get(
                        "probability",
                        0
                    )
                )

                log_ml_prediction(

                    title,
                    ml_probability,
                    prediction
                )

                # ======================================
                # EARLY REJECTION
                # ======================================

                if ml_probability < 45:

                    log_article_rejected(

                        title,

                        "Low ML confidence"
                    )

                    continue

                # ======================================
                # FULL EXTRACTION
                # ONLY NOW
                # ======================================

                extracted_text = (

                    extract_clean_article(
                        url
                    )
                )

                if extracted_text:

                    if language != "en-IN":

                        english_text = (

                            translate_to_english(
                                extracted_text
                            )
                        )

                    else:

                        english_text = (
                            extracted_text
                        )

                    normalized_text = (

                        normalize_text(
                            english_text
                        )
                    )

                # ======================================
                # SEMANTIC AI
                # ONLY FOR STRONG ARTICLES
                # ======================================

                semantic_score = 0

                if ml_probability >= 60:

                    semantic_score = (

                        semantic_crime_score(
                            normalized_text
                        )
                    )

                log_semantic_score(

                    title,
                    semantic_score
                )

                # ======================================
                # FINAL CONFIDENCE
                # ======================================

                confidence = (

                    final_confidence_score(

                        ml_probability,

                        semantic_score,

                        validation_result.get(
                            "action_score",
                            0
                        )
                    )
                )

                print(

                    f"CONFIDENCE: "
                    f"{confidence}"
                )

                # ======================================
                # FINAL FILTER
                # ======================================

                if confidence < 50:

                    log_article_rejected(

                        title,

                        "Low confidence"
                    )

                    continue

                # ======================================
                # LOCATION EXTRACTION
                # ======================================

                location_data = (

                    extract_location_entities(
                        normalized_text
                    )
                )

                primary_location = (

                    location_data.get(
                        "primary_location",
                        "Unknown"
                    )
                )

                # ======================================
                # GEOLOCATION
                # ======================================

                geo_result = (

                    geocode_location(
                        primary_location
                    )
                )

                # ======================================
                # DUPLICATE CHECK
                # ======================================

                duplicate_result = (

                    is_duplicate(

                        title=title,

                        summary=summary,

                        database_file=(
                            DATABASE_FILE
                        )
                    )
                )

                if duplicate_result.get(

                    "is_duplicate",
                    False
                ):

                    log_article_rejected(

                        title,

                        "Duplicate article"
                    )

                    continue

                # ======================================
                # INCIDENT CLUSTERING
                # ======================================

                cluster_result = (

                    cluster_incident(

                        title=title,

                        summary=summary,

                        primary_location=(
                            primary_location
                        ),

                        crime_type=(

                            validation_result.get(
                                "crime_type",
                                "Wildlife Crime"
                            )
                        ),

                        database_file=(
                            DATABASE_FILE
                        )
                    )
                )

                # ======================================
                # FINAL RECORD
                # ======================================

                final_record = {

                    "timestamp":

                    str(datetime.now()),

                    "language":
                    language,

                    "title":
                    title,

                    "summary":
                    summary,

                    "url":
                    url,

                    "clean_text":
                    normalized_text,

                    "crime_type":

                    validation_result.get(
                        "crime_type",
                        "Wildlife Crime"
                    ),

                    "ml_probability":
                    ml_probability,

                    "semantic_score":
                    semantic_score,

                    "action_score":

                    validation_result.get(
                        "action_score",
                        0
                    ),

                    "final_confidence":
                    confidence,

                    "primary_location":
                    primary_location,

                    "all_locations":

                    location_data.get(
                        "all_locations",
                        []
                    ),

                    "latitude":

                    geo_result.get(
                        "latitude",
                        None
                    ),

                    "longitude":

                    geo_result.get(
                        "longitude",
                        None
                    ),

                    "incident_cluster":

                    cluster_result.get(
                        "cluster_id",
                        "UNKNOWN_CLUSTER"
                    ),

                    "duplicate_score":

                    duplicate_result.get(
                        "similarity",
                        0
                    )
                }

                # ======================================
                # SAVE DATABASE
                # ======================================

                save_to_database(

                    final_record,

                    DATABASE_FILE
                )

                log_database_save(

                    cluster_result.get(
                        "cluster_id",
                        "UNKNOWN_CLUSTER"
                    )
                )

                # ======================================
                # SUCCESS LOG
                # ======================================

                log_article_accepted(

                    title,
                    confidence
                )

                print(

                    "\n===================="
                )

                print(

                    "SAVED SUCCESSFULLY"
                )

                print(

                    "CRIME:",

                    validation_result.get(
                        "crime_type",
                        "Wildlife Crime"
                    )
                )

                print(

                    "LOCATION:",
                    primary_location
                )

                print(

                    "CONFIDENCE:",
                    confidence
                )

                print(

                    "SEMANTIC:",
                    semantic_score
                )

                print(

                    "CLUSTER:",

                    cluster_result.get(
                        "cluster_id",
                        "UNKNOWN_CLUSTER"
                    )
                )

                print(

                    "===================="
                )

                time.sleep(0.5)

            except Exception as article_error:

                log_pipeline_error(

                    "ARTICLE_PROCESSOR",

                    str(article_error)
                )

                continue

        # ==============================================
        # WAIT BEFORE NEXT CYCLE
        # ==============================================

        print(

            "\nWAITING 5 MINUTES...\n"
        )

        time.sleep(300)

    except Exception as main_error:

        log_pipeline_error(

            "MAIN_LOOP",

            str(main_error)
        )

        time.sleep(30)