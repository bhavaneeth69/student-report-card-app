import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',           
        password='bhavaneeth555',  
        database='student_report_db'
    )
    return conn

if __name__ == "__main__":
    con = get_connection()
    print("Connection successful:", con.is_connected())
