import sqlite3
import os

# Define the absolute path for the database file
db_file = os.path.abspath('clothing_store.db')
print(f"Database file will be created at: {db_file}")

def connection():
    # Connect to create the database tables
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    return conn, cursor

def log_sql(sql_statement, result):
    with open("query.txt", "a") as file:
        file.write(f"SQL Statement: {sql_statement}\n")
        file.write(f"Result: {result}\n\n")

# Function to create the database table
def create_table():
    conn, cursor = connection()
    # Execute a script to drop existing tables and create new ones
    cursor.executescript('''
    DROP TABLE IF EXISTS Customer;
    DROP TABLE IF EXISTS Payment;
    DROP TABLE IF EXISTS CustomerOrder;
    DROP TABLE IF EXISTS Orderclothing;
    DROP TABLE IF EXISTS Category;
    DROP TABLE IF EXISTS Clothing;
    
    CREATE TABLE Customer (
        CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Sex TEXT NOT NULL,
        Address TEXT NOT NULL,
        Phonenum TEXT NOT NULL
    );
    
    CREATE TABLE Payment (
        PaymentID INTEGER PRIMARY KEY AUTOINCREMENT,
        serviceprov TEXT NOT NULL,
        cardholdername TEXT NOT NULL,
        cardnum INTEGER NOT NULL,
        expdate TEXT NOT NULL,
        cvv INTEGER NOT NULL
    );
    
    CREATE TABLE CustomerOrder (
        OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
        CustomerID INTEGER NOT NULL,
        PaymentID INTEGER NOT NULL,
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
        FOREIGN KEY (PaymentID) REFERENCES Payment(PaymentID)
    );    

    CREATE TABLE Clothing (
        ClothingID INTEGER PRIMARY KEY AUTOINCREMENT,
        fabric TEXT NOT NULL,
        color TEXT NOT NULL,
        cost REAL NOT NULL,
        CategoryID INTEGER NOT NULL,
        FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID)
    );
    
    CREATE TABLE Orderclothing (
        OrderclothingID INTEGER PRIMARY KEY AUTOINCREMENT,
        OrderID INTEGER NOT NULL,
        ClothingID INTEGER NOT NULL,
        FOREIGN KEY (OrderID) REFERENCES CustomerOrder(OrderID),
        FOREIGN KEY (ClothingID) REFERENCES Clothing(ClothingID)
    );    
    
    CREATE TABLE Category (
        CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL 
    );    
                         ''')
    
    conn.close()

