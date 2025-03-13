# Doctor Survey Attendance Predictor

## Overview

This project is a machine learning-based web application that predicts which doctors are likely to attend a survey at a given time. The app uses historical data about doctors' login/logout times, usage patterns, and survey attempts to make predictions. The trained model is deployed using **Streamlit**, making it easy to interact with and test.

The model achieves **perfect accuracy, precision, and recall (1.00)** on the test dataset. However, this indicates potential **overfitting** or issues such as data leakage, class imbalance, or overly simplistic data. Further investigation is recommended to ensure the model generalizes well to real-world scenarios.

---

## Features

- **Time-Based Prediction**: Users can input a specific time, and the app will predict which doctors are likely to attend a survey at that time.
- **Dynamic Feature Engineering**: The app calculates features like `Active_Duration`, `Overlap_With_Input_Time`, and `Time_Since_Last_Login` dynamically based on the input time.
- **Interactive UI**: Built using **Streamlit**, the app provides an intuitive interface for users to input time and download results.
- **Export Results**: Predicted doctor lists can be downloaded as an Excel file.

---

## Dataset

The dataset (`dummy_npi_data.csv`) contains the following columns:

| Column Name               | Description                                      |
|---------------------------|--------------------------------------------------|
| NPI                       | Unique ID for each doctor                        |
| Login Time                | Time when the doctor logs into the app           |
| Logout Time               | Time when the doctor logs out of the app         |
| Usage Time (mins)         | Total time the doctor spends active in the app daily |
| Count of Survey Attempts  | Number of surveys the doctor has taken in the past |
| Region                    | Geographic region of the doctor                  |
| Speciality                | Medical speciality of the doctor                 |

### Preprocessing Steps
1. Extracted `Login Time` and `Logout Time` into minutes since midnight (`Login_Time_Minutes`, `Logout_Time_Minutes`).
2. Created dynamic features:
   - `Active_Duration`: Total time the doctor is active daily.
   - `Overlap_With_Input_Time`: Whether the input time falls within the doctor's active hours.
   - `Time_Since_Last_Login`: Proximity of the input time to the doctor's last login.
3. Defined the target variable (`Likely_to_Attend`) based on whether the doctor has taken at least one survey in the past.

---

## Model

### Training Process
1. **Algorithm**: The model was trained using a **RandomForestClassifier** from `sklearn`.
2. **Features**: The following features were used:
   - `Login_Time_Minutes`
   - `Logout_Time_Minutes`
   - `Usage Time (mins)`
   - `Count of Survey Attempts`
   - `Active_Duration`
   - `Overlap_With_Input_Time`
   - `Time_Since_Last_Login`
3. **Target Variable**: `Likely_to_Attend` (binary: 1 if likely to attend, 0 otherwise).
4. **Evaluation Metrics**: Accuracy, Precision, Recall.

### Performance
- **Accuracy**: 1.00
- **Precision**: 1.00
- **Recall**: 1.00

### Observations
- The model achieves **perfect scores** on the test dataset, which suggests potential issues:
  - **Overfitting**: The model may have memorized the training data instead of generalizing.
  - **Data Leakage**: Features like `Count of Survey Attempts` might directly encode the target variable.
  - **Class Imbalance**: If most doctors are labeled as likely to attend, the model may achieve high accuracy by always predicting the majority class.
  - **Simplistic Data**: Synthetic or overly simple datasets can lead to unrealistic performance.

Further investigation is needed to address these concerns and improve the model's robustness.

---

## Deployment

The app is deployed using **Streamlit** and is hosted on **Streamlit Community Cloud** https://doctor-survey.streamlit.app .

## Files

| File Name              | Description                                      |
|------------------------|--------------------------------------------------|
| `app.py`               | Main Streamlit app script                        |
| `requirements.txt`     | List of Python dependencies                      |
| `survey_attendance_model.pkl` | Trained machine learning model            |
| `dummy_npi_data.csv`   | Dataset used for training and prediction         |
| `model.ipynb`            | The model code, which creates the pkl file     |

---

