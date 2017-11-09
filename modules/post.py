from modules import sql


class Post:
    def __init__(self,conn):
        self.conn=conn;

    def getAllPosts(self):
        sqlText="select users.name,post.comment,post.postid from users,post \
                where post.userid=users.userid order by post.date desc;"
        result=sql.queryDB(self.conn,sqlText)
        return result;
    
    def getPostsByPostid(self,postid):
        sqlText="select users.name,post.comment from users,post where \
                users.userid=post.userid and post.postid=%d"%(postid)
        result=sql.queryDB(self.conn,sqlText)
        return result;
    
    def getPostLike(self,postid):
        sqlText="select userid from post_like where postid=%d"%(postid)
        result=sql.queryDB(self.conn,sqlText)
        return result;

    def insertData(self,userid,post):
        sqlText="insert into post(userid,date,comment) \
                values(%d,current_timestamp(0),'%s');"%(userid,post);
        result=sql.insertDB(self.conn,sqlText)
        return result;


    def deletePost(self,postid):
        sqlText="delete from post_like where post_like.commentid=%d"%(postid)
        sql.deleteDB(self.conn,sqlText)
        sqlText="delete from post where post.postid=%d"%(postid)
        sql.deleteDB(self.conn,sqlText)