class add_stuff:
    # Inserting Customer
    def add_customer():
        conn, cursor = connection()
        # Basic Python list --> Customers
        customer_info = [
            (1, "Jaromir Tretiakov", "M", "157 Braemar Place", "(029) 8758-066"),
            (2, "Armen Mishin", "M", "73 Paerimu Street", "(026) 3179-474"),
            (3, "Qian Ho", "F", "20 Insignia Way", "(08) 9068 4900"),
            (4, "Maximilian Schwarz", "M", "1885 Thomas St", "082 620 5260")
        ]
        cursor.executemany('''
        INSERT INTO Customer (CustomerID, Name, Sex, Address, Phonenum) VALUES (?, ?, ?, ?, ?)
                    ''', customer_info)
        conn.commit()
        conn.close()
    
    # Add payment
    def add_payment():
        conn, cursor = connection()
        # Basic Python list --> Payment Details
        customer_payment = [
            (1, "mastercard", "Jaromir M Tretiakov", 5250229068534925, "08/25", 100),
            (2, "sketchy bank", "Qian Ho", 5430589986462753, "01/26", 750)
        ]
        cursor.executemany('''
        INSERT INTO Payment (PaymentID, serviceprov, cardholdername, cardnum, expdate, cvv) VALUES (?,?,?,?,?,?)
                           ''', customer_payment)
        conn.commit()
        conn.close()
    
    # Add Customer Order
    def add_customer_order():
        conn, cursor = connection()
        customer_order = [
                (1, 1, 1),
                (2, 2, 1),
                (3, 3, 2),
                (4, 4, 2)
            ]
        cursor.executemany('''
        INSERT INTO CustomerOrder (OrderID, CustomerID, PaymentID) VALUES (?, ?, ?)
                           ''', customer_order)
        conn.commit()
        conn.close()
        
    # Add Clothing
    def add_clothing():
        conn, cursor = connection()
        clothing = [
            (1, "wool", "Black", 30.50, 1),
            (2, "silk", "Darker Black", 23.80, 2),
            (3, "wood", "Even darker black", 13.00, 2)
        ]
        cursor.executemany('''
        INSERT INTO Clothing (ClothingID, fabric, color, cost, CategoryID) VALUES (?, ?, ?, ?, ?)                   
                           ''', 
                           clothing)
        conn.commit()
        conn.close()    
    # Connect Order + Clothing
    def rel_oc():
        conn, cursor = connection()
        oc = [
            (1, 1, 1),
            (2, 2, 3),
            (3, 4, 2)
        ]     
        cursor.executemany('''
        INSERT INTO Orderclothing (OrderclothingID, OrderID, ClothingID) VALUES (?, ?, ?)                   
                           ''', oc)
        conn.commit()
        conn.close()
        
    #define the category
    def cat():
        conn, cursor = connection()
        cat = [
            (1, "Dress"),
            (2, "Pants"),
            (3, "Underwear")
        ]
        cursor.executemany('''
        INSERT INTO Category (CategoryID, type) VALUES (?, ?)            
                           ''', cat)
        conn.commit()
        conn.close()

class query_1:
    #count
    def aggregate_count():
        conn, cursor = connection()
        sql_statement = '''
        SELECT COUNT(*) TotalCustomers FROM Customer;               
                       '''
        cursor.execute(sql_statement)
        result = cursor.fetchone()[0]
        print(f"TotalCustomers: {result}")
        log_sql(sql_statement, result)
        conn.commit()
        conn.close()
    
    #sum
    def aggregate_sum():
        conn, cursor = connection()
        sql_statement = '''
        SELECT SUM(cost) AS TotalClothingCost FROM Clothing;               
                       '''
        cursor.execute(sql_statement)
        result = cursor.fetchone()[0]
        print(f"TotalClothingCost: {result}")
        log_sql(sql_statement, result)
        conn.commit()
        conn.close()
    
    #avg
    def aggregate_avg():
        conn, cursor = connection()
        sql_statement = '''
        SELECT AVG(cost) AS AvgClothingCost FROM Clothing;               
                       '''
        cursor.execute(sql_statement)
        result = cursor.fetchone()[0]
        print(f"AvgClothingCost: {result}")
        log_sql(sql_statement, result)
        conn.commit()
        conn.close()
        
    #min
    def aggregate_min():
        conn, cursor = connection()
        sql_statement = '''
        SELECT MIN(cost) AS MinClothingCost FROM Clothing;               
                       '''
        cursor.execute(sql_statement)
        result = cursor.fetchone()[0]
        print(f"MinClothingCost: {result}")
        log_sql(sql_statement, result)
        conn.commit()
        conn.close()
    
    #max
    def aggregate_max():
        conn, cursor = connection()
        sql_statement = '''
        SELECT MAX(cost) AS MaxClothingCost FROM Clothing;               
                       '''
        cursor.execute(sql_statement)
        result = cursor.fetchone()[0]
        print(f"MaxClothingCost: {result}")
        log_sql(sql_statement, result)
        conn.commit()
        conn.close()
        
