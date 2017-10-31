from flask import Flask,session,redirect,url_for,request,render_template
import users

app=Flask(__name__)

@app.route("/")


#1.login web
@app.route("/login")
def login():
    return render_template('index.html')


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
        
        user=users.Users(UserName,PassWord)
        result=users.userLogin(user)
        if result == True:
            return """<script>alert('login successful');location.replace("/mainWindow");</script>"""
        else:
            #redirect(url_for("login"))
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

        user=users.Users(userName,userPsw,userBirthday,userEmail,userCountry)
        result=users.userApply(user)
        if result == True:
            return """<script>alert('create new account successful');location.replace("/login");</script>"""
        else:
            return """<script>alert('name exist');location.replace("/apply");</script>"""

    else:
        return """<script>alert('create new account error')</script>"""

#5.main window
@app.route("/mainWindow",methods=["POST","GET"])
def mainWindow():
    return render_template('mainWindow.html')



if __name__=="__main__":
    app.run(debug=True)
