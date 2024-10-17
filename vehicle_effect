import streamlit as st
import numpy as np

# Define the logistic regression function
def logistic_function(intercept, hdv_coeff, ldv_coeff, hdv_count, ldv_count):
    linear_combination = intercept + hdv_coeff * hdv_count + ldv_coeff * ldv_count
    probability = 1 / (1 + np.exp(-linear_combination))  # Logistic function
    return probability

# Model coefficients from your results
intercept = -0.39984
hdv_coeff = -0.15672
ldv_coeff = -0.13555

# Streamlit app layout
st.title("Bird Return to Nest Prediction")
st.write("Adjust the vehicle counts to see how they affect the probability of birds returning to the nest.")

# Section 1: Heavy-duty Vehicle Count (HDV)
with st.expander("Heavy-duty Vehicle Count (HDV)", expanded=True):
    hdv_count = st.slider("Select HDV Count", 0, 100, 0)  # Slider with range 0-100 for HDV

# Section 2: Light-duty Vehicle Count (LDV)
with st.expander("Light-duty Vehicle Count (LDV)", expanded=True):
    ldv_count = st.slider("Select LDV Count", 0, 100, 0)  # Slider with range 0-100 for LDV

# Calculate the probability using the logistic function
probability = logistic_function(intercept, hdv_coeff, ldv_coeff, hdv_count, ldv_count)

# Display the result
st.write(f"**Probability of bird returning to the nest:** {probability:.2%}")
