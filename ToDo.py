from flask import Flask,render_template,request,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
pymysql.install_as_MySQLdb()

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:@localhost:3307/todolist_db'
db = SQLAlchemy(app)

class Tasks(db.Model):
    __tablename__='todo'
    sno= db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(80),nullable=False)
    time=db.Column(db.DateTime,default=datetime.utcnow)

@app.route("/",methods=["Get","Post"])
def todo_list():
    if (request.method=='POST'):
        todo=request.form.get("todo")
        time=request.form.get("time")
        if time:
            time_obj=datetime.strptime(time,"%Y-%m-%dT%H:%M")
        else:
            time_obj=datetime.now()
        new_post=Tasks(todo=todo,time=time_obj)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("todo_list"))  
    all_tasks=Tasks.query.all()
    return render_template("ToDoList.html",tasks=all_tasks)

@app.route("/delete/<int:sno>")
def delete(sno):
      task_to_delete=Tasks.query.filter_by(sno=sno).first()
      db.session.delete(task_to_delete)
      db.session.commit()
      return redirect(url_for("todo_list"))
 
if __name__=="__main__":
    app.run(debug=True)