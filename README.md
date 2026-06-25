# 🚀 Digital Marketing Performance Analytics & ETL Pipeline

![Modern Data Stack](https://img.shields.io/badge/Architecture-Modern_Data_Stack-blue)
![Google BigQuery](https://img.shields.io/badge/Data_Warehouse-Google_BigQuery-blue)
![Python](https://img.shields.io/badge/Language-Python_3.10-yellow)
![Looker Studio](https://img.shields.io/badge/BI_Tool-Looker_Studio-orange)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

## 📊 Project Overview
This project is an End-to-End Data Engineering and Analytics solution designed to evaluate digital marketing campaign performance. It transforms raw data into actionable insights by implementing a **Modern Data Stack** architecture 100% in the cloud.

The system automates data extraction, calculates mathematically accurate financial KPIs, runs statistical A/B tests, and visualizes the results in an interactive dashboard, allowing marketing teams to optimize their budget in real-time and prevent ad spend waste.

## 🏗️ Data Architecture (ETL Pipeline)
The data flow follows a robust cloud-based ETL/ELT process:

1. **Extract:** Automated extraction of raw data stored in Google BigQuery using the official Python client.
2. **Transform:** Data cleaning and business metric calculations (CTR, CPC, CPA, ROAS) using **Pandas** in Python, effectively solving common issues like zero-division and aggregation bias.
3. **Load:** Insertion of the processed fact table (`marketing_kpis`) back into **Google BigQuery**.
4. **Business Rule Automation:** A Python script (`03_alerts_automation.py`) audits the database and triggers terminal alerts for campaigns with a ROAS below the 0.70 threshold.
5. **Visualization:** Native live connection between BigQuery and **Looker Studio** for corporate data consumption.

## 📈 Interactive Dashboard
The final product is a corporate dashboard focused on the financial health of the campaigns and ad spend monitoring.

*(Replace this line with a screenshot of your finished Dark Mode dashboard)*
![Dashboard Preview](<img width="1752" height="1020" alt="image" src="https://github.com/user-attachments/assets/58d7b84d-2dea-41cb-8bdc-b7dc1898ee63" />
)

### 💡 Business Questions Answered
* What is the global Return on Ad Spend (ROAS) and which active campaigns are operating below the profitability threshold?
* How does ad spend scale against daily generated revenue?
* Is there a statistically significant difference in the conversion rate between our two top-performing campaigns by impressions? *(A/B Testing implemented via Chi-Square and Z-Tests).*

## 🛠️ Technologies Used
* **Language:** Python (Pandas, Numpy, SciPy, Statsmodels)
* **Cloud Data Warehouse:** Google Cloud Platform (BigQuery)
* **Business Intelligence:** Looker Studio
* **Version Control:** Git & GitHub

## 📂 Repository Structure
```text
marketing-performance-dashboard/
│
├── data/
│   ├── raw/                  # Original raw data
│   └── processed/            # Cleaned data (Local backup copy)
│
├── notebooks/
│   ├── 01_eda.ipynb          # Exploratory Data Analysis & Cloud ETL Pipeline
│   └── 02_ab_testing.ipynb   # Statistical Hypothesis Testing
│
├── scripts/
│   └── 03_alerts_automation.py # Automated ad spend audit bot
│
├── .env.example              # Environment variables template
├── requirements.txt          # Python environment dependencies
└── README.md                 # Project technical documentation
```

## 🚀 How to Run This Project Locally

1. Clone this repository to your local machine:
   ```bash
   git clone [https://github.com/your-username/marketing-performance-dashboard.git](https://github.com/your-username/marketing-performance-dashboard.git)
   ```
2. Install the dependencies in your virtual environment:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Google Cloud Platform credentials (Service Account with BigQuery Admin roles).
4. Ensure the path to your JSON credentials file matches the one configured in the scripts.
5. Run the budget auditor to test the cloud connection:
   ```bash
   python scripts/03_alerts_automation.py
   ```

## 👤 Author
**Jorge Acuña Vallejos**
* [LinkedIn](https://www.linkedin.com/in/jacunav9105)
