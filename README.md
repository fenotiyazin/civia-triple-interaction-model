# CIVIA – Triple Interaction Model

This repository hosts an interactive visualization tool for exploring the pharmacodynamic interaction between **propofol, sevoflurane, and remifentanil**.  
It provides a **four-dimensional response surface model** with probability of no response (P) and equivalent MAC (eMAC) estimation.  

## 🔬 Model Information
- Based on response surface equations by **Zhang et al. (2025)**  
- Implemented by **Ahmet Rıdvan Doğan**  
- Ce50 and interaction parameters derived from:
  - Heyse (2012)  
  - Hannivoort (2016)  
  - Short (2002)  
  - Bouillon (2004)  

**Ce50 values used:**
- Propofol: 4.5 µg/mL  
- Sevoflurane ET: 2.6 %  
- Remifentanil: 1.5 ng/mL  

## ⚙️ Requirements
The app requires:
- Streamlit  
- Plotly  
- Numpy  

Install dependencies with:
```bash
pip install -r requirements.txt
