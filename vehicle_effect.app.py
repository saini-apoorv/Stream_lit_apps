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

# Calculate the probability and confidence intervals using the logistic function
probability = logistic_function(intercept, hdv_coeff, ldv_coeff, hdv_count, ldv_count)
lower_ci, upper_ci = calculate_ci(probability, standard_error)

# Display the probability result
st.write(f"**Probability of bird returning to the nest:** {probability:.2%}")
st.write(f"**95% Confidence Interval:** ({lower_ci:.2%}, {upper_ci:.2%})")

# Generate a range of values for HDV and LDV to show the effect on probability
hdv_values = np.arange(0, 19)  # HDV range (0 to 18)
ldv_values = np.arange(0, 20)  # LDV range (0 to 19)

# Calculate probabilities and confidence intervals for the entire range of HDV and LDV counts
hdv_probabilities = [logistic_function(intercept, hdv_coeff, ldv_coeff, hdv, ldv_count) for hdv in hdv_values]
hdv_lower_ci = [calculate_ci(p, standard_error)[0] for p in hdv_probabilities]
hdv_upper_ci = [calculate_ci(p, standard_error)[1] for p in hdv_probabilities]

ldv_probabilities = [logistic_function(intercept, hdv_coeff, ldv_coeff, hdv_count, ldv) for ldv in ldv_values]
ldv_lower_ci = [calculate_ci(p, standard_error)[0] for p in ldv_probabilities]
ldv_upper_ci = [calculate_ci(p, standard_error)[1] for p in ldv_probabilities]

# Plot the probability of decrease for both HDV and LDV with confidence intervals
fig = go.Figure()

# Add HDV probability line
fig.add_trace(go.Scatter(x=hdv_values, y=hdv_probabilities, mode='lines', name='HDV Probability',
                         line=dict(color='firebrick', width=2)))
# Add shaded CI for HDV
fig.add_trace(go.Scatter(x=hdv_values, y=hdv_upper_ci, mode='lines', fill=None, line=dict(color='firebrick', width=0), showlegend=False))
fig.add_trace(go.Scatter(x=hdv_values, y=hdv_lower_ci, mode='lines', fill='tonexty', line=dict(color='firebrick', width=0), name='HDV CI', showlegend=True))

# Add LDV probability line
fig.add_trace(go.Scatter(x=ldv_values, y=ldv_probabilities, mode='lines', name='LDV Probability',
                         line=dict(color='royalblue', width=2)))
# Add shaded CI for LDV
fig.add_trace(go.Scatter(x=ldv_values, y=ldv_upper_ci, mode='lines', fill=None, line=dict(color='royalblue', width=0), showlegend=False))
fig.add_trace(go.Scatter(x=ldv_values, y=ldv_lower_ci, mode='lines', fill='tonexty', line=dict(color='royalblue', width=0), name='LDV CI', showlegend=True))

# Customize the plot layout
fig.update_layout(
    title="Effect of HDV and LDV on Bird Return Probability with Confidence Intervals",
    xaxis_title="Vehicle Count",
    yaxis_title="Probability of Bird Returning to Nest",
    legend_title="Vehicle Type",
    font=dict(size=12),
    xaxis=dict(tickvals=np.arange(0, max(len(hdv_values), len(ldv_values)), 1)),  # Ensure tick marks for every count
    yaxis=dict(range=[0, 1])  # Probability should be between 0 and 1
)

# Display the plot in Streamlit
st.plotly_chart(fig)
