import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# Load the trained ML model
try:
    model = joblib.load('survey_attendance_model.pkl')
except Exception as e:
    st.error(f"Error loading the model: {str(e)}")
    st.stop()

# Load the dataset
try:
    data = pd.read_csv('dummy_npi_data.csv')

    # Rename columns to match the expected format (if necessary)
    # Ensure the column names match exactly what the model expects
    data.rename(columns={
        "Usage Time (mins)": "Usage Time (mins)",  # Keep original name
        "Count of Survey Attempts": "Count of Survey Attempts"  # Keep original name
    }, inplace=True)

except Exception as e:
    st.error(f"Error loading the dataset: {str(e)}")
    st.stop()

# Convert Login Time and Logout Time to minutes since midnight
try:
    data['Login_Time_Minutes'] = pd.to_datetime(data['Login Time']).dt.hour * 60 + pd.to_datetime(data['Login Time']).dt.minute
    data['Logout_Time_Minutes'] = pd.to_datetime(data['Logout Time']).dt.hour * 60 + pd.to_datetime(data['Logout Time']).dt.minute
except Exception as e:
    st.error(f"Error converting time columns: {str(e)}")
    st.stop()

# Streamlit App Title
st.title("Doctor Survey Attendance Predictor")

# User Input: Time Selection
input_time = st.time_input("Enter Time:", value=None)

if input_time:
    # Convert input time to minutes since midnight
    try:
        time_in_minutes = input_time.hour * 60 + input_time.minute
    except Exception as e:
        st.error(f"Invalid time format: {str(e)}")
        st.stop()

    # Add a new column for the input time
    data['Input_Time'] = time_in_minutes

    # Prepare the feature set for prediction
    # Ensure the feature names match exactly what the model expects
    required_features = ['Login_Time_Minutes', 'Logout_Time_Minutes', 'Usage Time (mins)', 'Count of Survey Attempts']

    # Check if all required features are present
    if not all(feature in data.columns for feature in required_features):
        st.error(f"Missing required features: {set(required_features) - set(data.columns)}")
        st.stop()

    # Predict likelihood of attendance
    try:
        # Use only the required features for prediction
        predictions = model.predict(data[required_features])
        data['Likely_to_Attend'] = predictions
    except Exception as e:
        st.error(f"Error during prediction: {str(e)}")
        st.stop()

    # Filter doctors likely to attend
    likely_doctors = data[data['Likely_to_Attend'] == 1][['NPI']]

    if likely_doctors.empty:
        st.warning("No doctors are likely to attend at the specified time.")
    else:
        st.success(f"{len(likely_doctors)} doctors are likely to attend at the specified time.")

        # Save the result to an Excel file
        output_file = 'likely_doctors.xlsx'
        try:
            likely_doctors.to_excel(output_file, index=False)
            st.success(f"Excel file saved successfully: {output_file}")
        except Exception as e:
            st.error(f"Error saving Excel file: {str(e)}")
            st.stop()

        # Download Button
        with open(output_file, "rb") as file:
            st.download_button(
                label="Download Doctors List (Excel)",
                data=file,
                file_name=output_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
