# ==========================================================
# ADVANCED MULTILINGUAL WILDLIFE CRIME ML CLASSIFIER
# PRODUCTION-GRADE HYBRID AI ENGINE
# ==========================================================

import os
import re
import joblib
import numpy as np

# ==========================================================
# BASE DIRECTORY
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# ==========================================================
# MODEL PATH
# ==========================================================

MODEL_PATH = os.path.join(

    BASE_DIR,
    "..",
    "models",
    "wildlife_crime_model.pkl"
)

# ==========================================================
# LOAD MODEL
# ==========================================================

try:

    model = joblib.load(MODEL_PATH)

    print("ML MODEL LOADED")

except Exception as e:

    print("MODEL LOAD ERROR:", e)

    model = None

# ==========================================================
# WILDLIFE KEYWORDS
# ==========================================================

WILDLIFE_KEYWORDS = [

    # Animals

    "tiger",
    "leopard",
    "pangolin",
    "elephant",
    "rhino",
    "deer",
    "bear",
    "owl",
    "parrot",
    "cobra",
    "snake",
    "peacock",
    "star tortoise",
    "monitor lizard",
    "wild boar",
    "wildlife",

    # Body Parts

    "ivory",
    "tusk",
    "skin",
    "scales",
    "horn",
    "fur",
    "bones",
    "claws",
    "teeth",

    # Crime Words

    "poaching",
    "trafficking",
    "smuggling",
    "illegal trade",
    "wildlife trade",
    "animal trade",
    "seized",
    "arrested",
    "raid",
    "gang",
    "racket",
    "contraband",
    "busted",
    "confiscated",
    "detained",
    "caught",

    # Legal Terms

    "wildlife protection act",
    "forest department",
    "wildlife crime control bureau",
    "wccb"
]

# ==========================================================
# STRONG ACTION WORDS
# ==========================================================

STRONG_ACTIONS = [

    "arrested",
    "seized",
    "confiscated",
    "raid",
    "raided",
    "detained",
    "booked",
    "busted",
    "caught",
    "recovered",
    "smuggling",
    "trafficking",
    "poaching",
    "illegal possession",
    "intercepted",
    "custody"
]

# ==========================================================
# STRICT REJECTION WORDS
# ==========================================================

STRICT_REJECT = [

    # Conservation

    "awareness",
    "conservation",
    "wildlife awareness",
    "environment awareness",
    "biodiversity awareness",

    # Education

    "essay",
    "seminar",
    "workshop",
    "conference",
    "education",
    "training program",

    # Tourism

    "tourism",
    "eco tourism",
    "wildlife tourism",
    "safari tourism",
    "zoo visit",

    # Media

    "documentary",
    "photography",
    "photo exhibition",
    "film festival",
    "blog",
    "history",
    "explained",

    # Non Crime

    "animal attack",
    "leopard attack",
    "tiger sighting",
    "wild elephant attack",
    "forest fire",
    "animal rescue",
    "injured animal",
    "nature camp"
]

# ==========================================================
# CLEAN TEXT
# ==========================================================

def clean_text(text):

    if not text:

        return ""

    text = text.lower()

    text = re.sub(

        r"http\S+",

        " ",

        text
    )

    text = re.sub(

        r"[^a-zA-Z0-9\s]",

        " ",

        text
    )

    text = re.sub(

        r"\s+",

        " ",

        text
    )

    return text.strip()

# ==========================================================
# STRICT REJECTION ENGINE
# ==========================================================

def reject_non_crime(text):

    for word in STRICT_REJECT:

        if word in text:

            return True

    return False

# ==========================================================
# KEYWORD ANALYZER
# ==========================================================

def keyword_score(text):

    score = 0

    found_keywords = []

    for word in WILDLIFE_KEYWORDS:

        if word in text:

            score += 1

            found_keywords.append(word)

    return score, found_keywords

# ==========================================================
# ACTION ANALYZER
# ==========================================================

