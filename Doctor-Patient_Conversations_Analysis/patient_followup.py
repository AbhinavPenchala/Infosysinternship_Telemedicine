import streamlit as st
import json
import requests

# Comprehensive Risk Assessment Data
data = {
    "Symptoms": [
        "Chest Pain", "Severe Headache", "High Fever", "Difficulty Breathing", 
        "Uncontrolled Bleeding", "Severe Abdominal Pain", "Seizures", 
        "Confusion", "Weakness on One Side", "Severe Burns", "Persistent Vomiting", 
        "Rapid Heartbeat", "Severe Back Pain", "Vision Loss", "Sudden Dizziness", 
        "Severe Allergic Reaction", "Coughing Blood", "Severe Dehydration", 
        "Pale Skin", "Loss of Consciousness", "Severe Fatigue", "Persistent Diarrhea", 
        "Severe Swelling", "Sudden Numbness", "Extreme Thirst", "Severe Joint Pain", 
        "Unexplained Weight Loss", "Severe Chest Tightness", "Severe Muscle Pain", 
        "Bluish Lips or Face"
    ],
    "Diseases": [
        "Heart Attack", "Stroke", "Sepsis", "Asthma Attack", "Pneumonia", 
        "Appendicitis", "Meningitis", "Kidney Failure", "Liver Failure", 
        "Diabetic Ketoacidosis", "COVID-19", "Cancer", "Tuberculosis", 
        "Hepatitis", "Malaria", "Dengue", "Chronic Obstructive Pulmonary Disease", 
        "Pulmonary Embolism", "Gastrointestinal Perforation", "Anaphylaxis", 
        "Severe Anemia", "Epilepsy", "Traumatic Brain Injury", "Heat Stroke", 
        "Hypothermia", "Hypertensive Crisis", "Rheumatoid Arthritis", 
        "Blood Clot", "Severe Infection", "Severe Depression"
    ]
} 
# Severity Scoring Dictionaries
disease_severity = {
    "Heart Attack": 9.5,
    "Stroke": 9.3,
    "Sepsis": 9.7,
    "Cancer": 9.0,
    "Organ Failure": 9.6,
    "COVID-19": 8.5,
    "Diabetic Ketoacidosis": 8.7,
    "Meningitis": 9.2,
    "Pulmonary Embolism": 8.8,
    "Anaphylaxis": 9.4
}

symptom_severity = {
    "Loss of Consciousness": 9.5,
    "Uncontrolled Bleeding": 9.3,
    "Difficulty Breathing": 8.7,
    "Chest Pain": 8.5,
    "Seizures": 9.0,
    "Severe Allergic Reaction": 9.2,
    "Coughing Blood": 8.8,
    "Sudden Numbness": 9.1,
    "Bluish Lips or Face": 9.4,
    "Severe Chest Tightness": 8.6
}
severity_keywords = {
    "High Risk": {
        "critical": 9.0,
        "life-threatening": 8.8,
        "emergency": 8.7,
        "acute": 8.5,
        "severe": 8.3,
        "fatal": 9.5,
        "unresponsive": 9.2
    },
    "Moderate Risk": {
        "moderate": 6.5,
        "serious": 7.0,
        "persistent": 7.2,
        "concerning": 6.8,
        "high": 7.8,
        "pain": 7.9,
        "significant": 7.5
        
    },
    "Low Risk": {
        "mild": 4.0,
        "minimal": 3.5,
        "slight": 3.8,
        "minor": 3.7
    }
}

def calculate_comprehensive_risk(symptoms, diseases, description):
    total_score = 0
    
    # Score diseases
    for disease in diseases:
        total_score += disease_severity.get(disease, 5.0)
    
    # Score symptoms
    for symptom in symptoms:
        total_score += symptom_severity.get(symptom, 4.0)
    
    # Score keywords in description
    for risk_level, keywords in severity_keywords.items():
        for keyword, score in keywords.items():
            if keyword in description.lower():
                total_score += score
    
    # Classify risk level
    if total_score > 15:
        return "High Risk", total_score
    elif total_score > 10:
        return "Moderate Risk", total_score
    elif total_score > 5:
        return "Low Risk", total_score
    else:
        return "Minimal Risk", total_score


