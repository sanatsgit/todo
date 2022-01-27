from turtle import title
import _tkinter
import fcntl
from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False                                  # ignore why it is required
db=SQLAlchemy(app)

class Todo(db.Model) :                                                               #class creation for fields to be included in database                                                              
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(250),nullable=False)
    content=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)


    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"








@app.route("/",methods=['GET','POST'])
def homepge():
    if request.method=="POST":
        titl=request.form['title']
        desc=request.form['desc']       
            
        todo=Todo(title=titl, content=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()

    return render_template('index.html',alltodo=alltodo)

@app.route('/show')
def show():
    alltodo= Todo.query.all()
    print(alltodo)
    return 'todo list'

@app.route('/delete/<int:sno>')
def dele(sno):
    dele=Todo.query.filter_by(sno=sno).first()
    db.session.delete(dele)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>',methods=['GET','POST'])
def upd(sno):
    if request.method=="POST":
         title=request.form['title']
         desc=request.form['desc']       
         todo=Todo.query.filter_by(sno=sno).first()
         todo.title=title
         todo.content=desc
         db.session.add(todo)
         db.session.commit()
         return redirect('/')
        
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('updates.html',todo=todo)                                       #aise hi eik variable passed named todo(could be any name)



if __name__=="__main__":
    app.run(debug=False,port=5000)