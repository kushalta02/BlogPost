# importing packages
from flask import Flask
from flask import render_template,request,url_for,session,flash
from flask_mysqldb  import MySQL
#from flask_sqlalchemy import SQLAlchemy
import datetime


#connecting flask and mysql --by importiong libaries

blog = Flask(__name__)
blog.config['MYSQL_HOST']='localhost'
blog.config['MYSQL_USER']='root'
blog.config['MYSQL_PASSWORD']='khushipushi'
blog.config['MYSQL_DB']='Blog_signin'
blog.config['SECRET_KEY']=' the blog post'
mysql=MySQL(blog)
@blog.route("/home")
def home():
    return render_template("index.html")
@blog.route("/login")
def login():
    return render_template("login.html")
@blog.route("/signin")
def signin():
    return render_template("signin.html")
@blog.route("/signed",methods=['POST','GET'])
def signed():

   if request.method=='POST':
        global name
        name=request.form['Name']
        global email
        email=request.form['Email']
        password=request.form['Password']

        cursor=mysql.connection.cursor()
        cursor.execute( '''INSERT INTO usr_sign VALUES(%s,%s,%s);''' ,(name,email,password))
        cursor.execute('''INSERT INTO Log_data VALUES(%s,%s);''',(email,password))
        
        mysql.connection.commit()
        return render_template("create_blog.html")
@blog.route("/blog" ,methods=['GET','POST'])
def blogg():
    if request.method=='POST':
        #title=request.form['Title']
        email=request.form['Email']
        password=request.form['Password']
        cursor= mysql.connection.cursor()
        cursor.execute('''INSERT INTO Log_data VALUES(%s,%s);''',(email,password))
        mysql.connection.commit()
        cursor.execute(f'select email,password  from usr_sign where  email="{email}";')
        sign_store=cursor.fetchone()
        cursor.execute(f'select email,password  from Log_data where  email="{email}";')
        log_store=cursor.fetchone()
        '''cursor.execute(f'select email  from Log_data where  email="{email}";')
        global store
        store=cursor.fetchone()'''
        loggedin=False
        showError=False
        if sign_store:#if signin table data matches the login i.e if email is there is sigin 
            if (log_store[1]==sign_store[1]):
                loggedin=True
                #cursor.execute(f'delete  from Log_data where  email="{email}";')

            else:
                showError=True
        else :
            showError=True
        if loggedin:
            
        
            return render_template("blog.html",methods=['GET','POST'])
            
            '''if request.method=='POST':
                @blog.route("/blogp",methods=['POST','GET'])
                def postb():
                    return render_template("post.html")'''
        if showError:
            flash("Invalid Crendials")
            return render_template("login.html")
            

    #return render_template("blog.html")
@blog.route("/reblog")
def rebg():
    return render_template('blog.html')
@blog.route("/blogp",methods=['POST','GET'])
def postb():
    if request.method=='POST':
        title=request.form['head']
        description=request.form['Description']
        
        cursor= mysql.connection.cursor()
        cursor.execute('''INSERT INTO blog_store VALUES(%s,%s);''',(title,description))
        mysql.connection.commit()
        cursor.execute(f'select email from Log_data;')
        em=cursor.fetchall()
        usr_email=len(em)#last index te lastest user i.e latest entry stored huni so ..access
        # could also use pop or sessions concept // Pending- using this logic (user ne login/sign kita after some time logout nd all ..like fr last wala ajna c instead of len)
        cursor.execute(f'select name from usr_sign;')
        n=cursor.fetchall()
        lst=len(n)
        return render_template("post.html",title=title,description=description,email=em[usr_email-1],name=n[lst-1])
            
'''
@blog.route("/blogp",methods=['POST','GET'])
def postb():
    return render_template("post.html")

@blog.route("/descr",methods=['POST','GET'])
def des():
    if request.method=='POST':
        title=request.form['Title']
        return render_template("descrip.html",title=title)'''


if __name__=="__main__":
    blog.run(debug=True)