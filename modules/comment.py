from modules import sql


class Comment:
    def __init__(self,user):
        self.user=user;
    
    def getCommentsByUser(self,userid):
        sqlText="select comment from comments order by date desc where userid=%d"%(userid)
        result=sql.queryDB(self.user.conn,sqlText)
        return result;
    
    def getCommentsByPostid(self,postid):
        sqlText="select name,comment from users,comments where \
                users.userid=comments.userid and postid=%d order by date desc;"%(postid)
        result=sql.queryDB(self.user.conn,sqlText)
        return result;

    def getCommentsLike(self,commentid):
        sqlText="select userid from comment_like where commentid=%d"%(commentid)
        result=sql.queryDB(self.user.conn,sqlText)
        return result;

