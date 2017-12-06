from flask import Flask,session,redirect,url_for,request,render_template
from modules import users,post,comment,sql
import json,base64

app=Flask(__name__)
app.secret_key='\xf1\x92Y\xdf\x8ejY\x04\x96\xb4V\x88\xfb\xfc\xb5\x18F\xa3\xee\xb9\xb9t\x01\xf0\x96'

conn=sql.connectDB("main_db","g1","0000");
#user=None;

@app.route("/")

#1.login web
@app.route("/login")
def login():
    return render_template('index.html')

@app.route("/sign_out")
def sign_out():
    session.pop("userid",None)
    session.pop("username",None)
    session.clear;
    return login();

#2.aplly account
@app.route("/apply")
def apply():
    return render_template('sign-up.html')

#3.check UserName and PassWord
@app.route("/check",methods=["POST","GET"])
def check():
    if request.method == "POST":
        UserName=request.form.get('username')
        tempPsw=request.form.get('password').encode(encoding="utf-8")
        PassWord=base64.encodestring(tempPsw).decode()
        #PassWord=request.form.get('password')
       
        user=users.Users(conn,UserName,PassWord)
        result=user.userLogin()
        if result == True:
            userid=user.getUserID()
            session["username"]=user.name
            session["userid"]=userid
            return """<script>location.replace("/mainWindow");</script>"""
        else:
            user.clean()
            return """<script>alert('username or password error');location.replace("/login");</script>"""
    else:
        print("get data error")




#4.create new account
@app.route("/createUser",methods=["POST","GET"])
def createUser():
    if request.method == "GET":
        userName=request.args.get('name')
        tempPsw=request.args.get('password').encode(encoding="utf-8")

        userPsw=base64.encodestring(tempPsw).decode()
        userEmail=request.args.get('email')
        userCountry=request.args.get('country')

        global conn
        user=users.Users(conn,userName,userPsw,userEmail,userCountry)
        result=user.userApply()
        if result == True:
            session["username"]=userName
            userid=user.getUserID()
            session["userid"]=userid

            return """<script>alert('create new account successful');location.replace("/mainWindow");</script>"""
        else:
            user.clean()
            return """<script>alert('name exist');location.replace("/apply");</script>"""

    else:
        return """<script>alert('create new account error')</script>"""

#5.main window
@app.route("/mainWindow",methods=["POST","GET"])
def mainWindow():
    global conn
    posts=post.Post(conn)
    userid=session.get("userid")
    
    if userid == None:
        return login();
    else:
        allBlogs=posts.getAllPosts(userid)

        datas=[];
        for item in allBlogs:
            datalist={
                    'username':item[0],
                    'post':item[1],
                    'postid':item[2],
                    'like':item[3],
                    'flag':item[4]
                    }
            datas.append(datalist)
        dataJson=json.dumps(datas)
    
        username=session.get("username")
        return render_template('mainWindow.html',username=username,json=dataJson)


#6.look through comments
@app.route("/commentWeb",methods=["POST","GET"])
def commentWeb():
    username=session.get("username")
    if username == None:
        return login();
    
    global conn
    
    postid=int(session.get("postid"))
    
    posts=post.Post(conn)
    post_datas=posts.getPostsByPostid(postid)
    postJson=[post_datas[0][0],post_datas[0][1],postid]
    
    userid=session.get("userid")

    comments=comment.Comment(conn)
    comment_datas=comments.getCommentsByPostid(postid,userid)
    comment_data=[];
    for item in comment_datas:
        datalist={
                'like':item[0],
                'flag':item[1],
                'commentid':item[2],
                'username':item[3],
                'comment':item[4]
                }
        comment_data.append(datalist)
    commentJson=json.dumps(comment_data)
    
    return render_template('comment.html',Musername=username,username=postJson[0],\
                userpost=postJson[1],postid=postJson[2],commentjson=commentJson)
    

@app.route("/Lcomment",methods=["POST","GET"])
def LcommentWeb():
    data=json.loads(request.form.get('data'))
    postid=data["postid"]
    session["postid"]=postid
    
    return ""
    


