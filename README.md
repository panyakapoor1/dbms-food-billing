# 🍽 Food Billing System

A simple yet functional **Food Billing System** built with **Python**, **Streamlit**, and **MySQL** to manage food items and generate customer bills in a restaurant or food outlet environment.

---

## 📌 Features

- 🔐 **User Authentication**  
  Secure login with username and password.

- ➕ **Add Item**  
  Add new food items to the database.

- 🗑 **Delete Item**  
  Remove food items using Item No.

- ✏ **Update Item**  
  Edit existing item name and price.

- 🔍 **Search Item**  
  Search for food items by name.

- 🧾 **Generate Bills**  
  Add items to a bill, view running total, and save the final bill with a unique bill number.

- 💾 **Save Bill to Database**  
  Records customer name, bill amount, and bill number in the database.

- 🔒 **Logout**  
  Log out securely from the session.

---

## 🛠 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: [Python](https://www.python.org/)
- **Database**: [MySQL](https://www.mysql.com/)

---

## 🧰 Requirements

- Python 3.7+
- Streamlit
- MySQL Server (running locally or remotely)
- MySQL Connector for Python

**Install the required dependencies with:**
- pip install streamlit mysql-connector-python

---

## ⚙️ Database Setup

**Ensure your MySQL database includes the following tables:**

```bash
CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50)
);

CREATE TABLE item (
    ItemNo INT PRIMARY KEY,
    ItemName VARCHAR(100),
    ItemPrice FLOAT
);

CREATE TABLE bills (
    Bill_No INT PRIMARY KEY,
    Customer_Name VARCHAR(100),
    Bill_Amount FLOAT
);
```

**Add at least one user to get started:**

```bash
INSERT INTO users (username, password) VALUES ('admin', 'admin123');
```

---

## 🚀 How to Run

- Clone the repository

**Edit your MySQL connection settings in the script:**

```bash
system = SQL.connect(
    host="127.0.0.1",
    user="yourusername",
    password="yourpassword",
    database="yourdatabase"
)
```
---

**Run the Streamlit app:**

- streamlit run food_billing_system.py

---

## 📌 To Do / Future Enhancements

- Role-based access (admin vs cashier)
- Date-wise bill history
- Export bill as PDF
- UI/UX Styling enhancements

---

## 🙌 Acknowledgments

- Special thanks to Streamlit and MySQL for enabling easy and rapid application development.

---

## 📂 Project Structure

```bash
food_billing_system/
│
├── project-code.py    # Main application file
└── requirements.txt   # Python dependencies
