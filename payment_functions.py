from db_connection import conn, cursor


def record_payment():
    project_id = int(input("Enter project ID: "))
    amount = float(input("Enter amount paid: "))
    method = input("Enter payment method: ")
    status = input("Enter payment status (Paid/Partial/Pending): ")

    cursor.callproc('AddPayment', [project_id, amount, method, status])
    conn.commit()

    print("Payment recorded successfully!")


def view_pending_payments():
    cursor.execute("SELECT * FROM PendingPaymentsView")
    result = cursor.fetchall()

    print("\n===== PENDING PAYMENTS =====")
    for row in result:
        print(row)