import sql

class Users:
    def __init__(self,name=None,password=None,email=None,country=None):
        self.name=name;
        self.password=password;
        self.birthday=None;
        self.email=email;
        self.country=country;
        self.inscription_date=None;
        self.picture=None;


#1.user login 
'''
return:
    -1:false connect 
     0:name error 
     1:password error 
     2:login success
'''
def userLogin(username,password):
    conn=sql.connectDB("test","lishaomin","19931004")
    flag=-1
    if conn == None:
        return flag
    else:
        flag=0
        sqlName="select count(*) from users where name='%s';"%(username)
        checkName=sql.queryDB(conn,sqlName)
        #check name
        for name in checkName:
            flag=flag+name[0]
        #check password
        if flag == 1:
            sqlPsw="select password from users where name='%s';"%(username)
            checkPsw=sql.queryDB(conn,sqlPsw)
            for psw in checkPsw:
                if password == psw[0]:
                    flag=flag+1
                    break
        
        sql.closeDB(conn)
        return flag

#2.user apply
'''
    return:
        -1:connect error
         1:name exist
         0:insert success
'''
def userApply(user=Users()):
    '''
    sql_insert1="insert into users(name,password,birthday,email,country,inscription_date,picture) \
            values('{name}','{psw}','{birthday}','{email}','{country}','{ins_date}','{picture}');"
    '''
    t_sql_insert="insert into users(name,password,email,country) values('{name}','{psw}','{email}','{country}');"
    sql_insert=t_sql_insert.format(name=user.name,psw=user.password,email=user.email,country=user.country)

    conn=sql.connectDB("test","lishaomin","19931004")
    flag=-1
    if conn == None:
        return flag
    else:
        flag=0;
        #check name
        sqlName="select count(*) from users where name='%s';"%(user.name)
        checkName=sql.queryDB(conn,sqlName)
        for name in checkName:
            flag=flag+name[0]
        
        if flag == 0:
            sql.insertDB(conn,sql_insert)
        
        sql.closeDB(conn)
        return flag;









