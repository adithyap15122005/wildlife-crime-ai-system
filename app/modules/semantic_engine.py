# ==========================================================
# FAST OPTIMIZED SEMANTIC ENGINE
# INDIA WILDLIFE CRIME AI SYSTEM
# ==========================================================

from sentence_transformers import (

    SentenceTransformer,

    util
)

# ==========================================================
# FAST LIGHTWEIGHT MODEL
# ==========================================================

semantic_model = SentenceTransformer(

    "paraphrase-MiniLM-L3-v2"
)

print("SEMANTIC MODEL LOADED")

# ==========================================================
# FAST CACHE
# ==========================================================

EMBEDDING_CACHE = {}

# ==========================================================
# FAST CRIME TERMS
# ==========================================================

FAST_CRIME_TERMS = [

    "arrested",
    "seized",
    "trafficking",
    "smuggling",
    "poaching",
    "raid",
    "raided",
    "confiscated",
    "pangolin",
    "tiger skin",
    "ivory",
    "wildlife trade",
    "illegal wildlife",
    "caught",
    "detained",
    "recovered",
    "leopard skin",
    "animal body parts"
]

# ==========================================================
# REFERENCE CRIME SENTENCES
# ==========================================================

REFERENCE_CRIMES = [

    # Poaching

    "Tiger poaching gang arrested",

    "Poachers caught in wildlife sanctuary",

    "Forest officers arrested poachers",

    # Trafficking

    "Wildlife traffickers arrested",

    "Illegal wildlife trade exposed",

    "Wildlife trafficking racket busted",

    # Ivory

    "Ivory smuggling case detected",

    "Elephant tusks seized by officials",

    # Pangolin

    "Pangolin scales seized",

    "Pangolin trafficking network exposed",

    # Leopard

    "Leopard skin seized",

    "Leopard poaching case registered",

    # Birds

    "Rare birds rescued from smugglers",

    "Illegal bird trafficking operation",

    # Snake trade

    "Snake venom smuggling racket",

    "Cobra trafficking case detected",

    # Enforcement

    "Wildlife criminals arrested",

    "Forest department raid conducted",

    "Illegal animal trade network busted",

    # Organized crime

    "Wildlife crime syndicate exposed",

    "International wildlife trafficking network",

    # Seizure

    "Wildlife products confiscated",

    "Animal body parts seized",

    # Smuggling

    "Illegal wildlife transport intercepted",

    "Wildlife smuggling gang caught"
]

# ==========================================================
# CREATE REFERENCE EMBEDDINGS
# ==========================================================

reference_embeddings = semantic_model.encode(

    REFERENCE_CRIMES,

    convert_to_tensor=True
)

# ==========================================================
# FAST SHORTCUT FILTER
# ==========================================================

def fast_keyword_shortcut(text):

    text_lower = text.lower()

    matches = 0

    for word in FAST_CRIME_TERMS:

        if word in text_lower:

            matches += 1

    # ======================================
    # STRONG CRIME SIGNAL
    # ======================================

    if matches >= 4:

        return 90

    elif matches >= 3:

        return 80

    elif matches >= 2:

        return 70

    return 0

# ==========================================================
# SEMANTIC SIMILARITY
# ==========================================================

def semantic_similarity(text):

    try:

        if not text:

            return 0

        # ======================================
        # CACHE CHECK
        # ======================================

        if text in EMBEDDING_CACHE:

            return EMBEDDING_CACHE[text]

        # ======================================
        # FAST SHORTCUT
        # ======================================

        shortcut_score = fast_keyword_shortcut(
            text
        )

        if shortcut_score > 0:

            EMBEDDING_CACHE[text] = shortcut_score

            return shortcut_score

        # ======================================
        # SHORTEN TEXT FOR SPEED
        # ======================================

        text = text[:400]

        # ======================================
        # ARTICLE EMBEDDING
        # ======================================

        article_embedding = semantic_model.encode(

            text,

            convert_to_tensor=True
        )

        # ======================================
        # COSINE SIMILARITY
        # ======================================

        similarities = util.cos_sim(

            article_embedding,

            reference_embeddings
        )

        # ======================================
        # MAX SCORE
        # ======================================

        max_score = similarities.max().item()

        final_score = round(

            max_score * 100,

            2
        )

        # ======================================
        # CACHE STORE
        # ======================================

        EMBEDDING_CACHE[text] = final_score

        return final_score

    except Exception as e:

        print(

            "Semantic Similarity Error:",

            e
        )

        return 0

# ==========================================================
# BEST REFERENCE MATCH
# ==========================================================

def best_matching_reference(text):

    try:

        text = text[:400]

        article_embedding = semantic_model.encode(

            text,

            convert_to_tensor=True
        )

        similarities = util.cos_sim(

            article_embedding,

            reference_embeddings
        )[0]

        best_index = similarities.argmax().item()

        best_score = similarities[
            best_index
        ].item()

        best_reference = REFERENCE_CRIMES[
            best_index
        ]

        return {

            "reference":

            best_reference,

            "score":

            round(best_score * 100, 2)
        }

    except Exception as e:

        print(

            "Reference Matching Error:",

            e
        )

        return {

            "reference": "",

            "score": 0
        }

# ==========================================================
# SEMANTIC VALIDATOR
# ==========================================================

def semantic_validator(text):

    semantic_score = semantic_similarity(
        text
    )

    reference_match = best_matching_reference(
        text
    )

    # ======================================
    # DECISION ENGINE
    # ======================================

    is_semantically_valid = False

    # ======================================
    # LOWERED THRESHOLDS
    # ======================================

    if semantic_score >= 60:

        is_semantically_valid = True

    elif semantic_score >= 50:

        is_semantically_valid = True

    else:

        is_semantically_valid = False

    return {

        "valid":

        is_semantically_valid,

        "semantic_score":

        semantic_score,

        "best_reference":

        reference_match["reference"],

        "reference_score":

        reference_match["score"]
    }

# ==========================================================
# INCIDENT SIMILARITY
# ==========================================================

def incident_similarity(

    text1,
    text2
):

    try:

        text1 = text1[:300]

        text2 = text2[:300]

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

        return round(

            similarity.item() * 100,

            2
        )

    except Exception as e:

        print(

            "Incident Similarity Error:",

            e
        )

        return 0

# ==========================================================
# COMPATIBILITY FUNCTION
# REQUIRED BY collector.py
# ==========================================================

def semantic_crime_score(text):

    try:

        return semantic_similarity(
            text
        )

    except Exception as e:

        print(

            f"Semantic Crime Score Error: {e}"
        )

        return 0

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    sample_article = """

    Forest officials arrested a wildlife
    trafficking gang involved in tiger
    skin smuggling and illegal ivory trade.
    """

    result = semantic_validator(
        sample_article
    )

    print("\n===================")

    for key, value in result.items():

        print(f"{key}: {value}")

    print("===================")