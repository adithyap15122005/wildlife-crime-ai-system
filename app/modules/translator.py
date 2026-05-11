# ==========================================================
# FAST MULTILINGUAL TRANSLATION ENGINE
# INDIA WILDLIFE CRIME AI SYSTEM
# OPTIMIZED VERSION
# ==========================================================

from deep_translator import GoogleTranslator
from langdetect import detect

import re

# ==========================================================
# TRANSLATION CACHE
# ==========================================================

TRANSLATION_CACHE = {}

# ==========================================================
# SUPPORTED LANGUAGES
# ==========================================================

SUPPORTED_LANGUAGES = [

    "en",
    "hi",
    "ta",
    "te",
    "ml",
    "kn",
    "bn",
    "mr",
    "gu",
    "pa",
    "or"
]

# ==========================================================
# FAST CRIME TERMS
# SKIP TRANSLATION FOR THESE
# ==========================================================

FAST_CRIME_TERMS = [

    "tiger",
    "pangolin",
    "ivory",
    "poaching",
    "wildlife",
    "trafficking",
    "smuggling",
    "arrested",
    "seized",
    "raid",
    "forest officials",
    "wildlife trade",
    "leopard",
    "animal parts"
]

# ==========================================================
# CLEAN TEXT
# ==========================================================

def clean_text(text):

    if not text:

        return ""

    # Remove HTML

    text = re.sub(

        r"<.*?>",

        " ",

        text
    )

    # Remove URLs

    text = re.sub(

        r"http\S+",

        " ",

        text
    )

    # Remove extra spaces

    text = re.sub(

        r"\s+",

        " ",

        text
    )

    return text.strip()

# ==========================================================
# DETECT LANGUAGE
# ==========================================================

def detect_language(text):

    try:

        if not text:

            return "unknown"

        return detect(text)

    except:

        return "unknown"

# ==========================================================
# FAST SHORTCUT
# AVOID UNNECESSARY TRANSLATION
# ==========================================================

def fast_english_check(text):

    text_lower = text.lower()

    matches = 0

    for word in FAST_CRIME_TERMS:

        if word in text_lower:

            matches += 1

    # ======================================
    # ALREADY ENGLISH-LIKE
    # ======================================

    return matches >= 2

# ==========================================================
# TRANSLATE TO ENGLISH
# ==========================================================

def translate_to_english(text):

    try:

        # ======================================
        # EMPTY CHECK
        # ======================================

        if not text:

            return ""

        # ======================================
        # CLEAN TEXT
        # ======================================

        text = clean_text(text)

        # ======================================
        # SHORTEN TEXT FOR SPEED
        # ======================================

        text = text[:1200]

        # ======================================
        # CACHE CHECK
        # ======================================

        if text in TRANSLATION_CACHE:

            return TRANSLATION_CACHE[text]

        # ======================================
        # FAST ENGLISH CHECK
        # ======================================

        if fast_english_check(text):

            TRANSLATION_CACHE[text] = text

            return text

        # ======================================
        # DETECT LANGUAGE
        # ======================================

        language = detect_language(text)

        # ======================================
        # ALREADY ENGLISH
        # ======================================

        if language == "en":

            TRANSLATION_CACHE[text] = text

            return text

        # ======================================
        # UNSUPPORTED LANGUAGE
        # ======================================

        if language not in SUPPORTED_LANGUAGES:

            return text

        # ======================================
        # TRANSLATE
        # ======================================

        translated = GoogleTranslator(

            source="auto",

            target="en"

        ).translate(text)

        # ======================================
        # CLEAN OUTPUT
        # ======================================

        translated = clean_text(
            translated
        )

        # ======================================
        # SAVE CACHE
        # ======================================

        TRANSLATION_CACHE[text] = translated

        return translated

    except Exception as e:

        print(

            f"Translation Error: {e}"
        )

        return text

# ==========================================================
# TRANSLATE ARTICLE
# ==========================================================

def translate_article(

    title,
    summary
):

    try:

        title = title or ""

        summary = summary or ""

        # ======================================
        # SHORTEN SUMMARY
        # ======================================

        summary = summary[:500]

        full_text = (

            title
            + " "
            + summary
        )

        return translate_to_english(
            full_text
        )

    except Exception as e:

        print(

            f"Article Translation Error: {e}"
        )

        return (

            title
            + " "
            + summary
        )

# ==========================================================
# TRANSLATE FIELD
# ==========================================================

def translate_field(text):

    try:

        return translate_to_english(
            text
        )

    except:

        return text

# ==========================================================
# LANGUAGE VALIDATION
# ==========================================================

def is_supported_language(text):

    try:

        lang = detect_language(
            text
        )

        return (

            lang
            in
            SUPPORTED_LANGUAGES
        )

    except:

        return False

# ==========================================================
# SAFE TRANSLATION
# ==========================================================

def safe_translate(text):

    try:

        if not text:

            return ""

        translated = (

            translate_to_english(
                text
            )
        )

        if len(translated) < 5:

            return text

        return translated

    except:

        return text

# ==========================================================
# NORMALIZE TRANSLATION
# ==========================================================

def normalize_translation(text):

    if not text:

        return ""

    text = text.lower()

    text = re.sub(

        r"\s+",

        " ",

        text
    )

    return text.strip()

# ==========================================================
# FULL PIPELINE
# ==========================================================

def translation_pipeline(

    title,
    summary
):

    translated = translate_article(

        title,
        summary
    )

    translated = normalize_translation(

        translated
    )

    return translated

# ==========================================================
# QUICK TEST
# ==========================================================

if __name__ == "__main__":

    sample = """

    वन्यजीव तस्करी गिरोह गिरफ्तार

    """

    result = translate_to_english(
        sample
    )

    print("\n================")

    print(result)

    print("================")