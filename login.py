import mysql.connector
import pandas as pd

conn =mysql.connector.connect(
        host='localhost',
        user='root',
        password='RajeshSingha@123',
        database = 'gs',
        auth_plugin = 'mysql_native_password')
    
mycursor = conn.cursor()




def first_menu():
    
    while True:
       
       

       first_input = input("""
      how would you like to proceed?
    1. not a member? Register
    2. Already a member? Login
    3. Forget Password!
    4. Log out                       

    """)


       if first_input == '1':
          register_user()

       elif first_input == '2':
          login_user()

       elif first_input =='3':
          reset_password()
          
       elif first_input == '4':
          break
       else:
          print('Enter valid number')

            

def login_user():
   email = input('enter the email: ')
   password = input('enter the password: ')
   sql = ("SELECT * FROM accounts where email = %s AND password = %s")
   data = (email, password)
   mycursor.execute(sql,data)
   result = mycursor.fetchone()
   
   conn.commit()
   if result:
      #print('login successfully')
      second_menu()

   else:
      print('you enter worng email and password')


    
def register_user():
    username = input('enter your name: ')
    email = input('enter your email: ')
    password = input('enter you password: ')

    mycursor.execute("SELECT * FROM accounts WHERE email = %s and password = %s", (email,password))
    existing_user = mycursor.fetchone()
    
    if existing_user:
        print("Email and password already exists. Please choose a different email password.")

    else:
       
       
       sql = "INSERT INTO accounts (username, email, password) VALUES (%s, %s, %s)"
       data = (username,email, password)

       try:
          mycursor.execute(sql,data)
          print('register successfully')
          conn.commit()

       except mysql.connector.Error as e:
          print('Error retrieving data from MYsql:',e)


def reset_password():
    try:
        email = input('Enter your email to reset the password: ')
        password = input('Enter new password: ')
        
        sql = """UPDATE accounts
                 SET password = %s
                 WHERE email = %s"""
        data = (password, email)

        mycursor.execute(sql, data)
        print('Password reset successful')
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
          



def second_menu():

   while True:



      second_input = input("""

         1.Enter one for new customer!
         2.Enter two for delete customer detealls!
         3.Enter three for show customer detealls!
         4.Enter four for update 
         5.Enter five for show history
         6.Enter six for total                                  
         7.Enter six for logout!

      """
      )

      if second_input == '1':
         product_insert()

      elif second_input == '2':
         customer_delete()


      elif second_input == '3':
         show_details()

      elif second_input =='4':
         customer_update()

      elif second_input == '5':
         show_history()

      elif second_input =='6':
         calculate_total()
      

      elif second_input == '7':

         break

      else:
         print('Enter valid number ')


def product_insert():
   Phone_number = input('enter your phone number:')
   CustomerName = input('enter your name: ')
   ProductName = input('enter product name: ')
   Quantity = int(input('enter how many product do you want you puchase')) 
   Price = float(input('enter the price of the product'))

   sql = "INSERT INTO ShoppingMall (Phone_number,  CustomerName, ProductName, Quantity, Price) VALUES (%s, %s, %s, %s, %s)"
   data = (Phone_number,CustomerName,ProductName,Quantity,Price)


   try:
      mycursor.execute(sql,data)
      print('New entry successfull')
      conn.commit()

   except mysql.connector.Error as e:
      print('Error retrieving data from MYsql:',e)



def show_details():
   number = input('enter your phone number to show your details: ')
   
   queary = 'select * from ShoppingMall where Phone_number = %s;'
   data = (number,)

   mycursor.execute(queary,data)
   records = mycursor.fetchall()
   

   
   for record in records:
       details = {}
       details['Phone Number'] = record[0]
       details['Customer Name'] = record[1]
       details['Product Name'] = record[2]
       details['Quantity'] = record[3]
       details['Price'] = record[4]
       

       for key,value in details.items():
          print(f"{key} : {value}")
   


   

def calculate_total():
   number = input('Enter your phone number to show your details: ')

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
   print(' ****As you bought above 2000 so you will get 10% discount***')

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
           print(' ****As you bought above 2000 so you will get 10% discount***')
           details['Discount'] = discount
           details['Total Price After Discount'] = total_price_with_discount
       else:
           details['Discount'] = 0
           details['Total Price '] = total_price

       for key, value in details.items():
           print(f"{key}: {value}")


def show_history():

   queary = """select * from ShoppingMall;"""
   mycursor.execute(queary)
   records = mycursor.fetchall()

   df = pd.DataFrame(records,columns = ['Phone_number','CustomerName', 'ProductName','Quantity','Price'])
   print(df)
   
   
def customer_update():

   Phone_number = input('enter your phone number:')
   CustomerName = input('enter your name: ')
   ProductName = input('enter product name: ')
   Quantity = int(input('enter how many product do you want you puchase')) 
   Price = float(input('enter the price of the product'))

   sql = """UPDATE ShoppingMall
         SET CustomerName= %s, ProductName = %s, Quantity = %s, Price = %s
         WHERE phone_number = %s;"""
   data = (CustomerName,ProductName,Quantity,Price,Phone_number)


   try:
      mycursor.execute(sql,data)
      print('new update successfull')
      conn.commit()

   except mysql.connector.Error as e:
      print('Error retrieving data from MYsql:',e)


def customer_delete():
   Phone_number = input('Enter your phone number to delete you details : ')
   sql = "DELETE FROM ShoppingMall WHERE phone_number = %s;"


   data = (Phone_number,)


   try:
      mycursor.execute(sql,data)
      print('delect successful')
      conn.commit()

   except mysql.connector.Error as e:
      print('Error retrieving data from MYsql:',e)



first_menu()






         

       




    

    













































































































































































































































































