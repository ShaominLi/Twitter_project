from flask import Flask,session,redirect,url_for,request,render_template
from modules import users,post,comment,sql
import json

app=Flask(__name__)
app.secret_key='\xf1\x92Y\xdf\x8ejY\x04\x96\xb4V\x88\xfb\xfc\xb5\x18F\xa3\xee\xb9\xb9t\x01\xf0\x96'

conn=sql.connectDB("test","lishaomin","19931004");
#user=None;

@app.route("/")

#1.login web
@app.route("/login")
def login():
    return render_template('index.html')

@app.route("/sign_out")
def sign_out():
    global conn
    sql.closeDB(conn)
    session.pop("username",None)
    session.pop("userid",None)
    session.pop("posts",None)
    session.pop("comments",None)
    return ;

#2.aplly account
@app.route("/apply")
def apply():
    return render_template('sign-up.html')

#3.check UserName and PassWord
@app.route("/check",methods=["POST","GET"])
def check():
    if request.method == "POST":
        UserName=request.form.get('username')
        PassWord=request.form.get('password')
       
        #print(UserName)
        #print(PassWord)

       #global user,conn
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
        userPsw=request.args.get('password')
        userEmail=request.args.get('email')
        userCountry=request.args.get('country')

        #print(userName)
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
    allBlogs=posts.getAllPosts()

    datas=[];
    for item in allBlogs:
        datalist={
                'username':item[0],
                'post':item[1],
                'postid':item[2]
                }
        datas.append(datalist)
    dataJson=json.dumps(datas)
    #test='''[{"name":"111"},{"name":"222"}]'''
    #test=json.loads(dataJson)
    #test="%s"%(dataJson)
    #print(test)
    username=session.get("username")
    return render_template('mainWindow.html',username=username,json=dataJson)


#6.look through comments
@app.route("/Lcomment",methods=["POST","GET"])
def Lcomment():
    global conn
    data=json.loads(request.form.get('data'))
    postid=int(data["postid"])
    #print(postid)
    posts=post.Post(conn)
    post_datas=posts.getPostsByPostid(postid)
    postJson=[post_datas[0][0],post_datas[0][1],postid]

    comments=comment.Comment(conn)
    comment_datas=comments.getCommentsByPostid(postid)
    comment_data=[];
    for item in comment_datas:
        datalist={
                'commentid':item[0],
                'username':item[1],
                'comment':item[2]
                }
        comment_data.append(datalist)
    commentJson=json.dumps(comment_data)
    #print(len(comment_data))
    session["posts"]=postJson
    session["comments"]=commentJson

    return ""
    #print("okkkkkkkk")

@app.route("/commentWeb",methods=["POST","GET"])
def commentWeb():
    username=session.get("username")
    postJson=session.get("posts")
    commentJson=session.get("comments")

    return render_template('comment.html',Musername=username,username=postJson[0],\
            userpost=postJson[1],postid=postJson[2],commentjson=commentJson)
    
    #return render_template('comment.html',user=user)


#7.submit comment
@app.route("/SubComment",methods=["POST","GET"])
def SubComment():
    data=json.loads(request.form.get('data'))
    postid=int(data["postid"])
    mycomment=data["comment"]
    #print(postid)
    #print(mycomment)
    global conn
    userid=session.get("userid")
    comments=comment.Comment(conn)
    result=comments.insertData(mycomment,userid,postid)

    comment_datas=comments.getCommentsByPostid(postid)
    comment_data=[];
    for item in comment_datas:
        datalist={
                'commentid':item[0],
                'username':item[1],
                'comment':item[2]
                }
        comment_data.append(datalist)
    newcommentJson=json.dumps(comment_data)
    session["comments"]=newcommentJson
    print(len(comment_data))
    return ""

@app.route("/newcommentWeb",methods=["POST","GET"])
def newcommentWeb():
    postJson=session.get("posts")
    username=session.get("username")
    newcommentJson=session.get("comments")
    return render_template('comment.html',Musername=username,username=postJson[0],\
            userpost=postJson[1],postid=postJson[2],commentjson=newcommentJson)


#7.send blogs
@app.route("/SendBlogs",methods=["POST","GET"])
def SendBlogs():
    username=session.get("username")
    return render_template("post.html",username=username);
@app.route("/postdata",methods=["POST","GET"])
def postdata():
    global conn
    if request.method == "POST":
        blogs=request.form.get('myblog')
        posts=post.Post(conn)
        #userid=int(1)
        userid=session.get("userid")
        ressult=posts.insertData(userid,blogs)
        
        return mainWindow();

#8.information
@app.route("/Information",methods=["POST","GET"])
def Information():
    global conn
    username=session.get("username")
    userid=session.get("userid")
    user=users.Users(conn)
    informations=user.getAllInformation(userid)
    userpassword=informations[0][1]
    useremail=informations[0][2]
    usercountry=informations[0][3]

    return render_template('information.html',username=username,\
            password=userpassword,email=useremail,country=usercountry)

@app.route("/ModifyInfo",methods=["POST","GET"])
def ModifyInfo():
    global conn
    if request.method == "GET":
        userName=request.args.get('name')
        userPsw=request.args.get('password')
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
    #print(postid)
    posts=post.Post(conn)
    posts.deletePost(postid)
    return mainWindow();


#10.delete comments
@app.route("/deleteComments",methods=["POST","GET"])
def deleteComments():
    global conn
    data=json.loads(request.form.get('data'))
    commentid=int(data["commentid"])
    #print(postid)
    comments=comment.Comment(conn)
    comments.deleteComment(commentid)
    postid=session.get("posts")[2]
    comment_datas=comments.getCommentsByPostid(postid)
    comment_data=[];
    for item in comment_datas:
        datalist={
                'commentid':item[0],
                'username':item[1],
                'comment':item[2]
                }
        comment_data.append(datalist)
    newcommentJson=json.dumps(comment_data)
    session["comments"]=newcommentJson
    return "";





if __name__=="__main__":
    app.run(debug=True)
