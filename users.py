import sql

class Users:
    def __init__(self,name=None,password=None,birthday=None,email=None,country=None):
        self.name=name
        self.password=password
        self.birthday=birthday
        self.email=email
        self.country=country
        self.inscription_date=None
        self.picture=None
        try:
            self.conn=sql.connectDB("test","lishaomin","19931004")
        except:
            pass 

    def clean(self):
        sql.closeDB(self.conn)


#1.user login 
def userLogin(user=Users()):

    sqlName="select count(*) from users where name='%s' and \
            password='%s';"%(user.name,user.password)
    checkName=sql.queryDB(user.conn,sqlName)

    result=checkName[0][0]
    if result == 0:
        return False
    else:
        user.conn=sql.connectDB("test","lishaomin","19931004")
        return True

#2.user apply
def userApply(user=Users()):
    t_sql_insert="insert into \
            users(name,password,birthday,email,country,inscription_date,picture) \
            values('{name}','{psw}','{birthday}','{email}','{country}',current_timestamp(0),'{picture}');"
    sql_insert=t_sql_insert.format(name=user.name,psw=user.password,birthday=user.birthday,\
            email=user.email,country=user.country,picture=None)

    sqlName="select count(*) from users where name='%s';"%(user.name)
    checkName=sql.queryDB(user.conn,sqlName)
    
    #no name
    if checkName[0][0] == 0:
        sql.insertDB(user.conn,sql_insert)
        return True
    else:
        return False









