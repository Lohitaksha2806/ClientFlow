from db_connection import conn, cursor


def add_revision():
    project_id = int(input("Enter project ID: "))
    revision_number = int(input("Enter revision number: "))
    revision_notes = input("Enter revision notes: ")

    query = """
    INSERT INTO Revisions(project_id, revision_number, revision_notes, revision_date)
    VALUES (%s, %s, %s, CURDATE())
    """

    values = (project_id, revision_number, revision_notes)

    cursor.execute(query, values)
    conn.commit()

    print("Revision added successfully!")