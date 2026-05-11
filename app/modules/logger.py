# ==========================================================
# ADVANCED LOGGER SYSTEM
# PRODUCTION MONITORING
# UTF-8 SAFE VERSION
# ==========================================================

import logging
import os

from datetime import datetime

# ==========================================================
# LOG DIRECTORY
# ==========================================================

LOG_FOLDER = "logs"

if not os.path.exists(LOG_FOLDER):

    os.makedirs(LOG_FOLDER)

# ==========================================================
# LOG FILE
# ==========================================================

LOG_FILE = (

    f"{LOG_FOLDER}/"
    f"wildlife_ai.log"
)

# ==========================================================
# LOGGER CONFIGURATION
# ==========================================================

logging.basicConfig(

    level=logging.INFO,

    format=(

        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    ),

    handlers=[

        logging.FileHandler(

            LOG_FILE,

            encoding="utf-8"
        ),

        logging.StreamHandler()
    ]
)

# ==========================================================
# LOGGER INSTANCE
# ==========================================================

logger = logging.getLogger(

    "WildlifeCrimeAI"
)

print("LOGGER SYSTEM LOADED")

# ==========================================================
# INFO LOG
# ==========================================================

def log_info(message):

    logger.info(message)

# ==========================================================
# WARNING LOG
# ==========================================================

def log_warning(message):

    logger.warning(message)

# ==========================================================
# ERROR LOG
# ==========================================================

def log_error(message):

    logger.error(message)

# ==========================================================
# CRITICAL LOG
# ==========================================================

def log_critical(message):

    logger.critical(message)

# ==========================================================
# DEBUG LOG
# ==========================================================

def log_debug(message):

    logger.debug(message)

# ==========================================================
# ARTICLE ACCEPTED
# ==========================================================

def log_article_accepted(

    title,
    confidence
):

    logger.info(

        f"ARTICLE ACCEPTED | "
        f"CONFIDENCE={confidence} | "
        f"TITLE={title}"
    )

# ==========================================================
# ARTICLE REJECTED
# ==========================================================

def log_article_rejected(

    title,
    reason
):

    logger.warning(

        f"ARTICLE REJECTED | "
        f"REASON={reason} | "
        f"TITLE={title}"
    )

# ==========================================================
# DUPLICATE DETECTED
# ==========================================================

def log_duplicate(

    title,
    similarity
):

    logger.warning(

        f"DUPLICATE DETECTED | "
        f"SIMILARITY={similarity} | "
        f"TITLE={title}"
    )

# ==========================================================
# PIPELINE ERROR
# ==========================================================

def log_pipeline_error(

    module_name,
    error_message
):

    logger.error(

        f"PIPELINE ERROR | "
        f"MODULE={module_name} | "
        f"ERROR={error_message}"
    )

# ==========================================================
# ML PREDICTION LOG
# ==========================================================

def log_ml_prediction(

    title,
    confidence,
    prediction
):

    logger.info(

        f"ML PREDICTION | "
        f"PREDICTION={prediction} | "
        f"CONFIDENCE={confidence} | "
        f"TITLE={title}"
    )

# ==========================================================
# SEMANTIC SCORE LOG
# ==========================================================

def log_semantic_score(

    title,
    score
):

    logger.info(

        f"SEMANTIC SCORE | "
        f"SCORE={score} | "
        f"TITLE={title}"
    )

# ==========================================================
# LOCATION LOG
# ==========================================================

def log_location_detection(

    location,
    latitude,
    longitude
):

    logger.info(

        f"GEOLOCATION | "
        f"LOCATION={location} | "
        f"LAT={latitude} | "
        f"LON={longitude}"
    )

# ==========================================================
# DATABASE SAVE LOG
# ==========================================================

def log_database_save(

    incident_id
):

    logger.info(

        f"DATABASE SAVE | "
        f"INCIDENT={incident_id}"
    )

# ==========================================================
# SYSTEM START LOG
# ==========================================================

def log_system_start():

    logger.info(

        "WILDLIFE AI SYSTEM STARTED"
    )

# ==========================================================
# SYSTEM SHUTDOWN LOG
# ==========================================================

def log_system_shutdown():

    logger.info(

        "WILDLIFE AI SYSTEM STOPPED"
    )

# ==========================================================
# PERFORMANCE LOG
# ==========================================================

def log_processing_time(

    module_name,
    seconds
):

    logger.info(

        f"PERFORMANCE | "
        f"MODULE={module_name} | "
        f"TIME={seconds}s"
    )

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    log_system_start()

    log_info(

        "System initialized"
    )

    log_ml_prediction(

        title="Tiger poaching case",

        confidence=91,

        prediction="crime"
    )

    log_semantic_score(

        title="Wildlife trafficking",

        score=88
    )

    log_duplicate(

        title="Tiger poaching",

        similarity=92
    )

    log_article_rejected(

        title="Wildlife awareness event",

        reason="Non-crime article"
    )

    log_pipeline_error(

        module_name="translator",

        error_message="Timeout"
    )

    log_system_shutdown()