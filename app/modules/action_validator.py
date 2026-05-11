# ==========================================================
# ADVANCED ACTION VALIDATOR
# HIGH-LEVEL VERSION
# ==========================================================

import re

# ==========================================================
# STRONG CRIME ACTIONS
# ==========================================================

STRONG_CRIME_ACTIONS = [

    # Arrests

    "arrested",
    "detained",
    "booked",
    "taken into custody",
    "held by police",

    # Seizures

    "seized",
    "confiscated",
    "recovered",
    "intercepted",

    # Wildlife Crime

    "poaching",
    "smuggling",
    "trafficking",
    "illegal trade",
    "illegal possession",
    "wildlife crime",

    # Enforcement

    "raid",
    "raided",
    "operation",
    "forest officials",
    "forest department",
    "wccb",
    "crime branch",

    # Organized Crime

    "gang",
    "network",
    "racket",
    "syndicate",

    # Legal

    "case registered",
    "fined",
    "charged",
    "investigation",
    "offence"
]

# ==========================================================
# WEAK ACTIONS
# ==========================================================

WEAK_ACTIONS = [

    "suspected",
    "under investigation",
    "allegedly",
    "reportedly"
]

# ==========================================================
# NON-CRIME CONTEXTS
# ==========================================================

NON_CRIME_CONTEXTS = [

    # Awareness

    "awareness",
    "campaign",
    "seminar",
    "conference",
    "workshop",

    # Conservation

    "conservation",
    "wildlife protection awareness",
    "environment day",

    # Tourism

    "tourism",
    "eco tourism",
    "safari",

    # Photography

    "photography",
    "photo contest",
    "bird watching",

    # Education

    "essay competition",
    "school event",
    "research project",

    # Media

    "documentary",
    "movie",
    "blog",
    "history"
]

# ==========================================================
# CLEAN TEXT
# ==========================================================

def clean_text(text):

    text = text.lower()

    text = re.sub(

        r"\s+",
        " ",
        text
    )

    return text.strip()

# ==========================================================
# STRONG ACTION DETECTOR
# ==========================================================

def detect_strong_actions(text):

    detected = []

    for action in STRONG_CRIME_ACTIONS:

        if action in text:

            detected.append(action)

    return detected

# ==========================================================
# WEAK ACTION DETECTOR
# ==========================================================

def detect_weak_actions(text):

    detected = []

    for action in WEAK_ACTIONS:

        if action in text:

            detected.append(action)

    return detected

# ==========================================================
# NON-CRIME DETECTOR
# ==========================================================

def detect_non_crime_context(text):

    detected = []

    for word in NON_CRIME_CONTEXTS:

        if word in text:

            detected.append(word)

    return detected

# ==========================================================
# ACTION SCORE ENGINE
# ==========================================================

def calculate_action_score(

    strong_actions,
    weak_actions
):

    score = 0

    # ======================================
    # STRONG ACTIONS
    # ======================================

    score += len(
        strong_actions
    ) * 20

    # ======================================
    # WEAK ACTIONS
    # ======================================

    score += len(
        weak_actions
    ) * 5

    return min(score, 100)

# ==========================================================
# MAIN VALIDATOR
# ==========================================================

def validate_criminal_activity(text):

    # ======================================
    # CLEAN
    # ======================================

    text = clean_text(text)

    # ======================================
    # NON-CRIME CONTEXT
    # ======================================

    non_crime = detect_non_crime_context(
        text
    )

    if len(non_crime) > 0:

        return {

            "valid": False,

            "reason":

            "Non-crime article",

            "non_crime_context":

            non_crime,

            "score": 0
        }

    # ======================================
    # DETECT ACTIONS
    # ======================================

    strong_actions = detect_strong_actions(
        text
    )

    weak_actions = detect_weak_actions(
        text
    )

    # ======================================
    # SCORE
    # ======================================

    action_score = calculate_action_score(

        strong_actions,

        weak_actions
    )

    # ======================================
    # DECISION ENGINE
    # ======================================

    is_valid = False

    # Strong enforcement context

    if len(strong_actions) >= 1:

        is_valid = True

    # Multiple weak actions

    if (

        len(weak_actions) >= 2

        and action_score >= 20
    ):

        is_valid = True

    # Strong action score

    if action_score >= 40:

        is_valid = True

    # ======================================
    # RETURN
    # ======================================

    return {

        "valid": is_valid,

        "action_score": action_score,

        "strong_actions": strong_actions,

        "weak_actions": weak_actions,

        "strong_action_count":

        len(strong_actions),

        "weak_action_count":

        len(weak_actions)
    }

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    sample_text = """

    Forest officials arrested
    a wildlife trafficking gang
    involved in ivory smuggling.
    Leopard skins were seized.
    """

    result = validate_criminal_activity(
        sample_text
    )

    print("\n===================")

    for key, value in result.items():

        print(f"{key}: {value}")

    print("===================")


# ==========================================================
# COMPATIBILITY FUNCTION
# REQUIRED BY collector.py
# ==========================================================

def validate_wildlife_crime(text):

    try:

        result = validate_criminal_activity(
            text
        )

        # ======================================
        # DETECT CRIME TYPE
        # ======================================

        text_lower = text.lower()

        crime_type = "Wildlife Crime"

        if "poaching" in text_lower:

            crime_type = "Poaching"

        elif "trafficking" in text_lower:

            crime_type = "Trafficking"

        elif "smuggling" in text_lower:

            crime_type = "Smuggling"

        elif "ivory" in text_lower:

            crime_type = "Ivory Trade"

        return {

            "is_valid":

            result["valid"],

            "reason":

            "Validated",

            "crime_type":

            crime_type,

            "action_score":

            result["action_score"]
        }

    except Exception as e:

        print(
            f"Validation Error: {e}"
        )

        return {

            "is_valid": False,

            "reason": "Validation failure",

            "crime_type": None,

            "action_score": 0
        }