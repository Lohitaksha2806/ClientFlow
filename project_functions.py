from db_connection import conn, cursor

def add_project():
    client_id = int(input("Enter client ID: "))
    project_name = input("Enter project name: ")
    project_type = input("Enter project type: ")
    deadline = input("Enter deadline (YYYY-MM-DD): ")
    budget = float(input("Enter project budget: "))

    query = """
    INSERT INTO Projects(client_id, project_name, project_type, start_date, deadline, status, budget)
    VALUES (%s, %s, %s, CURDATE(), %s, 'Pending', %s)
    """

    values = (client_id, project_name, project_type, deadline, budget)

    cursor.execute(query, values)
    conn.commit()

    print("Project added successfully!")

def view_projects():
    query = """
    SELECT project_id, project_name, project_type, deadline, status, budget
    FROM Projects
    """

    cursor.execute(query)
    result = cursor.fetchall()

    print("\n===== PROJECT LIST =====")
    for row in result:
        print(row)
        
        

from db_connection import cursor

def view_full_report():
    query = """
    SELECT 
        p.project_id,
        p.project_name,
        c.client_name,
        p.project_type,
        p.deadline,
        p.status,
        p.budget,
        IFNULL(SUM(pay.amount_paid), 0) AS total_paid
    FROM Projects p
    JOIN Clients c ON p.client_id = c.client_id
    LEFT JOIN Payments pay ON p.project_id = pay.project_id
    GROUP BY p.project_id, p.project_name, c.client_name, p.project_type, p.deadline, p.status, p.budget
    """

    cursor.execute(query)
    result = cursor.fetchall()

    print("\n===== FULL PROJECT REPORT =====")
    print("-" * 120)
    print(f"{'ID':<5}{'Project Name':<25}{'Client':<20}{'Type':<20}{'Deadline':<15}{'Status':<15}{'Budget':<12}{'Paid':<12}")
    print("-" * 120)

    for row in result:
        print(f"{row[0]:<5}{row[1]:<25}{row[2]:<20}{row[3]:<20}{str(row[4]):<15}{row[5]:<15}{str(row[6]):<12}{str(row[7]):<12}")