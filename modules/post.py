from modules import sql


class Post:
    def __init__(self,user):
        self.user=user;

    def getAllPosts(self):
        sqlText="select users.name,post.comment,post.postid from users,post \
                where post.userid=users.userid order by post.date desc;"
        result=sql.queryDB(self.user.conn,sqlText)
        return result;
    
    def getPostsByPostid(self,postid):
        sqlText="select users.name,post.comment from users,post where \
                users.userid=post.userid and post.postid=%d"%(postid)
        result=sql.queryDB(self.user.conn,sqlText)
        return result;
    
    def getPostLike(self,postid):
        sqlText="select userid from post_like where postid=%d"%(postid)
        result=sql.queryDB(self.user.conn,sqlText)
        return result;

