# ==========================================================
# ADVANCED LOCATION EXTRACTOR
# INDIA WILDLIFE CRIME AI SYSTEM
# ==========================================================

import spacy

import re

# ==========================================================
# LOAD NLP MODEL
# ==========================================================

nlp = spacy.load(
    "en_core_web_sm"
)

print("✅ LOCATION NLP LOADED")

# ==========================================================
# INDIAN STATES
# ==========================================================

INDIAN_STATES = [

    "andhra pradesh",
    "arunachal pradesh",
    "assam",
    "bihar",
    "chhattisgarh",
    "goa",
    "gujarat",
    "haryana",
    "himachal pradesh",
    "jharkhand",
    "karnataka",
    "kerala",
    "madhya pradesh",
    "maharashtra",
    "manipur",
    "meghalaya",
    "mizoram",
    "nagaland",
    "odisha",
    "punjab",
    "rajasthan",
    "sikkim",
    "tamil nadu",
    "telangana",
    "tripura",
    "uttar pradesh",
    "uttarakhand",
    "west bengal"
]

# ==========================================================
# WILDLIFE ZONES
# ==========================================================

WILDLIFE_ZONES = [

    "national park",
    "tiger reserve",
    "wildlife sanctuary",
    "biosphere reserve",
    "forest division",
    "reserve forest",
    "forest range"
]

# ==========================================================
# FOREST KEYWORDS
# ==========================================================

FOREST_KEYWORDS = [

    "forest",
    "sanctuary",
    "reserve",
    "park",
    "wildlife division",
    "range"
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
# EXTRACT NLP LOCATIONS
# ==========================================================

def extract_spacy_locations(text):

    doc = nlp(text)

    locations = []

    for ent in doc.ents:

        if ent.label_ in [

            "GPE",
            "LOC",
            "FAC"
        ]:

            locations.append(
                ent.text
            )

    return locations

# ==========================================================
# EXTRACT STATES
# ==========================================================

def extract_states(text):

    found_states = []

    for state in INDIAN_STATES:

        if state in text:

            found_states.append(state)

    return found_states

# ==========================================================
# EXTRACT WILDLIFE ZONES
# ==========================================================

def extract_wildlife_zones(text):

    detected = []

    lines = text.split(".")

    for line in lines:

        for zone in WILDLIFE_ZONES:

            if zone in line:

                detected.append(
                    line.strip()
                )

    return detected

# ==========================================================
# EXTRACT FOREST REFERENCES
# ==========================================================

def extract_forest_references(text):

    references = []

    lines = text.split(".")

    for line in lines:

        for keyword in FOREST_KEYWORDS:

            if keyword in line:

                references.append(
                    line.strip()
                )

    return references

# ==========================================================
# REMOVE DUPLICATES
# ==========================================================

def remove_duplicates(items):

    clean_items = []

    seen = set()

    for item in items:

        item = item.strip()

        if not item:

            continue

        if item.lower() in seen:

            continue

        seen.add(item.lower())

        clean_items.append(item)

    return clean_items

# ==========================================================
# MAIN LOCATION ENGINE
# ==========================================================

def extract_locations(text):

    # ======================================
    # CLEAN
    # ======================================

    text = clean_text(text)

    # ======================================
    # NLP EXTRACTION
    # ======================================

    spacy_locations = extract_spacy_locations(
        text
    )

    # ======================================
    # STATE EXTRACTION
    # ======================================

    states = extract_states(
        text
    )

    # ======================================
    # WILDLIFE ZONES
    # ======================================

    wildlife_zones = extract_wildlife_zones(
        text
    )

    # ======================================
    # FOREST REFERENCES
    # ======================================

    forest_references = extract_forest_references(
        text
    )

    # ======================================
    # COMBINE
    # ======================================

    all_locations = (

        spacy_locations
        + states
        + wildlife_zones
        + forest_references
    )

    # ======================================
    # REMOVE DUPLICATES
    # ======================================

    all_locations = remove_duplicates(
        all_locations
    )

    # ======================================
    # PRIMARY LOCATION
    # ======================================

    primary_location = "Unknown"

    if len(all_locations) > 0:

        primary_location = all_locations[0]

    # ======================================
    # RETURN
    # ======================================

    return {

        "primary_location":

        primary_location,

        "all_locations":

        all_locations,

        "states":

        states,

        "wildlife_zones":

        wildlife_zones,

        "forest_references":

        forest_references,

        "location_count":

        len(all_locations)
    }

# ==========================================================
# COMPATIBILITY FUNCTION
# REQUIRED BY collector.py
# ==========================================================

def extract_location_entities(text):

    try:

        return extract_locations(
            text
        )

    except Exception as e:

        print(
            f"Location Extraction Error: {e}"
        )

        return {

            "primary_location": "Unknown",

            "all_locations": [],

            "states": [],

            "wildlife_zones": [],

            "forest_references": [],

            "location_count": 0
        }

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    sample_text = """

    Forest officials arrested
    wildlife traffickers near
    Kaziranga National Park in Assam.
    Leopard skins were seized
    from a gang operating inside
    a reserve forest area.
    """

    result = extract_locations(
        sample_text
    )

    print("\n===================")

    for key, value in result.items():

        print(f"{key}: {value}")

    print("===================")