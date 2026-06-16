# Dr. Copper & Macro Freight Volatility Model

A Python-based financial risk engine that models macro-freight disruptions to predict industrial commodity volatility. This project mathematically isolates a **11-day transmission lag** between maritime supply chain shocks and copper return fluctuations, translating the statistical output into a dynamic Value-at-Risk (VaR) framework and an interactive Streamlit executive control room.

---

## 📊 Core Analytical Findings
* **The 11-Day Transmission Window:** Cross-correlation function (CCF) modeling mathematically proved that global maritime operational disruptions do not impact asset pricing immediately, but hit with a peak predictive lag of exactly **11 days**.
* **Asymmetric Risk Multiplier:** Utilizing a GARCH(1,1) time-series variance architecture, the model simulates a corporate copper inventory portfolio valued at **$5,000,000**. 
* **Capital Exposure Matrix:**
  * **Standard Operations Risk (Average Daily VaR):** `$64,106.56`
  * **Supply Chain Crisis Risk (Peak Daily VaR):** `$308,999.91` *(A ~5x spike in capital-at-risk moving across the 11-day lag pipeline).*

---

## 🛠️ Tech Stack & Methodology
* **Data Integration:** Consolidated multi-million row time-series data mapping daily freight risk indices alongside closing spot prices using `pandas` and `numpy`.
* **Statistical Modeling:** Leveraged `statsmodels` to execute forward-looking cross-correlation mapping.
* **Volatility Forecasting:** Implemented a `GARCH(1,1)` model via the `arch` library, treating supply chain disruptions as an exogenous variance factor to capture time-varying volatility clustering.
* **Interactive UI/UX:** Constructed an executive-facing simulation control room using `Streamlit` to allow parameter-driven scenario planning.

---

## 🚀 How to Run the Project

### 1. Clone the Repository & Install Dependencies
```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
pip install pandas numpy statsmodels arch streamlit
