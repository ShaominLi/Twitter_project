from flask import Flask,session,redirect,url_for,request,render_template
from modules import users,post,comment,data
import json

app=Flask(__name__)

@app.route("/")


#1.login web
@app.route("/login")
def login():
    return render_template('index.html')

@app.route("/sign_out")
def sign_out():
    global user
    user.clean()
    return ;

#2.aplly account
@app.route("/apply")
def apply():
    return render_template('sign-up.html')

user=None;

#3.check UserName and PassWord
@app.route("/check",methods=["POST","GET"])
def check():
    if request.method == "POST":
        UserName=request.form.get('username')
        PassWord=request.form.get('password')
       
        #print(UserName)
        #print(PassWord)
        
        global user

        user=users.Users(UserName,PassWord)
        result=user.userLogin()
        if result == True:
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
        userBirthday=request.args.get('birthday')
        userCountry=request.args.get('country')

        #print(userName)
        global user
        user=users.Users(userName,userPsw,userBirthday,userEmail,userCountry)
        result=user.userApply()
        if result == True:
            return """<script>alert('create new account successful');location.replace("/mainWindow");</script>"""
        else:
            user.clean()
            return """<script>alert('name exist');location.replace("/apply");</script>"""

    else:
        return """<script>alert('create new account error')</script>"""

#5.main window
@app.route("/mainWindow",methods=["POST","GET"])
def mainWindow():
    global user
    
    posts=post.Post(user)
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
    return render_template('mainWindow.html',user=user,json=dataJson)




postJson=None
commentJson=None
#6.look through comments
@app.route("/Lcomment",methods=["POST","GET"])
def Lcomment():
    global postJson,commentJson
    data=json.loads(request.form.get('data'))
    postid=int(data["postid"])
    #print(postid)
    posts=post.Post(user)
    post_datas=posts.getPostsByPostid(postid)
    postJson=[post_datas[0][0],post_datas[0][1],postid]

    comments=comment.Comment(user)
    comment_datas=comments.getCommentsByPostid(postid)
    comment_data=[];
    for item in comment_datas:
        datalist={
                'username':item[0],
                'comment':item[1]
                }
        comment_data.append(datalist)
    commentJson=json.dumps(comment_data)
    print(len(comment_data))
    
    return ""
    #print("okkkkkkkk")

@app.route("/commentWeb",methods=["POST","GET"])
def commentWeb():
    global postJson,commentJson
    return render_template('comment.html',user=user,username=postJson[0],\
            userpost=postJson[1],postid=postJson[2],commentjson=commentJson)
    
    #return render_template('comment.html',user=user)


newcommentJson=None;
#7.submit comment
@app.route("/SubComment",methods=["POST","GET"])
def SubComment():
    data=json.loads(request.form.get('data'))
    postid=int(data["postid"])
    mycomment=data["comment"]
    #print(postid)
    #print(mycomment)
    userid=user.getUserID()
    comments=comment.Comment(user)
    result=comments.insertData(mycomment,userid,postid)

    global newcommentJson
    comment_datas=comments.getCommentsByPostid(postid)
    comment_data=[];
    for item in comment_datas:
        datalist={
                'username':item[0],
                'comment':item[1]
                }
        comment_data.append(datalist)
    newcommentJson=json.dumps(comment_data)
    print(len(comment_data))
    return ""

@app.route("/newcommentWeb",methods=["POST","GET"])
def newcommentWeb():
    global postJson,newcommentJson
    return render_template('comment.html',user=user,username=postJson[0],\
            userpost=postJson[1],postid=postJson[2],commentjson=newcommentJson)


#7.send blogs
@app.route("/SendBlogs",methods=["POST","GET"])
def SendBlogs():
    return render_template("post.html",user=user);
@app.route("/postdata",methods=["POST","GET"])
def postdata():
    if request.method == "POST":
        blogs=request.form.get('myblog')
        posts=post.Post(user)
        #userid=int(1)
        userid=user.getUserID()
        ressult=posts.insertData(userid,blogs)
        
        return mainWindow();



if __name__=="__main__":
    app.run(debug=True)
