from flask import Flask,request,render_template
import sqlite3

connection=sqlite3.connect("expense.db")
cursor=connection.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS expense(
                   id Int Primary key,
                   title Text not null,
                   amount Int not null,
                   category text not null,
                   date text not null)''')
connection.commit()
connection.close()

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add-expense")
def add_expense():
    return render_template("add_expense.html")

@app.route("/show-expense")
def show_expense():
    return render_template("show_expense.html")

@app.route("/add-expense",methods=["GET","POST"])
def add_expense1():
    if request.method=="POST":
        title=request.form.get("title")
        amount=request.form.get("amount")
        category=request.form.get("category")
        date=request.form.get("date")
        data=(f"{date}{amount}",title,amount,category,date)
        with sqlite3.connect("expense.db") as connection:
            cursor=connection.cursor()
            cursor.execute('''Insert into expense(id,title,amount,category,date) values(?,?,?,?,?)''',data)
            cursor.execute('''select * from expense''')
            d=cursor.fetchall()
            # print(d)            
        return render_template("index.html")
    else:
        return "bye"
    
    
@app.route("/show_expense",methods=["GET","POST"])
def show_expense1():
    if request.method=="GET":
        date=request.args.get("date")
        print(date)
        with sqlite3.connect("expense.db") as connection:
            cursor=connection.cursor()
            cursor.execute('''select * from expense where date=?''',(date,))
            details=cursor.fetchall()
            print(details)
        return render_template("show_expense.html",details=details)
    else:
        return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)