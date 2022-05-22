import psycopg2

hostname = 'localhost'
database = 'PYQT'
username = 'pyqt'
paas = "password"
post = 5432
cur = None
con = None



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
    sql = ''' drop table if exists admin ;
              drop table if exists cust ;
              drop table if exists ord ;
              drop table if exists food;'''
    cur.execute(sql)
    print("table dropped")
    admin = '''
            create table admin (
                id integer primary key,
                name varchar(15),
                l_name  varchar(15),
                username  varchar(20),
                password  varchar(20)
            );
            insert into admin values(
                1,
                'ad',
                'min',
                'ad',
                'ad'
            );
            create table cust (
                id integer primary key,
                phone  bigint unique,
                f_name  varchar(20),
                l_name  varchar(20)
            );
            create table food (
                id integer primary key,
                name varchar(40),
                about varchar(500),
                price integer 
            );
            create table ord (
                id integer primary key,
                total  integer,
                dt varchar(20),
                ucust integer not null
            );
    '''

    cur.execute(admin)
    # user = '''
    #     create table food (
    #         id integer primary key,
    #         name varchar(40),
    #         about varchar(500),
    #         price integer 
    #     );
    # '''
    # cur.execute(user)
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
