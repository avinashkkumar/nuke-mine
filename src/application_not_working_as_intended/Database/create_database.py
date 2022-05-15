import psycopg2

hostname = 'localhost'
database = input("enter the Database Name : ")
username = input("enter the UserName : ")
paas = input("enter the password  : ")
post = 5432
cur = None
con = None


print(database,username,paas)

if database == "":
    print("default")
    database = 'PYQT'

if username == "":
    print("default")
    username = 'pyqt'

if paas == "":
    print("default")
    paas = 'password'


try:
    con = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=paas,
        port=post,
    )
    print("connection created")
    cur = con.cursor()
    print("cursor created")
    # deleting the table if exists
    sql = ''' drop table if exists "Admin" '''
    cur.execute(sql)
    print("table dropped")
    sql = '''
            create table admin (
            id integer primary key,
            name varchar(15),
            l_name  varchar(15),
            username  varchar(20),
            password  varchar(20),
            last_login  varchar(25),
            token  varchar(60)
            );
    '''

    cur.execute(sql)
    con.commit()

    
except:
    print("cannot connect to the database")


# closing the cursor and connection in any case even if program is not able to complete the try block
# this is to avoid leaving the connection and cursor open after the program completion.
finally:
    if cur is not None:
        cur.close()
        print("cursor destroyed")
    if con is not None:
        con.close()
        print("connection destroyed")
