from modules import sql

class Users:
    def __init__(self,conn=None,name=None,password=None,email=None,country=None):
        self.name=name
        self.password=password
        self.email=email
        self.country=country
        self.inscription_date=None
        self.picture=None 
        self.conn=conn

    def clean(self):
        self.name=None;
        self.password=None;
        self.email=None;
        self.count=None;
        self.inscription_date=None;
        self.picture=None;

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
                users(name,password,email,country,inscription_date,picture) \
                values('{name}','{psw}','{email}','{country}',current_timestamp(0),'{picture}');"
        sql_insert=t_sql_insert.format(name=self.name,psw=self.password,\
                email=self.email,country=self.country,picture=None)

        sqlName="select count(*) from users where name='%s';"%(self.name)
        checkName=sql.queryDB(self.conn,sqlName)
    
        #no name
        if checkName[0][0] == 0:
            sql.insertDB(self.conn,sql_insert)
            return True
        else:
            return False

    def getUserID(self):
        sqlName="select userid from users where name='%s';"%(self.name)
        userid=sql.queryDB(self.conn,sqlName)
        return userid[0][0];









