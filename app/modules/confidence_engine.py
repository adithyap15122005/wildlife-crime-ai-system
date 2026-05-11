
# ==========================================================
# ADVANCED CONFIDENCE ENGINE
# WILDLIFE INTELLIGENCE PIPELINE
# ==========================================================

# ==========================================================
# THRESHOLDS
# ==========================================================

MIN_FINAL_CONFIDENCE = 45

HIGH_CONFIDENCE = 80

MEDIUM_CONFIDENCE = 60

LOW_CONFIDENCE = 45

# ==========================================================
# FINAL CONFIDENCE ENGINE
# ==========================================================

def calculate_final_confidence(

    ml_result,
    semantic_result,
    action_result,
    location_result
):

    try:

        # ==================================================
        # FETCH SCORES
        # ==================================================

        ml_confidence = ml_result.get(
            "confidence",
            0
        )

        semantic_score = semantic_result.get(
            "semantic_score",
            0
        )

        action_score = action_result.get(
            "action_score",
            0
        )

        location_count = location_result.get(
            "location_count",
            0
        )

        wildlife_zones = location_result.get(
            "wildlife_zones",
            []
        )

        # ==================================================
        # WEIGHTED BASE SCORE
        # ==================================================

        final_score = (

            (ml_confidence * 0.50)

            +

            (semantic_score * 0.30)

            +

            (action_score * 0.20)

        )

        reasons = [

            f"ML Confidence: {ml_confidence}",

            f"Semantic Score: {semantic_score}",

            f"Action Score: {action_score}"
        ]

        # ==================================================
        # LOCATION BONUS
        # ==================================================

        location_bonus = min(
            location_count * 2,
            10
        )

        final_score += location_bonus

        reasons.append(
            f"Location Bonus: {location_bonus}"
        )

        # ==================================================
        # BOOSTS
        # ==================================================

        # Strong ML signal
        if ml_confidence >= 70:

            final_score += 5

            reasons.append(
                "High ML Confidence Boost"
            )

        # Strong semantic match
        if semantic_score >= 65:

            final_score += 5

            reasons.append(
                "High Semantic Boost"
            )

        # Strong action detection
        if action_score >= 50:

            final_score += 5

            reasons.append(
                "Action Detection Boost"
            )

        # Wildlife hotspot
        if len(wildlife_zones) > 0:

            final_score += 3

            reasons.append(
                "Wildlife Zone Boost"
            )

        # ==================================================
        # LIGHT PENALTIES
        # ==================================================

        if ml_confidence < 35:

            final_score -= 5

            reasons.append(
                "Low ML Penalty"
            )

        if semantic_score < 30:

            final_score -= 5

            reasons.append(
                "Low Semantic Penalty"
            )

        # ==================================================
        # NORMALIZE SCORE
        # ==================================================

        final_score = max(
            0,
            min(final_score, 100)
        )

        final_score = round(
            final_score,
            2
        )

        # ==================================================
        # VALIDATION
        # ==================================================

        is_valid = (

            final_score >=
            MIN_FINAL_CONFIDENCE
        )

        # ==================================================
        # CONFIDENCE LEVEL
        # ==================================================

        confidence_level = "VERY LOW"

        if final_score >= HIGH_CONFIDENCE:

            confidence_level = "HIGH"

        elif final_score >= MEDIUM_CONFIDENCE:

            confidence_level = "MEDIUM"

        elif final_score >= LOW_CONFIDENCE:

            confidence_level = "LOW"

        # ==================================================
        # RETURN
        # ==================================================

        return {

            "is_valid":

            is_valid,

            "final_confidence":

            final_score,

            "confidence_level":

            confidence_level,

            "reasons":

            reasons
        }

    except Exception as e:

        print(
            f"CONFIDENCE ENGINE ERROR: {e}"
        )

        return {

            "is_valid": False,

            "final_confidence": 0,

            "confidence_level": "ERROR",

            "reasons": [str(e)]
        }

# ==========================================================
# COMPATIBILITY FUNCTION
# REQUIRED BY collector.py
# ==========================================================

def final_confidence_score(

    ml_probability,
    semantic_score,
    action_score
):

    try:

        ml_result = {

            "confidence":

            ml_probability
        }

        semantic_result = {

            "semantic_score":

            semantic_score
        }

        action_result = {

            "action_score":

            action_score
        }

        location_result = {

            "location_count": 0,

            "wildlife_zones": []
        }

        result = calculate_final_confidence(

            ml_result,

            semantic_result,

            action_result,

            location_result
        )

        return result.get(

            "final_confidence",

            0
        )

    except Exception as e:

        print(
            f"Confidence Engine Error: {e}"
        )

        return 0

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    ml_result = {

        "confidence": 74
    }

    semantic_result = {

        "semantic_score": 71
    }

    action_result = {

        "action_score": 60
    }

    location_result = {

        "location_count": 3,

        "wildlife_zones":

        ["Kaziranga"]
    }

    result = calculate_final_confidence(

        ml_result,

        semantic_result,

        action_result,

        location_result
    )

    print("\n========================")

    print(
        "VALID:",
        result["is_valid"]
    )

    print(
        "CONFIDENCE:",
        result["final_confidence"]
    )

    print(
        "LEVEL:",
        result["confidence_level"]
    )

    print("\nREASONS:")

    for reason in result["reasons"]:

        print("-", reason)

    print("========================")
