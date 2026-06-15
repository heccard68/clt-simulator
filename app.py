import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("👹 The 'Build-Your-Own-Monster' CLT Simulator")
st.markdown("""
### Watch Chaos Turn Into Order
The Central Limit Theorem (CLT) states that if you take enough random samples from **any** population, the distribution of those **sample means** will look like a normal distribution (a bell curve), no matter how strange or "monstrous" the original population is.
""")

st.sidebar.header("Configuration")

# 1. Choose a built-in "Monster" distribution shape
distribution_shape = st.sidebar.selectbox(
    "Choose your parent 'Monster' distribution:",
    ["Severely Right-Skewed (Income-like)", "Bimodal (Two Peaks)", "Uniform (Flat Chaos)", "U-Shaped", "Power Law / Pareto (Firm Size)"]
)

# Generate the underlying parent population based on user choice
np.random.seed(42)  # For reproducibility
N_POPULATION = 50000

if distribution_shape == "Severely Right-Skewed (Income-like)":
    # Exponential/Pareto-like mix
    population = np.random.exponential(scale=2.0, size=N_POPULATION)
elif distribution_shape == "Bimodal (Two Peaks)":
    # Two distinct normal distributions combined
    pop1 = np.random.normal(loc=10, scale=2, size=N_POPULATION // 2)
    pop2 = np.random.normal(loc=30, scale=3, size=N_POPULATION // 2)
    population = np.concatenate([pop1, pop2])
elif distribution_shape == "Uniform (Flat Chaos)":
    # Completely flat
    population = np.random.uniform(low=0, high=100, size=N_POPULATION)
elif  # U-Shaped
    # Pushing values to the extremes
    base = np.random.beta(a=0.5, b=0.5, size=N_POPULATION)
    population = base * 100
else:  # <-- ADD THIS NEW DEFAULT BLOCK FOR POWER LAW
    # Pareto distribution (Power Law) for firm sizes (e.g., number of employees).
    # shape=1.5 creates a heavy "fat tail" where a few firms are gargantuan.
    # We add 1 and multiply to ensure a realistic baseline company size.
    population = (np.random.pareto(a=1.5, size=N_POPULATION) + 1) * 10

# 2. Controls for the CLT Experiment
st.sidebar.subheader("CLT Parameters")
sample_size = st.sidebar.slider("Sample Size ($n$)\nHow many individuals in each draw?", min_value=2, max_value=100, value=5, step=1)
num_samples = st.sidebar.slider("Number of Samples\nHow many means do we calculate?", min_value=100, max_value=10000, value=2000, step=100)

# Run the simulation
# Pulling 'num_samples' separate batches, each of size 'sample_size'
samples = np.random.choice(population, size=(num_samples, sample_size))
sample_means = np.mean(samples, axis=1)

# Layout Columns for side-by-side comparison
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. The Parent 'Monster' Population")
    st.write(f"This is the distribution of the individual data points (Total: {N_POPULATION:,}).")
    
    fig_pop = px.histogram(
        pd.DataFrame({"Value": population}), 
        x="Value", 
        nbins=50,
        color_discrete_sequence=['#ff4b4b'],
        labels={'Value': 'Individual Value'}
    )
    fig_pop.update_layout(showlegend=False, height=450)
    st.plotly_chart(fig_pop, use_container_width=True)
    st.metric("True Population Mean ($\mu$)", f"{np.mean(population):.2f}")

with col2:
    st.subheader("2. The Distribution of Sample Means")
    st.write(f"We took {num_samples:,} random samples of size $n={sample_size}$, calculated the average of each, and plotted those averages.")
    
    fig_clt = px.histogram(
        pd.DataFrame({"Sample Mean": sample_means}), 
        x="Sample Mean", 
        nbins=50,
        color_discrete_sequence=['#1f77b4'],
        labels={'Sample Mean': 'Value of Sample Mean ($\overline{x}$)'}
    )
    fig_clt.update_layout(showlegend=False, height=450)
    st.plotly_chart(fig_clt, use_container_width=True)
    st.metric("Average of Sample Means", f"{np.mean(sample_means):.2f}")

# Educational kicker at the bottom
st.info(f"""
👉 **What to show your students:** Keep the parent population on something ugly (like Bimodal or Right-Skewed). 
Start with Sample Size ($n$) at **2**. The right graph will still look somewhat ugly. 
Now, slowly slide the Sample Size ($n$) up to **30, 50, or 100**. 
Watch how the right graph miraculously sheds its 'monster' traits and morphs into a beautiful, symmetrical Bell Curve—centered exactly at the population mean!
""")
