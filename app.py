import streamlit as st
import joblib
import pandas as pd
from backend.database import SessionLocal, Application

# Load AI model
model = joblib.load("complaint_priority_model.pkl")

# Page settings
st.set_page_config(
    page_title="Transparent India",
    page_icon="🇮🇳",
    layout="centered"
)

# Title
st.title("🇮🇳 Transparent India")
st.subheader("Public Service Tracking & AI Complaint Analysis")

st.write(
    "Track public-service applications and analyze complaints using AI."
)

# Tabs
tab1, tab2 = st.tabs([
    "📋 Track Application",
    "🤖 AI Complaint Analysis"
])


# -------------------------
# TRACK APPLICATION
# -------------------------

with tab1:

    st.header("Track Your Application")

    application_id = st.text_input(
        "Enter Application ID",
        placeholder="Example: APP001"
    )

    if st.button("Track Application"):

        if application_id:

            db = SessionLocal()

            application = (
                db.query(Application)
                .filter(
                    Application.application_id == application_id
                )
                .first()
            )

            db.close()

            if application:

                st.success("Application Found!")

                st.write("**Citizen Name:**", application.citizen_name)
                st.write("**Service:**", application.service)
                st.write("**Status:**", application.status)
                st.write("**Days Passed:**", application.days_passed)
                st.write("**Expected Days:**", application.expected_days)

                if application.days_passed > application.expected_days:
                    st.error("⚠️ Application is Delayed")
                else:
                    st.success("✅ Application is On Time")

            else:
                st.error("❌ Application not found.")

        else:
            st.warning("Please enter an Application ID.")


# -------------------------
# AI COMPLAINT ANALYSIS
# -------------------------

with tab2:

    st.header("AI Complaint Analysis")

    category = st.text_input(
        "Category",
        placeholder="Example: Water Supply"
    )

    department = st.text_input(
        "Department",
        placeholder="Example: Municipal Corporation"
    )

    state = st.text_input(
        "State",
        placeholder="Example: Karnataka"
    )

    city = st.text_input(
        "City",
        placeholder="Example: Bengaluru"
    )

    status = st.text_input(
        "Status",
        placeholder="Example: Pending"
    )

    pending_days = st.number_input(
        "Pending Days",
        min_value=0,
        value=0
    )

    escalated = st.selectbox(
        "Escalated?",
        ["Yes", "No"]
    )

    if st.button("Analyze Complaint"):

        complaint = pd.DataFrame([{
            "Category": category,
            "Department": department,
            "State": state,
            "City": city,
            "Status": status,
            "Pending_Days": pending_days,
            "Escalated": escalated
        }])

        prediction = model.predict(complaint)

        st.success(
            f"🤖 Predicted Priority: {prediction[0]}"
        )


# Footer
st.divider()

st.caption(
    "Transparent India — A student project for public-service transparency."
)