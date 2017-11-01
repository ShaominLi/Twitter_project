import psycopg2



#链接数据库
def connectDB(dbname,uname,psw):
    #conn=psycopg2.connect(database="test",user="lishaomin",password="19931004",host="127.0.0.1",port="5432")
    conn=psycopg2.connect(database=dbname,user=uname,password=psw,host="127.0.0.1",port="5432")
    return conn


#查询数据库
def queryDB(conn,sql_select):
    print("query data")
    cur=conn.cursor()
    #sql_select="select * from users;"
    cur.execute(sql_select)
    rows=cur.fetchall()
    #for row in rows:
    #print ("user:%s"%(row[1]))
    return rows



#插入数据
def insertDB(conn,sql_insert):
    '''
    sql_insert1="insert into users(name,password,birthday,email,country,inscription_date,picture) \
            values('{name}','{psw}','{birthday}','{email}','{country}','{ins_date}','{picture}');"
    sql_insert2="insert into users(name,password,email,country,inscription_date,picture) \
            values('{name}','{psw}','{email}','{country}',current_timestamp(0),'{picture}');"
    sql_insert=sql_insert2.format(name="test7",psw="123456",email="2222@test.com",country="China",picture="qwwqdewrweq")
    '''
    cur=conn.cursor()
    result=cur.execute(sql_insert)
    conn.commit()
    print("insert data successfull")
    return result


#关闭链接
def closeDB(conn):
    conn.close()