# Function to schedule an appointment using Cal.com
def schedule_appointment(name, email, date, time):
    url = "https://api.cal.com/v2/bookings"
    
    formatted_time = time.strftime("%H:%M:%S")
    payload = json.dumps({
        "start": f"{date}T{formatted_time}Z",
        "eventTypeId": int(st.secrets["EVENT_TYPE_ID"]),  # Convert to integer
        "attendee": {
            "name": name,
            "email": email,
            "timeZone": "Asia/Kolkata",
            "language": "en"
        },
        "guests": []
    })
    
    headers = {
        "Authorization": f"Bearer {st.secrets['CAL_API_KEY']}",
        "Content-Type": "application/json",
        "cal-api-version": "2024-08-13"
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        response_json = response.json()
        if response.status_code == 201:
            return "Booking created successfully!", response_json
        else:
            return f"Failed to create booking. Error: {response_json}", None
    except json.JSONDecodeError:
        return "Failed to decode response.", None

# Streamlit UI
def main():
    st.title("Comprehensive Health Risk Assessment Tool with Appointment Scheduler")
    
    # User Information Section
    st.header("Personal Information")
    name = st.text_input("Full Name", placeholder="Enter your full name")
    email = st.text_input("Email", placeholder="Enter your email address")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    
    # Medical Information Section
    st.header("Medical Assessment")
    selected_symptoms = st.multiselect("Select Current Symptoms", data["Symptoms"])
    selected_diseases = st.multiselect("Select Known Medical Conditions", data["Diseases"])
    description = st.text_area("Describe Your Current Health Condition", placeholder="Provide additional details")
    # Risk Assessment Button
    if st.button("Assess Health Risk"):
        if not name or not email:
            st.warning("Please provide your name and email.")
        elif not selected_symptoms and not selected_diseases and not description:
            st.warning("Please provide some health information.")
        else:
            # Perform Risk Assessment
            risk_level, risk_score = calculate_comprehensive_risk(
                selected_symptoms, 
                selected_diseases, 
                description
            )
            
            # Display Results
            st.header("Risk Assessment Results")
            st.metric("Risk Level", risk_level)
            st.metric("Risk Score", f"{risk_score:.2f}")
            
            # Contextual Advice
            if risk_level == "High Risk":
                st.warning("🚨 High Risk: Consult Healthcare Professional ASAP")
                st.write("Your condition requires prompt medical evaluation.")
            elif risk_level == "Moderate Risk":
                st.info("⚕️ Moderate Risk: Schedule a Medical Consultation")
                st.write("Consider scheduling a doctor's appointment for thorough assessment.")
            else:
                st.success("✅ Low/Minimal Risk: Monitor Symptoms")
                st.write("Continue monitoring your health, but no immediate action required.")
    
    # Scheduling Section
    st.header("Schedule an Appointment")
    appointment_date = st.date_input("Select Appointment Date")
    appointment_time = st.time_input("Select Appointment Time")
    
    # Appointment Button
    if st.button("Schedule Appointment"):
        if not name or not email:
            st.warning("Please provide your name and email.")
        elif not selected_symptoms and not selected_diseases:
            st.warning("Please select at least one symptom or disease.")
        else:
            risk_level = "Moderate Risk"  # Example: Replace with actual risk calculation logic
            st.info(f"Your calculated risk level is: {risk_level}")
            
            # Schedule the appointment
            result, response_data = schedule_appointment(name, email, appointment_date, appointment_time)
            if response_data:
                st.success(f"Appointment Scheduled Successfully!\nDetails: {json.dumps(response_data, indent=4)}")
            else:
                st.error(result)

if __name__ == "__main__":
    main()
