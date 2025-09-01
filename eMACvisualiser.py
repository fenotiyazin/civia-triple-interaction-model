import streamlit as st
import numpy as np
import plotly.graph_objects as go

# === CSS hack: white background ===
st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
        color: black;
    }
    .block-container {
        background-color: white;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Parameters
Ce50_prop = 4.5
Ce50_sevo = 2.6
Ce50_remi = 1.5
gamma = 5.2
gamma_0 = 2.7

def compute_P_eMAC(ce_prop, ce_sevo, ce_remi):
    U = (ce_prop / Ce50_prop + ce_sevo / Ce50_sevo) * (1 + (ce_remi / Ce50_remi) ** gamma_0)
    P = (U ** gamma) / (1 + U ** gamma)
    eMAC = (P / (1 - P)) ** (1 / gamma)
    return P, eMAC

st.markdown(
    "<h3 style='text-align: left;'>CIVIA – Triple Interaction Model</h3>",
    unsafe_allow_html=True
)

# Sidebar sliders
st.sidebar.header("Set Drug Concentrations")
ce_prop = st.sidebar.slider("CeProp (µg/mL)", 0.0, 10.0, 1.6, 0.1)
ce_sevo = st.sidebar.slider("EtSevo (%)", 0.0, 6.0, 0.4, 0.1)
ce_remi = st.sidebar.slider("CeRemi (ng/mL)", 0.0, 6.0, 1.8, 0.1)

# Sidebar annotation
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    ### Model Information
    This visual model is based on formulas by **Zhang et al. (2025)**  
    and was implemented by **Ahmet Ridvan Dogan**.
    Ce50 values and interaction parameters were derived from:  
    - Heyse (2012)  
    - Hannivoort (2016)  
    - Short (2002)  
    - Bouillon (2004)  

    **Ce50 values used:**  
    - Propofol: 4.5 µg/mL  
    - Sevoflurane ET: 2.6 %  
    - Remifentanil: 1.5 ng/mL  

    **Model outputs:**  
    - Probability of no response (P)  
    - Equivalent MAC (eMAC)  
    """
)

# Compute outputs
P0, eMAC0 = compute_P_eMAC(ce_prop, ce_sevo, ce_remi)

# Grid
ce_prop_vals = np.linspace(0.0, 10.0, 30)
ce_sevo_vals = np.linspace(0.0, 6.0, 30)
ce_remi_vals = np.linspace(0.0, 6.0, 30)
CeProp, CeSevo, CeRemi = np.meshgrid(ce_prop_vals, ce_sevo_vals, ce_remi_vals, indexing='ij')
U_all = (CeProp / Ce50_prop + CeSevo / Ce50_sevo) * (1 + (CeRemi / Ce50_remi) ** gamma_0)
P_all = (U_all ** gamma) / (1 + U_all ** gamma)

fig = go.Figure()

# Surfaces
fig.add_trace(go.Isosurface(
    x=CeProp.flatten(), y=CeSevo.flatten(), z=CeRemi.flatten(),
    value=P_all.flatten(),
    isomin=0.49, isomax=0.51,
    opacity=0.3,
    colorscale=[[0, "red"], [0.5, "orange"], [1, "green"]],
    showscale=False
))
fig.add_trace(go.Isosurface(
    x=CeProp.flatten(), y=CeSevo.flatten(), z=CeRemi.flatten(),
    value=P_all.flatten(),
    isomin=0.94, isomax=0.96,
    opacity=0.3,
    colorscale=[[0, "red"], [0.5, "orange"], [1, "green"]],
    showscale=False
))

# User point
fig.add_trace(go.Scatter3d(
    x=[ce_prop], y=[ce_sevo], z=[ce_remi],
    mode='markers+text',
    marker=dict(
        size=12,
        color=[P0],
        cmin=0, cmax=1,
        colorscale=[[0, "red"], [0.5, "orange"], [1, "green"]],
        colorbar=dict(
            title='Probability (P)',
            tickvals=[0, 0.25, 0.5, 0.75, 1],
            len=0.75
        ),
        showscale=True
    ),
    text=[f"P={P0:.2f}, eMAC={eMAC0:.2f}"],
    textposition='top center'
))

# Layout (big graph)
fig.update_layout(
    scene=dict(
        xaxis=dict(title='CeProp (µg/mL)'),
        yaxis=dict(title='EtSevo (%)'),
        zaxis=dict(title='CeRemi (ng/mL)'),
        aspectmode="cube"
    ),
    margin=dict(l=0, r=0, t=40, b=0),
    width=1200, height=900,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color="black")
)

# Show graph (top)
st.plotly_chart(fig, use_container_width=False)

# Current values (below graph, small font)
st.markdown(
    f"""
    <div style="font-size:14px; line-height:1.6; color:black;">
    <b>Current Point Values</b><br>
    - CeProp = {ce_prop:.2f} µg/mL<br>
    - EtSevo = {ce_sevo:.2f} %<br>
    - CeRemi = {ce_remi:.2f} ng/mL<br>
    - P = {P0:.2f}<br>
    - eMAC = {eMAC0:.2f}
    </div>
    """,
    unsafe_allow_html=True
)
