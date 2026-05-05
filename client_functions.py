from db_connection import conn, cursor


def add_client():
    name = input("Enter client name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email: ")
    company = input("Enter company name: ")

    query = """
    INSERT INTO Clients(client_name, phone, email, company_name, joined_date)
    VALUES (%s, %s, %s, %s, CURDATE())
    """

    values = (name, phone, email, company)

    cursor.execute(query, values)
    conn.commit()

    print("Client added successfully!")


def view_clients():
    cursor.execute("SELECT * FROM Clients")
    result = cursor.fetchall()

    print("\n===== CLIENT LIST =====")
    for row in result:
        print(row)