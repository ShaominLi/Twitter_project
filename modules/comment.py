from modules import sql


class Comment:
    def __init__(self,conn):
        self.conn=conn;
    
    def getCommentsByUser(self,userid):
        sqlText="select comment from comments order by date desc where userid=%s"
        params=[userid]
        result=sql.queryDB(self.conn,sqlText,params)
        return result;
    
    def getCommentsByPostid(self,postid,userid):
        sqlText="select (select Count(*) from comment_like where \
        comments.commentid = comment_like.commentid) as like,(select Count(*) \
                from comment_like where comments.commentid = \
                comment_like.commentid and comment_like.userid=%s) as \
                flag,commentid,name,comment from users,comments where \
                users.userid=comments.userid and postid=%s order by date desc;"
        params=[userid,postid]
        result=sql.queryDB(self.conn,sqlText,params)
        return result;

    def getCommentsLike(self,commentid):
        sqlText="select userid from comment_like where commentid=%s"
        params=[commentid]
        result=sql.queryDB(self.conn,sqlText,params)
        return result;
	
    def insertData(self,comment,userid,postid):
        sqlText="insert into comments(comment,userid,date,postid) \
        values(%s,%s,current_timestamp(0),%s);"
        params=[comment,userid,postid]
        result=sql.insertDB(self.conn,sqlText,params)
        return result;

    def deleteComment(self,commentid):
        sqlText="delete from comments where commentid=%s"
        params=[commentid]
        result=sql.deleteDB(self.conn,sqlText,params)
        return result;

    def likeComments(self,commentid,userid):
        sqlText="insert into comment_like values(%s,%s);"
        params=[userid,commentid]
        result=sql.insertDB(self.conn,sqlText,params)
        return result;

    def dislikeComments(self,commentid,userid):
        sqlText="delete from comment_like where commentid=%s and userid=%s;"
        params=[commentid,userid]
        result=sql.deleteDB(self.conn,sqlText,params)
        return result;

    def getCommentsByCommentid(self,commentid):
        sqlText="select comment from comments where commentid=%s"
        params=[commentid]
        result=sql.queryDB(self.conn,sqlText,params)
        return result;

    def modifyData(self,commentid,text):
        sqlText="update comments set comment=%s where commentid=%s"
        params=[text,commentid]
        result=sql.updateDB(self.conn,sqlText,params)
        return result;


