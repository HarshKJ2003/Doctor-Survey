import streamlit as st
import pandas as pd
import joblib

# Load the trained ML model
try:
    model = joblib.load('survey_attendance_model.pkl')
except Exception as e:
    st.error(f"Error loading the model: {str(e)}")
    st.stop()

# Load the dataset
try:
    data = pd.read_csv('dummy_npi_data.csv')
    # Rename columns to match the expected format
    data.rename(columns={
        "Usage Time (mins)": "Usage_Time",
        "Count of Survey Attempts": "Survey_Attempts"
    }, inplace=True)
except Exception as e:
    st.error(f"Error loading the dataset: {str(e)}")
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

    # Predict likelihood of attendance
    try:
        predictions = model.predict(data[['Login_Time_Minutes', 'Logout_Time_Minutes', 'Usage_Time', 'Survey_Attempts', 'Input_Time']])
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
