# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 14:43:36 2021

@author: DRASHTI
"""


import pymysql
import hashlib
import random
from flask import Flask, render_template,request, redirect, session
import base64
import datetime
from datetime import date
import smtplib
#from flask_mail import Mail,Message
from werkzeug.utils import format_string
from flask_mysqldb import MySQL
from datetime import date

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


mysql=MySQL()
app=Flask(__name__)
app.config['MySQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='health'
app.config['MYSQL_HOST']='localhost'

mysql.init_app(app)
app.secret_key=hashlib.sha1('abcdef'.encode()).hexdigest()
msg=""
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

'''app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'thisisforpod@gmail.com'
app.config['MAIL_PASSWORD'] =' '
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)'''


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/firstpage')
def firstpage():
        un=session['name']
        id1=session['uid']
        cur=mysql.connection.cursor()
        q=cur.execute("Select * from sdetails where id LIKE %s", [id1])
        print("this")
        q=cur.fetchone()
        if q:
            session['addeddetails']=True
        try:
            bg=q[6]
            h=q[1]
            w=q[2]
            a=q[3]
            d=q[4]
            e=q[5]
        except:
            bg,h,w,a,d,e="","","","","",""
        
        try:
            cur=mysql.connection.cursor()
            q=cur.execute("Select date, status from appointment where sid LIKE %s", [id1])
            print("this")
            q=cur.fetchall()
            print(q)
        except:
            q=" "
        print(q)
        print(type(q))
        ap=list(q)
        print(ap)
        l=[]
        for j in ap:
            x=list(j)
            if x[1]==0:
                x[1]='Pending'
            elif x[1]==1:
                x[1]='Confirmed'
            else:
                x[1]='Conducted'
            l.append(x)
        print(l)            
        return render_template('firstpage.html',l=l,name=un, enroll=session['enroll'], username=un, h=h,w=w,bg=bg,a=a,d=d,e=e)


@app.route('/register')
def register():    
        return render_template('register.html')


@app.route('/login')
def login():    
        return render_template('login.html')


@app.route('/forgetpass')
def forgetpass():    
        return render_template('forgetpassemail.html')

@app.route('/forgetpassemailuser', methods=['POST'])
def forgetpassemailuser():  
        
        em=request.form['email']
        session['email']=em
        n = random.randint(1111,9999)
        session['secretkey']=n
        print(n)
        
        '''msg = Message('HealthCare System', sender = 'thisisforpod@gmail.com', recipients = [a])
        msg.body = "Yor secret key is "+ n
        mail.send(msg)'''
        s1 = smtplib.SMTP('smtp.gmail.com', 587)

        s1.starttls()
        s1.login("thisisforpod", "Thisis4pod")
        message =  "Your secret key is "+str(n)
        s1.sendmail("thisisforpod@gmail.com", em , message)
        s1.quit()
        msg=''
        return render_template('forgetpass.html', msg=msg)
  

@app.route('/forgetpass1', methods=['POST'])
def forgetpass1():  
        
        em=request.form['email']
        session['email']=em
        n = random.randit(1111,9999)
        session['secretkey']=n
        
        '''msg = Message('HealthCare System', sender = 'thisisforpod@gmail.com', recipients = [a])
        msg.body = "Yor secret key is "+ n
        mail.send(msg)'''
        s1 = smtplib.SMTP('smtp.gmail.com', 587)

        s1.starttls()
        s1.login("thisisforpod", "Thisis4pod")
        message =  "Your secret key is"+ n
        s1.sendmail("thisisforpod@gmail.com", em , message)
        s1.quit()
        msg=''
        return render_template('forgetpass.html', msg=msg)


@app.route('/forgetpassuser', methods=['POST'])
def forgetpassuser():
                msg=''
                sc=request.form["sc"]
                print(sc,session['secretkey'])
                if str(sc)!=str(session['secretkey']):
                    msg="Invalid secret key"
                    return render_template("forgetpass.html", msg=msg)
                password=request.form["password"]

                cur=mysql.connection.cursor()
        
                cur.execute("Update `user` SET `password` = %s where `email` = %s",(password,session['email'])); 
                mysql.connection.commit()
                cur.close()
                print("updated")
                
                return render_template('login.html')


@app.route('/registeruser', methods=["POST"])
def registeruser():
    
        name=request.form["name"]
        password=request.form["password"]
        
        cpassword=request.form["cpassword"]
        email=request.form["email"]
        enroll=request.form["enroll"]
        num=request.form["number"]
        session['userl']=email 
        session['enroll']=enroll
        
        session['name']=name 
        if password !=cpassword:
           return  render_template('register.html', msg="Passwords doesnot match")

        cur=mysql.connection.cursor()
        
        
        cur.execute("SELECT * from user WHERE `email` LIKE %s",[email])
        q=cur.fetchall()
        print(len(q))
        
        if len(q)>0:
           return  render_template('register.html', msg="Email already registered")
            
        else:  
                
            cur.execute("Insert into user (`name`,`enroll`,`number`, `email`, `password`) values(%s, %s, %s,%s, %s)", (name,enroll,num, email, password,));
            p=cur.lastrowid
            session['uid']=p 
            mysql.connection.commit()
            cur.close()
            return redirect('firstpage')

@app.route('/loginuser', methods=["POST"])
def loginuser():
        password=request.form["password"]
       
        email=request.form["email"]
        session['email']=email
        cur=mysql.connection.cursor()
        q=cur.execute("Select * from user where  email  LIKE %s", [email])
        q=cur.fetchone()
        print(q)
        if q==None:
            
            cur.close()
            msg="Email doesnot exists"
            print("enter correct password")
            return render_template('login.html', msg=msg)
            
        session['name']= q[1]
        session['enroll']=q[3]
        if email=='admin@admin.com' and password=='admin@admin':
            session['admin']=True
            d=[]
            for j in range(1,7):
                d.append(" ")
        
            return render_template('admin.html',username="Admin",d=d)
        if (q[5])==password:
            session['uid']=q[0]
            cur.close()
            return redirect('firstpage')
        else:
            cur.close()
            msg="Please try again"
            print("enter correct password")
            return render_template('login.html', msg=msg)
 

@app.route('/adddetailuser', methods=["POST"])
def adddetailuser():
            #print("hree")
        
            bg=request.form["bg"]
            allergy=request.form["a"]
            height=request.form["h"]
            weight=request.form["w"]
            major=request.form["md"]
            contact=request.form['e']
            print("num")
            num=session['uid']
            print(num,"num")
            cur=mysql.connection.cursor()
            '''
            
            cur.execute("SELECT * from sdetails WHERE `id` LIKE %s",[num])
            q=cur.fetchall()
            
            if len(q)>0:
                cur.execute("Update sdetails SET `id` = %s, `height`=%s, `weight`=%s, `bloodgroup`=%s, `allergy`=%s, `disease`=%s, `emergency`=%s  where id=%s",(num,height, weight,bg,allergy, major,contact, num)); 
                mysql.connection.commit()
                cur.close()
                print("updated")
                session['added']=True
                return redirect('firstpage')
                
            else: ''' 
                
            cur.execute("Insert into sdetails (`id`,`height`,`weight`, `bloodgroup`, `allergy`, `disease`, `emergency`) values(%s, %s, %s,%s, %s, %s, %s)", (num,height, weight,bg,allergy, major,contact));
            p=cur.lastrowid
            session['did']=p 
            mysql.connection.commit()
            cur.close()
            
            session['addeddetails']=True
            return redirect('firstpage')
  
    
@app.route('/adddetails')
def adddetails():
        
        return render_template('adddetails.html')


@app.route('/editdetailuser', methods=["POST"])
def editdetailuser():
        
            bg=request.form["bg"]
            allergy=request.form["a"]
            height=request.form["h"]
            weight=request.form["w"]
            major=request.form["md"]
            contact=request.form['e']
            print("num")
            num=session['uid']
            print(num,"num")
            cur=mysql.connection.cursor()
            cur.execute("Update sdetails SET `id` = %s, `height`=%s, `weight`=%s, `bloodgroup`=%s, `allergy`=%s, `disease`=%s, `emergency`=%s  where id=%s",(num,height, weight,bg,allergy, major,contact, num)); 
            mysql.connection.commit()
            cur.close()
            print("updated")
            session['addeddetails']=True
            return redirect('firstpage')
         
    
@app.route('/editdetails')
def editdetails():
    s=session['uid']
    cur=mysql.connection.cursor()
        
        
    cur.execute("SELECT * from sdetails WHERE `id` LIKE %s",[s])
    d=cur.fetchone()
    print(d)
    return render_template('editdetails.html', d=d)
    
@app.route('/logout')
def logout():
    print("logout")
    session.clear()
    
    print("logout")
    return render_template('login.html')

@app.route('/thanks')
def thanks():
    return render_template('thankyou.html')


@app.route('/searchdata', methods=['POST'])
def searchdata():
    eno=request.form['eno']
    print(eno)
    cur=mysql.connection.cursor() 
    cur.execute("SELECT id from user WHERE `enroll` LIKE %s",[eno])
    d=cur.fetchone()
    print(d,d[0])
    cur.execute("SELECT * from sdetails WHERE `id` LIKE %s",[d])
    d=cur.fetchone()
    

    return render_template('admin.html', d=d)

@app.route('/bookapp')
def bookapp():
    d=[]
    p={}
    wd=[]
    dt=date.today().strftime('%d-%m-%Y')
    
    d.append(dt)
    p[dt]=10
    wd.append(date.today().strftime('%A'))
    for i in range(1,4):
        dt=(datetime.datetime.now()+ datetime.timedelta(days=i)).strftime('%d-%m-%Y')
        wd1=(datetime.datetime.now()+ datetime.timedelta(days=i)).strftime('%A')
        d.append(dt)
        wd.append(wd1)
        dc=[]
        '''for j in d:
            j.strftime('%A')
        print(wd)
        cur=mysql.connection.cursor()
        cur.execute("SELECT slots from slots WHERE `date` LIKE %s",[dt])
        q=cur.fetchone()
        
        #print(q)
        #print(len(q))
        
        if q==None:
                cur.execute("Insert into slots (`date`) values(%s)",[dt])
                p[dt]=10
        
        else:
            x=list(q)
            p[dt]=int(x[0])
        
    mysql.connection.commit()
    cur.close()'''
    print(wd,"wd")
    for j in wd:
            if j=='Monday':
                dc.append("M.D. R K Sinha")
                
            elif j=='Tuesday':
                dc.append("M.D. R K Sinha")
            elif j=='Wednesday':
                dc.append("Ortho J R Shinde")
            elif j=='Thursday':
                dc.append("Dentist M P Hirani")
            elif j=='Friday':
                dc.append("M.D. R K Sinha")
            elif j=='Saturday':
                dc.append("Ortho J R Shinde")
            elif j=='Sunday':
                dc.append("Emergency Services")
    print(dc,wd)
        
    print(d)
    session['p']=p
    un=session['name']
    return render_template('bookapp.html', d=d,dc=dc, wd=wd, p=p, username=un,l=4)


@app.route('/book/<jk>/<s>')
def book(jk,s):
    print(jk, session['uid'])
    print(s)
    p=session['p']
    p[jk]-=1
    cur=mysql.connection.cursor()

    cur.execute("Insert into appointment(`sid`, `date`)values(%s,%s)",(session['uid'], jk))
        
    mysql.connection.commit()
    cur.close()
        

    if p[jk]==-1:

        return render_template('thankyou.html',username=session['name'], msg="Slots are not available, Please got for another slot.") 
    return render_template('thankyou.html',username=session['name'], msg="Thanks for booking, You will be notified on confirmation of appointment.")
    
@app.route('/allappointment')
def allappointment():
    d=[]
    for i in range(-7,7):
        dt=(datetime.datetime.now()+ datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        d.append(dt)
    print(dt)
    
    
    cur=mysql.connection.cursor()
    s='Select id, date, status from appointment where date in (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    print(s)
    cur.execute(s, d)  
    q=cur.fetchall()  
    print(q)
    mysql.connection.commit()
    cur.close()
    l=[]
    for s in q:
        l.append(list(s))
    print(l)
    return render_template('allappointment.html', l=l, username="Admin")

@app.route('/clk/<ida>/<t>')
def clk(ida,t):
    print(ida,t)
    cur=mysql.connection.cursor()
    
    cur.execute('Update appointment set `status`= %s where id = %s',[t,ida])
    
    mysql.connection.commit()
    cur.close()
    print("done")
    cur=mysql.connection.cursor()
    
    cur.execute('Select * from appointment where id = %s',[ida])
    q=cur.fetchone()
    w=list(q)
    print(w[1])
    cur.execute('Select email from user where id = %s',[w[1]])
    h=cur.fetchone()
    print(h,'h')
    h=list(h)
    print(h)
    a=h[0]
    mysql.connection.commit()
    cur.close()

    print("done")
    
    if t=='1':
        s='Confirmed'
        '''msg = Message('HealthCare System', sender = 'thisisforpod@gmail.com', recipients = [a])
        msg.body = "Yor appointment is scheduled on "+ w[2]+ " is "+ s
        mail.send(msg)'''
        s1 = smtplib.SMTP('smtp.gmail.com', 587)

        s1.starttls()
        s1.login("thisisforpod", "Thisis4pod")
        message =  "Your appointment is scheduled on "+ w[2]+ " is "+ s
        s1.sendmail("thisisforpod@gmail.com", a , message)
        s1.quit()

        print("Message sent")
    if t=='2':
        s='Cancelled'
    
        '''msg = Message('HealthCare System', sender = 'thisisforpod@gmail.com', recipients = [a])
        msg.body = "Yor appointment is scheduled on "+ w[2]+ " is "+ s
        mail.send(msg)'''
        s1 = smtplib.SMTP('smtp.gmail.com', 587)

        s1.starttls()
        s1.login("thisisforpod", "Thisis4pod")
        message =  "Your appointment is scheduled on "+ w[2]+ " is "+ s
        s1.sendmail("thisisforpod@gmail.com", a , message)
        s1.quit()

        print("Messaged")
    d=[]
    for i in range(-7,7):
        dt=(datetime.datetime.now()+ datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        d.append(dt)
    print(dt)
    
    
    cur=mysql.connection.cursor()
    s='Select id, date, status from appointment where date in (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    print(s)
    cur.execute(s, d)  
    q=cur.fetchall()  
    print(q)
    mysql.connection.commit()
    cur.close()
    l=[]
    for s in q:
        l.append(list(s))
    print(l)
    return render_template('allappointment.html', l=l, username="Admin")

@app.route('/consult/<ida>')
def consult(ida):
    session['aid']=ida
    return render_template('consult.html',a=ida)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/consultadd', methods=["POST"])
def consultadd():
    c=request.form["cons"]
    print(c)
    file=request.files['myfile']
    print("file")
    #print(f)
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))

    f1 = file.read()
        
    print("read")
    a=session['aid']
    cur=mysql.connection.cursor()

    print("here")
    sql_insert_blob_query = """ INSERT INTO consult
                          (aid, text, report) VALUES (%s,%s,%s)"""
    insert_blob_tuple = (a, c, f1)
    result = cur.execute(sql_insert_blob_query, insert_blob_tuple)
    mysql.connection.commit()
    cur.close()
    print("done")
    print("Image and file inserted successfully as a BLOB into python_employee table", result)

    return render_template('consult.html', a=a)

if __name__=='__main__':
    app.run()
