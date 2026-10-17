
# ============================================================
# MEDICAL REPORT ANALYZER
# CONFIGURATION FILE
# ============================================================

# ------------------------------------------------------------
# Medical Reference Ranges
# ------------------------------------------------------------
# IMPORTANT:
# These are illustrative ranges for a college/demo project.
# Actual reference ranges can vary by laboratory and patient
# context. A real system should prefer ranges printed on the
# patient's own laboratory report.
# ------------------------------------------------------------

REFERENCE_RANGES = {

    # ========================================================
    # CBC / COMPLETE BLOOD COUNT
    # ========================================================

    "hemoglobin": {
        "min": 12.0,
        "max": 17.0,
        "unit": "g/dL"
    },

    "wbc": {
        "min": 4000,
        "max": 11000,
        "unit": "/µL"
    },

    "rbc": {
        "min": 4.0,
        "max": 6.0,
        "unit": "million/µL"
    },

    "platelets": {
        "min": 150000,
        "max": 450000,
        "unit": "/µL"
    },

    # ========================================================
    # DIABETES / BLOOD SUGAR
    # ========================================================

    "glucose": {
        "min": 70,
        "max": 140,
        "unit": "mg/dL"
    },

    # ========================================================
    # LIPID PROFILE
    # ========================================================

    "cholesterol": {
        "min": 0,
        "max": 200,
        "unit": "mg/dL"
    },

    "triglycerides": {
        "min": 0,
        "max": 150,
        "unit": "mg/dL"
    },

    # ========================================================
    # KIDNEY FUNCTION
    # ========================================================

    "creatinine": {
        "min": 0.6,
        "max": 1.3,
        "unit": "mg/dL"
    },

    "urea": {
        "min": 15,
        "max": 45,
        "unit": "mg/dL"
    },

    # ========================================================
    # LIVER FUNCTION
    # ========================================================

    "alt": {
        "min": 7,
        "max": 56,
        "unit": "U/L"
    },

    "ast": {
        "min": 10,
        "max": 40,
        "unit": "U/L"
    },

    "bilirubin": {
        "min": 0.1,
        "max": 1.2,
        "unit": "mg/dL"
    },

    # ========================================================
    # THYROID
    # ========================================================

    "tsh": {
        "min": 0.4,
        "max": 4.0,
        "unit": "mIU/L"
    },

    # ========================================================
    # OTHER COMMON PARAMETERS
    # ========================================================

    "albumin": {
        "min": 3.5,
        "max": 5.0,
        "unit": "g/dL"
    },

    "total_protein": {
        "min": 6.0,
        "max": 8.3,
        "unit": "g/dL"
    }
}


# ============================================================
# APPLICATION SETTINGS
# ============================================================

APP_NAME = "Automated Medical Report Analyzer"

APP_VERSION = "1.0.0"

APP_DESCRIPTION = (
    "AI-powered educational application for extracting and "
    "analyzing information from medical reports."
)


# ============================================================
# SUPPORTED FILE TYPES
# ============================================================

SUPPORTED_FILE_TYPES = [
    "pdf",
    "png",
    "jpg",
    "jpeg"
]


# ============================================================
# FOLDER SETTINGS
# ============================================================

UPLOAD_FOLDER = "uploads"

OUTPUT_FOLDER = "outputs"

DATABASE_FOLDER = "database"


# ============================================================
# STATUS LABELS
# ============================================================

STATUS_NORMAL = "NORMAL"

STATUS_HIGH = "HIGH"

STATUS_LOW = "LOW"

STATUS_UNKNOWN = "UNKNOWN"


# ============================================================
# APPLICATION DISCLAIMER
# ============================================================

MEDICAL_DISCLAIMER = """
This application is developed for educational and demonstration
purposes only.

It does not provide medical diagnosis, treatment, or medical
advice.

Reference ranges are illustrative and may vary between
laboratories and individuals.

Always consult a qualified healthcare professional for
interpretation of medical test results.
"""


# ============================================================
# DISPLAY SETTINGS
# ============================================================

PAGE_TITLE = "Medical Report Analyzer"

PAGE_ICON = "🏥"

LAYOUT = "wide"

