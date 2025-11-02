import streamlit as st
import mysql.connector
import pandas as pd

# -------------------------------
# MySQL Connection Function
# -------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Replace with your MySQL password
        database="inventory_system"
    )

# -------------------------------
# Streamlit Title & Sidebar
# -------------------------------
st.title("Inventory Control Management System")
st.subheader("Supports SDG 12: Responsible Consumption & Production")

menu = ["Add Product", "View Inventory", "Update Stock", "Delete Product", "Search Product"]
choice = st.sidebar.selectbox("Menu", menu)

# -------------------------------
# Add Product
# -------------------------------
if choice == "Add Product":
    st.header("Add New Product")
    name = st.text_input("Product Name")
    qty = st.number_input("Quantity", min_value=0)
    price = st.number_input("Price per Unit", min_value=0.0)
    expiry = st.date_input("Expiry Date")

    if st.button("Save Product"):
        try:
            con = get_connection()
            cur = con.cursor()
            cur.execute(
                "INSERT INTO products (product_name, quantity, price, expiry_date) VALUES (%s, %s, %s, %s)",
                (name, qty, price, expiry)
            )
            con.commit()
            con.close()
            st.success("✅ Product Added Successfully")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# -------------------------------
# View Inventory + Alerts
# -------------------------------
elif choice == "View Inventory":
    st.header("Current Inventory")
    try:
        con = get_connection()
        df = pd.read_sql("SELECT * FROM products", con)
        df['expiry_date'] = pd.to_datetime(df['expiry_date'])
        st.table(df)

        # Expired products alert
        expired_df = df[df['expiry_date'] < pd.Timestamp('today')]
        if not expired_df.empty:
            st.warning("⚠️ Expired Products Found")
            st.table(expired_df)

        # Low stock alert
        low_stock_df = df[df['quantity'] < 10]  # Threshold can be changed
        if not low_stock_df.empty:
            st.warning("⚠️ Low Stock Products")
            st.table(low_stock_df)

        con.close()
    except Exception as e:
        st.error(f"❌ Error: {e}")

# -------------------------------
# Update Stock
# -------------------------------
elif choice == "Update Stock":
    st.header("Update Product Quantity")
    try:
        con = get_connection()
        df = pd.read_sql("SELECT * FROM products", con)
        product = st.selectbox("Select Product", df["product_name"])
        qty_change = st.number_input("Add / Remove Stock", min_value=-100, max_value=100)

        if st.button("Update Quantity"):
            cur = con.cursor()
            cur.execute(
                "UPDATE products SET quantity = quantity + %s WHERE product_name = %s",
                (qty_change, product)
            )
            con.commit()
            con.close()
            st.success("✅ Stock Updated Successfully")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# -------------------------------
# Delete Product
# -------------------------------
elif choice == "Delete Product":
    st.header("Delete Product from Inventory")
    try:
        con = get_connection()
        df = pd.read_sql("SELECT * FROM products", con)
        product = st.selectbox("Select Product to Delete", df["product_name"])

        if st.button("Delete"):
            cur = con.cursor()
            cur.execute("DELETE FROM products WHERE product_name = %s", (product,))
            con.commit()
            con.close()
            st.warning("❌ Product Deleted Successfully")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# -------------------------------
# Search Product
# -------------------------------
elif choice == "Search Product":
    st.header("Search Product in Inventory")
    try:
        con = get_connection()
        df = pd.read_sql("SELECT * FROM products", con)
        search_name = st.text_input("Enter Product Name to Search")

        if st.button("Search"):
            result = df[df['product_name'].str.contains(search_name, case=False)]
            if not result.empty:
                st.table(result)
            else:
                st.warning("⚠️ Product Not Found")
        con.close()
    except Exception as e:
        st.error(f"❌ Error: {e}")
