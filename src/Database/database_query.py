import psycopg2
from psycopg2.extras import RealDictCursor



# getting multiple row from the database
def query_list(sql):
    hostname = 'localhost'
    database = input("enter the Database Name : ")
    username = input("enter the UserName : ")
    paas = input("enter the password  : ")
    post = 5432
    cur = None
    con = None


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
        print("connected to Database")
    except:
        print("Cannot Connect to database")
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql)
    response = []
    for row in cur:
        response.append(dict(row))






    # comiting and closing the cursor
    if con is not None:
        con.commit()
        con.close()
        print("\n\ncommited and closed the connection")
    if cur is not None:
        cur.close()
        print("closed the cursor")
    return response






# searching single result from the database
def search(sql):
    hostname = 'localhost'
    # database = input("enter the Database Name : ")
    # username = input("enter the UserName : ")
    # paas = input("enter the password  : ")
    database = ""
    username = "" 
    paas = ""
    post = 5432
    cur = None
    con = None


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
        print("connected to Database")
    except:
        print("Cannot Connect to database")
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql)
    # print(cur)
    # response = dict(cur)
    for x in cur:
        print(dict(x))
        response = dict(x)
    if con is not None:
        con.commit()
        con.close()
        print("\n\ncommited and closed the connection")
    if cur is not None:
        cur.close()
        print("closed the cursor")
    return response



# print(query_list('''Select * from "Admin"'''))
# print("the response from the user is \t : \t ", search("select * from \"Admin\" where id=1;"))