class query_2():
    def g():
        conn, cursor = connection()
        sql_statement = '''
        SELECT Payment.serviceprov, COUNT(DISTINCT Customer.CustomerID) AS Customer_Count
        FROM Payment
        JOIN CustomerOrder ON CustomerOrder.PaymentID = Payment.PaymentID
        JOIN Customer ON CustomerOrder.CustomerID = Customer.CustomerID
        GROUP BY Payment.serviceprov;          
                       '''
        cursor.execute(sql_statement)
        result = cursor.fetchall()
        result_str = "Results:\n"
        for row in result:
            serviceprov, customer_count = row
            result_str = f"Service Provider: {serviceprov}, Customer Count: {customer_count}"
            print(result_str)
            result_str += result_str + "\n"
        log_sql(sql_statement, result_str)
        conn.commit()
        conn.close()
    
    def o():
        conn, cursor = connection()
        sql_statement = '''
        SELECT fabric, cost
        FROM Clothing
        ORDER BY cost ASC;        
                       '''
        cursor.execute(sql_statement)
        result = cursor.fetchall()
        result_str = "Results:\n"
        for row in result:
            fabric, cost = row
            result_str = f"Fabric: {fabric}, Cost: {cost}"
            print(result_str)
            result_str += result_str + "\n"
        log_sql(sql_statement, result_str)
        conn.commit()
        conn.close()
    
    def multiple_join():
        conn, cursor = connection()
        sql_statement = '''
        SELECT Customer.Name, Clothing.cost, Payment.serviceprov
        FROM CustomerOrder
        JOIN Customer ON CustomerOrder.CustomerID = Customer.CustomerID
        JOIN Orderclothing ON CustomerOrder.OrderID = Orderclothing.OrderID
        JOIN Clothing ON Orderclothing.ClothingID = Clothing.ClothingID
        JOIN Payment ON CustomerOrder.PaymentID = Payment.PaymentID;
        '''
        cursor.execute(sql_statement)
        result = cursor.fetchall()
        result_str = "Results:\n"
        for row in result:
            name, cost, serviceprov = row
            result_str = f"Name: {name}, Cost: {cost}, Service Provider: {serviceprov}"
            print(result_str)
        log_sql(sql_statement, result_str)
        conn.commit()
        conn.close()
    
    def calc():
        conn, cursor = connection()
        sql_statement = '''
            SELECT fabric, cost, (cost * 1000) AS costfor1000
            FROM Clothing
            '''
        cursor.execute(sql_statement)
        result = cursor.fetchall()
        result_str = "Results:\n"
        for row in result: 
            fabric, cost, costfor1000 = row
            result_str = f"fabric: {fabric}, cost: {cost}, Cost for x1000: {costfor1000}"
            print(result_str)
        log_sql(sql_statement, result_str)
        conn.commit()
        conn.close()
    
    def conc():
        conn, cursor = connection()
        sql_statement = '''
        SELECT CustomerID, name || ' (' || Phonenum || ')' AS Contacts
        FROM Customer
        '''
        cursor.execute(sql_statement)
        result = cursor.fetchall()
        result_str = "Results:\n"
        for row in result:
            CustomerID, Contacts = row
            result_str = f"CustomerID: {CustomerID}, Contact: {Contacts}"
            print(result_str)
        log_sql(sql_statement, result_str)
        conn.commit()
        conn.close()


def insert_customer_db(customerID, name, sex, address, phonenum):
    conn, cursor = connection()
    try:
        cursor.execute('''
        INSERT INTO Customer(CustomerID, Name, Sex, Address, Phonenum) VALUES (?, ?, ?, ?, ?)              
        ''', (customerID, name, sex, address, phonenum))
        conn.commit()
    except Exception as e:
        print(f"An error has occured: {e}")
    finally:
        conn.close()
        
def insert_customer():
    #customerID = input("Enter customerID: ")
    customerID = input("CustomerID: ")
    name = input("name: ")
    sex = input("sex: ")
    address = input("address: ")
    phonenum = input("phone number: ")
    insert_customer_db(customerID, name, sex, address, phonenum)
    
