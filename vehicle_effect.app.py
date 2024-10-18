import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Define the logistic regression function
def logistic_function(intercept, hdv_coeff, ldv_coeff, hdv_count, ldv_count):
    linear_combination = intercept + hdv_coeff * hdv_count + ldv_coeff * ldv_count
    probability = 1 / (1 + np.exp(-linear_combination))  # Logistic function
    return probability

# Function to calculate confidence intervals
def calculate_ci(probability, standard_error, z_score=1.96):  # z_score=1.96 for 95% CI
    lower_bound = probability - z_score * standard_error
    upper_bound = probability + z_score * standard_error
    # Ensure probabilities stay within [0, 1]
    lower_bound = np.clip(lower_bound, 0, 1)
    upper_bound = np.clip(upper_bound, 0, 1)
    return lower_bound, upper_bound

# Model coefficients and a rough estimate for standard error (this is simplified)
intercept = -0.39984
hdv_coeff = -0.15672
ldv_coeff = -0.13555
standard_error = 0.05  # Assuming a rough standard error for demonstration

# Streamlit app layout
st.title("Bird Return to Nest Prediction with Confidence Intervals")
st.write("Adjust the vehicle counts to see how they affect the probability of birds returning to the nest.")

# Section 1: Heavy-duty Vehicle Count (HDV)
with st.expander("Heavy-duty Vehicle Count (HDV)", expanded=True):
    hdv_count = st.slider("Select HDV Count", 0, 18, 0)  # Updated range 0-18 for HDV

# Section 2: Light-duty Vehicle Count (LDV)
with st.expander("Light-duty Vehicle Count (LDV)", expanded=True):
    ldv_count = st.slider("Select LDV Count", 0, 19, 0)  # Updated range 0-19 for LDV

# Toggle for showing/hiding confidence intervals
show_ci = st.checkbox("Show Confidence Intervals", value=True)

# Calculate the probability using the logistic function
probability = logistic_function(intercept, hdv_coeff, ldv_coeff, hdv_count, ldv_count)

# Display the probability result
st.write(f"**Probability of bird returning to the nest:** {probability:.2%}")

# Generate a range of values for HDV and LDV to show the effect on probability
hdv_values = np.arange(0, 19)  # HDV range (0 to 18)
ldv_values = np.arange(0, 20)  # LDV range (0 to 19)

# Calculate probabilities and confidence intervals for the entire range of HDV and LDV counts
hdv_probabilities = [logistic_function(intercept, hdv_coeff, ldv_coeff, hdv, ldv_count) for hdv in hdv_values]
ldv_probabilities = [logistic_function(intercept, hdv_coeff, ldv_coeff, hdv_count, ldv) for ldv in ldv_values]

# If CI is enabled, calculate the CI values
if show_ci:
    hdv_lower_ci = [calculate_ci(p, standard_error)[0] for p in hdv_probabilities]
    hdv_upper_ci = [calculate_ci(p, standard_error)[1] for p in hdv_probabilities]
    ldv_lower_ci = [calculate_ci(p, standard_error)[0] for p in ldv_probabilities]
    ldv_upper_ci = [calculate_ci(p, standard_error)[1] for p in ldv_probabilities]

# Plot HDV Probability
hdv_fig = go.Figure()

# Add HDV probability line
hdv_fig.add_trace(go.Scatter(x=hdv_values, y=hdv_probabilities, mode='lines', name='HDV Probability',
                             line=dict(color='firebrick', width=2)))

# Add dashed CI lines if CI is enabled
if show_ci:
    hdv_fig.add_trace(go.Scatter(x=hdv_values, y=hdv_upper_ci, mode='lines', name='HDV Upper CI', 
                                 line=dict(color='firebrick', dash='dash', width=1)))
    hdv_fig.add_trace(go.Scatter(x=hdv_values, y=hdv_lower_ci, mode='lines', name='HDV Lower CI', 
                                 line=dict(color='firebrick', dash='dash', width=1)))

# Customize the HDV plot layout
hdv_fig.update_layout(
    title="Effect of HDV on Bird Return Probability",
    xaxis_title="HDV Count",
    yaxis_title="Probability of Bird Returning to Nest",
    font=dict(size=12),
    yaxis=dict(range=[0, 1])  # Probability should be between 0 and 1
)

# Plot LDV Probability
ldv_fig = go.Figure()

# Add LDV probability line
ldv_fig.add_trace(go.Scatter(x=ldv_values, y=ldv_probabilities, mode='lines', name='LDV Probability',
                             line=dict(color='royalblue', width=2)))

# Add dashed CI lines if CI is enabled
if show_ci:
    ldv_fig.add_trace(go.Scatter(x=ldv_values, y=ldv_upper_ci, mode='lines', name='LDV Upper CI', 
                                 line=dict(color='royalblue', dash='dash', width=1)))
    ldv_fig.add_trace(go.Scatter(x=ldv_values, y=ldv_lower_ci, mode='lines', name='LDV Lower CI', 
                                 line=dict(color='royalblue', dash='dash', width=1)))

# Customize the LDV plot layout
ldv_fig.update_layout(
    title="Effect of LDV on Bird Return Probability",
    xaxis_title="LDV Count",
    yaxis_title="Probability of Bird Returning to Nest",
    font=dict(size=12),
    yaxis=dict(range=[0, 1])  # Probability should be between 0 and 1
)

# Display the HDV plot
st.plotly_chart(hdv_fig)

# Display the LDV plot
st.plotly_chart(ldv_fig)
