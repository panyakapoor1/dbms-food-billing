# food_billing_system.py

import streamlit as st # type: ignore
import mysql.connector as SQL # type: ignore
import random

# =================== Database Connection =====================
system = SQL.connect(
    host="127.0.0.1",            # 🖥 Change to your MySQL host if needed
    user="yourusername",         # 🔑 Your MySQL username
    password="yourpassword",     # 🔑 Your MySQL password
    database="yourdatabase"      # 🗄 Your MySQL database name
)
cursor = system.cursor()

# =================== Authentication =====================
def authenticate_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    return cursor.fetchone()

# =================== Functions =====================
def Addition(item_no, item_name, item_price):
    query = "INSERT INTO item VALUES (%s, %s, %s)"
    cursor.execute(query, (item_no, item_name, item_price))
    system.commit()
    st.success("New Item Added Successfully!")

def deletion(item_no):
    query = "DELETE FROM item WHERE ItemNo = %s"
    cursor.execute(query, (item_no,))
    system.commit()
    st.success("Item Deleted Successfully!")

def updation(item_no, item_name, item_price):
    query = "UPDATE item SET ItemName=%s, ItemPrice=%s WHERE ItemNo=%s"
    cursor.execute(query, (item_name, item_price, item_no))
    system.commit()
    st.success("Item Updated Successfully!")

def searching(item_name):
    query = "SELECT * FROM item WHERE ItemName LIKE %s"
    cursor.execute(query, ('%' + item_name + '%',))
    return cursor.fetchall()

# =================== Streamlit UI =====================
st.set_page_config(page_title="Food Billing System", page_icon="🍽")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = authenticate_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid Username or Password")
else:
    st.title("🍽 Food Billing System")

    menu = ["Add Item", "Delete Item", "Update Item", "Search Item", "Billing", "Logout"]
    choice = st.sidebar.radio("Menu", menu)

    if choice == "Add Item":
        st.subheader("➕ Add New Food Item")
        item_no = st.text_input("Enter Item No:")
        item_name = st.text_input("Enter Item Name:")
        item_price = st.text_input("Enter Item Price:")
        if st.button("Add Item"):
            if item_no and item_name and item_price:
                try:
                    Addition(int(item_no), item_name, float(item_price))
                except ValueError:
                    st.error("Please enter valid Item No and Price.")
            else:
                st.warning("Please fill all fields.")

    elif choice == "Delete Item":
        st.subheader("🗑 Delete Food Item")
        item_no = st.text_input("Enter Item No:")
        if st.button("Delete Item"):
            if item_no:
                try:
                    deletion(int(item_no))
                except ValueError:
                    st.error("Please enter a valid Item No.")
            else:
                st.warning("Please enter Item No.")

    elif choice == "Update Item":
        st.subheader("✏ Update Food Item")
        item_no = st.text_input("Enter Item No:")
        item_name = st.text_input("Enter New Item Name:")
        item_price = st.text_input("Enter New Item Price:")
        if st.button("Update Item"):
            if item_no and item_name and item_price:
                try:
                    updation(int(item_no), item_name, float(item_price))
                except ValueError:
                    st.error("Please enter valid Item No and Price.")
            else:
                st.warning("Please fill all fields.")

    elif choice == "Search Item":
        st.subheader("🔍 Search Food Item")
        item_name = st.text_input("Enter Item Name:")
        if st.button("Search"):
            if item_name:
                results = searching(item_name)
                if results:
                    for row in results:
                        st.write(f"Item No: {row[0]}, Name: {row[1]}, Price: ₹{row[2]}")
                else:
                    st.warning("No matching items found.")
            else:
                st.warning("Please enter an Item Name.")

    elif choice == "Billing":
        st.subheader("🛒 Generate Bill")

        if "bill_items" not in st.session_state:
            st.session_state.bill_items = []

        if "billing_complete" not in st.session_state:
            st.session_state.billing_complete = False

        cursor.execute("SELECT ItemNo, ItemName, ItemPrice FROM item")
        items = cursor.fetchall()

        if not st.session_state.billing_complete:
            if items:
                item_dict = {item[1]: (item[0], item[2]) for item in items}

                selected_item_name = st.selectbox("Select Food Item:", list(item_dict.keys()))

                qty = st.number_input("Enter Quantity:", min_value=1, step=1)

                if st.button("Add Item to Bill"):
                    if selected_item_name:
                        item_no, price = item_dict[selected_item_name]
                        st.session_state.bill_items.append((item_no, qty))
                        st.success(f"Added {selected_item_name} to bill!")
                    else:
                        st.warning("Please select an item.")

                st.write("### Current Bill Items:")
                if st.session_state.bill_items:
                    for idx, (item_no, qty) in enumerate(st.session_state.bill_items):
                        cursor.execute("SELECT ItemName FROM item WHERE ItemNo = %s", (item_no,))
                        item_name_result = cursor.fetchone()
                        if item_name_result:
                            item_name = item_name_result[0]
                            st.write(f"{idx+1}. {item_name}, Quantity: {qty}")

                if st.button("Finish Billing"):
                    if st.session_state.bill_items:
                        st.session_state.billing_complete = True
                    else:
                        st.warning("Please add items to the bill first.")
            else:
                st.warning("No items available in database.")

        else:
            if st.session_state.bill_items:
                total = 0
                st.write("## 🧾 Bill Details:")
                bill_data = []

                for item_no, qty in st.session_state.bill_items:
                    cursor.execute("SELECT * FROM item WHERE ItemNo = %s", (item_no,))
                    result = cursor.fetchone()
                    if result:
                        item_name = result[1]
                        item_price = result[2]
                        subtotal = qty * item_price
                        total += subtotal
                        bill_data.append((item_name, qty, item_price, subtotal))

                for idx, (item_name, qty, price, subtotal) in enumerate(bill_data):
                    st.write(f"{idx+1}. {item_name}** - {qty} × ₹{price} = ₹{subtotal}")

                st.success(f"### ✅ Total Bill Amount: ₹{total}")

                customer_name = st.text_input("Enter Customer Name to Save Bill:")
                if st.button("Save Bill"):
                    if customer_name:
                        bill_no = random.randint(1000, 9999)
                        try:
                            insert_query = "INSERT INTO bills (Bill_No, Customer_Name, Bill_Amount) VALUES (%s, %s, %s)"
                            cursor.execute(insert_query, (bill_no, customer_name, total))
                            system.commit()
                            st.success(f"Bill Saved Successfully! Bill No: {bill_no}")
                            # Reset billing
                            st.session_state.bill_items = []
                            st.session_state.billing_complete = False
                        except SQL.Error as e:
                            st.error(f"Error saving bill: {e}")
                    else:
                        st.warning("Please enter Customer Name.")
            else:
                st.warning("No items to bill.")

    elif choice == "Logout":
        st.session_state.logged_in = False
        st.success("Logged out successfully!")