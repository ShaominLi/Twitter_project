from modules import sql

class Users:
    def __init__(self,conn=None,name=None,password=None,email=None,country=None):
        self.name=name
        self.password=password
        self.email=email
        self.country=country
        self.conn=conn

    def clean(self):
        self.name=None;
        self.password=None;
        self.email=None;
        self.count=None;
 

    def userLogin(self):

        sqlName="select count(*) from users where name=%s and password=%s;"
        params = [self.name,self.password]
        checkName=sql.queryDB(self.conn,sqlName,params)
        result=checkName[0][0]
        if result == 0:
            self.clean()
            return False
        else:
            return True


    def userApply(self):
        sql_insert="insert into \
                users(name,password,email,country,inscription_date) \
                values(%s,%s,%s,%s,current_timestamp(0));"

        sqlName="select count(*) from users where name=%s;"
        params = [self.name]
        checkName=sql.queryDB(self.conn,sqlName,params)
        #no name
        if checkName[0][0] == 0:
            params.extend([self.password,self.email,self.country])
            sql.insertDB(self.conn,sql_insert,params)
            return True
        else:
            return False

    def getUserID(self):
        sqlName="select userid from users where name=%s;"
        params = [self.name]
        userid=sql.queryDB(self.conn,sqlName,params)
        return userid[0][0];

    def getAllPosts(self):
        sqlText="select comment from post where userid=%s order by date;"
        params = [self.userid]
        allposts=sql.queryDB(self.conn,sqlName,params)
        return allposts;


    def getAllComments(self):
        sqlText="select comment from comments where userid=%s order by date;"
        params = [self.userid]
        allposts=sql.queryDB(self.conn,sqlText,params)
        return allposts;

    def getAllInformation(self,userid):
        sqlText="select name,password,email,country from users where userid=%s;"
        params = [userid]
        information=sql.queryDB(self.conn,sqlText,params)
        return information;


    def modifyUserInfo(self,userid,flag):
        sqlText="update users \
                set name=%s,password=%s,email=%s,country=%s where userid=%s;"
        if(flag==1): 
            sqlName="select count(*) from users where name=%s;"
            params = [self.name]
            checkName=sql.queryDB(self.conn,sqlName,params)
            #no name
            if checkName[0][0] == 0:
                params.extend([self.password,self.email,self.country,userid])
                sql.updateDB(self.conn,sqlText,params)
                return True
            else:
                return False
        else:
            params=[self.name,self.password,self.email,self.country,userid]
            sql.updateDB(self.conn,sqlText,params)
            return True;

    def followFriends(self,userid,friendid):
        sqlText="insert into friends values(%s,%s);"
        params=[friendid,userid]
        result=sql.insertDB(self.conn,sqlText,params)
        return result;

    def cancelFollow(self,userid,friendid):
        sqlText="delete from friends where userid=%d and friendid=%s;"
        params=[userid,friendid]
        result=sql.deleteDB(self.conn,sqlText,params)
        return result;

    def getUsers(self,userid):
        sqlText="select userid,name,country,(select Count(*) from friends \
                where users.userid=friends.friendid and friends.userid=%s) as follow \
                from users;"
        params=[userid]
        result=sql.queryDB(self.conn,sqlText,params)
        return result;


    def getUsersByName(self,userid,username):
        sqlText="select userid,name,country,(select Count(*) from friends \
                where users.userid=friends.friendid and friends.userid=%s) as follow \
                from users where users.name~%s;"
        params=[userid,username]
        result=sql.queryDB(self.conn,sqlText,params)
        return result;







