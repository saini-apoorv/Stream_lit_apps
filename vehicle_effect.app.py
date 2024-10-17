import streamlit as st
import numpy as np
import plotly.graph_objects as go

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
    hdv_count = st.slider("Select HDV Count", 0, 18, 0)  # Updated range 0-18 for HDV

# Section 2: Light-duty Vehicle Count (LDV)
with st.expander("Light-duty Vehicle Count (LDV)", expanded=True):
    ldv_count = st.slider("Select LDV Count", 0, 19, 0)  # Updated range 0-19 for LDV

# Calculate the probability using the logistic function
probability = logistic_function(intercept, hdv_coeff, ldv_coeff, hdv_count, ldv_count)

# Display the probability result
st.write(f"**Probability of bird returning to the nest:** {probability:.2%}")

# Generate a range of values for HDV and LDV to show the effect on probability
hdv_values = np.arange(0, 19)  # HDV range (0 to 18)
ldv_values = np.arange(0, 20)  # LDV range (0 to 19)

# Calculate probabilities for the entire range of HDV and LDV counts
hdv_probabilities = [logistic_function(intercept, hdv_coeff, ldv_coeff, hdv, ldv_count) for hdv in hdv_values]
ldv_probabilities = [logistic_function(intercept, hdv_coeff, ldv_coeff, hdv_count, ldv) for ldv in ldv_values]

# Plot the probability of decrease for both HDV and LDV
fig = go.Figure()

# Add HDV probability line
fig.add_trace(go.Scatter(x=hdv_values, y=hdv_probabilities, mode='lines', name='HDV Probability',
                         line=dict(color='firebrick', width=2)))

# Add LDV probability line
fig.add_trace(go.Scatter(x=ldv_values, y=ldv_probabilities, mode='lines', name='LDV Probability',
                         line=dict(color='royalblue', width=2)))

# Customize the plot layout
fig.update_layout(
    title="Effect of HDV and LDV on Bird Return Probability",
    xaxis_title="Vehicle Count",
    yaxis_title="Probability of Bird Returning to Nest",
    legend_title="Vehicle Type",
    font=dict(
        size=12,
    ),
    xaxis=dict(tickvals=np.arange(0, max(len(hdv_values), len(ldv_values)), 1)),  # Ensure tick marks for every count
    yaxis=dict(range=[0, 1])  # Probability should be between 0 and 1
)

# Display the plot in Streamlit
st.plotly_chart(fig)

