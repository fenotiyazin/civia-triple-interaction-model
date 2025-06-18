import numpy as np
import plotly.graph_objects as go
from tkinter import Tk, Label, Entry, Button, Frame
import webbrowser
import os
from plotly.colors import sample_colorscale

# Constants
C50_prop = 3.4
C50_sevo = 2.6
C50_remi = 1.7
gamma = 4.0
gamma_0 = 2.71

def p_to_color(p):
    color_scale = [[0.0, 'rgb(255,0,0)'], [0.5, 'rgb(255,165,0)'], [1.0, 'rgb(0,128,0)']]
    return sample_colorscale(color_scale, p, low=0, high=1)[0]

def calculate_and_show():
    try:
        ce_prop = float(entry_prop.get())
        ce_remi = float(entry_remi.get())
        ce_sevo = float(entry_sevo.get())
    except ValueError:
        print("Please enter numeric values for all fields.")
        return

    U = (ce_prop / C50_prop + ce_sevo / C50_sevo) * (1 + (ce_remi / C50_remi) ** gamma_0)
    P = (U ** gamma) / (1 + U ** gamma)
    eMAC = (P / (1 - P)) ** (1 / gamma)
    color = p_to_color(P)

    ce_prop_vals = np.linspace(0.0, 6.0, 60)
    ce_sevo_vals = np.linspace(0.0, 3.0, 60)
    ce_remi_vals = np.linspace(0.0, 4.0, 60)
    CeProp, CeSevo, CeRemi = np.meshgrid(ce_prop_vals, ce_sevo_vals, ce_remi_vals, indexing='ij')

    U_all = (CeProp / C50_prop + CeSevo / C50_sevo) * (1 + (CeRemi / C50_remi) ** gamma_0)
    P_all = (U_all ** gamma) / (1 + U_all ** gamma)

    fig = go.Figure()

    fig.add_trace(go.Isosurface(
        x=CeProp.flatten(),
        y=CeSevo.flatten(),
        z=CeRemi.flatten(),
        value=P_all.flatten(),
        isomin=0.49,
        isomax=0.51,
        surface_count=1,
        opacity=0.4,
        caps=dict(x_show=False, y_show=False, z_show=False),
        colorscale=[[0, "orange"], [1, "orange"]],
        showscale=False,
        name="P ≈ 0.5"
    ))

    fig.add_trace(go.Isosurface(
        x=CeProp.flatten(),
        y=CeSevo.flatten(),
        z=CeRemi.flatten(),
        value=P_all.flatten(),
        isomin=0.94,
        isomax=0.96,
        surface_count=1,
        opacity=0.4,
        caps=dict(x_show=False, y_show=False, z_show=False),
        colorscale=[[0, "green"], [1, "green"]],
        showscale=False,
        name="P ≈ 0.95"
    ))

    fig.add_trace(go.Scatter3d(
        x=[ce_prop],
        y=[ce_sevo],
        z=[ce_remi],
        mode='markers+text',
        marker=dict(size=6, color=color),
        text=[f"<b>P={P:.2f}<br>eMAC={eMAC:.2f}</b>"],
        textposition='top center',
        name='User Input Point'
    ))

    # Colorbar
    fig.add_trace(go.Scatter3d(
        x=[None], y=[None], z=[None],
        mode='markers',
        marker=dict(
            colorscale=[[0, "red"], [0.5, "orange"], [1, "green"]],
            cmin=0, cmax=1,
            colorbar=dict(
                title='Probability (P)',
                tickvals=[0, 0.25, 0.5, 0.75, 1],
                len=0.75
            ),
            showscale=True
        ),
        showlegend=False
    ))

    fig.update_layout(
        title={
            'text': "CIVIA Protocol - Isosurface Visualization (3D)<br><sub>- Dr. Ahmet Rıdvan Doğan -</sub>",
            'x': 0.5,
            'xanchor': 'center'
        },
        scene=dict(
            xaxis_title=dict(text='CeProp (\u00b5g/mL)', font=dict(size=18, family='Arial', color='black', weight='bold')),
            yaxis_title=dict(text='EtSevo (%)', font=dict(size=18, family='Arial', color='black', weight='bold')),
            zaxis_title=dict(text='CeRemi (ng/mL)', font=dict(size=18, family='Arial', color='black', weight='bold'))
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(x=0, y=1),
        annotations=[
            dict(
                showarrow=False,
                text=(
                    f"<b>User-defined values:</b><br>"
                    f"<b>P = {P:.3f}</b><br>"
                    f"<b>eMAC = {eMAC:.3f}</b>"
                ),
                x=0.98,
                y=0.75,
                xanchor='right',
                yanchor='middle',
                align='right',
                font=dict(size=14, color='black', family='Arial', weight='bold'),
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='black',
                borderwidth=1,
                borderpad=6
            ),
            dict(
                showarrow=False,
                text=(
                    "This visual model is based on formulas by Zhang et al. (2025).<br>"
                    "Ce50 values and interaction parameters were derived from:<br>"
                    "Heyse (2012), Hannivoort (2016), Short (2002), Bouillon (2004).<br><br>"
                    "<b>Ce50 values used:</b><br>"
                    "- Propofol: 3.4 \u00b5g/mL<br>"
                    "- Sevoflurane ET: 2.6 %<br>"
                    "- Remifentanil: 1.7 ng/mL<br><br>"
                    "Model outputs include probability of no response (P)<br>"
                    "and equivalent MAC (eMAC) based on selected concentrations."
                ),
                x=0.005,
                y=0.01,
                xanchor='left',
                yanchor='bottom',
                align='left',
                font=dict(size=10, color='black'),
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='black',
                borderwidth=1,
                borderpad=4
            )
        ]
    )

    file_path = os.path.abspath("civia_isosurface.html")
    fig.write_html(file_path)
    webbrowser.open('file://' + file_path)

# GUI
window = Tk()
window.title("CIVIA Model Input (Plotly Isosurface)")
window.geometry("400x250")

frame = Frame(window)
frame.pack(pady=20, expand=True, fill='both')

Label(frame, text="CeProp (\u00b5g/mL):").grid(row=0, column=0, sticky='e', padx=10, pady=5)
entry_prop = Entry(frame, width=15)
entry_prop.grid(row=0, column=1, padx=10, pady=5)

Label(frame, text="CeRemi (ng/mL):").grid(row=1, column=0, sticky='e', padx=10, pady=5)
entry_remi = Entry(frame, width=15)
entry_remi.grid(row=1, column=1, padx=10, pady=5)

Label(frame, text="EtSevo (%):").grid(row=2, column=0, sticky='e', padx=10, pady=5)
entry_sevo = Entry(frame, width=15)
entry_sevo.grid(row=2, column=1, padx=10, pady=5)

Button(window, text="Calculate and Visualize", command=calculate_and_show).pack(pady=10)

window.mainloop()
