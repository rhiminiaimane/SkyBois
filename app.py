import streamlit as st
import pandas as pd
import numpy as np

# Constants
DISCOUNT_RULES = [
    (100, 1.00),
    (500, 0.95),
    (float('inf'), 0.90)
]

COLUMN_ORDER = [
    "Code", "Name", "Prix d'achat", "Prix de vente",
    "Profit", "Prix ajusté", "Profit ajusté"
]

def load_data():
    """Load and return the predefined product data."""
    return pd.DataFrame({
        "Code": ["BCCHN22", "BCCHN25", "BCCHN35", "BCCHN45", "BCCHN55", "BCHTR22", "BCHTR45", "BCHTR55"],
        "Name": ["Chêne 22", "Chêne 25", "Chêne 35", "Chêne 45", "Chêne 55", "Hêtre 22", "Hêtre 45", "Hêtre 55"],
        "Prix d'achat": [1.8, 2.0, 2.6, 3.3, 4.0, 1.7, 3.3, 3.9],
        "Prix de vente": [2.5, 2.85, 4.0, 5.15, 6.25, 2.5, 5.15, 6.25],
        "Profit": [0.7, 0.85, 1.4, 1.85, 2.25, 0.8, 1.85, 2.35]
    })

def get_discount_rate(measure):
    """Return the appropriate discount rate based on measurement."""
    for limit, rate in DISCOUNT_RULES:
        if measure < limit:
            return rate

def calculate_adjusted_prices(data, measure):
    """
    Calculate adjusted prices and profits based on measurement.
    
    Args:
        data: DataFrame containing product data
        measure: Measurement value for discount calculation
    
    Returns:
        DataFrame with adjusted prices and profits
    """
    discount_rate = get_discount_rate(measure)
    
    result = data.assign(
        **{
            "Prix ajusté": lambda df: df["Prix de vente"] * discount_rate,
            "Profit ajusté": lambda df: (df["Prix de vente"] * discount_rate) - df["Prix d'achat"]
        }
    )[COLUMN_ORDER]
    
    # Round numeric columns to 2 decimal places
    numeric_cols = result.select_dtypes(include=[np.number]).columns
    result[numeric_cols] = result[numeric_cols].round(2)
    
    return result

def display_invoice(product_data):
    """Display invoice generation section."""
    st.write("## Générer une facture")
    
    selected_product = st.selectbox(
        "Sélectionnez un produit",
        product_data["Name"],
        key="product_select"
    )
    
    quantity = st.number_input(
        "Entrez la quantité",
        min_value=1,
        step=1,
        key="quantity_input"
    )
    
    if selected_product and quantity:
        product_row = product_data[product_data["Name"] == selected_product].iloc[0]
        
        st.write("### Détails de la facture")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Produit sélectionné", selected_product)
            st.metric("Prix unitaire", f"{product_row['Prix ajusté']:.2f} DH")
        
        with col2:
            st.metric("Quantité", quantity)
            st.metric("Prix total", f"{product_row['Prix ajusté'] * quantity:.2f} DH")

def main():
    """Main application function."""
    st.title("Calculateur De Prix")
    
    # Load product data
    data = load_data()
    
    # Measurement input
    measure = st.number_input(
        "Entrez la mesure (m)",
        min_value=0,
        step=1,
        value=0,
        key="measure_input"
    )
    
    # Calculate adjusted prices
    adjusted_prices = calculate_adjusted_prices(data, measure)
    
    # Display adjusted prices table
    if measure > 0:
        st.write("### Tableau des prix ajustés")
        st.dataframe(adjusted_prices)
    
    # Invoice generation
    display_invoice(adjusted_prices)

if __name__ == "__main__":
    main()