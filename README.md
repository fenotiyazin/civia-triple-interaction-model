# CIVIA Triple Interaction Model Visualization Tool

This project provides an interactive visualization tool for the triple interaction pharmacodynamic model of propofol, remifentanil, and sevoflurane, based on the validated response surface model proposed by Zhang et al. (2025). The tool enables users to explore isosurfaces representing the probability of no response (P) based on user-defined drug concentrations.

- **Model:** Triple drug interaction model (propofol + remifentanil + sevoflurane)
- **Visualization:** 3D isosurfaces of constant P values (e.g., P ≈ 0.5, 0.95)
- **Output:** Interactive HTML visualization
- **Language:** Python
- **License:** Open for academic and non-commercial use

## How to Run

1. Install required Python packages (see `requirements.txt`).
2. Run the Python script:
    ```bash
    python eMAC_visual_english_edited.py
    ```
3. Enter desired effect-site concentrations and generate the visualization.

## Dependencies

- numpy
- plotly
- tkinter (usually pre-installed with Python)
- webbrowser (standard library)
- os (standard library)

## References

Zhang et al., Feasibility Study of an Indicator of Equivalent Anesthetic Effect for a Three-Drug Model (Anesth Analg, 2025).  
Additional parameter references: Heyse et al., Bouillon et al., Hannivoort et al.

## License

This code is provided for academic and non-commercial use only. Please cite the original article if used in publications.

---