#7.submit comment
@app.route("/SubComment",methods=["POST","GET"])
def SubComment():
    data=json.loads(request.form.get('data'))
    postid=int(data["postid"])
    mycomment=data["comment"]
    
    global conn
    userid=session.get("userid")
    comments=comment.Comment(conn)
    comments.insertData(mycomment,userid,postid)
    
    return ""



#7.send blogs
@app.route("/SendBlogs",methods=["POST","GET"])
def SendBlogs():
    username=session.get("username")
    print(username)
    if username == None:
        return login()
    else:
        return render_template("post.html",username=username);
@app.route("/postdata",methods=["POST","GET"])
def postdata():
    global conn
    if request.method == "POST":
        blogs=request.form.get('myblog')
        posts=post.Post(conn)
        
        userid=session.get("userid")
        ressult=posts.insertData(userid,blogs)
        return """<script>window.location.href="/mainWindow";</script>"""
    

#8.information
@app.route("/Information",methods=["POST","GET"])
def Information():
    global conn
    username=session.get("username")
    if username == None:
        return login();
    else:
        userid=session.get("userid")
        user=users.Users(conn)
        informations=user.getAllInformation(userid)
        userpassword=base64.decodestring(informations[0][1].encode(encoding="utf-8")).decode()
        useremail=informations[0][2]
        usercountry=informations[0][3]

        return render_template('information.html',username=username,\
                password=userpassword,email=useremail,country=usercountry)

@app.route("/ModifyInfo",methods=["POST","GET"])
def ModifyInfo():
    global conn
    if request.method == "GET":
        userName=request.args.get('name')
        tempPsw=request.args.get('password').encode(encoding="utf-8")
        userPsw=base64.encodestring(tempPsw).decode()
        userEmail=request.args.get('email')
        userCountry=request.args.get('country')

        user=users.Users(conn,userName,userPsw,userEmail,userCountry)
        userid=session.get("userid")
        temp=session.get("username")
        if(temp != userName):
            flag=1
        else:
            flag=0
        result=user.modifyUserInfo(userid,flag);
        if result == True:
            session["username"]=userName
            return """<script>alert('submit successful');location.replace("/Information");</script>"""
        else:
            user.clean()
            return """<script>alert('name exist');location.replace("/Information");</script>"""

    else:
        return """<script>alert('create new account error')</script>"""


#9.delete blogs
@app.route("/deletePosts",methods=["POST","GET"])
def deletePosts():
    global conn
    data=json.loads(request.form.get('data'))
    postid=int(data["postid"])
    
    posts=post.Post(conn)
    posts.deletePost(postid)
    return mainWindow();


#10.delete comments
@app.route("/deleteComments",methods=["POST","GET"])
def deleteComments():
    global conn
    data=json.loads(request.form.get('data'))
    commentid=int(data["commentid"])
    
    comments=comment.Comment(conn)
    comments.deleteComment(commentid)
    
    return "";

#11.like/dislike post
@app.route("/likePost",methods=["POST","GET"])
def likePost():
    global conn
    userid=session.get("userid")
    data=json.loads(request.form.get('data'))
    postid=int(data["postid"])
    posts=post.Post(conn);
    posts.likePost(postid,userid)
    return ""

@app.route("/dislikePost",methods=["POST","GET"])
def dislikePost():
    global conn
    userid=session.get("userid")
    data=json.loads(request.form.get('data'))
    postid=int(data["postid"])
    posts=post.Post(conn);
    posts.dislikePost(postid,userid)
    return ""

#12.like/dislike comment
@app.route("/likeComment",methods=["POST","GET"])
def likeComment():
    global conn
    userid=session.get("userid")
    data=json.loads(request.form.get('data'))
    commentid=int(data["commentid"])
    comments=comment.Comment(conn);
    comments.likeComments(commentid,userid)
    return ""

