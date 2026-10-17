import os

from dotenv import load_dotenv
from openai import OpenAI


# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()


# =====================================================
# GET OPENAI API KEY
# =====================================================

API_KEY = os.getenv("OPENAI_API_KEY")


# =====================================================
# CREATE OPENAI CLIENT
# =====================================================

client = None

if API_KEY:
    client = OpenAI(api_key=API_KEY)


# =====================================================
# AI SUMMARY FUNCTION
# =====================================================

def generate_ai_summary(report_text: str) -> str:

    # -------------------------------------------------
    # Check API Key
    # -------------------------------------------------

    if not API_KEY:

        return """
⚠️ **OpenAI API Key Not Found**

Please add your OpenAI API key in the `.env` file.

Example:

OPENAI_API_KEY=your_api_key_here
"""


    # -------------------------------------------------
    # Check Report Text
    # -------------------------------------------------

    if not report_text or not report_text.strip():

        return """
⚠️ **No Report Text Found**

The system could not find readable text
from the uploaded medical report.
"""


    # =================================================
    # AI PROMPT
    # =================================================

    prompt = f"""
You are a Medical Report Summarization Assistant.

Summarize ONLY the information present in the
medical report provided below.

IMPORTANT RULES:

1. Do NOT invent medical information.
2. Do NOT create a new diagnosis.
3. Do NOT assume diseases that are not present.
4. If a diagnosis is explicitly written, call it
   "Reported Diagnosis".
5. Do NOT prescribe medicines.
6. Do NOT recommend treatment.
7. Do NOT change medical values.
8. If information is missing, say:
   "Not mentioned in the report."
9. Keep the explanation simple.

Use this format:

## 👤 Patient Information

Mention patient name, age and gender if available.

## 🩺 Reported Diagnosis / Finding

Mention only the diagnosis/finding written
in the report.

## 🧪 Medical Test Results

Mention important test results with:
- Test Name
- Value
- Unit
- Reference Range
- Status

## 📋 Overall Summary

Give a short simple summary.

## ⚠️ Important Note

Mention that this AI summary is not a medical
diagnosis and should be reviewed by a qualified
healthcare professional.

MEDICAL REPORT:

{report_text}
"""


    # =================================================
    # CALL OPENAI API
    # =================================================

    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        result = response.output_text

        if result and result.strip():

            return result

        return "⚠️ AI returned an empty response."


    # =================================================
    # ERROR HANDLING
    # =================================================

    except Exception as e:

        error_message = str(e).lower()


        # ---------------------------------------------
        # CREDIT ERROR
        # ---------------------------------------------

        if (
            "credit_balance_exhausted" in error_message
            or "insufficient_quota" in error_message
            or "no credits remaining" in error_message
        ):

            return """
⚠️ **OpenAI API Credits Exhausted**

Your OpenAI API account currently has
no credits remaining.

Please add API credits to enable
AI Report Summary.

Your normal medical report analysis
can still work without AI.
"""


        # ---------------------------------------------
        # OTHER ERROR
        # ---------------------------------------------

        return f"""
❌ **AI Summary Error**

Something went wrong while generating
the AI summary.

Error:

`{str(e)}`
"""
