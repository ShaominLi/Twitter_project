from modules import sql


class Post:
    def __init__(self,user):
        self.user=user;

    def getAllPosts(self):
        sqlText="select comment from post by order date desc;"
        result=sql.queryDB(self.user.conn,sqlText)
        return result;
    
    def getPostsByUser(self,userid):
        sqlText="select comment from post by order date desc where userid=%d"%(userid)
        result=sql.queryDB(self.user.conn,sqlText)
        return result;
    
    def getPostLike(self,postid):
        sqlText="select userid from post_like where postid=%d"%(postid)
        result=sql.queryDB(self.user.conn,sqlText)
        return result;

