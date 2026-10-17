import os
import tempfile

import streamlit as st

from extractor import (
    extract_text_from_pdf,
    extract_text_from_image
)

from analyzer import analyze_report

from summary import generate_ai_summary

from qa_assistant import ask_question


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Medical Report Analyzer",
    page_icon="🏥",
    layout="wide"
)


# =====================================================
# APPLICATION TITLE
# =====================================================

st.title("🏥 Automated Medical Report Analyzer")

st.write(
    "Upload a medical report to extract patient information, "
    "reported diagnosis, medical test results, and generate "
    "an AI-based summary."
)

st.divider()


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("📌 About Project")

    st.write(
        """
        This project analyzes medical reports using:

        • PDF Text Extraction
        • OCR for Images
        • Medical Parameter Analysis
        • AI-based Report Summary
        • Medical Report QA Assistant
        """
    )

    st.divider()

    st.info(
        """
        🎓 This project is developed for
        educational and informational purposes.
        """
    )


# =====================================================
# FILE UPLOAD
# =====================================================

st.header("📤 Upload Medical Report")

uploaded_file = st.file_uploader(
    "Choose a PDF or Image file",
    type=[
        "pdf",
        "png",
        "jpg",
        "jpeg"
    ]
)


# =====================================================
# IF FILE IS UPLOADED
# =====================================================

if uploaded_file is not None:

    st.success(
        f"✅ File uploaded successfully: {uploaded_file.name}"
    )


    # =================================================
    # CREATE TEMPORARY FILE
    # =================================================

    file_extension = os.path.splitext(
        uploaded_file.name
    )[1]


    temp_file_path = None


    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_extension
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            temp_file_path = temp_file.name


        # =============================================
        # TEXT EXTRACTION
        # =============================================

        st.divider()

        st.header("🔍 Report Text Extraction")


        with st.spinner(
            "🔄 Reading medical report..."
        ):

            if uploaded_file.name.lower().endswith(".pdf"):

                extracted_text = extract_text_from_pdf(
                    temp_file_path
                )

            else:

                extracted_text = extract_text_from_image(
                    temp_file_path
                )


        # =============================================
        # CHECK EXTRACTED TEXT
        # =============================================

        if not extracted_text:

            st.error(
                "❌ No readable text was found in the report."
            )

            st.stop()


        if not extracted_text.strip():

            st.error(
                "❌ Extracted text is empty."
            )

            st.stop()


        st.success(
            "✅ Report text extracted successfully."
        )


        # =============================================
        # MEDICAL REPORT ANALYSIS
        # =============================================

        st.divider()

        st.header("🧠 Medical Report Analysis")


        try:

            report = analyze_report(
                extracted_text
            )

        except Exception as e:

            st.error(
                f"❌ Error during medical report analysis: {e}"
            )

            st.stop()


        # =================================================
        # PATIENT INFORMATION
        # =================================================

        st.subheader("👤 Patient Information")


        patient_name = report.get(
            "patient_name",
            "Not found"
        )


        if not patient_name:

            patient_name = "Not found"


        st.write(
            f"**Patient Name:** {patient_name}"
        )


        # =================================================
        # REPORTED DIAGNOSIS
        # =================================================

        st.subheader(
            "🩺 Reported Diagnosis / Finding"
        )


        diagnosis = report.get(
            "diagnosis",
            ""
        )


        if diagnosis and diagnosis.strip():

            st.warning(
                f"📋 **Reported Diagnosis:** {diagnosis}"
            )

        else:

            st.info(
                "No diagnosis/finding was clearly "
                "mentioned in the report."
            )


        # =================================================
        # MEDICAL TEST RESULTS
        # =================================================

        st.divider()

        st.subheader(
            "🧪 Medical Test Results"
        )


        parameters = report.get(
            "parameters",
            []
        )


        if parameters:

            # =============================================
            # STATUS COUNTS
            # =============================================

            normal_count = 0
            high_count = 0
            low_count = 0
            unknown_count = 0


            for item in parameters:

                status = str(
                    item.get(
                        "status",
                        ""
                    )
                ).lower()


                if status == "normal":

                    normal_count += 1

                elif status == "high":

                    high_count += 1

                elif status == "low":

                    low_count += 1

                else:

                    unknown_count += 1


            # =============================================
            # SUMMARY CARDS
            # =============================================

            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "🟢 Normal",
                    normal_count
                )


            with col2:

                st.metric(
                    "🔴 High",
                    high_count
                )


            with col3:

                st.metric(
                    "🟡 Low",
                    low_count
                )


            with col4:

                st.metric(
                    "⚪ Unknown",
                    unknown_count
                )


            st.write("")


            # =============================================
            # RESULTS TABLE
            # =============================================

            table_data = []


            for item in parameters:

                table_data.append(
                    {
                        "Test": item.get(
                            "test",
                            "Unknown"
                        ),

                        "Value": item.get(
                            "value",
                            "N/A"
                        ),

                        "Unit": item.get(
                            "unit",
                            ""
                        ),

                        "Reference Range": item.get(
                            "reference_range",
                            "N/A"
                        ),

                        "Status": item.get(
                            "status",
                            "Unknown"
                        )
                    }
                )


            st.dataframe(
                table_data,
                use_container_width=True,
                hide_index=True
            )


            # =============================================
            # DETAILED ANALYSIS
            # =============================================

            st.subheader(
                "📊 Detailed Parameter Analysis"
            )


            for item in parameters:

                test_name = item.get(
                    "test",
                    "Unknown Test"
                )


                value = item.get(
                    "value",
                    "N/A"
                )


                unit = item.get(
                    "unit",
                    ""
                )


                reference_range = item.get(
                    "reference_range",
                    "N/A"
                )


                status = item.get(
                    "status",
                    "Unknown"
                )


                status_lower = str(
                    status
                ).lower()


                if status_lower == "normal":

                    icon = "🟢"

                elif status_lower == "high":

                    icon = "🔴"

                elif status_lower == "low":

                    icon = "🟡"

                else:

                    icon = "⚪"


                with st.expander(
                    f"{icon} {test_name}"
                ):

                    st.write(
                        f"**Test:** {test_name}"
                    )

                    st.write(
                        f"**Value:** {value} {unit}"
                    )

                    st.write(
                        f"**Reference Range:** "
                        f"{reference_range}"
                    )

                    st.write(
                        f"**Status:** {status}"
                    )


        else:

            st.info(
                "ℹ️ No supported medical test "
                "parameters were detected."
            )


       # =================================================
