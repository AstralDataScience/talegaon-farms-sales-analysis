import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import glob

# Load and prepare data
@st.cache_data
def load_data():
    files = glob.glob(r'C:\\Users\\ACC1\\Desktop\\Project\\Big_Project\\*.xlsx')
    df = pd.concat([pd.read_excel(f) for f in files], ignore_index=True)
    df = df.drop(columns=['Mobile', 'Tower', 'Flat', 'Name'], errors='ignore')
    df = df.dropna(subset=['Building', 'Customer_ID'])
    df = df[df['Category'] != 'Sample']
    df = df[df['Order_Total'] > 0]
    df = df.dropna(subset=['Order_Total'])
    bulk_index = df[df['Order_Total'] == 37502.1].index
    df = df.drop(bulk_index[1:])
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Sidebar
st.sidebar.title("Talégaon Farms")
st.sidebar.markdown("Sales Analytics Dashboard")
page = st.sidebar.selectbox("Select Page", [
    "Overview", 
    "Product Analysis", 
    "Customer Segments",
    "Churn Prediction"
])

# Overview page
if page == "Overview":
    st.title("Business Overview")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"₹{df['Order_Total'].sum()/10000000:.1f} Cr")
    col2.metric("Total Orders", f"{len(df):,}")
    col3.metric("Unique Customers", f"{df['Customer_ID'].nunique():,}")
    
    st.subheader("Monthly Revenue Trend")
    monthly = df.groupby(df['Date'].dt.to_period('M'))['Order_Total'].sum()
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(monthly.index.astype(str), monthly.values, color='steelblue', linewidth=2)
    ax.set_xlabel('Month')
    ax.set_ylabel('Revenue (₹)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# Product Analysis page
elif page == "Product Analysis":
    st.title("Product Analysis")
    
    st.subheader("Revenue by Category")
    cat_rev = df.groupby('Category')['Order_Total'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(cat_rev.index, cat_rev.values, color='steelblue')
    ax.set_xlabel('Category')
    ax.set_ylabel('Revenue (₹)')
    plt.tight_layout()
    st.pyplot(fig)
    
    st.subheader("Top 10 Products by Revenue")
    prod_rev = df.groupby('Product')['Order_Total'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.barh(prod_rev.index, prod_rev.values, color='steelblue')
    ax.set_xlabel('Revenue (₹)')
    plt.tight_layout()
    st.pyplot(fig)

# Customer Segments page
elif page == "Customer Segments":
    st.title("Customer Segmentation")
    
    customer_activity = df.groupby('Customer_ID').agg(
        total_orders=('Date', 'count'),
        total_revenue=('Order_Total', 'sum'),
        last_order=('Date', 'max')
    ).reset_index()
    
    latest_date = df['Date'].max()
    customer_activity['days_since_last_order'] = (latest_date - customer_activity['last_order']).dt.days
    
    rfm = customer_activity[['Customer_ID', 'days_since_last_order', 'total_orders', 'total_revenue']].copy()
    rfm.columns = ['Customer_ID', 'Recency', 'Frequency', 'Monetary']
    
    rfm['R_Score'] = pd.qcut(rfm['Recency'].rank(method='first'), q=3, labels=[3,2,1])
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=3, labels=[1,2,3])
    rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), q=3, labels=[1,2,3])
    rfm['RFM_Score'] = rfm['R_Score'].astype(int) + rfm['F_Score'].astype(int) + rfm['M_Score'].astype(int)
    
    def rfm_segment(score):
        if score >= 8:
            return 'Champion'
        elif score >= 6:
            return 'Loyal'
        elif score >= 4:
            return 'Potential'
        else:
            return 'Lost'
    
    rfm['RFM_Segment'] = rfm['RFM_Score'].apply(rfm_segment)
    
    seg_counts = rfm['RFM_Segment'].value_counts()
    colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']
    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(seg_counts.index, seg_counts.values, color=colors)
    ax.set_xlabel('Segment')
    ax.set_ylabel('Number of Customers')
    plt.tight_layout()
    st.pyplot(fig)
    
    st.dataframe(rfm[['Customer_ID', 'Recency', 'Frequency', 'Monetary', 'RFM_Segment']].head(20))

# Churn Prediction page
elif page == "Churn Prediction":
    st.title("Churn Prediction")
    
    customer_activity = df.groupby('Customer_ID').agg(
        total_orders=('Date', 'count'),
        total_revenue=('Order_Total', 'sum'),
        last_order=('Date', 'max')
    ).reset_index()
    
    latest_date = df['Date'].max()
    customer_activity['days_since_last_order'] = (latest_date - customer_activity['last_order']).dt.days
    customer_activity['churn'] = (customer_activity['days_since_last_order'] > 180).astype(int)
    
    rfm = customer_activity[['Customer_ID', 'days_since_last_order', 'total_orders', 'total_revenue']].copy()
    rfm.columns = ['Customer_ID', 'Recency', 'Frequency', 'Monetary']
    
    X = rfm[['Frequency', 'Monetary']]
    y = customer_activity['churn']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = XGBClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    st.subheader("Predict Customer Churn")
    freq = st.slider("Order Frequency", 1, 100, 10)
    monetary = st.slider("Total Spend (₹)", 100, 100000, 5000)
    
    prediction = model.predict([[freq, monetary]])
    probability = model.predict_proba([[freq, monetary]])[0][1]
    
    if prediction[0] == 1:
        st.error(f"⚠️ High churn risk — {probability:.0%} probability of churning")
    else:
        st.success(f"✅ Low churn risk — {probability:.0%} probability of churning")