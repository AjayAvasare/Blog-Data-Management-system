import mysql.connector
# data base connection
conn_obj=mysql.connector.connect(host='localhost',
                        username='root',
                        password='1705200',
                        database='blogdatabase')
if conn_obj: # if connection is established
    print("connection established successfully")
else:
    print("please try again")
# create a cursor object
c1=conn_obj.cursor()
def create_table():# user define 
    # query for rows
    c1.execute("create table if not exists Blogtable(title Text,author Text,artical Text,post_date Date, image BLOB)")
def add_post(a,b,c,d,e):
    c1.execute("insert into Blogtable(title,author,artical,post_date,image) values(%s,%s,%s,%s,%s)",(a,b,c,d,e))
    conn_obj.commit()
def view_records():# view records
    c1.execute("select * from blogtable")
    data=c1.fetchall()
    return data
def get_title(x):
    c1.execute("select * from blogtable where title='{}'" .format(x))
    data=c1.fetchall()
    return data
def get_author(x):
    c1.execute("select * from blogtable where author='{}'" .format(x))
    data=c1.fetchall()
    return data
def delete_blog(author):
    c1.execute("delete from blogtable where author='{}'" .format(author))
    conn_obj.commit()