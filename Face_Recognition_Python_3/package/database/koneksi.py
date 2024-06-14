import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="db_odoo_16",
        port="5432",
        user="odoo_16",
        password="admin@odoo" #juliusryanlistianto25
    )
    return conn

