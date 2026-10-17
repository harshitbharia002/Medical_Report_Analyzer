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
# QUESTION ANSWER FUNCTION
# =====================================================

def ask_question(question: str, report_text: str) -> str:

    # -------------------------------------------------
    # Check API Key
    # -------------------------------------------------

    if not API_KEY:

        return """
⚠️ **OpenAI API Key Not Found**

Please add your OpenAI API key in the `.env` file.
"""


    # -------------------------------------------------
    # Check Question
    # -------------------------------------------------

    if not question or not question.strip():

        return "⚠️ Please enter a question."


    # -------------------------------------------------
    # Check Report
    # -------------------------------------------------

    if not report_text or not report_text.strip():

        return """
⚠️ No medical report has been uploaded
or no readable text was found.
"""


    # =================================================
    # AI PROMPT
    # =================================================

    prompt = f"""
You are a Medical Report Question Answering Assistant.

Answer the user's question using ONLY the
information contained in the medical report.

IMPORTANT RULES:

1. Do NOT invent information.
2. Do NOT assume information that is not present.
3. If the answer is not present, say:

"This information is not mentioned in the report."

4. If a diagnosis is explicitly written,
   call it "Reported Diagnosis".
5. Do NOT create a new diagnosis.
6. Do NOT prescribe medicines.
7. Do NOT recommend treatment.
8. Do NOT change medical test values.
9. Keep the answer simple.

USER QUESTION:

{question}

MEDICAL REPORT:

{report_text}

Answer ONLY from the medical report.
"""


    # =================================================
    # CALL OPENAI API
    # =================================================

    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        answer = response.output_text

        if answer and answer.strip():

            return answer

        return "⚠️ AI returned an empty answer."


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
the QA Assistant.
"""


        # ---------------------------------------------
        # OTHER ERROR
        # ---------------------------------------------

        return f"""
❌ **QA Assistant Error**

Something went wrong while answering
your question.

Error:

`{str(e)}`
"""