def action_score(text):

    score = 0

    found_actions = []

    for action in STRONG_ACTIONS:

        if action in text:

            score += 1

            found_actions.append(action)

    return score, found_actions

# ==========================================================
# ML PREDICTION
# ==========================================================

def ml_prediction(text):

    if model is None:

        return "non-crime", 0

    try:

        probabilities = model.predict_proba(
            [text]
        )[0]

        prediction = model.predict(
            [text]
        )[0]

        confidence = np.max(
            probabilities
        )

        return (

            prediction,

            round(
                confidence * 100,
                2
            )
        )

    except Exception as e:

        print(
            "ML Prediction Error:",
            e
        )

        return "non-crime", 0

# ==========================================================
# HYBRID AI CLASSIFICATION
# ==========================================================

def classify_article(text):

    # ======================================
    # CLEAN TEXT
    # ======================================

    text = clean_text(text)

    # ======================================
    # EMPTY CHECK
    # ======================================

    if len(text) < 50:

        return {

            "is_crime": False,

            "prediction": "non-crime",

            "probability": 0,

            "confidence": 0,

            "reason": "Text too short"
        }

    # ======================================
    # STRICT REJECTION
    # ======================================

    if reject_non_crime(text):

        return {

            "is_crime": False,

            "prediction": "non-crime",

            "probability": 0,

            "confidence": 0,

            "reason":

            "Rejected by strict filter"
        }

    # ======================================
    # ML ENGINE
    # ======================================

    prediction, confidence = ml_prediction(
        text
    )

    # ======================================
    # KEYWORD ANALYSIS
    # ======================================

    keyword_count, keywords = keyword_score(
        text
    )

    # ======================================
    # ACTION ANALYSIS
    # ======================================

    action_count, actions = action_score(
        text
    )

    # ======================================
    # HYBRID SCORING
    # ======================================

    hybrid_score = 0

    # ML contribution

    hybrid_score += confidence * 0.6

    # Wildlife context

    hybrid_score += min(

        keyword_count * 5,
        20
    )

    # Criminal action context

    hybrid_score += min(

        action_count * 8,
        20
    )

    # ======================================
    # ADVANCED DECISION LOGIC
    # ======================================

    is_crime = False

    decision_reason = "Rejected"

    # Strong ML

    if (

        prediction == "crime"

        and confidence >= 75
    ):

        is_crime = True

        decision_reason = (

            "Strong ML confidence"
        )

    # Hybrid

    elif (

        keyword_count >= 3

        and action_count >= 1

        and hybrid_score >= 75
    ):

        is_crime = True

        decision_reason = (

            "Hybrid AI detection"
        )

    # Strong context

    elif (

        keyword_count >= 5

        and action_count >= 2
    ):

        is_crime = True

        decision_reason = (

            "Strong wildlife crime context"
        )

    # High ML

    elif (

        confidence >= 85

        and keyword_count >= 2
    ):

        is_crime = True

        decision_reason = (

            "High confidence ML"
        )

    # ======================================
    # RETURN RESULTS
    # ======================================

    return {

        "is_crime":

        is_crime,

        "prediction":

        prediction,

        "probability":

        round(
            confidence,
            2
        ),

        "confidence":

        round(
            confidence,
            2
        ),

        "hybrid_score":

        round(
            hybrid_score,
            2
        ),

        "keyword_count":

        keyword_count,

        "action_count":

        action_count,

        "keywords_found":

        keywords,

        "actions_found":

        actions,

        "decision_reason":

        decision_reason
    }

# ==========================================================
# QUICK TEST
# ==========================================================

if __name__ == "__main__":

    sample_text = """

    Forest officials arrested a wildlife
    trafficking gang involved in tiger skin
    smuggling and illegal ivory trade
    near Assam border.

    """

    result = classify_article(
        sample_text
    )

    print("\n============================")

    for key, value in result.items():

        print(f"{key}: {value}")

    print("============================")