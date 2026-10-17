# ============================================================
# MEDICAL REPORT ANALYZER
# ============================================================

import re

from config import REFERENCE_RANGES


# ============================================================
# 1. EXTRACT PATIENT NAME
# ============================================================

def extract_patient_name(text):

    patterns = [
        r"patient\s*name\s*[:\-]?\s*([A-Za-z][A-Za-z .'-]{1,50})",
        r"name\s+of\s+the\s+student\s*[:\-]?\s*([A-Za-z][A-Za-z .'-]{1,50})",
        r"name\s*[:\-]\s*([A-Za-z][A-Za-z .'-]{1,50})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return "Not detected"


# ============================================================
# 2. EXTRACT REPORTED DIAGNOSIS
# ============================================================

def extract_diagnosis(text):

    patterns = [
        r"diagnosis\s*[:\-]\s*([^\n\r]+)",
        r"diagnosis\s*\n\s*([^\n\r]+)",
        r"clinical\s+diagnosis\s*[:\-]\s*([^\n\r]+)",
        r"impression\s*[:\-]\s*([^\n\r]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            diagnosis = match.group(1).strip()

            if diagnosis:
                return diagnosis

    # Look for common documented phrases
    common_phrases = [
        "acute viral fever with dehydration",
        "viral fever",
        "fever with dehydration",
        "dehydration"
    ]

    text_lower = text.lower()

    for phrase in common_phrases:

        if phrase in text_lower:

            return phrase.title()

    return "No diagnosis explicitly reported"


# ============================================================
# 3. EXTRACT MEDICAL PARAMETERS
# ============================================================

def extract_medical_values(text):

    results = {}

    patterns = {

        "hemoglobin":
            r"hemoglobin\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "wbc":
            r"(?:wbc|white blood cell count)\s*[:\-]?\s*(\d+(?:,\d+)?)",

        "rbc":
            r"(?:rbc|red blood cell count)\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "platelets":
            r"platelets?\s*[:\-]?\s*(\d+(?:,\d+)?)",

        "glucose":
            r"(?:glucose|blood sugar)\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "cholesterol":
            r"(?:total cholesterol|cholesterol)\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "triglycerides":
            r"triglycerides?\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "creatinine":
            r"creatinine\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "urea":
            r"urea\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "alt":
            r"(?:alt|sgpt)\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "ast":
            r"(?:ast|sgot)\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "bilirubin":
            r"bilirubin\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "tsh":
            r"tsh\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "albumin":
            r"albumin\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "total_protein":
            r"(?:total protein)\s*[:\-]?\s*(\d+(?:\.\d+)?)"
    }

    for parameter, pattern in patterns.items():

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = match.group(1)

            value = value.replace(",", "")

            try:

                results[parameter] = float(value)

            except ValueError:

                pass

    return results


# ============================================================
# 4. ANALYZE VALUES
# ============================================================

def analyze_values(values):

    analysis = []

    for parameter, value in values.items():

        if parameter not in REFERENCE_RANGES:
            continue

        reference = REFERENCE_RANGES[parameter]

        minimum = reference["min"]
        maximum = reference["max"]
        unit = reference["unit"]

        if value < minimum:

            status = "LOW"

        elif value > maximum:

            status = "HIGH"

        else:

            status = "NORMAL"

        analysis.append({

            "parameter": parameter,
            "value": value,
            "unit": unit,
            "min": minimum,
            "max": maximum,
            "status": status

        })

    return analysis


# ============================================================
# 5. COMPLETE REPORT ANALYSIS
# ============================================================

def analyze_report(text):

    patient_name = extract_patient_name(text)

    diagnosis = extract_diagnosis(text)

    values = extract_medical_values(text)

    analysis = analyze_values(values)

    return {

        "patient_name": patient_name,

        "diagnosis": diagnosis,

        "parameters": analysis

    }