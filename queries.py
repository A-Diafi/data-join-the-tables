# pylint:disable=C0111,C0103
import sqlite3

conn = sqlite3.connect('data/ecommerce.sqlite')
db = conn.cursor()

def detailed_orders(db):
    '''return a list of all orders (order_id, customer.contact_name,
    employee.firstname) ordered by order_id'''

    query = """
    SELECT Orders.OrderID, Customers.ContactName AS Cust_name, Employees.FirstName AS Emp_name
    FROM Orders
    LEFT JOIN Customers ON Orders.CustomerID = Customers.CustomerID
    LEFT JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID
    """
    db.execute(query)
    rows = db.fetchall()
    return rows


def spent_per_customer(db):
    '''return the total amount spent per customer ordered by ascending total
    amount (to 2 decimal places)
    Exemple :
        Jean   |   100
        Marc   |   110
        Simon  |   432
        ...
    '''
    query = """
    SELECT Customers.ContactName AS Cust_name, ROUND(SUM(UnitPrice * Quantity), 2) AS Total_spent
    FROM Orders
    LEFT JOIN Customers ON Orders.CustomerID = Customers.CustomerID
    LEFT JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
    GROUP BY Cust_name
    ORDER BY Total_spent ASC
    """

    db.execute(query)
    rows = db.fetchall()
    return rows

def best_employee(db):
    '''Implement the best_employee method to determine who’s the best employee! By “best employee”, we mean the one who sells the most.
    We expect the function to return a tuple like: ('FirstName', 'LastName', 6000 (the sum of all purchase)). The order of the information is irrelevant'''

    query = """
    SELECT ROUND(SUM(UnitPrice * Quantity), 2) AS Total_spent, Employees.FirstName AS first_name, Employees.LastName AS last_name
    FROM Orders
    LEFT JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID
    LEFT JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
    GROUP BY Employees.EmployeeID
    ORDER BY Total_spent DESC
    """
    db.execute(query)
    rows = db.fetchall()
    return rows[0]



def orders_per_customer(db):
    '''Return a list of tuples where each tuple contains the contactName
    of the customer and the number of orders they made (contactName,
    number_of_orders). Order the list by ascending number of orders'''

    query = """
    SELECT Customers.ContactName AS Cust_name, COUNT(DISTINCT Orders.OrderID) AS num_of_orders
    FROM Customers
    LEFT JOIN Orders ON Orders.CustomerID = Customers.CustomerID
    LEFT JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
    GROUP BY Cust_name
    ORDER BY num_of_orders ASC
    """

    db.execute(query)
    rows = db.fetchall()
    return rows
