from modules import sql


class Comment:
    def __init__(self,conn):
        self.conn=conn;
    
    def getCommentsByUser(self,userid):
        sqlText="select comment from comments order by date desc where userid=%d"%(userid)
        result=sql.queryDB(self.conn,sqlText)
        return result;
    
    def getCommentsByPostid(self,postid):
        sqlText="select name,comment from users,comments where \
                users.userid=comments.userid and postid=%d order by date desc;"%(postid)
        result=sql.queryDB(self.conn,sqlText)
        return result;

    def getCommentsLike(self,commentid):
        sqlText="select userid from comment_like where commentid=%d"%(commentid)
        result=sql.queryDB(self.conn,sqlText)
        return result;
	
    def insertData(self,comment,userid,postid):
        sqlText="insert into comments(comment,userid,date,postid) values('%s',%d,current_timestamp(0),%d);"%(comment,userid,postid)
        result=sql.insertDB(self.conn,sqlText)
        return result;

    def deleteComment(self,Commentid):
        sqlText="delete from comment_like where comment_like.commentid=%d"%(commentid)
        sql.deleteDB(self.conn,sqlText)
        sqlText="delete from comments where comments.commentid=%d"%(commentid)
        sql.deleteDB(self.conn,sqlText)


