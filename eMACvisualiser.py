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

# === Parameters ===
Ce50_prop = 7.58     # µg/mL
Ce50_sevo = 2.59     # %
Ce50_remi = 1.36     # ng/mL
gamma = 5.22
gamma_0 = 1.0

# === Function to compute P and eMAC ===
def compute_P_eMAC(ce_prop, ce_sevo, ce_remi):
    U = (ce_prop / Ce50_prop + ce_sevo / Ce50_sevo) * (
        1 + (ce_remi / Ce50_remi) ** gamma_0
    )
    P = (U ** gamma) / (1 + U ** gamma)
    eMAC = (P / (1 - P)) ** (1 / gamma)  # Zhang formülü
    return P, eMAC

# === Title ===
st.markdown(
    "<h3 style='text-align: left;'>CIVIA – Triple Interaction Model</h3>",
    unsafe_allow_html=True
)

# === Sidebar sliders ===
st.sidebar.header("Set Drug Concentrations")
ce_prop = st.sidebar.slider("CeProp (µg/mL)", 0.0, 10.0, 1.6, 0.1, format="%.1f")
ce_sevo = st.sidebar.slider("EtSevo (%)", 0.0, 6.0, 0.4, 0.1, format="%.1f")
ce_remi = st.sidebar.slider("CeRemi (ng/mL)", 0.0, 6.0, 1.8, 0.1, format="%.1f")

# === Sidebar annotation ===
st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    ### Model Information
    This visual model is based on formulas by **Zhang et al. (2025)**  
    and was implemented by **Ahmet Ridvan Dogan**.  

    **Ce50 values:**  
    - Propofol: {Ce50_prop:.2f} µg/mL  
    - Sevoflurane ET: {Ce50_sevo:.2f} %  
    - Remifentanil: {Ce50_remi:.2f} ng/mL  

    **Parameters:**  
    - γ = {gamma:.2f}  
    - γ₀ = {gamma_0:.2f}  

    **Model outputs:**  
    - Probability of no response (P)  
    - Equivalent MAC (eMAC)  
    """
)

# === Compute outputs ===
P0, eMAC0 = compute_P_eMAC(ce_prop, ce_sevo, ce_remi)

# === Grid for isosurfaces ===
ce_prop_vals = np.linspace(0.0, 10.0, 25)
ce_sevo_vals = np.linspace(0.0, 6.0, 25)
ce_remi_vals = np.linspace(0.0, 6.0, 25)
CeProp, CeSevo, CeRemi = np.meshgrid(
    ce_prop_vals, ce_sevo_vals, ce_remi_vals, indexing="ij"
)
U_all = (CeProp / Ce50_prop + CeSevo / Ce50_sevo) * (
    1 + (CeRemi / Ce50_remi) ** gamma_0
)
P_all = (U_all ** gamma) / (1 + U_all ** gamma)

fig = go.Figure()

# === Isosurface P = 0.5 (orange) ===
fig.add_trace(
    go.Isosurface(
        x=CeProp.flatten(),
        y=CeSevo.flatten(),
        z=CeRemi.flatten(),
        value=P_all.flatten(),
        isomin=0.5,
        isomax=0.5,
        surface_count=1,
        opacity=0.3,
        colorscale=[[0, "orange"], [1, "orange"]],
        showscale=False,
        hovertemplate=(
            "Prop (CeProp): %{x:.1f} µg/mL<br>"
            "Sevo (EtSevo): %{y:.1f} %<br>"
            "Remi (CeRemi): %{z:.1f} ng/mL<br>"
            "P = %{value:.2f}<extra></extra>"
        ),
    )
)


# === Isosurface P = 0.95 (green) ===
fig.add_trace(
    go.Isosurface(
        x=CeProp.flatten(),
        y=CeSevo.flatten(),
        z=CeRemi.flatten(),
        value=P_all.flatten(),
        isomin=0.95,
        isomax=0.95,
        surface_count=1,
        opacity=0.3,
        colorscale=[[0, "green"], [1, "green"]],
        showscale=False,
        hovertemplate=(
            "Prop (CeProp): %{x:.1f} µg/mL<br>"
            "Sevo (EtSevo): %{y:.1f} %<br>"
            "Remi (CeRemi): %{z:.1f} ng/mL<br>"
            "P = %{value:.2f}<extra></extra>"
        ),
    )
)

# === User point ===
fig.add_trace(
    go.Scatter3d(
        x=[ce_prop],
        y=[ce_sevo],
        z=[ce_remi],
        mode="markers+text",
        marker=dict(
            size=6,
            color=[P0],
            cmin=0,
            cmax=1,
            colorscale=[[0, "red"], [0.5, "orange"], [1, "green"]],
            colorbar=dict(
                title="Probability (P)",
                tickvals=[0, 0.25, 0.5, 0.75, 1],
                len=0.75,
            ),
            showscale=True,
        ),
        text=[f"P={P0:.1f}, eMAC={eMAC0:.1f}"],
        textposition="top center",
        hovertemplate=(
            "Prop (CeProp): %{x:.1f} µg/mL<br>"
            "Sevo (EtSevo): %{y:.1f} %<br>"
            "Remi (CeRemi): %{z:.1f} ng/mL<br>"
            "P = %{marker.color:.1f}<extra></extra>"
        ),
    )
)

# === Layout (big graph) ===
fig.update_layout(
    scene=dict(
        xaxis=dict(title="CeProp (µg/mL)"),
        yaxis=dict(title="EtSevo (%)"),
        zaxis=dict(title="CeRemi (ng/mL)"),
        aspectmode="cube",
    ),
    margin=dict(l=0, r=0, t=40, b=0),
    width=1200,
    height=900,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color="black"),
)

# === Show graph ===
st.plotly_chart(fig, use_container_width=False)

# === Current values (below graph) ===
st.markdown(
    f"""
    <div style="font-size:14px; line-height:1.6; color:black;">
    <b>Current Point Values</b><br>
    - CeProp = {ce_prop:.1f} µg/mL<br>
    - EtSevo = {ce_sevo:.1f} %<br>
    - CeRemi = {ce_remi:.1f} ng/mL<br>
    - P = {P0:.1f}<br>
    - eMAC = {eMAC0:.1f}
    </div>
    """,
    unsafe_allow_html=True,
)