# AI SUMMARY
# =================================================

        st.divider()

        st.header("🤖 AI Report Summary")

        st.info(
    """
    AI Summary is currently unavailable because
    OpenAI API credits are exhausted.

    You can still view the extracted report,
    patient information, diagnosis, and test results.
    """
)


        # =================================================
# QA ASSISTANT
# =================================================

        st.divider()

        st.header("💬 Medical Report QA Assistant")

        st.warning(
    """
    QA Assistant is currently unavailable because
    OpenAI API credits are exhausted.

    Please add API credits to enable AI question answering.
    """
)

        # =================================================
        # EXTRACTED TEXT
        # =================================================

        st.divider()

        st.header(
            "📄 Extracted Report Text"
        )


        with st.expander(
            "Click here to view complete extracted text"
        ):

            st.text(
                extracted_text
            )


    except Exception as e:

        st.error(
            f"❌ Something went wrong: {e}"
        )


    finally:

        # ===============================================
        # DELETE TEMPORARY FILE
        # ===============================================

        if temp_file_path:

            try:

                if os.path.exists(
                    temp_file_path
                ):

                    os.remove(
                        temp_file_path
                    )

            except Exception:

                pass


# =====================================================
# IF NO FILE IS UPLOADED
# =====================================================

else:

    st.info(
        "👆 Please upload a medical PDF or image "
        "to start the analysis."
    )


# =====================================================
# MEDICAL DISCLAIMER
# =====================================================

st.divider()

st.warning(
    """
    ⚠️ **Medical Disclaimer**

    This application is an educational project and
    should not be used as a substitute for professional
    medical advice, diagnosis, or treatment.

    The system reports information found in the
    uploaded document and generates a summary.

    A reported diagnosis shown by the application means
    that the diagnosis was found in the uploaded report.
    It is NOT an AI-generated medical diagnosis.

    Always consult a qualified healthcare professional
    for medical decisions.
    """
)
