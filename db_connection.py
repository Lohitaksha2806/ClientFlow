import mysql.connector # type: ignore

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="$Tea42Uetq2BU^TF",
    database="video_editing_db"
)

cursor = conn.cursor()