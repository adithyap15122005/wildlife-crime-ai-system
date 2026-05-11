
# ==========================================================
# ADVANCED DATABASE ENGINE
# WILDLIFE INTELLIGENCE STORAGE
# ==========================================================

import pandas as pd
import os
import uuid

from datetime import datetime

# ==========================================================
# CREATE DATA DIRECTORY
# ==========================================================

BASE_DIR = os.getcwd()

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

os.makedirs(
    DATA_DIR,
    exist_ok=True
)

# ==========================================================
# DATABASE FILE
# ==========================================================

DATABASE_FILE = os.path.join(
    DATA_DIR,
    "wildlife_crimes.csv"
)

# ==========================================================
# DATABASE COLUMNS
# ==========================================================

DATABASE_COLUMNS = [

    "incident_id",
    "timestamp",
    "language",
    "title",
    "summary",
    "url",
    "primary_location",
    "all_locations",
    "states",
    "crime_type",
    "ml_confidence",
    "semantic_score",
    "action_score",
    "severity_score",
    "final_confidence",
    "confidence_level",
    "duplicate_status",
    "incident_cluster",
    "hash"
]

# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

def initialize_database():

    try:

        if not os.path.exists(DATABASE_FILE):

            df = pd.DataFrame(
                columns=DATABASE_COLUMNS
            )

            df.to_csv(
                DATABASE_FILE,
                index=False
            )

            print("\n✅ DATABASE CREATED")

        else:

            print("\n✅ DATABASE EXISTS")

        print(
            f"📁 CSV LOCATION: {DATABASE_FILE}"
        )

    except Exception as e:

        print(
            f"❌ DATABASE INIT ERROR: {e}"
        )

# ==========================================================
# GENERATE INCIDENT ID
# ==========================================================

def generate_incident_id():

    return (
        "WCI-" +
        str(uuid.uuid4())[:8].upper()
    )

# ==========================================================
# GENERATE CLUSTER ID
# ==========================================================

def generate_cluster_id(
    location,
    crime_type
):

    timestamp = datetime.now().strftime(
        "%Y%m%d"
    )

    location = str(location)[:3]
    crime_type = str(crime_type)[:3]

    return (
        f"{crime_type}-{location}-{timestamp}"
    ).upper()

# ==========================================================
# SAVE INCIDENT
# ==========================================================

def save_incident(

    language,
    title,
    summary,
    url,

    location_data,

    ml_result,

    semantic_result,

    action_result,

    confidence_result,

    duplicate_result,

    hash_value
):

    try:

        initialize_database()

        # ==================================================
        # LOAD EXISTING CSV
        # ==================================================

        if os.path.getsize(DATABASE_FILE) > 0:

            df = pd.read_csv(
                DATABASE_FILE
            )

        else:

            df = pd.DataFrame(
                columns=DATABASE_COLUMNS
            )

        # ==================================================
        # BUILD RECORD
        # ==================================================

        incident_id = generate_incident_id()

        primary_location = location_data.get(
            "primary_location",
            "Unknown"
        )

        cluster_id = generate_cluster_id(
            primary_location,
            action_result.get(
                "crime_type",
                "Wildlife Crime"
            )
        )

        new_record = {

            "incident_id":
            incident_id,

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

            "primary_location":
            primary_location,

            "all_locations":
            str(
                location_data.get(
                    "all_locations",
                    []
                )
            ),

            "states":
            str(
                location_data.get(
                    "states",
                    []
                )
            ),

            "crime_type":
            action_result.get(
                "crime_type",
                "Wildlife Crime"
            ),

            "ml_confidence":
            ml_result.get(
                "confidence",
                0
            ),

            "semantic_score":
            semantic_result.get(
                "semantic_score",
                0
            ),

            "action_score":
            action_result.get(
                "action_score",
                0
            ),

            "severity_score":
            action_result.get(
                "severity_score",
                0
            ),

            "final_confidence":
            confidence_result.get(
                "final_confidence",
                0
            ),

            "confidence_level":
            confidence_result.get(
                "confidence_level",
                "LOW"
            ),

            "duplicate_status":
            duplicate_result.get(
                "duplicate_type",
                "UNIQUE"
            ),

            "incident_cluster":
            cluster_id,

            "hash":
            hash_value
        }

        # ==================================================
        # APPEND RECORD
        # ==================================================

        new_df = pd.DataFrame(
            [new_record]
        )

        df = pd.concat(
            [df, new_df],
            ignore_index=True
        )

        # ==================================================
        # SAVE CSV
        # ==================================================

        df.to_csv(
            DATABASE_FILE,
            index=False
        )

        # ==================================================
        # VERIFY SAVE
        # ==================================================

        verify_df = pd.read_csv(
            DATABASE_FILE
        )

        print("\n✅ INCIDENT SAVED")
        print(f"🆔 ID: {incident_id}")
        print(f"📊 TOTAL ROWS: {len(verify_df)}")
        print(f"📁 SAVED TO: {DATABASE_FILE}")

        return incident_id

    except Exception as e:

        print(
            f"\n❌ SAVE INCIDENT ERROR: {e}"
        )

        return None

# ==========================================================
# LOAD DATABASE
# ==========================================================

def load_database():

    initialize_database()

    try:

        return pd.read_csv(
            DATABASE_FILE
        )

    except:

        return pd.DataFrame(
            columns=DATABASE_COLUMNS
        )

# ==========================================================
# GET TOTAL INCIDENTS
# ==========================================================

def get_total_incidents():

    df = load_database()

    return len(df)

# ==========================================================
# SAVE TO DATABASE
# REQUIRED BY collector.py
# ==========================================================

def save_to_database(

    final_record,

    database_file=None
):

    try:

        location_data = {

            "primary_location":

            final_record.get(
                "primary_location",
                "Unknown"
            ),

            "all_locations":

            final_record.get(
                "all_locations",
                []
            ),

            "states":

            final_record.get(
                "states",
                []
            )
        }

        ml_result = {

            "confidence":

            final_record.get(
                "ml_probability",
                final_record.get(
                    "probability",
                    0
                )
            )
        }

        semantic_result = {

            "semantic_score":

            final_record.get(
                "semantic_score",
                0
            )
        }

        action_result = {

            "action_score":

            final_record.get(
                "action_score",
                0
            ),

            "crime_type":

            final_record.get(
                "crime_type",
                "Wildlife Crime"
            ),

            "severity_score":

            final_record.get(
                "severity_score",
                0
            )
        }

        confidence_result = {

            "final_confidence":

            final_record.get(
                "final_confidence",
                0
            ),

            "confidence_level":

            "HIGH"
        }

        duplicate_result = {

            "duplicate_type":

            "UNIQUE"
        }

        hash_value = str(

            hash(
                final_record.get(
                    "title",
                    ""
                )
            )
        )

        return save_incident(

            language=
            final_record.get(
                "language",
                "en"
            ),

            title=
            final_record.get(
                "title",
                ""
            ),

            summary=
            final_record.get(
                "summary",
                ""
            ),

            url=
            final_record.get(
                "url",
                ""
            ),

            location_data=
            location_data,

            ml_result=
            ml_result,

            semantic_result=
            semantic_result,

            action_result=
            action_result,

            confidence_result=
            confidence_result,

            duplicate_result=
            duplicate_result,

            hash_value=
            hash_value
        )

    except Exception as e:

        print(
            f"\n❌ DATABASE SAVE ERROR: {e}"
        )

        return None

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    initialize_database()

    print("\n======================")
    print(
        "TOTAL INCIDENTS:",
        get_total_incidents()
    )
    print("======================")

