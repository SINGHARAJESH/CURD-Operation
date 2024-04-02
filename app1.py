import mysql.connector
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Rajesh Singha")


conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='RajeshSingha@123',
    database='gs',
    auth_plugin='mysql_native_password')

mycursor = conn.cursor()


if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False


def first_menu():
    st.title("Welcome to the Shopping Mall")
    if st.session_state.logged_in:
        second_menu()
    else:
        st.title("First Menu")
        first_input = st.sidebar.selectbox("Menu Options", ["Login", "Register", "Forget Password"])
        
        if first_input == "Login":
            login_user()
        elif first_input == "Register":
            register_user() 
        elif first_input == "Forget Password":
            reset_password()


def login_user():
    st.title("Login")
    email = st.text_input("Enter your email:")
    password = st.text_input("Enter your password:", type="password")

    if st.button("Login"):
        sql = ("SELECT * FROM accounts where email = %s AND password = %s")
        data = (email, password)
        mycursor.execute(sql, data)
        result = mycursor.fetchone()
        conn.commit()
        if result:
            st.session_state.logged_in = True
            second_menu()
        else:
            st.error("Wrong email or password")


def register_user():
    st.title("Register")
    username = st.text_input("Enter your name:")
    email = st.text_input("Enter your email:")
    password = st.text_input("Enter your password:", type="password")

    if st.button("Register"):
        sql = "SELECT * FROM accounts WHERE email = %s"
        data = (email,)
        mycursor.execute(sql,data)
        existing_user = mycursor.fetchone()
        if existing_user:
            st.error("Email already exists. Please choose a different email.")
        else:
            sql = "INSERT INTO accounts (username, email, password) VALUES (%s, %s, %s)"
            data = (username, email, password)
            mycursor.execute(sql, data)
            conn.commit()
            st.success("Registration successful")


def reset_password():
    st.title("Reset Password")
    email = st.text_input("Enter your email:")
    new_password = st.text_input("Enter new password:", type="password")

    if st.button("Reset Password"):
        sql = """UPDATE accounts
                 SET password = %s
                 WHERE email = %s"""
        data = (new_password, email)

        mycursor.execute(sql, data)
        conn.commit()
        st.success("Password reset successful")


def second_menu():
    st.title("Second Menu")

    
    second_input = st.sidebar.selectbox("Menu Options", ["New Customer", "Delete Customer Details", "Show Customer Details", "Update",
                                     "Show History", "Total", "Logout"])

    if second_input == "New Customer":
        product_insert()
    elif second_input == "Delete Customer Details":
        customer_delete()
    elif second_input == "Show Customer Details":
        show_details()
    elif second_input == "Update":
        customer_update()
    elif second_input == "Show History":
        show_history()
    elif second_input == "Total":
        calculate_total()
    elif second_input == "Logout":
        st.session_state.logged_in = False
        first_menu()


def product_insert():
    st.title("New Customer")
    Phone_number = st.text_input("Enter your phone number:")
    CustomerName = st.text_input("Enter your name:")
    ProductName = st.text_input("Enter product name:")
    Quantity = st.number_input("Enter quantity:", min_value=1)
    Price = st.number_input("Enter the price of the product:", format="%.2f")

    if st.button("Submit"):
        sql = "INSERT INTO ShoppingMall (Phone_number,  CustomerName, ProductName, Quantity, Price) VALUES (%s, %s, %s, %s, %s)"
        data = (Phone_number, CustomerName, ProductName, Quantity, Price)

        try:
            mycursor.execute(sql, data)
            conn.commit()
            st.success("New entry successful")
        except mysql.connector.Error as e:
            st.error(f"Error: {e}")


def show_details():
    st.title("Customer Details")
    number = st.text_input("Enter phone number to show details:")

    if st.button("Show"):
        query = 'select * from ShoppingMall where Phone_number = %s;'
        data = (number,)
        mycursor.execute(query, data)
        records = mycursor.fetchall()

        for record in records:
            details = {}
            details['Phone Number'] = record[0]
            details['Customer Name'] = record[1]
            details['Product Name'] = record[2]
            details['Quantity'] = record[3]
            details['Price'] = record[4]

            for key, value in details.items():
                st.write(f"{key}: {value}")


def calculate_total():
    st.title("Calculate Total")
    number = st.text_input("Enter your phone number:")

    if st.button("Calculate"):

        query = """SELECT Phone_number, 
               CustomerName, 
               ProductName, 
               Quantity, 
               Price, 
               Quantity * Price AS TotalPrice
               FROM ShoppingMall
               WHERE phone_number = %s;"""
        data = (number,)
        mycursor.execute(query, data)
        records = mycursor.fetchall()

        for record in records:
            details = {}
            details['Phone Number'] = record[0]
            details['Customer Name'] = record[1]
            details['Product Name'] = record[2]
            details['Quantity'] = record[3]
            details['Price'] = record[4]
            total_price = float(record[5])

            if total_price > 2000:
                discount = total_price * 0.1
                total_price_with_discount = total_price - discount
                st.write("<h3 style='color:blue;'>As you bought above 2000 so you will get 10% discount</h3>", unsafe_allow_html=True)


                #print(' ****As you bought above 2000 so you will get 10% discount***')

                details['Discount'] = discount
                details['Total Price After Discount'] = total_price_with_discount
            else:
                st.write("<h4 style='color:blue;'>As you bought below 2000 so you will not  get any discount</h4>", unsafe_allow_html=True)


                details['Discount'] = 0
                details['Total Price'] = total_price

            for key, value in details.items():
                st.write(f"{key}: {value}")


def show_history():
    st.title("Show History")
    query = """select * from ShoppingMall;"""
    mycursor.execute(query)
    records = mycursor.fetchall()
    df = pd.DataFrame(records, columns=['Phone_number', 'CustomerName', 'ProductName', 'Quantity', 'Price'])
    st.write(df)


def customer_update():
    st.title("Update Customer Details")
    Phone_number = st.text_input("Enter your phone number:")
    CustomerName = st.text_input("Enter your name:")
    ProductName = st.text_input("Enter product name:")
    Quantity = st.number_input("Enter quantity:", min_value=1)
    Price = st.number_input("Enter the price of the product:", format="%.2f")

    if st.button("Update"):
        sql = """UPDATE ShoppingMall
             SET CustomerName= %s, ProductName = %s, Quantity = %s, Price = %s
             WHERE phone_number = %s;"""
        data = (CustomerName, ProductName, Quantity, Price, Phone_number)

        try:
            mycursor.execute(sql, data)
            conn.commit()
            st.success("Update successful")
        except mysql.connector.Error as e:
            st.error(f"Error: {e}")


def customer_delete():
    st.title("Delete Customer Details")
    Phone_number = st.text_input("Enter your phone number to delete your details:")

    if st.button("Delete"):
        sql = "DELETE FROM ShoppingMall WHERE phone_number = %s;"
        data = (Phone_number,)

        try:
            mycursor.execute(sql, data)
            conn.commit()
            st.success("Delete successful")
        except mysql.connector.Error as e:
            st.error(f"Error: {e}")


if __name__ == "__main__":
    first_menu()
