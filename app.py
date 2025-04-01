import streamlit as st
import pandas as pd

def calculate_discounted_prices(data, measurement):
    temp_data = data.copy()
    
    if measurement < 100:
        temp_data["Prix ajusté"] = temp_data["Prix de vente"]  # No discount
    elif 100 <= measurement <= 500:
        temp_data["Prix ajusté"] = temp_data["Prix de vente"] * 0.95  # 5% discount
    else:
        temp_data["Prix ajusté"] = temp_data["Prix de vente"] * 0.90  # 10% discount
    
    # Calculate adjusted profit
    temp_data["Profit ajusté"] = temp_data["Prix ajusté"] - temp_data["Prix d'achat"]
    
    return temp_data[["Code", "Name", "Prix d'achat", "Prix de vente", "Profit", "Prix ajusté", "Profit ajusté"]]

# Predefined DataFrame
data = pd.DataFrame({
    "Code": ["BCCHN22", "BCCHN25", "BCCHN35", "BCCHN45", "BCCHN55", "BCHTR22", "BCHTR45", "BCHTR55"],
    "Name": ["Chêne 22", "Chêne 25", "Chêne 35", "Chêne 45", "Chêne 55", "Hetre 22", "Hetre 45", "Hetre 55"],
    "Prix d'achat": [1.8, 2.0, 2.6, 3.3, 4.0, 1.7, 3.3, 3.9],
    "Prix de vente": [2.5, 2.85, 4.0, 5.15, 6.25, 2.5, 5.15, 6.25],
    "Profit": [0.7, 0.85, 1.4, 1.85, 2.25, 0.8, 1.85, 2.35]
})

st.title("Price Adjustment Calculator")

measurement = st.number_input("Enter measurement (m)", min_value=0, step=1, value=0)

adjusted_prices = calculate_discounted_prices(data, measurement)

if measurement > 0:
    st.write("### Adjusted Prices Table")
    st.dataframe(adjusted_prices)

st.write("## Generate Invoice")
selected_product = st.selectbox("Select a product", data["Name"])
selected_quantity = st.number_input("Enter quantity", min_value=1, step=1)

if selected_product and selected_quantity:
    product_row = adjusted_prices[adjusted_prices["Name"] == selected_product].iloc[0]
    total_price = product_row["Prix ajusté"] * selected_quantity
    
    st.write("### Invoice")
    st.write(f"**Product:** {selected_product}")
    st.write(f"**Unit Price (Adjusted):** {product_row['Prix ajusté']} DH")
    st.write(f"**Quantity:** {selected_quantity}")
    st.write(f"**Total Price:** {total_price} DH")
    st.write("**Thank you for your purchase!**")