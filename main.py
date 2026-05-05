from client_functions import add_client, view_clients
from project_functions import add_project, view_projects
from payment_functions import record_payment, view_pending_payments
from revision_functions import add_revision
from project_functions import add_project, view_projects, view_full_report
while True:
    print("\n===== VIDEO EDITING CLIENT MANAGEMENT SYSTEM =====")
    print("1. Add Client")
    print("2. View Clients")
    print("3. Add Project")
    print("4. View Projects")
    print("5. View Full Report")
    print("6. Record Payment")
    print("7. View Pending Payments")
    print("8. Add Revision")
    print("9. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_client()
    elif choice == '2':
        view_clients()
    elif choice == '3':
        add_project()
    elif choice == '4':
        view_projects()
    elif choice == '5':
        view_full_report()
    elif choice == '6':
        record_payment()
    elif choice == '7':
        view_pending_payments()
    elif choice == '8':
        add_revision()
    elif choice == '9':
        print("Exiting system...")
        break