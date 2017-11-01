from modules import sql

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
        self.name=None;
        self.password=None;
        self.birthday=None;
        self.email=None;
        self.count=None;
        self.inscription_date=None;
        self.picture=None;
        sql.closeDB(self.conn)

    def userLogin(self):

        sqlName="select count(*) from users where name='%s' and \
                password='%s';"%(self.name,self.password)
        checkName=sql.queryDB(self.conn,sqlName)

        result=checkName[0][0]
        if result == 0:
            self.clean()
            return False
        else:
            return True

    def userApply(self):
        t_sql_insert="insert into \
                users(name,password,birthday,email,country,inscription_date,picture) \
                values('{name}','{psw}','{birthday}','{email}','{country}',current_timestamp(0),'{picture}');"
        sql_insert=t_sql_insert.format(name=self.name,psw=self.password,birthday=self.birthday,\
                email=self.email,country=self.country,picture=None)

        sqlName="select count(*) from users where name='%s';"%(self.name)
        checkName=sql.queryDB(self.conn,sqlName)
    
        #no name
        if checkName[0][0] == 0:
            sql.insertDB(self.conn,sql_insert)
            return True
        else:
            return False