@app.route("/dislikeComment",methods=["POST","GET"])
def dislikeComment():
    global conn
    userid=session.get("userid")
    data=json.loads(request.form.get('data'))
    commentid=int(data["commentid"])
    comments=comment.Comment(conn);
    comments.dislikeComments(commentid,userid)
    return ""

#13.follow friends
@app.route("/friends",methods=["POST","GET"])
def friends():
    global conn
    username=session.get("username")
    if username == None:
        return login();
    userid=session.get("userid")
    user=users.Users(conn)
    allUsers=user.getUsers(userid)
    user_data=[];
    for item in allUsers:
        datalist={
                'userid':item[0],
                'username':item[1],
                'country':item[2],
                'follow':item[3]
                }
        user_data.append(datalist)
    AllUsers=json.dumps(user_data)
    return render_template('friends.html',Musername=username,users=AllUsers)

@app.route("/followfriend",methods=["POST","GET"])
def followfriend():
    global conn
    username=session.get("username")
    userid=session.get("userid")
    data=json.loads(request.form.get('data'))
    friendid=int(data["userid"])
    user=users.Users(conn)
    user.followFriends(userid,friendid)
    return ""


@app.route("/cancelfollow",methods=["POST","GET"])
def cancelfollow():
    global conn
    username=session.get("username")
    userid=session.get("userid")
    data=json.loads(request.form.get('data'))
    friendid=int(data["userid"])
    user=users.Users(conn)
    user.cancelFollow(userid,friendid)
    return ""

@app.route("/searchUser",methods=["POST","GET"])
def searchUser():
    global conn
    user=users.Users(conn)
    data=json.loads(request.form.get('data'))
    username=data["username"]
    userid=session.get("userid")
    allUsers=user.getUsersByName(userid,username)
    if allUsers != []:
        for item in allUsers:
            datalist={
                    'userid':item[0],
                    'username':item[1],
                    'country':item[2],
                    'follow':item[3]
                    }
        AllUsers=json.dumps(datalist)
        return AllUsers;
    else:
        return "nobody"


#14.modify post and comments
@app.route("/modifyPosts",methods=["POST","GET"])
def modifyPosts():
    data=json.loads(request.form.get('data'))
    postid=data["postid"]
    session["postid"]=postid
    return ""
@app.route("/modifypostweb",methods=["POST","GET"])
def modifypostweb():
    username=session.get("username")
    if username == None:
        return login();
    global conn
    postid=int(session.get("postid"))
    posts=post.Post(conn)
    post_datas=posts.getPostsByPostid(postid)
    userpost=post_datas[0][1]
    return render_template('modifypost.html',username=username,post=userpost)
@app.route("/modifypostdata",methods=["POST","GET"])
def modifypostdata():
    global conn
    if request.method == "POST":
        blogs=request.form.get('myblog')
        postid=int(session.get("postid"))
        posts=post.Post(conn)
        print(postid)
        ressult=posts.modifyData(postid,blogs)
        return """<script>window.location.href="/mainWindow";</script>"""


@app.route("/modifyComments",methods=["POST","GET"])
def modifyComments():
    data=json.loads(request.form.get('data'))
    commentid=data["commentid"]
    session["commentid"]=commentid
    return ""
@app.route("/modifycommentweb",methods=["POST","GET"])
def modifycommentweb():
    username=session.get("username")
    if username == None:
        return login();
    global conn
    commentid=int(session.get("commentid"))
    comments=comment.Comment(conn);
    datas=comments.getCommentsByCommentid(commentid)
    text=datas[0][0]
    return render_template('modifycomment.html',username=username,comment=text)
@app.route("/modifycommentdata",methods=["POST","GET"])
def modifycommentdata():
    global conn
    if request.method == "POST":
        blogs=request.form.get('myblog')
        commentid=int(session.get("commentid"))
        comments=comment.Comment(conn);
        ressult=comments.modifyData(commentid,blogs)
        return """<script>window.location.href="/commentWeb";</script>"""





if __name__=="__main__":
    app.run(debug=True)
