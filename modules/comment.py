from modules import sql


class Comment:
    def __init__(self,user):
        self.user=user;
    
    def getCommentsByUser(self,userid):
        sqlText="select comment from comments order by date desc where userid=%d"%(userid)
        result=sql.queryDB(self.user.conn,sqlText)
        return result;
    
    def getCommentsByPost(self,postid):
        sqlText="select comment from comments order by date desc where postid=%d"%(postid)
        result=sql.queryDB(self.user.conn,sqlText)
        return result;

    def getCommentsLike(self,commentid):
        sqlText="select userid from comment_like where commentid=%d"%(commentid)
        result=sql.queryDB(self.user.conn,sqlText)
        return result;

