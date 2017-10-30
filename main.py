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

        flag=users.userLogin(UserName,PassWord)
        if flag == 2:
            return """<script>alert('login successful')</script>"""
        elif flag == -1:
            return """<script>alert('can't connect database')</script>"""
        else:
            #redirect(url_for("login"))
            return """<script>alert('username or password error')</script>"""
    else:
        print("get data error")




#4.create new account
@app.route("/createUser",methods=["POST","GET"])
def createUser():
    if request.method == "POST":
        userName=request.form.get('name')
        userPsw=request.form.get('psw')
        userEmail=request.form.get('email')
        userCountry=request.form.get('country')

        user=users.Users(userName,userPsw,userEmail,userCountry)
        flag=users.userApply(user)
        if flag == 0:
            return """<script>alert('create new account successful')</script>"""
        elif flag == -1:
            return """<script>alert('can't connect database')</script>"""
        else:
            #redirect(url_for("login"))
            return """<script>alert('name exist')</script>"""


    else:
        return """<script>alert('create new account error')</script>"""





if __name__=="__main__":
    app.run(debug=True)
