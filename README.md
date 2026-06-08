# Talegaon Farms — Sales Analytics Dashboard

## Project Overview
End-to-end data analytics project built on 5 years of real sales data 
from Talegaon Farms, a Mumbai-based farm delivery company serving 60+ 
housing societies.

## Business Problem
The business had 5 years of sales data but no structured way to understand 
customer behaviour, identify at-risk customers, or predict demand.

## What I Built
- Cleaned and combined 113,000+ records from 6 years of Excel files
- Performed exploratory data analysis to identify revenue patterns
- Built RFM customer segmentation (Champion, Loyal, Potential, Lost)
- Developed a churn prediction model using XGBoost (72% accuracy)
- Deployed an interactive Streamlit dashboard

## Key Findings
- Dairy accounts for 72% of total revenue
- Saturday generates 58% of weekly revenue
- Crescent Bay, historically the top building, declined 90% after Feb 2024
- 54% of customers have churned — retention is the biggest business risk
- Order frequency is the strongest predictor of churn (60% feature importance)

## Tech Stack
Python, Pandas, Matplotlib, Scikit-learn, XGBoost, Streamlit

## How to Run
pip install -r requirements.txt
streamlit run dashboard.py

## Data Privacy
All customer contact information was removed before analysis. 
This project was built with explicit permission from Talegaon Farms.