
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Daily eCommerce Report", layout="wide")
st.title("📊 Daily eCommerce Analytics Report")

uploaded_file = st.file_uploader("Upload your CSV report", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Day'] = pd.to_datetime(df['Day'])
    df = df.sort_values(by='Day')

    # Calculate day-on-day change
    delta_df = df.copy()
    numeric_cols = df.select_dtypes(include='number').columns
    for col in numeric_cols:
        delta_df[f"{col} Δ%"] = df[col].pct_change().fillna(0) * 100

    # Display table with metrics and deltas
    st.subheader("📅 Daily Metrics with Day-on-Day Changes")
    st.dataframe(delta_df.style.format({col: "{:.2f}" for col in numeric_cols}).format({f"{col} Δ%": "{:+.2f}%" for col in numeric_cols}))

    # Auto commentary generation (basic)
    st.subheader("📝 Daily Commentary")
    for i in range(1, len(df)):
        today = df.iloc[i]
        yesterday = df.iloc[i - 1]
        day_label = today['Day'].strftime("%A, %B %d")

        # Example insights
        sales_change = (today['Total sales'] - yesterday['Total sales']) / yesterday['Total sales'] * 100
        visitors_change = (today['Online store visitors'] - yesterday['Online store visitors']) / yesterday['Online store visitors'] * 100
        cr_change = (today['Conversion rate'] - yesterday['Conversion rate']) / yesterday['Conversion rate'] * 100

        st.markdown(f"**{day_label}:**")
        st.markdown(
            f"- Total sales {'increased' if sales_change >= 0 else 'decreased'} by {sales_change:+.1f}% to ${today['Total sales']:.2f}.\n"
            f"- Visitor traffic {'rose' if visitors_change >= 0 else 'fell'} by {visitors_change:+.1f}%.\n"
            f"- Conversion rate {'improved' if cr_change >= 0 else 'declined'} by {cr_change:+.1f}% to {today['Conversion rate']:.2%}."
        )

        st.text_area(f"Add notes for {day_label}", key=f"notes_{i}")
