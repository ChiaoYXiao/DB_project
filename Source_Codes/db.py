import mysql.connector


#建立DB連線
def get_conn():
    conn = mysql.connector.connect(host='localhost', \
           port='3306', \
           database='invest', \
           user='root', \
           password='c0830814', \
           charset='utf8mb4') 
    return conn

def query_data(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()
        
def process_data(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        return 0
    except mysql.connector.Error as error:
        return error
    finally:
        conn.close()
        
#if __name__ == "__main__":
        
        
        