def update_customer_db(customerID, name, sex, address, phonenum):
    conn, cursor = connection()
    try:
        cursor.execute('''
        UPDATE Customer
        SET Name = ?, Sex = ?, Address = ?, Phonenum = ?
        WHERE CustomerID = ?                
        ''', (name, sex, address, phonenum, customerID))
        conn.commit()
    except Exception as e:
        print(f"An error occured: {e}")
    finally:
        conn.close()

def update_customer():
    customerID = input("Enter customerID: ")
    name = input("name: ")
    sex = input("Sex: ")
    address = input("address: ")
    phonenum = input("Phone Number: ")
    insert_customer_db(customerID, name, sex, address, phonenum)
    
def delete_customer_db(customerID):
    conn, cursor = connection()
    try: 
        cursor.execute('''
        DELETE FROM Customer
        WHERE customerID = ?               
        ''', (customerID,))
        conn.commit()
    except Exception as e:
        print(f"An error occured: {e}")
    finally:
        conn.close()

def delete_customer():
    customerID = input("Enter customerID to delete: ")
    delete_customer_db(customerID,)
            
def selection():
    while True:
        print("-----------------------------")
        print("1. TotalCustomer (count)")
        print("2. TotalClothingCost (sum)")
        print("3. AvgClothingCost (average)")
        print("4. MinClothingCost (minimum)")
        print("5. MaxClothingCost (maximum)")
        print("6. Customer_Count (Group By)")
        print("7. Fabric + Price Ordering (Order By 'Ascending Order')")
        print("8. Selecting information from multiple entities (multiple joins)")
        print("9. Calculated Field")
        print("10. Concatenated Field")
        print("11. Quit")
        print("-----------------------------")
        second_selection = input("Enter choice --> ")
        
        if second_selection == "1":
            query_1.aggregate_count()
        elif second_selection == "2":
            query_1.aggregate_sum()
        elif second_selection == "3":
            query_1.aggregate_avg()
        elif second_selection == "4":
            query_1.aggregate_min()
        elif second_selection == "5":
            query_1.aggregate_max()
        elif second_selection == "6":
            query_2.g()
        elif second_selection == "7":
            query_2.o()
        elif second_selection == "8":
            query_2.multiple_join()
        elif second_selection == "9":
            query_2.calc()
        elif second_selection == "10":
            query_2.conc()
            
        #quit
        elif second_selection == "11":
            print("Going back into regular mode...")
            break
        else:
            print("action failed ❌ , returning...")
            break
        
#interface for inserting, deleting and updating records
def record_modification():
    while True:
        print("-----------------------------")
        print("1. Insert Customer")
        print("2. Update Customer")
        print("3. Delete Customer")
        print("4. Quit")
        print("-----------------------------")
        third_selection = input("Enter choice --> ")
        
    #if statements go here
        if third_selection == "1":
            insert_customer()
        elif third_selection == "2":
            update_customer()
        elif third_selection == "3":
            delete_customer()
        elif third_selection == "4":
            print("Going back into regular mode...")
            break
        else:
            print("action failed ❌ , returning...")
            break
        
# A list of options --> Selection mech.
def main():
    while True:
        print("-----------------------------")
        print("1. Create Database")
        print("2. Insert Data")
        print("3. Select SQL Query")
        print("4. Insert, update, delete")
        print("5. Quit")
        print("-----------------------------")
        user_select = input("Enter choice --> ")
    
    #if statements go here
        if user_select == "1":
            #calling create_table definition
            create_table()
            print("DATABASE HAS BEEN CREATED ✅")
        elif user_select == "2":
            #calling all items underneath the add_stuff class. 
            add_stuff.add_customer()
            add_stuff.add_payment()
            add_stuff.add_customer_order()
            add_stuff.add_clothing()
            add_stuff.rel_oc()
            add_stuff.cat()
            print("DATA HAS BEEN INSERTED INTO DATABASE ✅")
        elif user_select == "3":
            selection()
        elif user_select == "4":
            record_modification()
        elif user_select == "5":
            print("Quitting... :()")
            break
        else:
            print("Invalid Choice ❌")
        
if __name__ == "__main__":
    main()

